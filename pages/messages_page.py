from datetime import datetime
from playwright.sync_api import expect

from pages.base_page import BasePage


class MessagesPage(BasePage):
    courierDetailsBreadcr = "//a[normalize-space()='Courier Details View']"
    courierMessagesBreadcr = "//a[normalize-space()='Messages']"

    def isCourierMessagesPage(self):
        self.dataLoaded()
        # Wait for either the table to have rows or the "No Result" to appear
        try:
            self.page.locator("//tbody//tr[1]").wait_for(timeout=5000)
        except Exception:
            # If still empty, try to refresh once as messages might take time to sync
            self.page.reload()
            self.dataLoaded()
            self.page.locator("//tbody//tr[1]").wait_for(timeout=10000)
        
        expect(self.page.locator(self.courierMessagesBreadcr)).to_be_visible()
        return self

    def isBlockedMessagesSent(self):
        # The loop was likely intended to wait for rows, but let's make it robust
        self.page.locator("//tbody//tr[1]/td[5]").wait_for()
        time_stamp = self.page.locator("//tbody//tr[1]/td[5]").inner_text()
        date = datetime.strptime(time_stamp, "%d/%m/%Y,%H:%M")
        assert date >= BasePage.localDate
        
        expect(self.page.locator("//tbody//tr[1]/td[1]")).to_contain_text("WEBSOCKET")
        expect(self.page.locator("//tbody//tr[1]/td[4]")).to_contain_text('{"code":51,"event":"accountBlocked"}')
        expect(self.page.locator("//tbody//tr[2]/td[1]")).to_contain_text("PUSH_NOTIFICATION")
        return self

    def backToCourierDetailsPage(self):
        self.page.click(self.courierDetailsBreadcr)
        from pages.courier_details_page import CourierDetailsPage
        return CourierDetailsPage(self.page)
