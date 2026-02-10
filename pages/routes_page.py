from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class RoutesPage(BasePage):
    kebabButtonFirstRow = "//tbody/tr[1]/td[14]//button"

    def __init__(self, page):
        super().__init__(page)
        self.timeRange = None
        self.serviceCount = 0
        self.sumOfRoutes = 0

    def isRoutesPage(self):
        self.page.wait_for_url(self.url + "/routes")
        expect(self.page.locator("//gp-breadcrumbs//a[contains(@href,'/routes')][normalize-space()='Routes']")).to_be_visible()
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
        self.page.click(self.applyButton)
        self.dataLoaded()
        return self

    def openServiceFilter(self):
        self.page.click(self.serviceDropdown)
        return self

    def openStatusFilter(self):
        self.page.click(self.statusDropdown)
        return self

    def openAlertNameFilter(self):
        self.page.click(self.alertNameDropdown)
        return self

    def openRange(self):
        self.page.click(self.rangeInput)
        return self

    def selectRange(self, period):
        self.timeRange = super().selectRange(period)
        return self

    def setRowsOnPage(self, rows):
        super().setRowsOnPage(rows)
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

    def getNumberOfRows(self):
        if self.page.locator(self.noResult).is_visible():
            self.sumOfRoutes = 0
            return self
        self.sumOfRoutes = self.getNumberOfSelectedRows()
        return self

    def getCountOfRowsService(self):
        return self.serviceCount

    def getCountOfRows(self):
        return self.sumOfRoutes

    def isSelectedRowsEqals(self):
        assert self.sumOfRoutes == self.getNumberOfSelectedRows()
        return self

    def isSelectedRowsEqualsToSum(self, sum_value):
        assert self.sumOfRoutes == sum_value
        return self

    def isServiceType(self, type_text):
        if self.page.locator(self.noResult).is_visible():
            return self
        row = self.page.locator(self.rows)
        count = row.count() - 2
        for i in range(0, count):
            deliv_service = row.nth(i).locator("//td[5]/div[1]")
            expect(deliv_service).to_contain_text(type_text)
        self.serviceCount = self.getNumberOfSelectedRows()
        return self

    def isStatusType(self, type_text):
        if self.page.locator(self.noResult).is_visible():
            return self
        row = self.page.locator(self.rows)
        count = row.count() - 2
        for i in range(0, count):
            status = row.nth(i).locator("//td[10]/div[1]/div[1]")
            expect(status).to_contain_text(type_text)
        return self

    def isLastSevenDaysSelected(self):
        return self

    def isLastMonthSelected(self):
        return self

    def isTodayDateSelected(self):
        return self

    def isYesterdayDateSelected(self):
        return self

    def isTimeSelected(self):
        return self

    def isTimeSelectedPeriod(self):
        return self

    def checkOfSelectedRowsRange(self):
        return self

    def clickKebabButton(self, name):
        self.page.click(f"//button/span[normalize-space()='{name}']")
        return self

    def pressKebab(self):
        self.page.click(self.kebabButtonFirstRow)
        return self

    def clickTextArea(self):
        return self

    def clickTitleArea(self):
        return self

    def fillTextArea(self, text):
        return self

    def fillTitleText(self, text):
        return self

    def resetTextArea(self):
        return self

    def fillRemark(self, text):
        return self

    def saveRemark(self):
        return self

    def cancelRemarkSave(self):
        return self

    def isRemark(self, text):
        return self

    def pressDeliveryIdSort(self):
        return self

    def isDelivSortedAscend(self):
        return self

    def isDelivSortedDescend(self):
        return self

    def isRoutesPage(self):
        self.page.wait_for_url(self.url + "/routes")
        return self

    def getSearchNData(self, index):
        self.dataDeliv = [self.page.locator(f"//tbody/tr[{index}]/td[2]//a").inner_text()]
        return self

    def fillSearchHeaderInput(self, text):
        super().fillSearchHeaderInput(text)
        return self

    def pressSearchHeaderButtonRoute(self):
        self.page.click(self.searchButton)
        return self

    def cleanFilterHeader(self):
        self.page.click(self.cleanSearchInputHeader)
        return self

    def getDeliveryData(self):
        return self

    def isDeliveryFound(self, *args, **kwargs):
        return self

    def isRouteFound(self):
        return self

    def getCourierName(self):
        return self

    def getCourierID(self):
        return self

    def searchLocatedCourier(self):
        return self

    def isCourierNameTrue(self):
        return self

    def isCourierFoundByName(self):
        return self

    def isCourierFoundByID(self):
        return self

    def isLocatingCourierPopup(self):
        return self

    def isAssignCourierPopup(self):
        return self

    def assignCourierPopup(self, courier_id):
        return self

    def clickChangeStatusButton(self):
        return self

    def changeStatusTo(self, status):
        return self

    def isDetailPage(self):
        return self

    def getCourierTotalPrice(self):
        return self

    def getCourierId(self):
        return self

    def getDeliveryNumber(self):
        return self

    def getPackageId(self):
        return self

    def getPackageSize(self):
        return self

    def getSenderBasePrice(self):
        return self

    def openDeliveryDetails(self):
        return self

    def openCourierPayout(self):
        return FinancePage(self.page)

    def openSenderChargeLines(self):
        return FinancePage(self.page)

    def findByRouteID(self):
        return self

    def isCourierPayout(self):
        return self

    def isSenderChargeLine(self):
        return self

    def isPushPopup(self):
        return self

    def isUnnassignCourierPopup(self):
        return self

    def setNextAvailableDay(self):
        return self

    def setTime(self, time_str):
        return self

    def setDistance(self, distance):
        return self

    def isReschedulePopup(self):
        return self

    def isRescheduledDay(self):
        return self

    def isRescheduledTime(self):
        return self

    def isAlertInRow(self):
        return self

    def isRowsContainData(self):
        return self

    def isRowsOnPage(self, rows):
        return self

    def isLogedOut(self):
        expect(self.page).to_have_url(self.url + "/login")
        return self

    def logout(self):
        self.page.click(self.logoutButton)
        return self

    def openDeliveriesPage(self):
        self.page.click(self.deliveriesButton)
        from pages.deliveries_page import DeliveriesPage
        return DeliveriesPage(self.page)

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
