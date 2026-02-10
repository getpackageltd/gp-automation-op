import os
from playwright.sync_api import expect

from config import DOWNLOADS_DIR
from pages.base_page import BasePage
from pages.courier_details_page import CourierDetailsPage
from pages.deliveries_page import DeliveriesPage
from pages.routes_page import RoutesPage


class CouriersPage(BasePage):
    searchInput = "//input[@id='mat-input-18']"
    couriersBreadcrumbs = "//gp-breadcrumbs//a[@href='/couriers']"
    accStatusFilter = "//div[@class='gp-filters-layout__fields']/mat-form-field[3]"
    finStatusFilter = "//div[@class='gp-filters-layout__fields']/mat-form-field[4]"
    finOperabilityFilter = "//div[@class='gp-filters-layout__fields']/mat-form-field[5]"
    addCourierButton = "//div[@class='gp-couriers']/button"
    newCourierPopup = "//mat-dialog-container"
    firstNameNewCour = newCourierPopup + "//input[@formcontrolname='firstName']"
    lastNameNewCour = newCourierPopup + "//input[@formcontrolname='lastName']"
    emailNewCour = newCourierPopup + "//input[@formcontrolname='email']"
    IDNewCour = newCourierPopup + "//input[@formcontrolname='nationalId']"
    phoneNewCour = newCourierPopup + "//input[@formcontrolname='phoneNumber']"
    passwordNewCour = newCourierPopup + "//input[@formcontrolname='password']"
    regionNewCour = newCourierPopup + "//mat-select[@formcontrolname='courierRegion']"
    listFirstRow = "//div[@role='listbox']/mat-option[1]"
    cityNewCour = newCourierPopup + "//input[@formcontrolname='city']"
    vehicleNewCour = newCourierPopup + "//mat-select[@formcontrolname='vehicleType']"
    taxStatNewCour = newCourierPopup + "//mat-select[@formcontrolname='taxStatus']"
    addressNewCour = newCourierPopup + "//input[@formcontrolname='address']"
    languageNewCour = newCourierPopup + "//mat-select[@formcontrolname='language']"
    cancelButtNewCour = newCourierPopup + "//button[1]"
    saveButtNewCour = newCourierPopup + "//button[2]"

    def __init__(self, page):
        super().__init__(page)
        self.sumOfCouriers = 0
        self.rowsNum = 0

    def isAllEquals(self):
        assert self.sumOfCouriers - self.getNumberOfSelectedRows() == 0
        return self

    def isCourierCreated(self):
        if not BasePage.dataCourier:
            BasePage.dataCourier = [None, "", "", "", "", "", "", ""]
        self.page.locator("//tbody/tr[1]/td[2]/a").wait_for()
        BasePage.dataCourier[0] = self.page.locator("//tbody/tr[1]/td[2]/a").inner_text()
        self.newCourierID = BasePage.dataCourier[0]
        # Validate creation by matching the phone number in the first row
        expect(self.page.locator("//tbody/tr[1]/td[5]")).to_contain_text(BasePage.dataCourier[3])
        return self

    def saveNewCourier(self):
        self.page.locator(self.saveButtNewCour).wait_for()
        self.page.click(self.saveButtNewCour, force=True)
        self.dataLoaded()
        self.page.locator("//tbody/tr[1]/td[2]/a").wait_for()
        return self

    def isRequired(self, count):
        expect(self.page.locator("//mat-error")).to_have_count(count)
        expect(self.page.locator(self.saveButtNewCour)).to_be_disabled()
        return self

    def fillNewCourierData(self, courier_details):
        self.page.locator(self.newCourierPopup).wait_for()
        self.page.fill(self.firstNameNewCour, courier_details.getCFirstName())
        self.page.fill(self.lastNameNewCour, courier_details.getCLastName())
        self.page.fill(self.emailNewCour, courier_details.getCEmail())
        self.page.fill(self.IDNewCour, courier_details.getCNationalId())
        self.page.fill(self.phoneNewCour, courier_details.getCPhone())
        self.page.fill(self.passwordNewCour, courier_details.getCPassword())
        self.page.click(self.regionNewCour, force=True)
        self.page.locator("//div[@role='listbox']/mat-option").first.wait_for()
        self.page.click(f"//div[@role='listbox']/mat-option[{courier_details.getCRegion()}]")
        self.page.fill(self.cityNewCour, courier_details.getCCity())
        self.page.locator(self.listFirstRow).wait_for()
        self.page.click(self.listFirstRow)
        self.page.click(self.vehicleNewCour, force=True)
        self.page.locator("//div[@role='listbox']/mat-option").first.wait_for()
        self.page.click(f"//div[@role='listbox']/mat-option[{courier_details.getCVehicle()}]")
        self.page.click(self.taxStatNewCour, force=True)
        self.page.locator("//div[@role='listbox']/mat-option").first.wait_for()
        self.page.click(f"//div[@role='listbox']/mat-option[{courier_details.getCTaxStat()}]")
        self.page.fill(self.addressNewCour, courier_details.getCAddress())
        self.isGooglAddressAppeared()
        self.page.click(self.googleAddr)
        self.page.click(self.languageNewCour, force=True)
        self.page.locator("//div[@role='listbox']/mat-option").first.wait_for()
        self.page.click(f"//div[@role='listbox']/mat-option[{courier_details.getCLanguage()}]")

        BasePage.dataCourier = [
            None,
            f"{courier_details.getCLastName()} {courier_details.getCFirstName()}",
            courier_details.getCNationalId(),
            courier_details.getCPhone(),
            "Active",
            courier_details.getCCity(),
            "Car",
            "allowed",
        ]
        return self

    def openCourierDetails(self):
        if BasePage.dataCourier and BasePage.dataCourier[0] and self.page.locator(f"//tbody//td[2]/a[normalize-space()='{BasePage.dataCourier[0]}']").is_visible():
            self.page.locator(f"//tbody//td[2]/a[normalize-space()='{BasePage.dataCourier[0]}']").click()
        else:
            self.page.locator("//tbody//td[2]/a").first.click()
        return CourierDetailsPage(self.page)

    def getNumberOfRows(self):
        if self.page.locator(self.noResult).is_visible():
            self.sumOfCouriers = 0
            return self
        self.sumOfCouriers = self.getNumberOfSelectedRows()
        return self

    def selectAllCheckbox(self):
        super().selectAllCheckbox()
        return self

    def cleanFilter(self):
        self.page.click(self.clearButton)
        self.dataLoaded()
        return self

    def isCourierFound(self):
        self.dataLoaded()
        # Ensure only 1 result is found as requested by the user
        expect(self.page.locator("//tbody/tr")).to_have_count(1, timeout=10000)
        row = 1
        expect(self.page.locator(f"//tbody/tr[{row}]/td[2]/a")).to_contain_text(BasePage.dataCourier[0])
        expect(self.page.locator(f"//tbody/tr[{row}]/td[3]")).to_contain_text(BasePage.dataCourier[1])
        expect(self.page.locator(f"//tbody/tr[{row}]/td[4]")).to_contain_text(BasePage.dataCourier[2])
        expect(self.page.locator(f"//tbody/tr[{row}]/td[5]")).to_contain_text(BasePage.dataCourier[3])
        expect(self.page.locator(f"//tbody/tr[{row}]/td[6]/div").first).to_contain_text(BasePage.dataCourier[4])
        expect(self.page.locator(f"//tbody/tr[{row}]/td[8]")).to_contain_text(BasePage.dataCourier[5])
        expect(self.page.locator(f"//tbody/tr[{row}]/td[9]")).to_contain_text(BasePage.dataCourier[6])
        expect(self.page.locator(f"//tbody/tr[{row}]/td[13]")).to_contain_text(BasePage.dataCourier[7])
        return self

    def isStatusType(self, type_text):
        if self.page.locator(self.noResult).is_visible():
            return self
        row = self.page.locator(self.rows)
        count = row.count() - 1
        for i in range(0, count - 1):
            acc_type = row.nth(i).locator("//td[6]/div[1]")
            expect(acc_type).to_contain_text(type_text)
        self.sumOfCouriers -= self.getNumberOfSelectedRows()
        if type_text == "Blocked":
            assert self.sumOfCouriers == 0
        return self

    def isFinStatusType(self, type_text):
        self.pause(0.4)
        if self.page.locator(self.noResult).is_visible():
            return self
        row = self.page.locator(self.rows)
        count = row.count() - 1
        for i in range(0, count - 1):
            fin_type = row.nth(i).locator("//td[7]/div[1]")
            display = type_text
            if type_text == "None":
                display = "-"
            if type_text == "Failed Output":
                display = "FAILED OUTPUT"
            expect(fin_type).to_contain_text(display)
        self.sumOfCouriers -= self.getNumberOfSelectedRows()
        if type_text == "None":
            assert self.sumOfCouriers == 0
        return self

    def isFinOperabilityType(self, type_text):
        self.pause(0.4)
        if self.page.locator(self.noResult).is_visible():
            return self
        row = self.page.locator(self.rows)
        count = row.count() - 1
        for i in range(0, count - 1):
            fin_type = row.nth(i).locator("//td[13]")
            expect(fin_type).to_contain_text(type_text.lower())
        self.sumOfCouriers += self.getNumberOfSelectedRows()
        return self

    def pressExport(self):
        self.page.click(self.exportButton)
        return self

    def isFileDownLoaded(self, file_name):
        file_path = os.path.join(DOWNLOADS_DIR, f"{file_name}.xlsx")
        assert os.path.exists(file_path)
        return self

    def downloadCurrentPage(self, file_name):
        with self.page.expect_download() as download_info:
            self.page.click(self.exportCurrentPage)
        file_path = os.path.join(DOWNLOADS_DIR, f"{file_name}.xlsx")
        download_info.value.save_as(file_path)
        self.dataLoaded()
        self.rowsNum = self.page.locator(self.rows).count()
        return self

    def downloadAllPages(self, file_name):
        with self.page.expect_download() as download_info:
            self.page.click(self.exportAllPages)
        file_path = os.path.join(DOWNLOADS_DIR, f"{file_name}.xlsx")
        download_info.value.save_as(file_path)
        self.dataLoaded()
        self.rowsNum = self.getNumberOfSelectedRows()
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

    def isCourierFromCity(self):
        self.pause(0.4)
        row = self.page.locator(self.rows)
        count = row.count() - 1
        for i in range(0, count - 1):
            city = row.nth(i).locator("//td[8]")
            expect(city).to_contain_text(BasePage.dataCourier[5])
        return self

    def closeDropdownByEsc(self):
        self.pressEsc()
        return self

    def selectCheckbox(self, type_text):
        self.pressCheckbox(type_text)
        return self

    def openAccStatusFilter(self):
        self.page.click(self.accStatusFilter)
        return self

    def openFinStatusFilter(self):
        self.page.click(self.finStatusFilter)
        return self

    def openFinOperabilityFilter(self):
        self.page.click(self.finOperabilityFilter)
        return self

    def selectLastMonth(self):
        self.page.click(self.lastMonthButton)
        return self

    def isLastMonthSelected(self):
        self.openDatePicker()
        day = int(self.getMinusDayDD(29))
        expect(self.page.locator(f"//td[normalize-space()='{day}' and contains(@class,'active start-date')]")).to_be_visible()
        self.closeDatePicker()
        return self

    def isLastSevenDaysSelected(self):
        self.openDatePicker()
        day = int(self.getMinusDayDD(6))
        expect(self.page.locator(f"//td[normalize-space()='{day}' and contains(@class,'active start-date')]")).to_be_visible()
        self.closeDatePicker()
        return self

    def cancelNewCourierPopup(self):
        self.page.click(self.cancelButtNewCour)
        return self

    def clickAllFields(self):
        self.page.click(self.firstNameNewCour)
        self.page.click(self.lastNameNewCour)
        self.page.click(self.emailNewCour)
        self.page.click(self.IDNewCour)
        self.page.click(self.phoneNewCour)
        self.page.click(self.regionNewCour)
        self.closeDropdownByEsc()
        self.page.click(self.vehicleNewCour)
        self.closeDropdownByEsc()
        self.page.click(self.taxStatNewCour)
        self.closeDropdownByEsc()
        self.page.click(self.addressNewCour)
        self.page.click(self.languageNewCour)
        self.closeDropdownByEsc()
        return self

    def pressAddCourier(self):
        self.page.click(self.addCourierButton)
        self.page.locator(self.newCourierPopup).wait_for()
        self.page.locator(self.firstNameNewCour).wait_for()
        return self

    def pressApply(self):
        apply_button = self.page.locator(self.applyButton)
        if apply_button.is_visible():
            apply_button.click()
        else:
            # Fallback: trigger search by pressing Enter in the search input
            try:
                search_input = self.page.locator(self.searchInput).first
                if search_input.is_visible():
                    search_input.press("Enter")
            except Exception:
                pass
        self.dataLoaded()
        self.page.wait_for_load_state()
        return self

    def selectLastSevenDays(self):
        self.page.click(self.lastWeekButton)
        return self

    def openDatePicker(self):
        self.page.click(self.openCalendar)
        return self

    def isCouriersPage(self):
        self.page.wait_for_url(self.url + "/couriers")
        self.page.mouse.click(20, 20)
        expect(self.page.locator(self.couriersBreadcrumbs)).to_be_visible()
        return self

    def getCourierData(self, row):
        BasePage.dataCourier = []
        if row <= 0:
            row = 10
        BasePage.dataCourier.append(self.page.locator(f"//tbody/tr[{row}]/td[2]/a").inner_text())
        BasePage.dataCourier.append(self.page.locator(f"//tbody/tr[{row}]/td[3]").inner_text())
        BasePage.dataCourier.append(self.page.locator(f"//tbody/tr[{row}]/td[4]").inner_text())
        BasePage.dataCourier.append(self.page.locator(f"//tbody/tr[{row}]/td[5]").inner_text())
        BasePage.dataCourier.append(self.page.locator(f"//tbody/tr[{row}]/td[6]/div").first.inner_text())
        BasePage.dataCourier.append(self.page.locator(f"//tbody/tr[{row}]/td[8]").inner_text())
        BasePage.dataCourier.append(self.page.locator(f"//tbody/tr[{row}]/td[9]").inner_text())
        BasePage.dataCourier.append(self.page.locator(f"//tbody/tr[{row}]/td[13]").inner_text())
        return self

    def fillSearchInputBy(self, attribute):
        if attribute == "name":
            attribute = BasePage.dataCourier[1]
        elif attribute == "phone":
            attribute = BasePage.dataCourier[3]
        elif attribute == "city":
            attribute = BasePage.dataCourier[5]
        else:
            attribute = BasePage.dataCourier[0]
        search_input = self.page.locator(self.searchInput).first
        search_input.wait_for()
        search_input.fill(attribute)
        # Some MDC inputs require an Enter to trigger the filter
        search_input.press("Enter")
        return self

    def openDeliveriesPage(self):
        self.page.click(self.deliveriesButton)
        return DeliveriesPage(self.page)

    def openRoutesPage(self):
        self.page.click(self.routesButton)
        return RoutesPage(self.page)
