from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.deliveries_page import DeliveriesPage
from pages.routes_page import RoutesPage
from models.user_details import UserDetails


class UsersPage(BasePage):
    usersBreadcrumbs = "//gp-breadcrumbs//a[@href='/users']"
    searchUserInput = "//gp-external-users-filters//mat-label[contains(normalize-space(),'Search')]/ancestor::div/input"

    def isStatusUser(self, status):
        count = self.page.locator(self.rows).count()
        for i in range(1, count + 1):
            expect(self.page.locator(f"{self.rows}[{count}]/td[4]/div")).to_contain_text(status)
        return self

    def setStatusUser(self, status):
        self.page.click(self.statusDropdown)
        self.pressCheckbox(status)
        self.pressEsc()
        return self

    def isUserFound(self):
        r = "//gp-external-users-table" + self.rows
        expect(self.page.locator(r + "[1]/td[1]")).to_contain_text(self.userDetails.getDateCreate())
        expect(self.page.locator(r + "[1]/td[2]/a")).to_contain_text(self.userDetails.getUserId())
        expect(self.page.locator(r + "[1]/td[3]")).to_contain_text(self.userDetails.getUserName())
        expect(self.page.locator(r + "[1]/td[4]/div")).to_contain_text(self.userDetails.getUserStatus())
        return self

    def isUserFoundByName(self):
        r = "//gp-external-users-table" + self.rows
        expect(self.page.locator(r + "[1]/td[3]")).to_contain_text(self.userDetails.getUserName())
        return self

    def findUserByUserName(self):
        self.clearFilter()
        self.page.fill(self.searchUserInput, self.userDetails.getUserName())
        self.pressApply()
        return self

    def findUserByUserId(self):
        self.clearFilter()
        self.page.fill(self.searchUserInput, self.userDetails.getUserId())
        self.pressApply()
        return self

    def openDatePicker(self):
        self.page.click(self.openCalendar)
        return self

    def selectLastSevenDays(self):
        self.page.click(self.lastWeekButton)
        return self

    def isLastSevenDaysSelected(self):
        return self

    def pressApply(self):
        self.page.click("//gp-external-users-filters" + self.applyButton)
        self.page.locator("//gp-external-users-table" + self.rows + "[1]").first.wait_for()
        return self

    def clearFilter(self):
        self.page.click("//gp-external-users-filters" + self.clearButton)
        self.page.locator(self.rows + "[20]").wait_for()
        return self

    def getUserDetailsFromTable(self):
        self.page.locator(self.rows + "[20]").wait_for()
        count = self.page.locator("//gp-external-users-table" + self.rows).count()
        count = max(1, count)
        row = min(count, 1)
        self.userDetails = UserDetails.builder()\
            .userName(self.page.locator(self.rows + f"[{row}]/td[3]").inner_text())\
            .userStatus(self.page.locator(self.rows + f"[{row}]/td[4]/div").inner_text())\
            .userId(self.page.locator(self.rows + f"[{row}]/td[2]/a").inner_text())\
            .dateCreate(self.page.locator(self.rows + f"[{row}]/td[1]").inner_text())\
            .build()
        return self

    def isUsersPage(self):
        self.page.wait_for_url(self.url + "/users")
        self.page.mouse.click(20, 20)
        expect(self.page.locator(self.usersBreadcrumbs)).to_be_visible()
        return self

    def openDeliveriesPage(self):
        self.page.click(self.deliveriesButton)
        return DeliveriesPage(self.page)

    def openRoutesPage(self):
        self.page.click(self.routesButton)
        return RoutesPage(self.page)
