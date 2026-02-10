import os
from playwright.sync_api import expect

from config import DOWNLOADS_DIR
from pages.base_page import BasePage
from pages.sender_details_page import SenderDetailsPage
from pages.deliveries_page import DeliveriesPage
from pages.routes_page import RoutesPage
from pages.logs_page import LogsPage
from pages.orders_history_page import OrdersHistoryPage
from pages.branches_page import BranchesPage
from pages.account_users_page import AccountUsersPage


class SendersPage(BasePage):
    sendersBreadcrumbs = "//gp-breadcrumbs//a[@href='/senders']"
    filtersBlock = "//gp-senders-filters"
    regDatePicker = filtersBlock + "//mat-form-field[1]//input"
    lastOrderDatePicker = filtersBlock + "//mat-form-field[1]//input"
    accTypeFilter = filtersBlock + "//mat-form-field[3]//mat-select"
    accStatusFilter = filtersBlock + "//mat-form-field[4]//mat-select"
    chargingTypeFilter = filtersBlock + "//mat-form-field[5]//mat-select"
    paymentMethodFilter = filtersBlock + "//mat-form-field[6]//mat-select"
    searchInput = filtersBlock + "//mat-form-field[7]//input"
    confirmationPopup = "//gp-confirmation-dialog"
    blockButton = "//button/span[normalize-space()='Block']"
    activateButton = "//button/span[normalize-space()='Activate']"

    def __init__(self, page):
        super().__init__(page)
        self.sumOfSenders = 0
        self.rowsNum = 0

    def reloadPage(self):
        self.page.reload()
        return self

    def openSenderDetailsPage(self):
        self.page.click(self.rows + "/td[1]/a")
        return SenderDetailsPage(self.page)

    def openSelectedSenderDetailsPage(self):
        self.page.click(self.rows + f"/td[1]/a[normalize-space()='{self.dataSender.getSenderId()}']")
        return SenderDetailsPage(self.page)

    def isAccountBlocked(self):
        self.page.locator(self.rows + "/td[5]/div[normalize-space()='Blocked']").wait_for()
        expect(self.page.locator(self.rows + "/td[5]/div")).to_contain_text("Blocked")
        return self

    def isAccountActive(self):
        self.page.locator(self.rows + "/td[5]/div[normalize-space()='Active']").wait_for()
        expect(self.page.locator(self.rows + "/td[5]/div")).to_contain_text("Active")
        return self

    def activateAccount(self):
        self.page.click(self.rows + "/td[9]/button")
        self.page.click(self.confirmationPopup + self.activateButton)
        return self

    def blockAccount(self):
        self.page.click(self.rows + "/td[9]/button")
        self.page.click(self.confirmationPopup + self.blockButton)
        return self

    def isFileDownLoaded(self, file_name):
        file_path = os.path.join(DOWNLOADS_DIR, f"{file_name}.xlsx")
        assert os.path.exists(file_path)
        return self

    def downloadAllPages(self, file_name):
        with self.page.expect_download() as download_info:
            self.page.click(self.exportAllPages)
        download = download_info.value
        file_path = os.path.join(DOWNLOADS_DIR, f"{file_name}.xlsx")
        download.save_as(file_path)
        self.dataLoaded()
        self.rowsNum = self.getNumberOfSelectedRows()
        return self

    def downloadCurrentPage(self, file_name):
        with self.page.expect_download() as download_info:
            self.page.click(self.exportCurrentPage)
        download = download_info.value
        file_path = os.path.join(DOWNLOADS_DIR, f"{file_name}.xlsx")
        download.save_as(file_path)
        self.dataLoaded()
        self.rowsNum = self.page.locator(self.rows).count()
        return self

    def pressExport(self):
        self.page.click(self.exportButton)
        return self

    def setRowsOnPage(self, rows):
        super().setRowsOnPage(rows)
        self.waitForCountRows(rows)
        return self

    def waitForCountRows(self, count):
        c = 0
        while self.page.locator(self.rows).count() != count:
            self.pause(0.1)
            c += 1
            if c > 50:
                break

    def fillSearchInput(self, attribute):
        if attribute == "ID":
            attribute = self.dataSender.getSenderId()
        self.page.fill(self.searchInput, attribute)
        return self

    def isSenderFoundByAccName(self, text):
        self.page.locator("//gp-senders-table//tbody/tr/td//button").first.wait_for()
        expect(self.page.locator("//gp-senders-table//tbody/tr/td[2]").first).to_contain_text(text)
        return self

    def isSenderFoundByOwnerName(self, text):
        self.page.locator("//gp-senders-table//tbody/tr/td//button").first.wait_for()
        expect(self.page.locator("//gp-senders-table//tbody/tr/td[6]").first).to_contain_text(text)
        return self

    def isSenderFound(self):
        row = 1
        while self.page.locator(f"//tbody/tr[{row}]/td[1]/a").inner_text() != self.dataSender.getSenderId():
            row += 1
            if row > 20:
                break
        expect(self.page.locator(f"//tbody/tr[{row}]/td[1]/a")).to_contain_text(self.dataSender.getSenderId())
        expect(self.page.locator(f"//tbody/tr[{row}]/td[2]")).to_contain_text(self.dataSender.getSAccountName())
        expect(self.page.locator(f"//tbody/tr[{row}]/td[3]")).to_contain_text(self.dataSender.getCreatedAt())
        expect(self.page.locator(f"//tbody/tr[{row}]/td[5]/div").first).to_contain_text(self.dataSender.getAccStatus())
        expect(self.page.locator(f"//tbody/tr[{row}]/td[6]")).to_contain_text(self.dataSender.getSOwnerName())
        expect(self.page.locator(f"//tbody/tr[{row}]/td[7]")).to_contain_text(self.dataSender.getAccType())
        expect(self.page.locator(f"//tbody/tr[{row}]/td[8]")).to_contain_text(self.dataSender.getSPayMethod())
        return self

    def getSenderData(self, row):
        from models.sender_details import SenderDetails
        self.dataSender = SenderDetails.builder().build()
        if row <= 0:
            row = 10
        self.dataSender.setSenderId(self.page.locator(f"//tbody/tr[{row}]/td[1]/a").inner_text())
        self.dataSender.setSAccountName(self.page.locator(f"//tbody/tr[{row}]/td[2]").inner_text())
        self.dataSender.setCreatedAt(self.page.locator(f"//tbody/tr[{row}]/td[3]").inner_text())
        self.dataSender.setLastOrder(self.page.locator(f"//tbody/tr[{row}]/td[4]").inner_text())
        self.dataSender.setAccStatus(self.page.locator(f"//tbody/tr[{row}]/td[5]/div").first.inner_text())
        self.dataSender.setSOwnerName(self.page.locator(f"//tbody/tr[{row}]/td[6]").inner_text())
        self.dataSender.setAccType(self.page.locator(f"//tbody/tr[{row}]/td[7]").inner_text())
        self.dataSender.setSPayMethod(self.page.locator(f"//tbody/tr[{row}]/td[8]").inner_text())
        return self

    def isAccType(self, type_text):
        if self.page.locator(self.noResult).is_visible():
            return self
        row = self.page.locator(self.rows)
        count = row.count() - 1
        for i in range(0, count - 1):
            acc_type = row.nth(i).locator("//td[7]")
            expect(acc_type).to_contain_text(type_text)
        self.sumOfSenders -= self.getNumberOfSelectedRows()
        return self

    def isAccStatus(self, type_text):
        if self.page.locator(self.noResult).is_visible():
            return self
        row = self.page.locator(self.rows)
        count = row.count() - 1
        for i in range(0, count - 1):
            acc_type = row.nth(i).locator("//td[5]/div[1]")
            expect(acc_type).to_contain_text(type_text)
        self.sumOfSenders -= self.getNumberOfSelectedRows()
        return self

    def isPaymentMethod(self, method):
        if self.page.locator(self.noResult).is_visible():
            return self
        row = self.page.locator(self.rows)
        count = row.count() - 1
        for i in range(0, count - 1):
            acc_type = row.nth(i).locator("//td[8]")
            expect(acc_type).to_contain_text(method, ignore_case=True)
        self.sumOfSenders -= self.getNumberOfSelectedRows()
        return self

    def selectCheckbox(self, type_text):
        self.pressCheckbox(type_text)
        return self

    def cleanFilter(self):
        self.page.wait_for_response(self.urlOpApi + "/v1/graphql/", lambda: self.page.click(self.clearButton))
        self.pause(1)
        return self

    def isAllEquals(self):
        assert self.sumOfSenders - self.getNumberOfSelectedRows() == 0
        return self

    def closeDropdownByEsc(self):
        self.pressEsc()
        return self

    def selectAllCheckbox(self):
        super().selectAllCheckbox()
        return self

    def openPeymentMethod(self):
        self.page.click(self.paymentMethodFilter)
        return self

    def openAccTypeFilter(self):
        self.page.click(self.accTypeFilter)
        return self

    def openAccStatusFilter(self):
        self.page.click(self.accStatusFilter)
        return self

    def getNumberOfRows(self):
        if self.page.locator(self.noResult).is_visible():
            self.sumOfSenders = 0
            return self
        self.sumOfSenders = self.getNumberOfSelectedRows()
        return self

    def isSendersPage(self):
        self.page.wait_for_url(self.url + "/senders")
        self.page.mouse.click(20, 20)
        expect(self.page.locator(self.sendersBreadcrumbs)).to_be_visible()
        return self

    def isLastSevenDaysSelected(self):
        self.openRegDatePicker()
        day = int(self.getMinusDayDD(6))
        expect(self.page.locator(f"//td[normalize-space()='{day}' and contains(@class,'active start-date')]")).to_be_visible()
        self.closeDatePicker()
        return self

    def isLastMonthSelected(self):
        self.openRegDatePicker()
        day = int(self.getMinusDayDD(29))
        expect(self.page.locator(f"//td[normalize-space()='{day}' and contains(@class,'active start-date')]")).to_be_visible()
        self.closeDatePicker()
        return self

    def pressApply(self):
        self.page.wait_for_response(lambda response: response.status == 200, lambda: self.page.click(self.applyButton))
        self.page.wait_for_load_state()
        self.pause(5)
        self.dataLoaded()
        return self

    def selectLastSevenDays(self):
        self.page.click(self.lastWeekButton)
        return self

    def selectLastMonth(self):
        self.page.click(self.lastMonthButton)
        return self

    def openRegDatePicker(self):
        self.page.click(self.regDatePicker)
        return self

    def openDeliveriesPage(self):
        self.page.click(self.deliveriesButton)
        return DeliveriesPage(self.page)

    def openRoutesPage(self):
        self.page.click(self.routesButton)
        return RoutesPage(self.page)

    def openLogs(self):
        self.page.click("//a[normalize-space()='Logs']")
        return LogsPage(self.page)

    def openOrderHistoryPage(self):
        self.page.click("//div[normalize-space()='Orders History']")
        return OrdersHistoryPage(self.page)

    def openBranches(self):
        self.page.click("//div[normalize-space()='Branches']")
        return BranchesPage(self.page)

    def openAccountUsersPage(self):
        self.page.click("//div[normalize-space()=\"Account's Users\"]")
        return AccountUsersPage(self.page)
