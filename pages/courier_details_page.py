from datetime import datetime
from playwright.sync_api import expect

import os

from config import DOWNLOADS_DIR, RESOURCES_DIR
from pages.base_page import BasePage
from pages.deliveries_page import DeliveriesPage
from pages.logs_page import LogsPage
from pages.messages_page import MessagesPage
from models.bank_details import BankDetails


class CourierDetailsPage(BasePage):
    nameBlock = "//div[@class='gp-top-account-details-grid']"
    courierName = nameBlock + "/div[2]"
    addEditPhoto = nameBlock + "//mat-icon[normalize-space()='edit']"
    photoTitle = nameBlock + "//img"
    status = nameBlock + "/div[3]/div"
    blockAccButton = "//span[normalize-space()='Block Account']"
    changeStatusButton = "//*[local-name()='path' and @class='a']"
    courierDetailsBlock = "//gp-courier-general-info//div[@class='gp-general-info-account-details gp-general-info-card']"
    accountID = courierDetailsBlock + "//div[normalize-space()='Account ID']/../div[2]"
    nationID = courierDetailsBlock + "//div[normalize-space()='National Id']/../div[2]"
    userID = courierDetailsBlock + "//div[normalize-space()='User ID']/../div[2]"
    phone = courierDetailsBlock + "//div[normalize-space()='Phone Number']/../div[2]"
    email = courierDetailsBlock + "//div[normalize-space()='Email']/../div[2]"
    city = courierDetailsBlock + "//div[normalize-space()='City']/../div[2]"
    vehicle = courierDetailsBlock + "//div[normalize-space()='Vehicle Type']/../div[2]"
    editVehicleTypeButton = courierDetailsBlock + "//div[normalize-space()='Vehicle Type']/../mat-icon"
    editVehiclePopup = "//gp-edit-vehicle-type"
    dropdownMenu = "//mat-select | //mat-mdc-select"
    courierFinDetails = "//gp-courier-general-info//div[contains(@class,'gp-general-info-financial-details')]"
    editFinDetailsPopup = "//gp-edit-financial-details"
    taxStatus = courierFinDetails + "//div[normalize-space()='Tax status']/../div[2]"
    editTaxStatusButton = courierFinDetails + "//div[normalize-space()='Tax status']/../mat-icon"
    taxID = courierFinDetails + "//div[normalize-space()='Tax Id']/../div[2]"
    editTaxIdButton = courierFinDetails + "//div[normalize-space()='Tax Id']/../mat-icon"
    editFinEmailButton = courierFinDetails + "//div[normalize-space()='Account Email']/../mat-icon"
    finEmail = courierFinDetails + "//div[normalize-space()='Account Email']/../div[2]"
    finName = courierFinDetails + "//div[normalize-space()='Financial Name']/../div[2]"
    editFinNameButton = courierFinDetails + "//div[normalize-space()='Financial Name']/../mat-icon"
    finOperability = courierFinDetails + "//div[normalize-space()='Financial Operability']/../div[2]"
    editFinOperability = courierFinDetails + "//div[normalize-space()='Financial Operability']/..//mat-icon"
    taxWithholding = courierFinDetails + "//div[normalize-space()='Active Tax Withholding']/../div[2]/div"
    editTaxWithholdingButton = courierFinDetails + "//div[normalize-space()='Active Tax Withholding']/..//mat-icon"
    courierBankDetails = "//gp-courier-general-info//div[@class='gp-general-info-credit-card-details gp-general-info-card']"
    editBankButton = courierBankDetails + "//mat-icon[normalize-space()='edit']"
    deleteBankButton = courierBankDetails + "//mat-icon[normalize-space()='delete']"
    courierBankName = courierBankDetails + "//div[normalize-space()='Name']/../div[2]"
    courierBankBranch = courierBankDetails + "//div[normalize-space()='Branch Number']/../div[2]"
    courierBankAcc = courierBankDetails + "//div[normalize-space()='Account Number']/../div[2]"
    courierBankNationId = courierBankDetails + "//div[normalize-space()='Owner National Id']/../div[2]"
    courierBankFullName = courierBankDetails + "//div[normalize-space()='Owner Full Name']/../div[2]"
    editBankPopup = "//gp-edit-bank-details/div"
    bankNameDropdown = editBankPopup + "//span[normalize-space()='Name:']/../mat-form-field//mat-select"
    bankBranchInput = editBankPopup + "//span[normalize-space()='Branch:']/../mat-form-field//input"
    bankAccountInput = editBankPopup + "//span[normalize-space()='Account:']/../mat-form-field//input"
    bankNationalIdInput = editBankPopup + "//span[normalize-space()='National Id:']/../mat-form-field//input"
    bankFullNameInput = editBankPopup + "//span[normalize-space()='Full Name:']/../mat-form-field//input"
    natIdErrorMess = "//gp-edit-bank-details/div//span[normalize-space()='National Id:']/../mat-form-field//mat-error"
    saveButton = "//button//span[contains(@class, 'mdc-button__label') and normalize-space()='Save'] | //button/span[normalize-space()='Save']"
    cancelButton = "//button/span[normalize-space()='Cancel']"
    deleteButton = "//button/span[normalize-space()='Delete']"
    admRemarks = "//gp-account-admin-remarks"
    admRemarksInput = admRemarks + "//input"
    saveAdmRemarkButton = admRemarks + "//img[contains(@src,'check.svg')]"
    cancelAdmRemark = admRemarks + "//img[contains(@src,'cancel.svg')]"
    deleteRemarkButton = admRemarks + "//mat-icon[normalize-space()='delete']"
    createAdmRemarkButton = admRemarks + "//button"
    remarkContent = admRemarks + "//div[contains(@class,'gp-remark')]//div[contains(@class,'gp-remark-comment')]"
    confirmationPopup = "//gp-confirmation-dialog"
    editCourierStatusPopup = "//gp-edit-account-status"
    messagesButton = "//a[normalize-space()='Messages']"
    logsButton = "//a[normalize-space()='Logs']"

    def isCourierDetailsPage(self):
        self.page.wait_for_url(self.url + "/couriers/" + self.dataCourier[0])
        return self

    def isCourierDetails(self):
        if BasePage.dataCourier and BasePage.dataCourier[0]:
            self.page.wait_for_url(self.url + "/couriers/" + BasePage.dataCourier[0])
        # Best-effort read; do not fail if the value cell is slow or missing
        try:
            account_id = self.page.locator(self.accountID).nth(1).inner_text(timeout=3000)
            BasePage.dataCourier[0] = account_id
        except Exception:
            pass
        return self

    def openUserID(self):
        self.dataLoaded()
        self.pause(1)
        BasePage.userIdNumber = self.page.locator(self.userID).inner_text()
        BasePage.dataCourier[1] = self.page.locator(self.courierName).inner_text().split(" ")[1]
        self.page.click(self.userID)
        from pages.user_details_page import UserDetailsPage
        return UserDetailsPage(self.page)

    def openCourierDetails(self):
        if not self.page.locator(self.accountID).is_visible():
            DeliveriesPage(self.page).openCouriersPage().isCouriersPage()
            # Click the first courier ID row
            first_row_link = self.page.locator("//tbody/tr[1]/td[2]/a")
            first_row_link.wait_for()
            target_id = first_row_link.inner_text()
            first_row_link.click()
            BasePage.dataCourier = BasePage.dataCourier or [None, "", "", "", "", "", "", ""]
            BasePage.dataCourier[0] = target_id
        BasePage.localDate = datetime.strptime(datetime.now().strftime("%d/%m/%Y,%H:%M"), "%d/%m/%Y,%H:%M")
        return self

    def isPhotoAdded(self):
        expect(self.page.locator(self.photoTitle)).to_be_visible()
        self.photoLink = self.page.get_attribute(self.photoTitle, "src")
        return self

    def addPhotoCourier(self):
        file_path = os.path.join(DOWNLOADS_DIR, "courier_profile_pic.jpg")
        if not os.path.exists(file_path):
            file_path = os.path.join(RESOURCES_DIR, "picture.png")
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(self.addEditPhoto).click()
        fc_info.value.set_files(file_path)
        return self

    def openLogs(self):
        self.page.click(self.logsButton)
        self.dataLoaded()
        return LogsPage(self.page)

    def openMessages(self):
        self.page.click(self.messagesButton)
        self.dataLoaded()
        return MessagesPage(self.page)

    def changeCourierStatus(self, status, reason):
        self.changeStatusTo(status, reason)
        self.dataCourier[4] = status
        return self

    def unblockAccount(self):
        self.changeStatusTo("Active", "Block Removed")
        self.dataCourier[4] = "active"
        return self

    def changeStatusTo(self, status, reason):
        self.page.click(self.changeStatusButton)
        self.pause(0.5)
        self.selectFromDropDown(self.editCourierStatusPopup, status)
        if status in {"Active", "In review", "Blocked"}:
            self.selectReason(self.editCourierStatusPopup, reason)
        
        # Wait for the save button to become enabled before clicking
        save_btn = self.page.locator(self.saveButton)
        expect(save_btn).to_be_enabled(timeout=5000)
        save_btn.click()
        
        self.pause(0.7)
        self.dataLoaded()
        return self

    def isCourierStatusPending(self):
        expect(self.page.locator(self.status + "[normalize-space()='pending']")).to_be_visible()
        expect(self.page.locator("//img[@class='license-image-app']")).to_be_visible()
        expect(self.page.locator("//img[@class='avatar-image-app']")).to_be_visible()
        return self

    def isCourierStatusInReview(self, reason):
        expect(self.page.locator(self.status + "[normalize-space()='in review']")).to_be_visible()
        expect(self.page.locator(self.status + f"[normalize-space()='{reason}']")).to_be_visible()
        expect(self.page.locator("//img[@class='license-image-app']")).to_be_visible()
        expect(self.page.locator("//img[@class='avatar-image-app']")).to_be_visible()
        return self

    def isAccountBlocked(self):
        expect(self.page.locator(self.status)).to_contain_text("blocked")
        self.dataCourier[4] = "blocked"
        return self

    def blockCourierAccount(self):
        self.changeStatusTo("Blocked", "")
        return self

    def changeTaxWithholding(self, name):
        self.pressEditAccDetails(self.editTaxWithholdingButton, self.editFinDetailsPopup)
        self.page.fill(self.editFinDetailsPopup + "//input", name)
        self.page.click("//span[normalize-space()='Active Tax Withholding:']")
        self.saveSelected()
        return self

    def changeFinName(self, name):
        self.pressEditAccDetails(self.editFinNameButton, self.editFinDetailsPopup)
        self.page.fill(self.editFinDetailsPopup + "//input", name)
        self.saveSelected()
        return self

    def changeFinEmail(self, email):
        try:
            self.pressEditAccDetails(self.editFinEmailButton, self.editFinDetailsPopup)
        except Exception:
            return self
        if not self.page.locator(self.editFinDetailsPopup).is_visible():
            return self
        self.page.fill(self.editFinDetailsPopup + "//input", email)
        self.saveSelected()
        return self

    def changeTaxId(self, number):
        self.pressEditAccDetails(self.editTaxIdButton, self.editFinDetailsPopup)
        self.page.fill(self.editFinDetailsPopup + "//input", number)
        self.saveSelected()
        return self

    def changeFinStatus(self, status):
        self.pressEditAccDetails(self.editFinOperability, self.editFinDetailsPopup)
        self.selectFromDropDown(self.editFinDetailsPopup, status)
        self.saveSelected()
        return self

    def changeTaxStatus(self, status):
        self.pressEditAccDetails(self.editTaxStatusButton, self.editFinDetailsPopup)
        self.selectFromDropDown(self.editFinDetailsPopup, status)
        self.saveSelected()
        return self

    def changeVehicleType(self, vType):
        self.pressEditAccDetails(self.editVehicleTypeButton, self.editVehiclePopup)
        self.selectFromDropDown(self.editVehiclePopup, vType)
        self.saveSelected()
        return self

    def isVehicleTypeChanged(self, vType):
        if vType == "FamilyCar":
            vType = "Family Car"
        elif vType == "MotorWithBox":
            vType = "Motor With Box"
        expect(self.page.locator(self.vehicle)).to_contain_text(vType)
        return self

    def addAdminRemarks(self, remark):
        self.fillAdminRemarks(remark)
        self.saveAdminRemark()
        return self

    def isNoAdminRemarks(self):
        self.dataLoaded()
        expect(self.page.locator(self.admRemarks + "//div[contains(@class,'gp-remarks-container')]/div")).to_have_count(1)
        return self

    def isAdminRemarkAdded(self, remark):
        self.dataLoaded()
        expect(self.page.locator(self.remarkContent).last).to_contain_text(remark)
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

    def fillAdminRemarks(self, remark):
        self.page.fill(self.admRemarksInput, remark)
        return self

    def saveAdminRemark(self):
        self.page.click(self.saveAdmRemarkButton)
        return self

    def isFinStatusChanged(self, status):
        expect(self.page.locator(self.finOperability)).to_contain_text(status)
        self.dataCourier[7] = self.page.locator(self.finOperability).inner_text()
        return self

    def isTaxStatusChanged(self, status):
        expect(self.page.locator(self.taxStatus)).to_contain_text(status)
        return self

    def isTaxWithholdChanged(self, number):
        expect(self.page.locator(self.taxWithholding)).to_contain_text(number)
        return self

    def isFinNameChanged(self, number):
        expect(self.page.locator(self.finName)).to_contain_text(number)
        return self

    def isFinEmailChanged(self, number):
        expect(self.page.locator(self.finEmail)).to_contain_text(number)
        return self

    def isTaxIdChanged(self, number):
        expect(self.page.locator(self.taxID)).to_contain_text(number)
        self.dataCourier[2] = number
        return self

    def saveSelected(self):
        self.page.click(self.saveButton)
        self.dataLoaded()
        try:
            self.page.locator("//snack-bar-container").wait_for(timeout=5000)
            self.dataLoaded()
        except Exception:
            pass
        return self

    def selectReason(self, locator, type_text):
        self.pause(0.5)
        self.page.locator(locator + self.dropdownMenu).last.click()
        self.pause(0.5)
        if type_text:
            option = self.page.locator(f"//div[@role='listbox']/mat-option//*[normalize-space()='{type_text}']")
            option.wait_for()
            option.click(force=True)
        else:
            option = self.page.locator("//div[@role='listbox']/mat-option").first
            option.wait_for()
            option.click(force=True)
        self.pause(0.5)
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

    def addBankDetails(self, bd: BankDetails):
        self.page.click(self.editBankButton)
        self.page.locator(self.editBankPopup).wait_for()
        self.bankDetails = bd
        self.fillBankDetails(self.bankDetails)
        return self

    def saveBankDetails(self):
        self.page.click(self.saveButton)
        self.dataLoaded()
        try:
            self.page.locator("//snack-bar-container").wait_for(timeout=5000)
            self.text = self.page.locator("//snack-bar-container//span[@class='mat-simple-snack-bar-content']").inner_text()
            self.page.click("//snack-bar-container//button")
        except Exception:
            pass
        self.dataLoaded()
        return self

    def fillBankDetails(self, bd: BankDetails):
        self.bankDetails = bd
        self.page.click(self.bankNameDropdown)
        self.pause(0.5)
        if not self.page.locator(f"//mat-option[span[normalize-space()='{self.bankDetails.getBankName()}']]").is_visible():
            self.page.click(self.bankNameDropdown)
        self.page.click(f"//mat-option[span[normalize-space()='{self.bankDetails.getBankName()}']]" )
        self.page.fill(self.bankBranchInput, self.bankDetails.getBankBranch())
        self.page.fill(self.bankAccountInput, self.bankDetails.getBankAccount())
        self.page.fill(self.bankNationalIdInput, self.bankDetails.getBankNationaID())
        self.page.fill(self.bankFullNameInput, self.bankDetails.getBankFullName())
        return self

    def isBankDetails(self):
        expect(self.page.locator(self.courierBankName)).to_contain_text("54")
        expect(self.page.locator(self.courierBankBranch)).to_contain_text(self.bankDetails.getBankBranch())
        expect(self.page.locator(self.courierBankAcc)).to_contain_text(self.bankDetails.getBankAccount())
        expect(self.page.locator(self.courierBankNationId)).to_contain_text(self.bankDetails.getBankNationaID().lstrip('0'))
        expect(self.page.locator(self.courierBankFullName)).to_contain_text(self.bankDetails.getBankFullName())
        return self

    def deleteBankDetails(self):
        if self.page.locator(self.courierBankName).inner_text() == "-":
            self.addBankDetails(BankDetails.builder().bankName("בנק ירושלים").bankBranch("1").bankAccount("12345").bankNationaID("123456789").bankFullName("Courier From_OP").build()).saveBankDetails()
        self.page.click(self.deleteBankButton)
        try:
            self.page.locator("//snack-bar-container").wait_for(timeout=5000)
            self.page.click("//snack-bar-container//button")
        except Exception:
            pass
        self.dataLoaded()
        return self

    def isBankDetailsDeleted(self):
        expect(self.page.locator(self.courierBankName)).to_contain_text("-")
        expect(self.page.locator(self.courierBankAcc)).to_contain_text("-")
        return self

    def isWrongNationalId(self):
        expect(self.page.locator(self.natIdErrorMess)).to_be_visible()
        return self

    def isSaveButtonDisabled(self):
        expect(self.page.locator(self.saveButton)).to_be_disabled()
        return self

    def isInvalidBankDetails(self):
        assert self.text == "Bank Detals are invalid!"
        return self
