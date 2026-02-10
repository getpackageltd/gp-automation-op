from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.deliveries_page import DeliveriesPage
from pages.routes_page import RoutesPage


class OpsRealTimePage(BasePage):
    realTimeBreadcrumbs = "//gp-breadcrumbs//a[@href='/dashboard-real-time']"

    def isOpsRealTimePage(self):
        self.page.wait_for_url(self.url + "/dashboard-real-time")
        self.page.mouse.click(20, 20)
        expect(self.page.locator(self.realTimeBreadcrumbs)).to_be_visible()
        return self

    def openDeliveriesPage(self):
        self.page.click(self.deliveriesButton)
        return DeliveriesPage(self.page)

    def openRoutesPage(self):
        self.page.click(self.routesButton)
        return RoutesPage(self.page)
