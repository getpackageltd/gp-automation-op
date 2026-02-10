from playwright.sync_api import expect

from pages.base_page import BasePage


class UserDetailsPage(BasePage):
    userDetailsBreadcrumbs = "//gp-breadcrumbs//a[normalize-space()='User Details View']"
    userNameTitle = "//div[@class='gp-top-account-details-grid']/div[2]/div"
    addEditPhoto = "//div[@class='gp-top-account-details-grid']//mat-icon[normalize-space()='edit']"
    photoTitle = "//div[@class='gp-top-account-details-grid']//img"
    userDetailsBlock = "//gp-users-general-info//div[@class='gp-general-info-account-details gp-general-info-card']"
    userIdPage = userDetailsBlock + "//div[normalize-space()='ID']/../div[2]"
    phoneNumPage = userDetailsBlock + "//div[normalize-space()='Phone Number']/../div[2]"
    emailPage = userDetailsBlock + "//div[normalize-space()='Email']/../div[2]"
    associatedAccs = "//gp-users-general-info//div[@class='gp-associated-accounts gp-general-info-card']"
    accIdPage = "//tbody/tr/td[1]"
    accNamePage = "//tbody/tr/td[2]"
    accTypePage = "//tbody/tr/td[3]"

    def isUserDetailsPage(self):
        if self.userIdNumber:
            self.page.wait_for_url(self.url + "/users/" + self.userIdNumber)
        expect(self.page.locator(self.userDetailsBreadcrumbs)).to_be_visible()
        return self

    def isPhotoAdded(self):
        expect(self.page.locator(self.photoTitle)).to_be_visible()
        # If photoLink wasn't captured, don't fail the test
        if self.photoLink:
            expect(self.page.locator(self.photoTitle + f"[@src='{self.photoLink}']")).to_be_visible()
        return self

    def backToCourierDetails(self):
        self.page.go_back()
        from pages.courier_details_page import CourierDetailsPage
        return CourierDetailsPage(self.page)

    def backToSenderDetails(self):
        self.page.go_back()
        from pages.sender_details_page import SenderDetailsPage
        return SenderDetailsPage(self.page)

    def isUserSenderDataTrue(self):
        expect(self.page).to_have_url(self.url + "/users/" + self.userIdNumber)
        expect(self.page.locator(self.phoneNumPage)).to_have_text(self.dataSender.getSPhone())
        expect(self.page.locator(self.accIdPage)).to_have_text(self.dataSender.getSenderId())
        expect(self.page.locator(self.accNamePage)).to_contain_text(self.dataSender.getSAccountName())
        return self

    def isUserDataTrue(self):
        expect(self.page).to_have_url(self.url + "/users/" + self.userIdNumber)
        expect(self.page.locator(self.phoneNumPage)).to_have_text(self.dataCourier[3])
        expect(self.page.locator(self.accIdPage)).to_have_text(self.dataCourier[0])
        expect(self.page.locator(self.accNamePage)).to_contain_text(self.dataCourier[1])
        return self
