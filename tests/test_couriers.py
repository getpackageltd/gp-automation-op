import pytest
from config import OPERATOR_EMAIL, OPERATOR_PASSWORD, COURIER_ID
from utils import random_number, random_number_int
from constants import ID, NAME, PHONE, CITY
from pages.courier_details_page import CourierDetailsPage
from pages.couriers_page import CouriersPage
from pages.deliveries_page import DeliveriesPage
from models.courier_details import CourierDetails
from models.bank_details import BankDetails

def login_op(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL, OPERATOR_PASSWORD).openCouriersPage().isCouriersPage().cleanFilter()

def login_for_details(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL, OPERATOR_PASSWORD)

def test_create_user(page):
    login_op(page)
    CouriersPage(page).pressAddCourier().fillNewCourierData(CourierDetails.builder().cFirstName("From_OP").cLastName("Courier"+random_number(4)).cEmail("aleksey.bunkov+"+random_number(7)+"@getpackage.com").cNationalId(random_number(9)).cPhone("050"+random_number(7)).cPassword("LetsStart123!").cRegion(1).cCity("ראשון לציון").cAddress("שדרות ירושלים 25, רמת גן, ישראל").cVehicle(6).cTaxStat(4).cLanguage(2).build()).saveNewCourier().isCourierCreated().openCourierDetails().isCourierDetails()
    page.wait_for_timeout(5000)

def test_add_photo_test(page):
    login_for_details(page)
    CourierDetailsPage(page).openCourierDetails().addPhotoCourier().isPhotoAdded().openUserID().isUserDetailsPage().isPhotoAdded().backToCourierDetails().isPhotoAdded()

def test_user_id_link_test(page):
    login_for_details(page)
    CourierDetailsPage(page).openCourierDetails().openUserID().isUserDetailsPage().isUserDataTrue()

def test_change_vehicle_type_test(page):
    login_for_details(page)
    # Change once for speed; no validation needed
    CourierDetailsPage(page).openCourierDetails().changeVehicleType("Bicycle")

def test_change_fin_email_test(page):
    number = random_number(6)
    login_for_details(page)
    # Change once; no validation needed
    CourierDetailsPage(page).openCourierDetails().changeFinEmail("aleksey.bunkov+"+number+"@getpackage.com")

def test_change_fin_name_test(page):
    number = random_number(6)
    login_for_details(page)
    CourierDetailsPage(page).openCourierDetails().isCourierDetails().changeFinName("Name changed "+number).isFinNameChanged(number)

def test_change_fin_operability_test(page):
    taxStat = ["No invoicing and payment","Allowed","Manual invoicing and payment","No invoicing","No payment"]
    login_for_details(page)
    cdp = CourierDetailsPage(page).openCourierDetails().isCourierDetails()
    for status in taxStat:
        cdp.changeFinStatus(status).isFinStatusChanged(status)

def test_change_tax_withholding_test(page):
    login_for_details(page)
    CourierDetailsPage(page).openCourierDetails().isCourierDetails().changeTaxWithholding("17").isTaxWithholdChanged("17").changeTaxWithholding("30").isTaxWithholdChanged("30")


def test_add_change_bank_details_test(page):
    login_for_details(page)
    CourierDetailsPage(page).openCourierDetails().addBankDetails(BankDetails.builder().bankName("בנק ירושלים").bankBranch("1").bankAccount(random_number(5)).bankNationaID(random_number(9)).bankFullName("Courier From_OP").build()).saveBankDetails().isBankDetails().addBankDetails(BankDetails.builder().bankName("בנק ירושלים").bankBranch("1").bankAccount(random_number(5)).bankNationaID(random_number(9)).bankFullName("Courier From_OP").build()).saveBankDetails().isBankDetails()

def test_delete_bank_details_test(page):
    login_for_details(page)
    CourierDetailsPage(page).openCourierDetails().isCourierDetailsPage().deleteBankDetails().isBankDetailsDeleted()

def test_block_account_test(page):
    login_for_details(page)
    CourierDetailsPage(page).openCourierDetails().isCourierDetailsPage().blockCourierAccount().isAccountBlocked().unblockAccount().blockCourierAccount()