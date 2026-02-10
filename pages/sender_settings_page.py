from playwright.sync_api import expect

from pages.base_page import BasePage


class SenderSettingsPage(BasePage):
    senderSettingsCard = "//gp-sender-settings"
    dropOffOptPromptIcon = "//gp-sender-settings//div[normalize-space()='Drop-off Options:']/img"
    prompt = "//div[@class='mat-tooltip mat-tooltip-show']"
    directlyToReceiverButton = "//mat-radio-group/mat-radio-button"
    allowAlternativeButton = "//mat-radio-group/div/mat-radio-button"
    settingsButton = "//div[normalize-space()='Settings']"
    vipSenderCheckbox = senderSettingsCard + "/div[2]//mat-checkbox/label[1]/span[1]"
    checkboxBlock = "//gp-sender-settings/div[1]/div[2]"
    allCheckbox = checkboxBlock + "/mat-checkbox"

    def isAllAlternativeHandoff(self):
        self.reloadSettings()
        expect(self.page.locator(self.allCheckbox + "/../div//input[@aria-checked='true']")).to_have_count(8)
        return self

    def isAlternativeHandoff(self, index):
        self.reloadSettings()
        expect(self.page.locator(self.allCheckbox + f"/../div[{index}]//input")).to_have_attribute("aria-checked", "true")
        return self

    def alternativeHandoff(self, index=None):
        if index is None:
            self.page.click(self.allowAlternativeButton)
        elif isinstance(index, str):
            self.page.click(self.allCheckbox + f"//span[normalize-space(text())='{index}']")
        else:
            self.page.click(self.allCheckbox + f"/../div[{index}]/mat-checkbox")
        return self

    def isVipSender(self):
        self.reloadSettings()
        expect(self.page.locator(self.vipSenderCheckbox + "//input[@aria-checked='true']")).to_be_visible()
        return self

    def vipSender(self):
        self.page.click(self.vipSenderCheckbox)
        return self

    def reloadSettings(self):
        self.page.reload()
        self.page.wait_for_load_state()
        self.page.click(self.settingsButton)
        return self

    def isDirectlyToReceiver(self):
        self.reloadSettings()
        expect(self.page.locator(self.directlyToReceiverButton + "//input[@tabindex='0']")).to_be_visible()
        return self

    def directlyToReceiver(self):
        self.page.click(self.directlyToReceiverButton)
        return self

    def isSenderSettingsPage(self):
        handle = self.page.query_selector(self.dropOffOptPromptIcon)
        handle.hover()
        self.page.locator(self.prompt).wait_for()
        expect(self.page.locator(self.prompt)).to_be_visible()
        return self
