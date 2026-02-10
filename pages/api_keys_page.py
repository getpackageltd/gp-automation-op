import time

from playwright.sync_api import expect

from pages.base_page import BasePage


class ApiKeysPage(BasePage):
    createApiPage = "//gp-sender-api-keys"
    createApiButton = createApiPage + "//button//mat-icon[normalize-space()='add']"
    createApiPopup = "//gp-create-api-key"
    apiKeyName = createApiPopup + "//mat-form-field[1]//input"
    seviceDropdown = createApiPopup + "//mat-select"
    saveButton = createApiPopup + "//button//span[normalize-space()='Save']"
    confirmationPopup = "//gp-confirmation-dialog"
    deleteButton = confirmationPopup + "//button/span[normalize-space()='Delete']"

    apiKeyData = None

    def isApiKeyCreated(self):
        expect(self.page.locator(self.createApiPage + self.rows + "[last()]/td[1]")).to_contain_text(self.apiKeyData[0])
        expect(self.page.locator(self.createApiPage + self.rows + "[last()]/td[2]")).to_contain_text(self.getDateDDmmYYYY())
        expect(self.page.locator(self.createApiPage + self.rows + "[last()]/td[3]")).to_contain_text(self.apiKeyData[1])
        key_len = len(self.page.locator(self.createApiPage + self.rows + "[last()]/td[5]").inner_text())
        assert key_len >= 36
        return self

    def deleteApiKey(self):
        self.page.click(self.createApiPage + self.rows + "[last()]/td[6]/div[1]/div[2]/button")
        self.pressDeleteButton()
        return self

    def createNewApiKey(self, service):
        self.apiKeyData = []
        self.pressCreateApi()
        self.fillApiKeyDetails(service)
        self.pressSaveButton()
        return self

    def editApiKey(self):
        name = "ApiKey_" + str(int(time.time()))
        self.page.click(self.createApiPage + self.rows + "[last()]/td[6]/div[1]/div[1]/button")
        self.page.fill(self.apiKeyName, name)
        self.apiKeyData[0] = name
        self.pressSaveButton()
        return self

    def fillApiKeyDetails(self, service):
        name = "ApiKey_" + str(int(time.time()))
        self.page.fill(self.apiKeyName, name)
        self.selectService(service)
        self.apiKeyData.append(name)
        self.apiKeyData.append(service)
        return self

    def pressSaveButton(self):
        self.page.click(self.saveButton)
        self.page.locator("//snack-bar-container").wait_for()
        self.page.click("//snack-bar-container//button")
        self.dataLoaded()
        return self

    def pressDeleteButton(self):
        self.page.click(self.deleteButton)
        self.page.locator("//snack-bar-container").wait_for()
        self.page.click("//snack-bar-container//button")
        self.dataLoaded()
        return self

    def selectService(self, service):
        self.page.click(self.seviceDropdown)
        self.page.locator(f"//span[normalize-space()='{service}']").click(force=True)
        return self

    def pressCreateApi(self):
        self.page.click(self.createApiButton)
        return self

    def isApiKeysPage(self):
        expect(self.page.locator(self.createApiButton)).to_be_visible()
        return self
