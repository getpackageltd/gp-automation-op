from playwright.sync_api import expect

from pages.base_page import BasePage
from models.branch_details import BranchDetails
from apimodule.requests_builder import RequestsBuilder


class BranchesPage(BasePage):
    branchesFilter = "//gp-branches-filters"
    addBranchButton = "//div[@class='gp-page-actions']//button[1]"
    addNewBranchPopup = "//gp-add-branch-modal"
    branchNameInput = addNewBranchPopup + "//input[@formcontrolname='branch_name']"
    branchNumberInput = addNewBranchPopup + "//input[@formcontrolname='client_branch_id']"
    branchAddressInput = addNewBranchPopup + "//input[@formcontrolname='branch_address']"
    branchCommentInput = addNewBranchPopup + "//input[@formcontrolname='branch_comment']"
    branchContNameInput = addNewBranchPopup + "//input[@formcontrolname='contactName']"
    branchContPhoneInput = addNewBranchPopup + "//input[@formcontrolname='contactPhoneNumber']"
    branchDayCheckbox = addNewBranchPopup + "//gp-weekdays//mat-checkbox"
    addWorkingHoursButton = addNewBranchPopup + "//span[normalize-space()='add_circle_outline']"
    createButton = addNewBranchPopup + "//button//span[normalize-space()='add']"
    saveButton = addNewBranchPopup + "//button//span[normalize-space()='Save']"
    blockButton = "//gp-block-branch-modal//button[normalize-space()='Block']"
    activateButton = "//gp-block-branch-modal//button[normalize-space()='Activate']"
    searchInput = branchesFilter + "//mat-form-field[3]//input"
    applyButton = branchesFilter + "//button/span[normalize-space()='Apply']"
    clearButton = branchesFilter + "//button/span[normalize-space()='Clear']"
    statusDropdown = branchesFilter + "//mat-form-field[2]"

    bd: BranchDetails | None = None

    def isStatusFound(self, status):
        count = self.page.locator("//gp-branches-table" + self.rows).count()
        for i in range(1, count + 1):
            expect(self.page.locator(f"//gp-branches-table{self.rows}[{i}]/td[6]/span")).to_contain_text(status)
        return self

    def closeDropdownByEsc(self):
        self.pressEsc()
        return self

    def selectCheckbox(self, type_text):
        self.pressCheckbox(type_text)
        return self

    def openStatusFilter(self):
        self.page.click(self.statusDropdown)
        return self

    def cleanFilter(self):
        self.page.click(self.clearButton)
        self.dataLoaded()
        return self

    def isBranchFound(self):
        self.dataLoaded()
        expect(self.page.locator(f"//gp-branches-table{self.rows}[1]/td[2]")).to_contain_text(self.bd.getBranchGpId())
        expect(self.page.locator(f"//gp-branches-table{self.rows}[1]/td[3]")).to_contain_text(self.bd.getBranchNumber())
        return self

    def pressApplyButton(self):
        self.page.click(self.applyButton)
        self.dataLoaded()
        return self

    def fillSearchByGpId(self):
        self.page.fill(self.searchInput, self.bd.getBranchGpId())
        return self

    def fillSearchById(self):
        self.page.fill(self.searchInput, self.bd.getBranchNumber())
        return self

    def getBranchData(self, row_number):
        self.bd = BranchDetails.builder().build()
        self.bd.setBranchNumber(self.page.locator(f"//gp-branches-table{self.rows}[{row_number}]/td[3]").inner_text())
        self.bd.setBranchGpId(self.page.locator(f"//gp-branches-table{self.rows}[{row_number}]/td[2]").inner_text())
        return self

    def isBranchesPage(self):
        expect(self.page.locator(self.branchesFilter)).to_be_visible()
        return self

    def prepareBranchesForSearchTest(self):
        if self.page.locator(self.rows).count() < 6:
            while self.page.locator(self.rows).count() < 6:
                number = self.getDateDD() + self.getMinusDayDD(1)
                self.addBranch(
                    BranchDetails.builder()
                    .branchName("Branch_" + number)
                    .branchNumber(number)
                    .branchAddress(RequestsBuilder().getRandomeAddress())
                    .branchComment("Comment for branch " + number)
                    .branchContactName("Contact")
                    .branchContactPhone("0538451111")
                    .build()
                )
        return self

    def addBranch(self, branch_details: BranchDetails):
        self.pressAddBranch()
        self.fillBranchDetails(branch_details)
        self.pressCreateBranch()
        self.bd = branch_details
        return self

    def fillBranchDetails(self, branch_details: BranchDetails):
        self.bd = branch_details
        self.page.fill(self.branchNameInput, branch_details.getBranchName())
        self.page.fill(self.branchNumberInput, branch_details.getBranchNumber())
        self.page.fill(self.branchAddressInput, branch_details.getBranchAddress())
        self.isGooglAddressAppeared()
        self.page.click(self.googleAddr)
        self.page.fill(self.branchCommentInput, branch_details.getBranchComment())
        self.page.fill(self.branchContNameInput, branch_details.getBranchContactName())
        self.page.fill(self.branchContPhoneInput, branch_details.getBranchContactPhone())
        return self

    def pressAddBranch(self):
        self.page.click(self.addBranchButton)
        return self

    def pressCreateBranch(self):
        self.page.click(self.createButton)
        self.dataLoaded()
        return self
