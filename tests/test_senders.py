import pytest
from config import OPERATOR_EMAIL, OPERATOR_PASSWORD, COURIER_ID
from utils import random_number, random_number_int
from constants import ID, NAME, PHONE, CITY
from pages.deliveries_page import DeliveriesPage
from pages.sender_details_page import SenderDetailsPage
from pages.senders_page import SendersPage
from models.sender_details import SenderDetails
from models.branch_details import BranchDetails
from apimodule.requests_builder import RequestsBuilder

def login_op(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL, OPERATOR_PASSWORD).openSendersPage().isSendersPage().cleanFilter()

def login_for_details(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL, OPERATOR_PASSWORD)

def test_reg_date_last_month_filter_test(page):
    login_op(page)
    SendersPage(page).openRegDatePicker().selectLastMonth().pressApply().isLastMonthSelected()

def test_reg_date_last_week_filter_test(page):
    login_op(page)
    SendersPage(page).openRegDatePicker().selectLastSevenDays().pressApply().isLastSevenDaysSelected()

def test_acc_type_filter_test(page):
    stats = ["Private","Business"]
    login_op(page)
    p = SendersPage(page).getNumberOfRows().openAccTypeFilter().selectAllCheckbox().closeDropdownByEsc().pressApply().isAllEquals().cleanFilter()
    for status in stats:
        p = p.openAccTypeFilter().selectCheckbox(status).closeDropdownByEsc().pressApply().isAccType(status).cleanFilter()

def test_acc_status_filter_test(page):
    stats = ["Active","Blocked"]
    login_op(page)
    p = SendersPage(page).getNumberOfRows().openAccStatusFilter().selectAllCheckbox().closeDropdownByEsc().pressApply().cleanFilter()
    for status in stats:
        p = p.openAccStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply().isAccStatus(status).cleanFilter()

def test_payment_method_filter_test(page):
    stats = ["Bank Transfer","Credit Card"]
    login_op(page)
    p = SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().pressApply()
    for status in stats:
        p = p.openPeymentMethod().selectCheckbox(status).closeDropdownByEsc().pressApply().isPaymentMethod(status).openPeymentMethod().selectCheckbox(status).closeDropdownByEsc()

def test_search_by_id_filter_test(page):
    login_op(page)
    SendersPage(page).getSenderData(int(random_number(1))).fillSearchInput(ID).pressApply().isSenderFound().cleanFilter()

def test_search_by_acc_name_filter_test(page):
    login_op(page)
    SendersPage(page).fillSearchInput("חברה טסט").pressApply().isSenderFoundByAccName("חברה טסט").cleanFilter()

def test_search_by_owner_name_filter_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().fillSearchInput("הרשמהעסקי").pressApply().isSenderFoundByOwnerName("הרשמהעסקי").cleanFilter()

def test_export_excel_current_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().pressApply().setRowsOnPage(50).pressExport().downloadCurrentPage("expsender").isFileDownLoaded("expsender").cleanFilter()

def test_export_excel_all_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Blocked").closeDropdownByEsc().pressApply().setRowsOnPage(20).pressExport().downloadAllPages("expsender").isFileDownLoaded("expsender").cleanFilter()

def test_block_acc_from_table_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().pressApply().getSenderData(int(random_number(1))).fillSearchInput(ID).pressApply().isSenderFound().blockAccount().cleanFilter().fillSearchInput(ID).pressApply().isAccountBlocked().activateAccount().isAccountActive()

def test_details_page_business_test(page):
    login_op(page)
    SendersPage(page).fillSearchInput("0506664422").pressApply().isSenderFoundByAccName("Test").getSenderData(1).openSenderDetailsPage().isSenderDetailsPage().isSenderDatailsBusinessTrue(SenderDetails.builder().sAccountName("Test").sAddress("רוטשילד 1, ראשון לציון, ישראל").sOwnerName("test").sEmail("aleksey.bunkov+24356@getpackage.com").sPhone("0506664422").sPayMethod("Credit Card").sTaxId("192837465").finName("API").sBillingEmail("aleksey.bunkov+24356@getpackage.com").sCreditCard("************4242").build())

def test_details_page_private_test(page):
    login_op(page)
    SendersPage(page).openAccTypeFilter().selectCheckbox("Private").closeDropdownByEsc().fillSearchInput("aleksey.bunkov+9999@getpackage.com").pressApply().isSenderFoundByAccName("API Test").getSenderData(1).openSenderDetailsPage().isSenderDetailsPage().isSenderDatailsPrivateTrue(SenderDetails.builder().sAccountName("API Test").sOwnerName("API Test").sEmail("aleksey.bunkov+9999@getpackage.com").sPhone("0538451010").sPayMethod("Credit Card").sCreditCard("************1111").build())

def test_add_brand_name_private_test(page):
    brandName = "Brand_"+int(random_number(4))
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Private").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().editBrandName(brandName).isBrandName(brandName)

def test_block_private_acc_from_details_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Private").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().blockSenderAccount().isAccountBlocked().openLogs().isLogsRecordBlock().backToSenderDetailsPage().activateSenderAccount().openLogs().isLogsPage().isLogsRecordActivated().backToSenderDetailsPage()

def test_user_id_link_private_test(page):
    login_op(page)
    SendersPage(page).openAccTypeFilter().selectCheckbox("Private").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().updateSenderDetails().openUserID().isUserDetailsPage().isUserSenderDataTrue()

def test_add_delete_admin_remarks_private_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Private").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().addAdminRemarks("Added admin remark for private sender test").isAdminRemarkAdded("Added admin remark for private sender test").createNewAdmRemark().addAdminRemarks("Another admin remark for private").isAdminRemarkAdded("Another admin remark for private").cancelAdditionRemark().createNewAdmRemark().cancelAdditionRemark().deleteAdminRemarks(2).isNoAdminRemarks()

def test_add_credit_card_private_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Private").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().addCreditCard("4242424242424242","000000000").isCreditCardNumber("**********4242").addCreditCard("4111111111111111","000000000").isCreditCardNumber("**********1111")

def test_is_order_history_private_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Private").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().openOrderHistoryPage().isOrderHistoryPage().backToSenderDetailsPage()

def test_add_brand_name_business_test(page):
    brandName = "Brand_"+int(random_number(4))
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Business").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().editBrandName(brandName).isBrandName(brandName)

def test_add_photo_business_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Business").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().updateSenderDetails().addPhotoSender().isPhotoAdded()

def test_block_business_acc_from_details_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Business").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().blockSenderAccount().isAccountBlocked().openLogs().isLogsRecordBlock().backToSenderDetailsPage().activateSenderAccount().openLogs().isLogsPage().isLogsRecordActivated().backToSenderDetailsPage()

def test_user_id_link_business_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Business").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().updateSenderDetails().openUserID().isUserDetailsPage().isUserSenderDataTrue()

def test_add_delete_admin_remarks_business_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Business").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().addAdminRemarks("Added admin remark for business sender test").isAdminRemarkAdded("Added admin remark for business sender test").createNewAdmRemark().addAdminRemarks("Another admin remark for business").isAdminRemarkAdded("Another admin remark for business").cancelAdditionRemark().createNewAdmRemark().cancelAdditionRemark().deleteAdminRemarks(2).isNoAdminRemarks()

def test_add_credit_card_business_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openPeymentMethod().selectCheckbox("Credit Card").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Business").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().addCreditCard("4242424242424242","000000000").isCreditCardNumber("**********4242").addCreditCard("4111111111111111","000000000").isCreditCardNumber("**********1111")

def test_lines_of_business_test(page):
    lineOfBusiness = [
        "trade-sites",
        "clothing-and-fashion",
        "entertainment",
        "banking-and-finance",
        "health-beauty",
        "insurance",
        "food-and-drinks",
        "restaurants",
        "deliveries-distribution",
        "advertising-and-marketing",
        "retail",
        "communications-and-electronics",
        "educational-institutions",
        "hitech-digital",
        "others",
    ]
    login_op(page)
    sdp = SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Business").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage()
    for line in lineOfBusiness:
        sdp = sdp.changeLineOfBusiness(line).isLineOfBusiness(line)
    sdp.openLogs().isLogsPage().isLineOfBusinessLogs(lineOfBusiness).backToSenderDetailsPage()

def test_address_change_test(page):
    login_for_details(page)
    SenderDetailsPage(page).openSenderDetailsBusiness().changeAddress().isAddressChanged()

def test_charging_type_and_payment_method(page):
    login_for_details(page)
    SenderDetailsPage(page).openSenderDetailsBusiness().changeChargingType("Monthly").isChargingType("Monthly").changePaymentMethod("BankTransfer").isPaymentMethod("Bank Transfer").isNoCreditCard().pressEditAccDetails("//gp-sender-general-info/div/div[2]//div[normalize-space()='Charging Type']/../mat-icon","//gp-edit-financial-details").selectFromDropDown("//gp-edit-financial-details", "PerTransaction").isImpossibleToChange().closeEditFinDetailsPopup().changePaymentMethod("CreditCard").isPaymentMethod("Credit Card").changeChargingType("PerTransaction").isChargingType("Per Transaction").isSenderDetailsPage()

def test_edit_tax_id_test(page):
    number = random_number(9)
    login_for_details(page)
    SenderDetailsPage(page).openSenderDetailsBusiness().editTaxId(number).isTaxId(number)

def test_edit_fin_name_test(page):
    name = "FinName_"+random_number(4)
    login_for_details(page)
    SenderDetailsPage(page).openSenderDetailsBusiness().editFinName(name).isFinName(name)

def test_edit_billing_email_test(page):
    email = "aleksey.bunkov+"+random_number(7)+"@getpackage.com"
    login_for_details(page)
    SenderDetailsPage(page).openSenderDetailsBusiness().updateSenderDetails().editEmailBilling(email).isPendingEmailBilling(email).editEmailBilling().isEmailBilling()

def test_add_branch_test(page):
    number = random_number(4)
    login_for_details(page)
    SenderDetailsPage(page).openSenderDetailsBusiness().openBranches().isBranchesPage().addBranch(BranchDetails.builder().branchName("Branch_"+number).branchNumber(number).branchAddress(RequestsBuilder().getRandomeAddress()).branchComment("Comment for branch "+number).branchContactName("Contact").branchContactPhone("538451111").build()).isBranchAdded().editBranch(1, BranchDetails.builder().branchName("Branch_"+random_number(4)).branchNumber(random_number(4)).branchAddress(RequestsBuilder().getRandomeAddress()).branchComment("Comment "+random_number(4)).branchContactName("New Contact").branchContactPhone("538451112").build()).isBranchEdited().blockBranch().isBranchBlocked().activateBranch().isBranchActive()

def test_find_branch_filter_test(page):
    login_op(page)
    SendersPage(page).reloadPage().fillSearchInput("0538455020").pressApply().openSenderDetailsPage().isSenderDetailsPhone("0538455020").openBranches().isBranchesPage().prepareBranchesForSearchTest().getBranchData(5).fillSearchById().pressApplyButton().isBranchFound().cleanFilter().getBranchData(3).fillSearchByGpId().pressApplyButton().isBranchFound().cleanFilter().openStatusFilter().selectCheckbox("Blocked").closeDropdownByEsc().pressApplyButton().isStatusFound("BLOCKED").cleanFilter().openStatusFilter().selectCheckbox("Blocked").selectCheckbox("Active").closeDropdownByEsc().pressApplyButton().isStatusFound("ACTIVE")

def test_invite_new_user_test(page):
    number = random_number(6)
    login_op(page)
    SendersPage(page).fillSearchInput("0538455020").pressApply().openSenderDetailsPage().isSenderDetailsPhone("0538455020").openAccountUsersPage().isAccountUsersPage().inviteNewUser("aleksey.bunkov+"+number+"@getpackage.com", "Employee").isUserInvited().cancelInvitation().inviteNewUser("538"+random_number(6), "BranchManager").isUserInvited().cancelInvitation()

def test_create_api_key_test(page):
    login_for_details(page)
    SenderDetailsPage(page).openSenderDetailsBusiness().openApiKeysPage().isApiKeysPage().createNewApiKey("branches").isApiKeyCreated().editApiKey().isApiKeyCreated().createNewApiKey("deliveries").isApiKeyCreated().deleteApiKey().deleteApiKey()

def test_settings_test(page):
    login_for_details(page)
    SenderDetailsPage(page).openSenderDetailsBusiness().openSenderSettings().isSenderSettingsPage().directlyToReceiver().isDirectlyToReceiver().vipSender().isVipSender().vipSender().alternativeHandoff().alternativeHandoff("All").isAllAlternativeHandoff().alternativeHandoff("All").alternativeHandoff(1).isAlternativeHandoff(1).alternativeHandoff(1).alternativeHandoff(2).isAlternativeHandoff(2).alternativeHandoff(2).alternativeHandoff(3).isAlternativeHandoff(3).alternativeHandoff(3).alternativeHandoff(4).isAlternativeHandoff(4).alternativeHandoff(4).alternativeHandoff(5).isAlternativeHandoff(5).alternativeHandoff(5).alternativeHandoff(6).isAlternativeHandoff(6).alternativeHandoff(6).alternativeHandoff(7).isAlternativeHandoff(7).alternativeHandoff(7).alternativeHandoff(8).isAlternativeHandoff(8).alternativeHandoff("All")

def test_is_order_history_business_test(page):
    login_op(page)
    SendersPage(page).openAccStatusFilter().selectCheckbox("Active").closeDropdownByEsc().openAccTypeFilter().selectCheckbox("Business").closeDropdownByEsc().fillSearchInput("UserCheckout Test").pressApply().getSenderData(int(random_number(1))).openSelectedSenderDetailsPage().isSenderDetailsPage().openOrderHistoryPage().isOrderHistoryPage().backToSenderDetailsPage()
