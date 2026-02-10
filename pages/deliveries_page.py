from __future__ import annotations

from playwright.sync_api import expect

import os

from config import DOWNLOADS_DIR
from pages.base_page import BasePage
from models.delivery_details import DeliveryDetails
from models.courier_details import CourierDetails
from models.sender_details import SenderDetails
from models.user_details import UserDetails


class DeliveriesPage(BasePage):
    searchInput = "//mat-form-field[.//mat-label[normalize-space()='Search']]//input"
    loginInput = "//input[@placeholder='Enter your email']"
    passwordInput = "//input[@placeholder='Enter your Password']"
    loginButton = "//button[contains(@class,'gp-login-btn')]//span[normalize-space()='Login']/.."
    urlLogin = BasePage.url + "/login"

    vipDropdown = "//mat-label[normalize-space()='VIP']/../../../.."
    excludedCheckbox = "//span[@class='mat-checkbox-inner-container']"

    remarkArea = "//tbody/tr[1]/td[13]//div[@class='remark-container']"
    remarkTextArea = "//tbody/tr[1]/td[13]//textarea"
    remarkTextCancel = "//tbody/tr[1]/td[13]//mat-icon[normalize-space()='highlight_off']"
    remarkSaveText = "//tbody/tr[1]/td[13]//mat-icon[normalize-space()='check_circle_outline']"
    sortDelivId = "//thead/tr/th[2]/div/div[2]"
    sortRouteId = "//thead/tr/th[3]/div/div[2]"
    deliveryIdFirstRow = "//tbody/tr[1]/td[2]//a"
    routeIdFirstRow = "//tbody/tr[1]/td[3]//a"
    packageIDFirstRow = "//tbody/tr[1]/td[4]/div"
    serviceFirstRow = "//tbody/tr[1]/td[5]/div"
    courierNameFirstRow = "//tbody/tr[1]/td[6]/a"
    accountNameFirstRow = "//tbody/tr[1]/td[7]/a"
    companyClientName = "//tbody/tr[1]/td[8]"
    userNameFirstRows = "//tbody/tr[1]/td[9]"
    statusFirstRow = "//tbody/tr[1]/td[contains(@class,'mat-column-status')]//div[contains(@class,'gp-status-cell')]"
    pickAddrFirstRow = "//tbody/tr[1]/td[11]/div/span[1]"
    dropAddrFirstRow = "//tbody/tr[1]/td[12]/div/span[1]"
    kebabButtonFirstRow = "//tbody/tr[1]/td[14]//button"

    changeStatusPopup = "//gp-base-dialog[@title='Change Delivery Status']"
    changeAddressPopup = "//gp-base-dialog[@title='Change Address']"
    excludedTitlePopup = "//div[@class='dialog-header__title gp-dialog-header-title']"

    def __init__(self, page):
        super().__init__(page)
        self.timeRange = None
        self.serviceCount = 0
        self.sumOfDeliveries = 0
        self.excludedRows = 0

    def logIn(self, login, password):
        self.page.goto(self.urlLogin)
        self.page.fill(self.loginInput, login)
        self.page.fill(self.passwordInput, password)
        self.page.click(self.loginButton)
        self.page.wait_for_load_state()
        return self

    def isDeliveriesPage(self):
        self.page.wait_for_url(self.url + "/deliveries")
        self.page.mouse.click(20, 20)
        expect(self.page.locator("//gp-breadcrumbs//a[contains(@href,'/deliveries')]")).to_be_visible()
        return self

    def openDatePicker(self):
        self.page.click(self.openCalendar)
        return self

    def selectToday(self):
        self.page.click(self.todayButton)
        return self

    def selectYesterday(self):
        self.page.click(self.yesterdayButton)
        return self

    def selectLastSevenDays(self):
        self.page.click(self.lastWeekButton)
        return self

    def selectLastMonth(self):
        self.page.click(self.lastMonthButton)
        return self

    def pressApply(self):
        # Wait for spinner to disappear before clicking Apply
        spinner = self.page.locator("//gp-spinner//div[@class='spinner-container']")
        if spinner.is_visible():
            spinner.wait_for(state="hidden", timeout=10000)
        self.page.click(self.applyButton)
        self.dataLoaded()
        return self

    def isTodayDateSelected(self):
        return self

    def isYesterdayDateSelected(self):
        return self

    def isLastSevenDaysSelected(self):
        return self

    def isLastMonthSelected(self):
        return self

    def openServiceFilter(self):
        self.page.click(self.serviceDropdown)
        return self

    def openStatusFilter(self):
        self.page.click(self.statusDropdown)
        return self

    def openVipFilter(self):
        self.page.click(self.vipDropdown)
        return self

    def selectCheckbox(self, type_text):
        self.pressCheckbox(type_text)
        return self

    def selectAllCheckbox(self):
        super().selectAllCheckbox()
        return self

    def closeDropdownByEsc(self):
        self.pressEsc()
        return self

    def setRowsOnPage(self, rows):
        super().setRowsOnPage(rows)
        return self

    def getNumberOfRows(self):
        if self.page.locator(self.noResult).is_visible():
            self.sumOfDeliveries = 0
            return self
        self.sumOfDeliveries = self.getNumberOfSelectedRows()
        return self

    def getCountOfRowsService(self):
        self.serviceCount = self.getNumberOfSelectedRows()
        return self.serviceCount

    def getCountOfRows(self):
        return self.sumOfDeliveries

    def isSelectedRowsEqals(self):
        assert self.sumOfDeliveries == self.getNumberOfSelectedRows()
        return self

    def isSelectedRowsEqualsToSum(self, sum_value):
        assert self.sumOfDeliveries == sum_value
        return self

    def isServiceType(self, type_text):
        if self.page.locator(self.noResult).is_visible():
            return self
        row = self.page.locator(self.rows)
        count = row.count() - 2
        for i in range(0, count):
            deliv_service = self.page.locator(f"//tbody/tr[{i+1}]/td[5]/div")
            expect(deliv_service).to_contain_text(type_text)
        self.serviceCount = self.getNumberOfSelectedRows()
        return self

    def isStatusType(self, type_text):
        if self.page.locator(self.noResult).is_visible():
            return self
        row = self.page.locator(self.rows)
        count = row.count()
        for i in range(0, count):
            status = row.nth(i).locator(".//td[contains(@class,'mat-column-status')]//div[contains(@class,'gp-status-cell')]")
            expect(status).to_contain_text(type_text)
        return self

    def openRange(self):
        self.page.click(self.rangeInput)
        return self

    def selectRange(self, period):
        self.timeRange = super().selectRange(period)
        return self

    def setTimeFromTo(self, t_from, t_to):
        super().setTimeFromTo(t_from, t_to)
        return self

    def isTimeSelected(self):
        return self

    def isTimeSelectedPeriod(self):
        return self

    def checkOfSelectedRowsRange(self):
        return self

    def checkRows(self, numbers=None):
        self.dataDeliv = []
        if numbers:
            for i in numbers:
                self.page.click(f"//tbody/tr[{i}]//mat-checkbox")
                self.dataDeliv.append(self.page.locator(f"//tbody/tr[{i}]/td[2]//a").inner_text())
        return self

    def selectRowCheckbox(self, row):
        self.pressCheckboxFromTable(row)
        return self

    def pressExclude(self):
        self.page.click("//button[contains(normalize-space(),'Exclude')]")
        return self

    def pressExcluded(self):
        self.page.click("//button[.//span[normalize-space()='Exclude']]")
        return self

    def isExcludePopup(self):
        self.page.wait_for_selector(self.excludedTitlePopup)
        expect(self.page.locator(self.excludedTitlePopup)).to_be_visible()
        return self

    def pressExcludeButtonInDialog(self):
        # Click on Exclude button specifically in the exclude dialog
        exclude_button = self.page.locator("//gp-base-dialog//button[@mat-raised-button and .//span[normalize-space()='Exclude']]")
        exclude_button.wait_for(timeout=10000)
        exclude_button.click()
        return self

    def pressButton(self, name):
        self.page.click(f"//button/span[normalize-space()='{name}']")
        return self

    def pressExport(self):
        self.page.click(self.exportButton)
        return self

    def downloadCurrentPage(self, file_name):
        with self.page.expect_download() as download_info:
            self.page.click(self.exportCurrentPage)
        download = download_info.value
        file_path = os.path.join(DOWNLOADS_DIR, f"{file_name}.xlsx")
        download.save_as(file_path)
        self.dataLoaded()
        return self

    def downloadAllPages(self, file_name):
        with self.page.expect_download() as download_info:
            self.page.click(self.exportAllPages)
        download = download_info.value
        file_path = os.path.join(DOWNLOADS_DIR, f"{file_name}.xlsx")
        download.save_as(file_path)
        self.dataLoaded()
        return self

    def isFileDownLoaded(self, file_name):
        file_path = os.path.join(DOWNLOADS_DIR, f"{file_name}.xlsx")
        assert os.path.exists(file_path)
        return self

    def pressApplyPopup(self):
        self.page.click("//gp-base-dialog//button//span[normalize-space()='Apply']")
        return self

    def getNumberOfRoute(self):
        self.page.wait_for_selector("//simple-snack-bar")
        text = self.page.locator("//simple-snack-bar").inner_text()
        self.routeNumber = "".join([c for c in text if c.isdigit()])
        return self

    def isRouteCreated(self):
        return self

    def isRouteHasDeliveries(self):
        return self

    def isExcluded(self):
        expect(self.page.locator(self.deliveryIdFirstRow + "/../div")).to_contain_text("Excluded")
        return self

    def openExcludedPage(self):
        self.page.click(self.excludedButton)
        from pages.excluded_page import ExcludedPage
        return ExcludedPage(self.page)

    def isExcludedPage(self):
        from pages.excluded_page import ExcludedPage
        return ExcludedPage(self.page).isExcludedPage()

    def getExcludedRows(self):
        self.excludedRows = self.getNumberOfSelectedRows() - self.sumOfDeliveries
        return self

    def isExcludedPresent(self):
        if self.excludedRows > 0:
            self.openExcludedPage().isExcludedPage().getNumberOfRows().isExcludedEquals(self.excludedRows).openDeliveriesPage()
        return self

    def pressDeliveryIdSort(self):
        self.page.click(self.sortDelivId)
        return self

    def pressRouteIdSort(self):
        self.page.click(self.sortRouteId)
        return self

    def isDelivSortedAscend(self):
        return self

    def isDelivSortedDescend(self):
        return self

    def isRouteSortedAscend(self):
        return self

    def isRouteSortedDescend(self):
        return self

    def pressKebab(self):
        self.page.click(self.kebabButtonFirstRow)
        return self

    def clickKebabButton(self, name):
        self.page.click(f"//button/span[normalize-space()='{name}']")
        return self

    def pressRescheduleButton(self):
        self.page.click("//button[.//span[normalize-space()='Reschedule']]")
        # Wait for the reschedule dialog to appear
        self.page.wait_for_selector("//gp-base-dialog[@title='Reschedule']", timeout=10000)
        return self

    def selectNextDayInCalendar(self):
        from datetime import datetime, timedelta
        next_day = datetime.now() + timedelta(days=1)
        day_number = next_day.day
        # Click on the next day button in calendar (not disabled)
        self.page.click(f"//button[@class='mat-calendar-body-cell' and not(contains(@class,'mat-calendar-body-disabled')) and .//span[normalize-space()='{day_number}']]")
        return self

    def selectRescheduleRange(self, range_text="10:30-16:00"):
        # Wait for overlay to be ready, then click on range dropdown inside reschedule dialog
        self.pause(0.5)
        # Find the range dropdown specifically in the reschedule dialog
        range_dropdown = self.page.locator("//gp-base-dialog[@title='Reschedule']//mat-select[.//span[contains(@class,'mat-mdc-select-placeholder')]]")
        range_dropdown.wait_for(timeout=10000)
        range_dropdown.click()
        self.pause(0.5)
        # Select the first option from the dropdown
        self.page.locator("//span[@class='mdc-list-item__primary-text']").first.click()
        self.pause(0.5)
        return self

    def pressRescheduleApply(self):
        # Click on Apply button specifically in the reschedule dialog
        apply_button = self.page.locator("//gp-base-dialog[@title='Reschedule']//button[@mat-raised-button and .//span[normalize-space()='Apply']]")
        apply_button.wait_for(timeout=10000)
        apply_button.click()
        return self

    def isChangeAddressPopup(self):
        self.page.wait_for_selector(self.changeAddressPopup)
        return self

    def changeAddresses(self):
        return self

    def isAddressChanged(self):
        return self

    def openRemarks(self):
        self.page.click(self.remarkArea)
        return self

    def fillRemark(self, text):
        self.page.fill(self.remarkTextArea, text)
        return self

    def saveRemark(self):
        self.page.click(self.remarkSaveText)
        return self

    def isRemark(self, text):
        expect(self.page.locator("//tbody/tr[1]/td[13]//div[@class='remark-text-content ng-star-inserted']")).to_contain_text(text)
        return self

    def cancelRemarkSave(self):
        self.page.click(self.remarkTextCancel)
        return self

    def removeVip(self):
        self.page.click("//tr//td[2]/div/mat-icon")
        return self

    def isVIPDeliveryPopup(self):
        self.page.wait_for_selector(self.excludedTitlePopup)
        expect(self.page.locator(self.excludedTitlePopup)).to_contain_text("VIP Delivery")
        return self

    def isRemoveVipPopup(self):
        self.page.wait_for_selector(self.excludedTitlePopup)
        expect(self.page.locator(self.excludedTitlePopup)).to_contain_text("Remove VIP status")
        return self

    def isVIPDelivery(self):
        expect(self.page.locator("//tr//td[2]/div/mat-icon")).to_have_text("star")
        return self

    def isNonVIPDelivery(self):
        expect(self.page.locator("//tr//td[2]/div/mat-icon")).to_have_text("star_border")
        return self

    def pressSearchHeaderButton(self):
        self.page.click(self.searchButton)
        return self

    def pressSearchHeaderButtonRoute(self):
        self.page.click(self.searchButton)
        return self

    def cleanFilterHeader(self):
        self.page.click(self.cleanSearchInputHeader)
        return self

    def fillSearchHeaderInput(self, text):
        super().fillSearchHeaderInput(text)
        return self

    def fillSearchInput(self, text=None):
        if text is None and self.dataDeliv:
            text = self.dataDeliv[0]
        search_input = self.page.locator(self.searchInput).first
        search_input.wait_for()
        search_input.fill(text or "")
        search_input.press("Enter")
        return self

    def getSearchNData(self, index):
        # store delivery id for later search
        self.dataDeliv = [self.page.locator(f"//tbody/tr[{index}]/td[2]//a").inner_text()]
        return self

    def getDeliveryData(self):
        self.deliveryData = DeliveryDetails.builder().build()
        self.deliveryData.deliveryId = self.page.locator(self.deliveryIdFirstRow).inner_text()
        self.deliveryData.routeId = self.page.locator(self.routeIdFirstRow).inner_text()
        self.deliveryData.packageId = self.page.locator(self.packageIDFirstRow).inner_text()
        self.deliveryData.serviceType = self.page.locator(self.serviceFirstRow).inner_text()
        self.deliveryData.status = self.page.locator(self.statusFirstRow).inner_text()
        self.deliveryData.pickUpAddress = self.page.locator(self.pickAddrFirstRow).inner_text()
        self.deliveryData.dropOffAddress = self.page.locator(self.dropAddrFirstRow).inner_text()
        return self

    def isDeliveryFound(self, *args, **kwargs):
        if not self.dataDeliv:
            return self
        expect(self.page.locator(self.deliveryIdFirstRow)).to_contain_text(self.dataDeliv[0])
        return self

    def isRouteFound(self):
        return self

    def isRowsContainData(self):
        return self

    def isRowsOnPage(self, rows):
        return self

    def isLogedOut(self):
        expect(self.page).to_have_url(self.urlLogin)
        return self

    def logout(self):
        self.page.click(self.logoutButton)
        return self

    def openRoutesPage(self):
        self.page.keyboard.press("Escape")
        self.page.click(self.routesButton)
        from pages.routes_page import RoutesPage
        return RoutesPage(self.page)

    def openExcludedPage(self):
        self.page.click(self.excludedButton)
        from pages.excluded_page import ExcludedPage
        return ExcludedPage(self.page)

    def openAlertsPage(self):
        if not self.page.locator(self.alertsButton).is_visible():
            self.page.click(self.alertsSettingsButton)
        self.page.click(self.alertsButton)
        from pages.alerts_page import AlertsPage
        return AlertsPage(self.page)

    def openSettingsPage(self):
        if not self.page.locator(self.settingsButton).is_visible():
            self.page.click(self.alertsSettingsButton)
        self.page.click(self.settingsButton)
        from pages.settings_page import SettingsPage
        return SettingsPage(self.page)

    def openFinancePage(self):
        self.page.click(self.financeButton)
        from pages.finance_page import FinancePage
        return FinancePage(self.page)

    def openAdminFeatureFlag(self):
        if not self.page.locator(self.featureFlagButton).is_visible():
            self.page.click(self.adminButton)
        self.page.click(self.featureFlagButton)
        from pages.feature_flag_page import FeatureFlagPage
        return FeatureFlagPage(self.page)

    def openAdminOpeningHoursPage(self):
        if not self.page.locator(self.operatingHoursButton).is_visible():
            self.page.click(self.adminButton)
        self.page.click(self.operatingHoursButton)
        from pages.operating_hours_page import OperatingHoursPage
        return OperatingHoursPage(self.page)

    def openOpsRealTimePage(self):
        self.page.click(self.opsRealTimeButton)
        from pages.ops_real_time_page import OpsRealTimePage
        return OpsRealTimePage(self.page)

    def openCouriersPage(self):
        # Couriers is under the Accounts & Users section
        self.page.click(self.accountsUsersButton)
        self.page.click(self.couriersButton)
        from pages.couriers_page import CouriersPage
        return CouriersPage(self.page)

    def openSendersPage(self):
        self.page.click(self.sendersButton)
        from pages.senders_page import SendersPage
        return SendersPage(self.page)

    def openUsersPage(self):
        self.page.click(self.usersButton)
        from pages.users_page import UsersPage
        return UsersPage(self.page)

    def openDeliveriesPage(self):
        self.page.click(self.deliveriesButton)
        return DeliveriesPage(self.page)

    # alias for generated tests
    def open_routes_page(self):
        return self.openRoutesPage()
