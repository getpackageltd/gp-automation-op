from datetime import datetime
from playwright.sync_api import expect

from config import RESOURCES_DIR
from pages.base_page import BasePage
from pages.api_keys_page import ApiKeysPage
from pages.account_users_page import AccountUsersPage
from pages.branches_page import BranchesPage
from pages.logs_page import LogsPage
from pages.orders_history_page import OrdersHistoryPage
from pages.sender_settings_page import SenderSettingsPage
from pages.user_details_page import UserDetailsPage
from apimodule.requests_builder import RequestsBuilder


class SenderDetailsPage(BasePage):
    accDetViewBeadcrumbs = "//a[normalize-space()='Account Details View']"
    titleArea = "//div[@class='gp-top-account-details-grid']"
    titleName = titleArea + "/div[2]"
    titleStatus = titleArea + "/div[3]"
    titleAccType = titleArea + "/div[4]"
    addPhotoButton = titleArea + "//button/mat-icon"
    sendersPhoto = titleArea + "//img"
    senderGenInfoArea = "//gp-sender-general-info/div"
    accDetailsCard = senderGenInfoArea + "//div[normalize-space()='Account Details']/../.."
    accId = accDetailsCard + "//div[normalize-space()='Account ID']/../div[2]"
    userIdSender = accDetailsCard + "//div[normalize-space()='User ID']/../div[2]"
    lineOfBusiness = accDetailsCard + "//div[normalize-space()='Line of Business']/../div[2]"
    editLineOfBusinessButton = accDetailsCard + "//div[normalize-space()='Line of Business']/../mat-icon"
    managedAcc = accDetailsCard + "//div[normalize-space()='Managed Account']/../div[2]"
    editManagedAcc = accDetailsCard + "//div[normalize-space()='Managed Account']/../mat-icon"
    addressSender = accDetailsCard + "//div[normalize-space()='Address']/../div[2]"
    editAddressSender = accDetailsCard + "//div[normalize-space()='Address']/../mat-icon"
    createdSender = accDetailsCard + "//div[normalize-space()='Created At']/../div[2]"
    lastOrderSender = accDetailsCard + "//div[normalize-space()='Last Order']/../div[2]"
    brandName = accDetailsCard + "//div[normalize-space()='Brand name']/../div[2]"
    editBrandName = accDetailsCard + "//div[normalize-space()='Brand name']/../mat-icon"
    accFinDetails = senderGenInfoArea + "//div[normalize-space()='Account Financial Details']/../.."
    chargingType = accFinDetails + "//div[normalize-space()='Charging Type']/../div[2]"
    editChargingType = accFinDetails + "//div[normalize-space()='Charging Type']/../mat-icon"
    paymentMethod = accFinDetails + "//div[normalize-space()='Payment Method']/../div[2]"
    editPaymentMethod = accFinDetails + "//div[normalize-space()='Payment Method']/../mat-icon"
    taxIdSender = accFinDetails + "//div[normalize-space()='Tax ID']/../div[2]"
    editTaxIdSender = accFinDetails + "//div[normalize-space()='Tax ID']/../mat-icon"
    finNameSender = accFinDetails + "//div[normalize-space()='Financial Name']/../div[2]"
    editFinNameSender = accFinDetails + "//div[normalize-space()='Financial Name']/../mat-icon"
    billingEmailSender = accFinDetails + "//div[normalize-space()='Billing e-mail']/../div[2]/div"
    editBillingEmailSender = accFinDetails + "//div[normalize-space()='Billing e-mail']/..//mat-icon"
    accPaymentCard = senderGenInfoArea + "//div[normalize-space()='Credit Card Details']/../.."
    cardNumber = accPaymentCard + "//div[normalize-space()='CC Number']/../div[2]"
    editCardNumber = accPaymentCard + "//mat-icon[@mattooltip='Edit Credit Card']"

    ownerDetailsCard = senderGenInfoArea + "//div[normalize-space()='Owner Details']/../.."
    ownerName = ownerDetailsCard + "//div[normalize-space()='Name']/../div[2]"
    ownerEmail = ownerDetailsCard + "//div[normalize-space()='Email']/../div[2]"
    ownerPhoneNumber = ownerDetailsCard + "//div[normalize-space()='Phone Number']/../div[2]"
    adminRemarksCard = "//gp-account-admin-remarks"
    admRemarksInput = adminRemarksCard + "//input"
    saveAdmRemarkButton = adminRemarksCard + "//img[contains(@src,'check.svg')]"
    remarkContent = adminRemarksCard + "//div[contains(@class,'gp-remark')]//div[contains(@class,'gp-remark-comment')]"
    createAdmRemarkButton = adminRemarksCard + "//button"
    cancelAdmRemark = adminRemarksCard + "//img[contains(@src,'cancel.svg')]"
    deleteRemarkButton = adminRemarksCard + "//mat-icon[normalize-space()='delete']"
    popup = "//mat-dialog-container"
    input = "//input"
    confirmationPopup = "//gp-confirmation-dialog"
    saveButton = "//button/span[normalize-space()='Save']"
    cancelButton = "//button/span[normalize-space()='Cancel']"
    deleteButton = "//button/span[normalize-space()='Delete']"
    blockAccButton = "//span[normalize-space()='Block Account']"
    activateAccButton = "//span[normalize-space()='Activate Account']"
    logsButton = "//a[normalize-space()='Logs']"
    ordersHistoryButton = "//div[normalize-space()='Orders History']"
    genInfoButton = "//div[normalize-space()='General Information']"
    branchesButton = "//div[normalize-space()='Branches']"
    accountsButton = "//div[normalize-space()=\"Account's Users\"]"
    apiKeysButton = "//div[normalize-space()='API Keys']"
    settingsButton = "//div[normalize-space()='Settings']"

    editLineOfBusinessPopup = "//gp-edit-line-of-business"
    editAddressPopup = "//gp-edit-address"
    editFinDetailsPopup = "//gp-edit-financial-details"
    dropdownMenu = "//mat-select"

    def openSenderSettings(self):
        if not self.page.locator(self.settingsButton + "[contains(@class,'active')]").is_visible():
            self.page.click(self.settingsButton)
        return SenderSettingsPage(self.page)

    def openAccountUsersPage(self):
        if not self.page.locator(self.accountsButton + "[contains(@class,'active')]").is_visible():
            self.page.click(self.accountsButton)
        return AccountUsersPage(self.page)

    def openBranches(self):
        if not self.page.locator(self.branchesButton + "[contains(@class,'active')]").is_visible():
            self.page.click(self.branchesButton)
        return BranchesPage(self.page)

    def isAddressChanged(self):
        expect(self.page.locator(self.addressSender)).not_to_contain_text(self.dataSender.getSAddress())
        return self

    def isTaxId(self, number):
        expect(self.page.locator(self.taxIdSender)).to_contain_text(number)
        return self

    def editTaxId(self, number):
        self.pressEditAccDetails(self.editTaxIdSender, self.editFinDetailsPopup)
        self.page.fill(self.editFinDetailsPopup + self.input, number)
        self.saveSelected()
        return self

    def isPendingEmailBilling(self, email):
        expect(self.page.locator(self.billingEmailSender + "[2]")).to_contain_text(email)
        return self

    def isEmailBilling(self):
        expect(self.page.locator(self.billingEmailSender)).to_contain_text(self.dataSender.getSEmail())
        expect(self.page.locator(self.billingEmailSender + "[2]")).not_to_be_visible()
        return self

    def editEmailBilling(self, email=None):
        self.pressEditAccDetails(self.editBillingEmailSender, self.editFinDetailsPopup)
        self.page.fill(self.editFinDetailsPopup + self.input, email or self.dataSender.getSEmail())
        self.pause(1)
        self.saveSelected()
        return self

    def editFinName(self, name):
        self.pressEditAccDetails(self.editFinNameSender, self.editFinDetailsPopup)
        self.page.fill(self.editFinDetailsPopup + self.input, name)
        self.saveSelected()
        return self

    def isFinName(self, name):
        expect(self.page.locator(self.finNameSender)).to_contain_text(name)
        return self

    def changeAddress(self):
        self.dataSender.setSAddress(self.page.locator(self.addressSender).inner_text())
        self.pressEditAccDetails(self.editAddressSender, self.editAddressPopup)
        self.page.fill(self.editAddressPopup + self.input, RequestsBuilder().getRandomeAddress())
        self.isGooglAddressAppeared()
        address = self.page.locator(self.googleAddr).inner_text()
        self.page.click(self.googleAddr)
        self.saveSelected()
        return self

    def openApiKeysPage(self):
        if not self.page.locator(self.apiKeysButton + "[contains(@class,'active')]").is_visible():
            self.page.click(self.apiKeysButton)
        return ApiKeysPage(self.page)

    def openSenderDetailsBusiness(self):
        if not self.page.locator(self.accId).is_visible():
            if self.senderBusinessID is None:
                from pages.deliveries_page import DeliveriesPage
                DeliveriesPage(self.page).openSendersPage().isSendersPage().openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Business").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(1).openSelectedSenderDetailsPage().isSenderDetailsPage()
            else:
                self.page.navigate(self.url + "/senders/" + self.senderBusinessID)
                self.dataSender.setSenderId(self.senderBusinessID)
                self.isSenderDetailsPage()
        return self

    def isLineOfBusiness(self, text):
        expect(self.page.locator(self.lineOfBusiness)).to_contain_text(text)
        return self

    def saveSelected(self):
        self.page.click(self.saveButton, force=False)
        self.page.locator("//snack-bar-container").wait_for()
        self.page.click("//snack-bar-container//button")
        self.dataLoaded()
        return self

    def selectFromDropDown(self, locator, type_text):
        self.page.locator(locator + self.dropdownMenu).first.click()
        self.page.click(f"//div[@role='listbox']/mat-option//*[normalize-space()='{type_text}']", force=True)
        return self

    def pressEditAccDetails(self, locator, popup_name):
        self.page.locator(locator).wait_for()
        self.page.click(locator)
        self.page.locator(popup_name).wait_for()
        return self

    def closeEditFinDetailsPopup(self):
        self.page.locator(self.editFinDetailsPopup + self.cancelButton).click()
        return self

    def isImpossibleToChange(self):
        expect(self.page.locator("//gp-edit-financial-details//mat-error[normalize-space()=\"When Charge type is 'Per Transaction', Payment method must be 'Credit Card'\"]")).to_be_visible()
        return self

    def isNoCreditCard(self):
        expect(self.page.locator(self.accPaymentCard + "//div[normalize-space()='Credit Card Details']")).not_to_be_visible()
        return self

    def isPaymentMethod(self, text):
        self.page.locator(self.paymentMethod).wait_for()
        self.pause(0.5)
        expect(self.page.locator(self.paymentMethod)).to_contain_text(text)
        return self

    def isChargingType(self, text):
        self.page.locator(self.chargingType).wait_for()
        self.pause(0.5)
        expect(self.page.locator(self.chargingType)).to_contain_text(text)
        return self

    def changePaymentMethod(self, text):
        self.pressEditAccDetails(self.editPaymentMethod, self.editFinDetailsPopup)
        self.selectFromDropDown(self.editFinDetailsPopup, text)
        self.saveSelected()
        return self

    def changeChargingType(self, text):
        self.pressEditAccDetails(self.editChargingType, self.editFinDetailsPopup)
        self.selectFromDropDown(self.editFinDetailsPopup, text)
        self.saveSelected()
        return self

    def changeLineOfBusiness(self, text):
        self.pressEditAccDetails(self.editLineOfBusinessButton, self.editLineOfBusinessPopup)
        self.selectFromDropDown(self.editLineOfBusinessPopup, text)
        self.saveSelected()
        return self

    def openOrderHistoryPage(self):
        self.page.click(self.ordersHistoryButton)
        return OrdersHistoryPage(self.page)

    def isCreditCardNumber(self, number):
        self.pause(2)
        self.page.locator(self.cardNumber).wait_for()
        expect(self.page.locator(self.cardNumber)).to_contain_text(number)
        return self

    def addCreditCard(self, c_card, id_number):
        self.page.click(self.editCardNumber)
        self.fillCreditCard(c_card, id_number)
        self.dataLoaded()
        self.page.locator("//snack-bar-container//span[@class='mat-simple-snack-bar-content']").wait_for()
        self.page.click("//snack-bar-container//button")
        return self

    def fillCreditCard(self, c_card, id_number):
        frame = self.page.frame_locator("#payment_iframe")
        frame.locator("#Track2CardNo").fill(c_card)
        self.pause(0.1)
        frame.locator("#expYear").click()
        self.page.keyboard.type("222222")
        frame.locator("#expMonth").click()
        self.page.keyboard.type("00000")
        frame.locator("#cvv").fill("123")
        frame.locator("#personalId").fill(id_number)
        frame.locator("#submitBtn").click()

    def isNoAdminRemarks(self):
        self.dataLoaded()
        expect(self.page.locator(self.adminRemarksCard + "//div[contains(@class,'gp-remarks-container')]/div")).to_have_count(1)
        return self

    def deleteAdminRemarks(self, count):
        while count > 0:
            self.page.locator(self.deleteRemarkButton).last.click()
            self.page.click(self.confirmationPopup + self.deleteButton)
            self.pause(0.5)
            self.dataLoaded()
            count -= 1
        return self

    def cancelAdditionRemark(self):
        self.page.click(self.cancelAdmRemark)
        return self

    def createNewAdmRemark(self):
        self.page.click(self.createAdmRemarkButton)
        return self

    def isAdminRemarkAdded(self, remark):
        self.dataLoaded()
        expect(self.page.locator(self.remarkContent).last).to_contain_text(remark)
        return self

    def saveAdminRemark(self):
        self.page.click(self.saveAdmRemarkButton)
        return self

    def fillAdminRemarks(self, remark):
        self.page.fill(self.admRemarksInput, remark)
        return self

    def addAdminRemarks(self, remark):
        self.fillAdminRemarks(remark)
        self.saveAdminRemark()
        return self

    def openLogs(self):
        self.page.click(self.logsButton)
        self.dataLoaded()
        return LogsPage(self.page)

    def isAccountBlocked(self):
        expect(self.page.locator(self.titleStatus)).to_contain_text("Blocked")
        self.dataSender.setAccStatus("Blocked")
        return self

    def blockSenderAccount(self):
        self.page.click(self.blockAccButton)
        self.page.click("//span[normalize-space()='Block']")
        self.dataSender.setAccStatus("Blocked")
        self.dataLoaded()
        return self

    def activateSenderAccount(self):
        self.page.click(self.activateAccButton)
        self.page.click("//span[normalize-space()='Activate']")
        self.dataSender.setAccStatus("Active")
        self.dataLoaded()
        return self

    def updateSenderDetails(self):
        self.dataSender.setUserId(self.page.locator(self.userIdSender).inner_text())
        self.dataSender.setSPhone(self.page.locator(self.ownerPhoneNumber).inner_text())
        self.dataSender.setSEmail(self.page.locator(self.ownerEmail).inner_text())
        return self

    def openUserID(self):
        self.dataLoaded()
        self.pause(1)
        self.page.locator(self.titleName).wait_for()
        self.userIdNumber = self.page.locator(self.userIdSender).inner_text()
        self.dataSender.setSAccountName(self.page.locator(self.titleName).inner_text())
        self.page.click(self.userIdSender)
        return UserDetailsPage(self.page)

    def isPhotoAdded(self):
        self.page.locator(self.sendersPhoto).wait_for()
        expect(self.page.locator(self.sendersPhoto)).to_be_visible()
        self.pause(1)
        self.photoLink = self.page.get_attribute(self.sendersPhoto, "src")
        return self

    def addPhotoSender(self):
        file_path = f"{RESOURCES_DIR}/picture.png"
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(self.addPhotoButton).click()
        fc_info.value.set_files(file_path)
        return self

    def isBrandName(self, text):
        expect(self.page.locator(self.brandName)).to_contain_text(text)
        return self

    def editBrandName(self, text):
        self.page.click(self.editBrandName)
        self.page.fill(self.popup + self.input, text)
        self.page.click(self.saveButton, force=True)
        return self

    def isSenderDatailsBusinessTrue(self, sender_details):
        expect(self.page.locator(self.titleName)).to_contain_text(sender_details.getSAccountName())
        expect(self.page.locator(self.addressSender)).to_contain_text(sender_details.getSAddress())
        expect(self.page.locator(self.ownerName)).to_contain_text(sender_details.getSOwnerName())
        expect(self.page.locator(self.ownerEmail)).to_contain_text(sender_details.getSEmail())
        expect(self.page.locator(self.ownerPhoneNumber)).to_contain_text(sender_details.getSPhone())
        expect(self.page.locator(self.paymentMethod)).to_contain_text(sender_details.getSPayMethod())
        expect(self.page.locator(self.taxIdSender)).to_contain_text(sender_details.getSTaxId())
        expect(self.page.locator(self.finNameSender)).to_contain_text(sender_details.getFinName())
        expect(self.page.locator(self.billingEmailSender)).to_contain_text(sender_details.getSBillingEmail())
        expect(self.page.locator(self.cardNumber)).to_contain_text(sender_details.getSCreditCard())
        return self

    def isSenderDatailsPrivateTrue(self, sender_details):
        expect(self.page.locator(self.titleName)).to_contain_text(sender_details.getSAccountName())
        expect(self.page.locator(self.ownerName)).to_contain_text(sender_details.getSOwnerName())
        expect(self.page.locator(self.ownerEmail)).to_contain_text(sender_details.getSEmail())
        expect(self.page.locator(self.ownerPhoneNumber)).to_contain_text(sender_details.getSPhone())
        expect(self.page.locator(self.paymentMethod)).to_contain_text(sender_details.getSPayMethod())
        expect(self.page.locator(self.cardNumber)).to_contain_text(sender_details.getSCreditCard())
        return self

    def isSenderDetailsPage(self):
        self.page.click(self.genInfoButton)
        self.page.locator(self.accDetViewBeadcrumbs).wait_for()
        expect(self.page.locator(self.accDetViewBeadcrumbs)).to_be_visible()
        expect(self.page.locator(self.titleName)).to_be_visible()
        self.page.locator(self.accDetailsCard).wait_for()
        expect(self.page.locator(self.accDetailsCard)).to_be_visible()
        expect(self.page.locator(self.accFinDetails)).to_be_visible()
        expect(self.page.locator(self.ownerDetailsCard)).to_be_visible()
        expect(self.page.locator(self.adminRemarksCard)).to_be_visible()
        BasePage.localDate = datetime.strptime(datetime.now().strftime("%d/%m/%Y,%H:%M"), "%d/%m/%Y,%H:%M")
        if self.dataSender.getAccType() == "Business":
            self.senderBusinessID = self.dataSender.getSenderId()
        return self

    def isSenderDetailsPhone(self, phone):
        self.page.click(self.genInfoButton)
        self.page.locator(self.accDetViewBeadcrumbs).wait_for()
        expect(self.page.locator(self.accDetViewBeadcrumbs)).to_be_visible()
        expect(self.page.locator(self.titleName)).to_be_visible()
        self.page.locator(self.accDetailsCard).wait_for()
        expect(self.page.locator(self.accDetailsCard)).to_be_visible()
        expect(self.page.locator(self.accFinDetails)).to_be_visible()
        expect(self.page.locator(self.ownerDetailsCard)).to_be_visible()
        expect(self.page.locator(self.adminRemarksCard)).to_be_visible()
        self.page.locator(self.ownerPhoneNumber + f"[normalize-space()='{phone}']").wait_for()
        return self
