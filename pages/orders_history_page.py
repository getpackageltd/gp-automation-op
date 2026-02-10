from playwright.sync_api import expect

from pages.base_page import BasePage


class OrdersHistoryPage(BasePage):
    ordersHistoryButton = "//div[normalize-space()='Orders History']"
    genInfoButton = "//div[normalize-space()='General Information']"
    filterBoard = "//gp-senders-charge-lines-filters/gp-page-filter-layout/mat-card"

    def isOrderHistoryPage(self):
        expect(self.page.locator(self.ordersHistoryButton + "[contains(@class,'active')]")).to_be_visible()
        expect(self.page.locator(self.filterBoard)).to_be_visible()
        return self

    def backToSenderDetailsPage(self):
        self.page.click(self.genInfoButton)
        from pages.sender_details_page import SenderDetailsPage
        return SenderDetailsPage(self.page)
