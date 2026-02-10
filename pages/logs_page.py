from datetime import datetime
from playwright.sync_api import expect

from pages.base_page import BasePage


class LogsPage(BasePage):
    courierDetailsBreadcr = "//a[normalize-space()='Courier Details View']"
    senderDetailsBreadcr = "//a[normalize-space()='Account Details View']"
    courierLogsBreadcr = "//a[normalize-space()='Logs']"

    def backToCourierDetailsPage(self):
        self.page.click(self.courierDetailsBreadcr)
        from pages.courier_details_page import CourierDetailsPage
        return CourierDetailsPage(self.page)

    def backToSenderDetailsPage(self):
        self.page.click(self.senderDetailsBreadcr)
        from pages.sender_details_page import SenderDetailsPage
        return SenderDetailsPage(self.page)

    def isLineOfBusinessLogs(self, lines):
        i = 15
        for line in lines:
            time_stamp = self.page.locator(f"//tbody//tr[{i}]/td[3]").inner_text()
            date = datetime.strptime(time_stamp, "%d/%m/%Y,%H:%M")
            assert date >= BasePage.localDate
            expect(self.page.locator(f"//tbody//tr[{i}]/td[6]")).to_contain_text(line)
            i -= 1
        return self

    def isLogsPage(self):
        self.page.locator("//tbody//tr[2]").wait_for()
        expect(self.page.locator(self.courierLogsBreadcr)).to_be_visible()
        return self

    def isLogsRecordBlockRemoved(self):
        time_stamp = self.page.locator("//tbody//tr[1]/td[3]").inner_text()
        date = datetime.strptime(time_stamp, "%d/%m/%Y,%H:%M")
        assert date >= BasePage.localDate
        expect(self.page.locator("//tbody//tr[1]/td[1]")).to_contain_text("Change Status Reason Was Changed")
        expect(self.page.locator("//tbody//tr[1]/td[6]")).to_contain_text("The Change Status Reason was changed from Unset to: Active Block Removed")
        return self

    def isLogsRecordActivated(self):
        time_stamp = self.page.locator("//tbody//tr[1]/td[3]").inner_text()
        date = datetime.strptime(time_stamp, "%d/%m/%Y,%H:%M")
        assert date >= BasePage.localDate
        expect(self.page.locator("//tbody//tr[1]/td[1]")).to_contain_text("Activate")
        return self

    def isLogsRecordBlock(self):
        self.pause(0.5)
        time_stamp = self.page.locator("//tbody//tr[1]/td[3]").inner_text()
        date = datetime.strptime(time_stamp, "%d/%m/%Y,%H:%M")
        assert date >= BasePage.localDate
        expect(self.page.locator("//tbody//tr[1]/td[1]")).to_contain_text("Blocked")
        return self

    def isLogsRecord(self, status):
        time_stamp = self.page.locator("//tbody//tr[1]/td[3]").inner_text()
        date = datetime.strptime(time_stamp, "%d/%m/%Y,%H:%M")
        expect(self.page.locator("//tbody//tr[1]/td[6]")).to_contain_text(status)
        assert date >= BasePage.localDate
        return self
