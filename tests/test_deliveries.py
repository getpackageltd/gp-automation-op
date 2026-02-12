import pytest
from config import OPERATOR_EMAIL, OPERATOR_PASSWORD, COURIER_ID
from utils import random_number, random_number_int
from constants import ID, NAME, PHONE, CITY
from pages.deliveries_page import DeliveriesPage
from apimodule.api_requests import ApiRequests

distribCount = 0
expressCount = 0
shrCount = 0
projectsCount = 0
rangeFirst = 0
rangeSecond = 0
notInLineCount = 0
locatingCourierCount = 0
assignedCount = 0
startedCount = 0
pickedUpCount = 0
completedCount = 0
canceledCount = 0
canceledByCourierCount = 0
failedDropCount = 0
returnedCount = 0
nonVipCount = 0
vipCount = 0

def test_calendar_filter_today_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectToday().pressApply().isTodayDateSelected()

def test_calendar_filter_yesterday_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectYesterday().pressApply().isYesterdayDateSelected()

def test_calendar_filter_last_seven_days_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply().isLastSevenDaysSelected()

def test_calendar_filter_last_month_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().pressApply().isLastMonthSelected()

def test_service_type_distribution_filter_test(page):
    global distribCount
    distribCount = DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Distribution").closeDropdownByEsc().pressApply().setRowsOnPage(100).getCountOfRowsService()

def test_service_type_express_filter_test(page):
    global expressCount
    expressCount = DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Express").closeDropdownByEsc().pressApply().setRowsOnPage(100).getCountOfRowsService()

def test_service_type_shr_filter_test(page):
    global shrCount
    shrCount = DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().pressApply().setRowsOnPage(100).getCountOfRowsService()

def test_service_type_projects_filter_test(page):
    global projectsCount
    projectsCount= DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().pressApply().setRowsOnPage(100).getCountOfRowsService()

def test_service_type_all_filter_test(page):
    serviceSum = distribCount+expressCount+shrCount+projectsCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().pressApply().openServiceFilter().selectAllCheckbox().closeDropdownByEsc().pressApply()

def test_service_type_combination_filter_test(page):
    serviceSum = expressCount+shrCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Express").selectCheckbox("Shared Windows").closeDropdownByEsc().pressApply().openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().pressApply().openServiceFilter().selectAllCheckbox().selectAllCheckbox().closeDropdownByEsc().pressApply()


def test_not_in_line_status_filter_test(page):
    global notInLineCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Not In Line").closeDropdownByEsc().pressApply()

def test_locating_courier_status_filter_test(page):
    global locatingCourierCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Locating Courier For Route").closeDropdownByEsc().pressApply()

def test_assigned_status_filter_test(page):
    global assignedCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Assigned").closeDropdownByEsc().pressApply()

def test_started_status_filter_test(page):
    global startedCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Started").closeDropdownByEsc().pressApply()

def test_picked_up_status_filter_test(page):
    global pickedUpCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Picked Up").closeDropdownByEsc().pressApply()

def test_completed_status_filter_test(page):
    global completedCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Completed").closeDropdownByEsc().pressApply()

def test_canceled_status_filter_test(page):
    global canceledCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Canceled").closeDropdownByEsc().pressApply()

def test_canceled_by_courier_status_filter_test(page):
    global canceledByCourierCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Canceled By Courier On Pickup").closeDropdownByEsc().pressApply()

def test_failed_drop_status_filter_test(page):
    global failedDropCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Failed Dropoff").closeDropdownByEsc().pressApply()

def test_returned_status_filter_test(page):
    global returnedCount
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Returned").closeDropdownByEsc().pressApply()

def test_all_status_filter_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().pressApply().openStatusFilter().selectAllCheckbox().closeDropdownByEsc().pressApply()

def test_vip_filter_test(page):
    global nonVipCount, vipCount
    nonVipCount
    vipCount
    nonVipCount = DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectToday().openServiceFilter().selectAllCheckbox().selectCheckbox("Projects").closeDropdownByEsc().openVipFilter().selectCheckbox("Non Vip").closeDropdownByEsc().pressApply().getNumberOfRows().getCountOfRows()
    vipCount = DeliveriesPage(page).openVipFilter().selectCheckbox("Vip").selectCheckbox("Non Vip").closeDropdownByEsc().pressApply().getNumberOfRows().getCountOfRows()
    DeliveriesPage(page).openVipFilter().selectAllCheckbox().selectAllCheckbox().closeDropdownByEsc().pressApply().getNumberOfRows().openVipFilter().selectAllCheckbox().closeDropdownByEsc().pressApply().isSelectedRowsEqals().isSelectedRowsEqualsToSum(nonVipCount+vipCount)

def test_excluded_checkbox_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().openStatusFilter().selectAllCheckbox().selectCheckbox("Canceled").closeDropdownByEsc().pressApply()

def test_delivery_idsearch_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply()

def test_route_idsearch_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().openStatusFilter().selectCheckbox("Completed").closeDropdownByEsc().pressApply()

def test_pack_idsearch_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply()

def test_courier_name_search_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().openStatusFilter().selectCheckbox("Completed").closeDropdownByEsc().pressApply()

def test_account_name_search_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply()

def test_address_pick_search_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply()

def test_address_drop_search_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply()

def test_number_of_rows_page_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().pressApply().setRowsOnPage(100).isRowsOnPage(100).setRowsOnPage(50).isRowsOnPage(50).setRowsOnPage(20).isRowsOnPage(20)

def test_delivery_idheader_search_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply()

def test_route_idheader_search_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().openStatusFilter().selectCheckbox("Completed").closeDropdownByEsc().pressApply()

def test_package_idheader_search_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply()

def test_menu_buttons_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage()

def test_table_data_presents_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastMonth().setRowsOnPage(100).isRowsContainData()

def test_logout_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().logout()

def test_add_remarks_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply()

def test_sort_by_delivery_id(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply().setRowsOnPage(100).pressDeliveryIdSort().isDelivSortedAscend().pressDeliveryIdSort().isDelivSortedDescend()

def test_sort_by_route_id(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().openStatusFilter().selectCheckbox("Completed").closeDropdownByEsc().pressApply()

def test_export_page_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply().setRowsOnPage(50).pressExport().downloadCurrentPage("expage").isFileDownLoaded("expage")

def test_export_all_test(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().openDatePicker().selectLastSevenDays().pressApply().pressExport().downloadAllPages("expages").isFileDownLoaded("expages")

def test_details_shr_kebab_test(page):
    stats = ["Not In Line", "Locating Courier For Route", "Assigned", "Started", "Picked Up", "Completed", "Canceled", "Canceled By Courier On Pickup", "Failed Dropoff", "Returned"]
    ApiRequests().createShrDeliveries(2)
    deliveriesPage = DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage()
    for status in stats:
        deliveriesPage = deliveriesPage.cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()

def test_details_express_kebab_test(page):
    stats = ["Not In Line", "Locating Courier For Route", "Assigned", "Started", "Picked Up", "Completed", "Canceled", "Canceled By Courier On Pickup", "Failed Dropoff", "Returned"]
    deliveriesPage = DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage()
    for status in stats:
        deliveriesPage = deliveriesPage.cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Express").closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()

def test_details_projects_kebab_test(page):
    stats = ["Not In Line", "Locating Courier For Route", "Assigned", "Started", "Picked Up", "Completed", "Canceled", "Canceled By Courier On Pickup", "Failed Dropoff", "Returned"]
    deliveriesPage = DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage()
    for status in stats:
        deliveriesPage = deliveriesPage.cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()

def test_change_pack_size_kebab_test(page):
    sz = ["Envelope","Small","Medium","Large"]
    deliveriesPage =DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage()
    for size in sz:
        deliveriesPage = deliveriesPage.cleanFilter().openDatePicker().selectLastSevenDays().openStatusFilter().selectCheckbox("Not In Line").closeDropdownByEsc().pressApply()

def test_change_status_shr_kebab_test(page):
    stats = ["Not In Line", "Locating Courier For Route", "Assigned", "Started", "Picked Up"]
    deliveriesPage = DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage()
    for status in stats:
        deliveriesPage = deliveriesPage.cleanFilter().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openRange().selectRange(1).closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()

def test_change_status_express_kebab_test(page):
    ApiRequests().createShrDeliveries(2)
    stats = ["Locating Courier For Route", "Assigned", "Started", "Picked Up"]
    deliveriesPage = DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage()
    for status in stats:
        deliveriesPage = deliveriesPage.cleanFilter().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Express").closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()


# def test_exclude_shr_test(page):
#     ApiRequests().createShrDeliveries(2)
#     DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openStatusFilter().selectCheckbox("Not In Line").closeDropdownByEsc().pressApply().checkRows([1, 2, 3]).pressExclude().pressExcludeButtonInDialog()

# def test_exclude_multi_shr_test(page):
#     DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openRange().selectCheckbox("10:30 - 16:00").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier For Route").closeDropdownByEsc().fillSearchInput("תל אביב-יפו").pressApply().checkRows([1, 2, 3]).pressExclude().pressExcludeButtonInDialog()

def test_reschedule_shr_test(page):
    ApiRequests().createShrDeliveries(1)
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openStatusFilter().selectCheckbox("Not In Line").closeDropdownByEsc().pressApply().selectRowCheckbox(1).pressRescheduleButton().selectNextDayInCalendar().selectRescheduleRange("10:30-16:00").pressRescheduleApply()

def test_set_vip_shr_test(page):
    ApiRequests().createShrDeliveries(1)
    DeliveriesPage(page).logIn(OPERATOR_EMAIL,OPERATOR_PASSWORD).isDeliveriesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openStatusFilter().selectCheckbox("Not In Line").closeDropdownByEsc().pressApply()
