from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.deliveries_page import DeliveriesPage
from pages.routes_page import RoutesPage


class ExcludedPage(BasePage):
    numberOfRows = "//div[@class='gp-page-info']/div[@class='ng-star-inserted']"
    excludedBreadcrumbs = "//gp-breadcrumbs//a[@href='/excluded']"
    button = "//button"
    createManuallyPopup = "//gp-base-dialog[@title='Create Route Manually']/div[@class='dialog-container']"
    createManuallyPopupTitle = "//gp-base-dialog[@title='Create Route Manually']/div[@class='dialog-container']//div[@class='dialog-header__title gp-dialog-header-title']"
    createManuallyPopupMap = "//div[@class='gm-style']"
    gotIt = "//simple-snack-bar[@class='mat-simple-snackbar ng-star-inserted']"

    def __init__(self, page):
        super().__init__(page)
        self.numberOfRowsSelected = 0

    def getNumberOfSelectedRows(self):
        num_text = self.page.locator(self.numberOfRows).inner_text()
        parts = num_text.split()
        return int(parts[2]) if len(parts) >= 3 else 0

    def checkRows(self):
        if not self.dataDeliv:
            return self
        for deliv_id in self.dataDeliv:
            self.page.click(f"//tbody/tr/td//a[normalize-space()='{deliv_id}']/../../../td[1]//mat-checkbox")
        return self

    def setRowsOnPage(self, rows):
        super().setRowsOnPage(rows)
        return self

    def getNumberOfRows(self):
        self.numberOfRowsSelected = self.getNumberOfSelectedRows()
        return self

    def isExcludedPage(self):
        self.page.wait_for_url(self.url + "/excluded")
        self.dataLoaded()
        expect(self.page.locator(self.excludedBreadcrumbs)).to_be_visible()
        return self

    def isExcludedEquals(self, number):
        assert number == self.numberOfRowsSelected
        return self

    def openDeliveriesPage(self):
        self.page.click(self.deliveriesButton)
        return DeliveriesPage(self.page)

    def openRoutesPage(self):
        self.page.click(self.routesButton)
        return RoutesPage(self.page)

    def selectRowCheckbox(self, row):
        self.pressCheckboxFromTable(row)
        return self

    def pressButton(self, button):
        self.page.click(self.button + f"//div[normalize-space()='{button}']")
        self.dataLoaded()
        return self

    def isCeationRoutePopup(self):
        self.page.wait_for_selector(self.createManuallyPopup)
        expect(self.page.locator(self.createManuallyPopupTitle)).to_be_visible()
        expect(self.page.locator(self.createManuallyPopupMap)).to_be_visible()
        return self

    def pressApplyPopup(self):
        self.page.click(self.createManuallyPopup + "//button//span[normalize-space()='Apply']")
        return self

    def getNumberOfRoute(self):
        self.page.wait_for_selector(self.gotIt)
        self.routeNumber = "".join([c for c in self.page.locator(self.gotIt).inner_text() if c.isdigit()])
        return self
