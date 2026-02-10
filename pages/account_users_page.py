from playwright.sync_api import expect

from pages.base_page import BasePage


class AccountUsersPage(BasePage):
    accUsersPage = "//gp-accounts-users"
    inviteUserButton = accUsersPage + "//button/span/mat-icon[normalize-space()='add']"
    invitePopup = "//gp-invite-user-modal"
    emailInput = invitePopup + "//span[normalize-space()='Send invitation By Email:']/../mat-form-field//input"
    phoneInput = invitePopup + "//span[normalize-space()='Send invitation By Phone:']/../mat-form-field//input"
    branchesDropdown = invitePopup + "//span[normalize-space()='Branch:']/../mat-form-field//mat-select"
    roleDropdown = invitePopup + "//span[normalize-space()='Role:']/../mat-form-field//mat-select"
    inviteButton = invitePopup + "//button//span[normalize-space()='Invite']"
    cancelInvitationPopup = "//gp-cancel-invitation-employee-modal"
    approveButton = cancelInvitationPopup + "//button//span[normalize-space()='Approve']"

    newUserData = None

    def isUserInvited(self):
        if "@" in self.newUserData[0]:
            expect(self.page.locator(self.accUsersPage + self.rows + "[last()]/td[3]/span")).to_contain_text(self.newUserData[0])
        else:
            expect(self.page.locator(self.accUsersPage + self.rows + "[last()]/td[4]")).to_contain_text(self.newUserData[0])
        expect(self.page.locator(self.accUsersPage + self.rows + "[last()]/td[6]//span[2]/b")).to_contain_text(self.newUserData[1])
        expect(self.page.locator(self.accUsersPage + self.rows + "[last()]/td[6]//span[2]")).to_contain_text(self.newUserData[2])
        return self

    def isAccountUsersPage(self):
        self.page.locator(self.inviteUserButton).wait_for()
        expect(self.page.locator(self.inviteUserButton)).to_be_visible()
        return self

    def inviteNewUser(self, emailPhone, role):
        self.newUserData = [emailPhone, "Branch Manager" if "Employee" not in role else role]
        self.pressInviteNewUser()
        if "@" in emailPhone:
            self.page.fill(self.emailInput, emailPhone)
        else:
            self.page.fill(self.phoneInput, emailPhone)
        self.page.click(self.branchesDropdown)
        options = self.page.locator("//span/../mat-pseudo-checkbox/../span")
        branch_name = options.nth(1).inner_text()
        self.newUserData.append(branch_name)
        self.selectBranch(branch_name)
        self.selectRole(role)
        self.pressInviteButton()
        return self

    def selectRole(self, role):
        self.page.click(self.roleDropdown)
        self.page.locator(f"//span[normalize-space()='{role}']").click(force=True)
        return self

    def selectBranch(self, branch):
        self.pressCheckbox(branch)
        self.pressEsc()
        return self

    def pressInviteNewUser(self):
        self.page.click(self.inviteUserButton)
        return self

    def pressInviteButton(self):
        self.page.click(self.inviteButton)
        self.page.locator("//snack-bar-container").wait_for()
        self.page.click("//snack-bar-container//button")
        self.dataLoaded()
        return self

    def cancelInvitation(self):
        self.page.click(self.accUsersPage + self.rows + "[last()]/td[7]//button[1]")
        self.page.locator(self.cancelInvitationPopup).wait_for()
        self.page.click(self.approveButton)
        self.page.locator("//snack-bar-container").wait_for()
        self.page.click("//snack-bar-container//button")
        self.dataLoaded()
        return self
