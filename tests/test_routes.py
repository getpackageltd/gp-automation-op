import pytest
from config import OPERATOR_EMAIL, OPERATOR_PASSWORD, COURIER_ID
from utils import random_number, random_number_int
from constants import ID, NAME, PHONE, CITY
from pages.deliveries_page import DeliveriesPage
from pages.routes_page import RoutesPage

def open_routes_page(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL, OPERATOR_PASSWORD).openRoutesPage().isRoutesPage().cleanFilter()

distribCount = 0
expressCount = 0
shrCount = 0
projectsCount = 0
rangeFirst = 0
rangeSecond = 0
locatingCourierCount = 0
assignedCount = 0
onMyWayCount = 0
completedCount = 0
canceledCount = 0
canceledPickCount = 0

def login_op(page):
    DeliveriesPage(page).logIn(OPERATOR_EMAIL, OPERATOR_PASSWORD).open_routes_page().isRoutesPage().cleanFilter(page)

def test_calendar_filter_today_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectToday().pressApply().isTodayDateSelected()

def test_calendar_filter_yesterday_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectYesterday().pressApply().isYesterdayDateSelected()

def test_calendar_filter_last_seven_days_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().pressApply().isLastSevenDaysSelected()

def test_calendar_filter_last_month_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().pressApply().isLastMonthSelected()

def test_service_type_distribution_filter_test(page):
    global distribCount
    login_op(page)
    distribCount = RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Distribution").closeDropdownByEsc().pressApply().setRowsOnPage(100).isServiceType("Distribution").getCountOfRowsService()

def test_service_type_express_filter_test(page):
    global expressCount
    login_op(page)
    expressCount = RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Express").closeDropdownByEsc().pressApply().setRowsOnPage(100).isServiceType("Express").getCountOfRowsService()

def test_service_type_shr_filter_test(page):
    global shrCount
    login_op(page)
    shrCount = RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().pressApply().setRowsOnPage(100).isServiceType("Shared Windows").getCountOfRowsService()

def test_service_type_projects_filter_test(page):
    global projectsCount
    login_op(page)
    projectsCount= RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().pressApply().setRowsOnPage(100).isServiceType("Projects").getCountOfRowsService()

def test_service_type_all_filter_test(page):
    login_op(page)
    serviceSum = distribCount+expressCount+shrCount+projectsCount
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().pressApply().getNumberOfRows().openServiceFilter().selectAllCheckbox().closeDropdownByEsc().pressApply().isSelectedRowsEqals().isSelectedRowsEqualsToSum(serviceSum-1)

def test_service_type_combination_filter_test(page):
    login_op(page)
    serviceSum = expressCount+shrCount
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Express").selectCheckbox("Shared Windows").closeDropdownByEsc().pressApply().getNumberOfRows().isSelectedRowsEqualsToSum(serviceSum-1).openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().pressApply().getNumberOfRows().isSelectedRowsEqualsToSum(serviceSum-1+projectsCount).openServiceFilter().selectAllCheckbox().selectAllCheckbox().closeDropdownByEsc().pressApply().getNumberOfRows().isSelectedRowsEqualsToSum(serviceSum-1+projectsCount+distribCount)

def test_time_first_range_test(page):
    global rangeFirst
    login_op(page)
    rangeFirst = RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().openRange().selectRange(1).closeDropdownByEsc().pressApply().setRowsOnPage(100).checkOfSelectedRowsRange().getNumberOfRows().getCountOfRows()

def test_time_second_range_test(page):
    global rangeSecond
    login_op(page)
    rangeSecond = RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().openRange().selectRange(2).closeDropdownByEsc().pressApply().setRowsOnPage(100).checkOfSelectedRowsRange().getNumberOfRows().getCountOfRows()

def test_all_time_range_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().pressApply().getNumberOfRows().openRange().selectAllCheckbox().closeDropdownByEsc().pressApply().isSelectedRowsEqals().openRange().selectAllCheckbox().closeDropdownByEsc().pressApply().isSelectedRowsEqals()

def test_combined_time_range_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().openRange().selectRange(1).selectRange(2).closeDropdownByEsc().pressApply().getNumberOfRows().isSelectedRowsEqualsToSum(rangeFirst+rangeSecond)

def test_time_picker_amtest(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().setTimeFromTo("1015AM","1015AM").pressApply().isTimeSelected("10:15")

def test_time_picker_pmtest(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().setTimeFromTo("1515","1545").pressApply().isTimeSelectedPeriod()

def test_locating_courier_status_filter_test(page):
    global locatingCourierCount
    login_op(page)
    locatingCourierCount = RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().isStatusType("Locating Courier").getNumberOfRows().getCountOfRows()

def test_assigned_status_filter_test(page):
    global assignedCount
    login_op(page)
    assignedCount = RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Courier Assigned").closeDropdownByEsc().pressApply().isStatusType("Courier Assigned").getNumberOfRows().getCountOfRows()

def test_on_my_way_status_filter_test(page):
    global onMyWayCount
    login_op(page)
    onMyWayCount = RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("On My Way").closeDropdownByEsc().pressApply().isStatusType("On My Way").getNumberOfRows().getCountOfRows()

def test_completed_status_filter_test(page):
    global completedCount
    login_op(page)
    completedCount = RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Completed").closeDropdownByEsc().pressApply().isStatusType("Completed").getNumberOfRows().getCountOfRows()

def test_canceled_status_filter_test(page):
    global canceledCount
    login_op(page)
    canceledCount = RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Canceled").closeDropdownByEsc().pressApply().isStatusType("Canceled").getNumberOfRows().getCountOfRows()

def test_canceled_on_pickup_status_filter_test(page):
    global canceledPickCount
    login_op(page)
    canceledPickCount = RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openStatusFilter().selectCheckbox("Canceled On Pick Up").closeDropdownByEsc().pressApply().isStatusType("Canceled On Pick Up").getNumberOfRows().getCountOfRows()

def test_all_status_filter_test(page):
    login_op(page)
    statuses = (
        locatingCourierCount
        + assignedCount
        + onMyWayCount
        + completedCount
        + canceledCount
        + canceledPickCount
    )
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().pressApply().getNumberOfRows().openStatusFilter().selectAllCheckbox().closeDropdownByEsc().pressApply().isSelectedRowsEqals().isSelectedRowsEqualsToSum(statuses)

def test_alerts_filter_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().openAlertNameFilter().selectCheckbox("Pu Time, No Courier").closeDropdownByEsc().pressApply().isAlertInRow().openAlertNameFilter().selectCheckbox("Pu Time, Courier Late").selectCheckbox("Pu Time, No Courier").closeDropdownByEsc().pressApply().isAlertInRow().openAlertNameFilter().selectCheckbox("Do Time, Courier Late").selectCheckbox("Pu Time, Courier Late").closeDropdownByEsc().pressApply().isAlertInRow().openAlertNameFilter().selectCheckbox("Gett Pu Time, No Courier").selectCheckbox("Do Time, Courier Late").closeDropdownByEsc().pressApply().isAlertInRow().openAlertNameFilter().selectCheckbox("Gett Pu Time, Courier Late").selectCheckbox("Gett Pu Time, No Courier").closeDropdownByEsc().pressApply().isAlertInRow().openAlertNameFilter().selectCheckbox("Gett Do Time, Courier Late").selectCheckbox("Gett Pu Time, Courier Late").closeDropdownByEsc().pressApply().isAlertInRow()

def test_route_idsearch_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().pressApply().getSearchNData(2).fillSearchInput().pressApply().isDeliveryFound(2).cleanFilter(page)

def test_courier_name_search_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().pressApply().getSearchNData(4).fillSearchInput().pressApply().isDeliveryFound(4).cleanFilter(page)

def test_address_pick_search_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().pressApply().getSearchNData(5).fillSearchInput().pressApply().isDeliveryFound(5).cleanFilter(page)

def test_address_drop_search_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().pressApply().getSearchNData(6).fillSearchInput().pressApply().isDeliveryFound(6).cleanFilter(page)

def test_number_of_rows_page_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().pressApply().setRowsOnPage(100).isRowsOnPage(100).setRowsOnPage(50).isRowsOnPage(50).setRowsOnPage(20).isRowsOnPage(20)

def test_route_idheader_search_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().getSearchNData(2).setSearchByRouteIdHeader().fillSearchHeaderInput().pressSearchHeaderButtonRoute().isRouteFound().cleanFilterHeader()

def test_menu_buttons_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDeliveriesPage().isDeliveriesPage().open_routes_page().isRoutesPage().openExcludedPage().isExcludedPage().open_routes_page().isRoutesPage().openAlertsPage().isAlertsPage().open_routes_page().isRoutesPage().openSettingsPage().isSettingsPage().open_routes_page().isRoutesPage().openFinancePage().isFinancePage().open_routes_page().isRoutesPage().openAdminFeatureFlag().isAdminFeatureFlag().open_routes_page().isRoutesPage().isRoutesPage().openAdminOpeningHoursPage().isAdminOpeningHoursPage().open_routes_page().openCouriersPage().isCouriersPage().open_routes_page().isRoutesPage().openSendersPage().isSendersPage().open_routes_page().isRoutesPage().openUsersPage().isUsersPage().open_routes_page().isRoutesPage().openOpsRealTimePage().isOpsRealTimePage().open_routes_page().isRoutesPage()

def test_table_data_presents_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastMonth().setRowsOnPage(100).isRowsContainData()

def test_logout_test(page):
    RoutesPage(page).isRoutesPage().logout().isLogedOut()

def test_add_remarks_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().pressApply().openRemarks().fillRemark("Remarks test").cancelRemarkSave().openRemarks().fillRemark("Remarks test").saveRemark().getSearchNData(2).fillSearchInput().pressApply().isDeliveryFound(2).isRemark("Remarks test").openRemarks().fillRemark("Remarks changed").saveRemark().cleanFilter().fillSearchInput().pressApply().isDeliveryFound(2).isRemark("Remarks changed").openRemarks().fillRemark("").saveRemark().isRemark("")

def test_sort_by_route_id(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().openDatePicker().selectLastSevenDays().pressApply().setRowsOnPage(100).pressDeliveryIdSort().isDelivSortedAscend().pressDeliveryIdSort().isDelivSortedDescend()

def test_details_shr_kebab_test(page):
    stats = ["Locating Courier", "Courier Assigned", "On My Way", "Completed", "Canceled", "Canceled On Pick Up"]
    login_op(page)
    routesPage = RoutesPage(page).isRoutesPage()
    for status in stats:
        routesPage = routesPage.cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()
        if routesPage.isNoResult():
            routesPage.getSearchNData(2).fillSearchInput().pressApply().getDeliveryData().pressKebab().clickKebabButton("Details").isDetailPage().isRouteDataOnDeliveryPage().backToRoutesPage()

def test_details_express_kebab_test(page):
    stats = ["Locating Courier", "Courier Assigned", "On My Way", "Completed", "Canceled", "Canceled On Pick Up"]
    login_op(page)
    routesPage = RoutesPage(page).isRoutesPage()
    for status in stats:
        routesPage = routesPage.cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Express").closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()
        if routesPage.isNoResult():
            routesPage.getSearchNData(2).setSearchByRouteIdHeader().fillSearchHeaderInput().pressSearchHeaderButtonRoute().getDeliveryData().pressKebab().clickKebabButton("Details").isDetailPage().isRouteDataOnDeliveryPage().backToRoutesPage()

def test_details_projects_kebab_test(page):
    stats = ["Locating Courier", "Courier Assigned", "On My Way", "Completed", "Canceled", "Canceled On Pick Up"]
    login_op(page)
    routesPage = RoutesPage(page).isRoutesPage()
    for status in stats:
        routesPage = routesPage.cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()
        if routesPage.isNoResult():
            routesPage.getSearchNData(2).fillSearchInput().pressApply().getDeliveryData().pressKebab().clickKebabButton("Details").isDetailPage().isRouteDataOnDeliveryPage().backToRoutesPage()

def test_change_price_shr_kebab_test(page):
    stats = ["Locating Courier", "Courier Assigned", "On My Way"]
    login_op(page)
    routesPage = RoutesPage(page).isRoutesPage()
    for status in stats:
        routesPage = routesPage.cleanFilter().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()
        if routesPage.isNoResult():
            routesPage.getSearchNData(2).fillSearchInput().pressApply().pressKebab().clickKebabButton("Change Price").fillDelta("0").pressButton("Change").getSearchNData(13).pressKebab().clickKebabButton("Change Price").isChangePricePopup().fillDelta("11.19").isPriceCalculated().pressButton("Change").isPriceChanged().pressKebab().clickKebabButton("Change Price").isChangePricePopup().fillDelta("0").isPriceCalculated().pressButton("Change").isPriceChanged()

def test_change_price_express_kebab_test(page):
    stats = ["Locating Courier", "Courier Assigned", "On My Way"]
    login_op(page)
    routesPage = RoutesPage(page).isRoutesPage()
    for status in stats:
        routesPage = routesPage.cleanFilter().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Express").closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()
        if routesPage.isNoResult():
            routesPage.getSearchNData(2).fillSearchInput().pressApply().pressKebab().clickKebabButton("Change Price").fillDelta("0").pressButton("Change").getSearchNData(13).pressKebab().clickKebabButton("Change Price").isChangePricePopup().fillDelta("11.19").isPriceCalculated().pressButton("Change").isPriceChanged().pressKebab().clickKebabButton("Change Price").isChangePricePopup().fillDelta("0").isPriceCalculated().pressButton("Change").isPriceChanged()

def test_change_price_project_kebab_test(page):
    stats = ["Locating Courier", "Courier Assigned", "On My Way"]
    login_op(page)
    routesPage = RoutesPage(page).isRoutesPage()
    for status in stats:
        routesPage = routesPage.cleanFilter().openDatePicker().selectLastMonth().openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().openStatusFilter().selectCheckbox(status).closeDropdownByEsc().pressApply()
        if routesPage.isNoResult():
            routesPage.getSearchNData(2).fillSearchInput().pressApply().pressKebab().clickKebabButton("Change Price").fillDelta("0").pressButton("Change").getSearchNData(13).pressKebab().clickKebabButton("Change Price").isChangePricePopup().fillDelta("11.19").isPriceCalculated().pressButton("Change").isPriceChanged().pressKebab().clickKebabButton("Change Price").isChangePricePopup().fillDelta("0").isPriceCalculated().pressButton("Change").isPriceChanged()

def test_assign_courier_shr_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().getSearchNData(2).fillSearchInput().pressApply().pressKebab().pressButton("Assign Courier").isAssignCourierPopup().assignCourierPopup(COURIER_ID).pressButton("Assign").isStatusType("Courier Assigned").pressKebab().pressButton("Unassign Courier").isUnnassignCourierPopup().pressButton("Unassign").isStatusType("Locating Courier")

def test_assign_courier_express_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Express").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().getSearchNData(2).fillSearchInput().pressApply().pressKebab().pressButton("Assign Courier").isAssignCourierPopup().assignCourierPopup(COURIER_ID).pressButton("Assign").isStatusType("Courier Assigned").pressKebab().pressButton("Unassign Courier").isUnnassignCourierPopup().pressButton("Unassign").isStatusType("Locating Courier")

def test_assign_courier_projects_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().getSearchNData(2).fillSearchInput().pressApply().pressKebab().pressButton("Assign Courier").isAssignCourierPopup().assignCourierPopup(COURIER_ID).pressButton("Assign").isStatusType("Courier Assigned").pressKebab().pressButton("Unassign Courier").isUnnassignCourierPopup().pressButton("Unassign").isStatusType("Locating Courier")

def test_locating_courier_shr_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().getSearchNData(2).fillSearchInput().pressApply().pressKebab().pressButton("Locating Courier").isLocatingCourierPopup().openCourierTypes().selectCheckbox("Monthly Active").closeDropdownByEsc().setDistance("100").pressButton("Apply").getCourierName().searchLocatedCourier().isCourierFoundByName().pressButton("Clear").openCourierTypes().selectCheckbox("Monthly Active").closeDropdownByEsc().setDistance("100").pressButton("Apply").getCourierID().searchLocatedCourier().isCourierFoundByID().pressButton("Assign Courier").isAssignCourierPopup().pressButton("Assign").openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().isCourierNameTrue().isStatusType("Courier Assigned").pressKebab().pressButton("Unassign Courier").isUnnassignCourierPopup().pressButton("Unassign").isStatusType("Locating Courier")

def test_locating_courier_express_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Express").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().getSearchNData(2).fillSearchInput().pressApply().pressKebab().pressButton("Locating Courier").isLocatingCourierPopup().openCourierTypes().selectCheckbox("Monthly Active").closeDropdownByEsc().setDistance("100").pressButton("Apply").getCourierName().searchLocatedCourier().isCourierFoundByName().pressButton("Clear").openCourierTypes().selectCheckbox("Monthly Active").closeDropdownByEsc().setDistance("100").pressButton("Apply").getCourierID().searchLocatedCourier().isCourierFoundByID().pressButton("Assign Courier").isAssignCourierPopup().pressButton("Assign").openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().isCourierNameTrue().isStatusType("Courier Assigned").pressKebab().pressButton("Unassign Courier").isUnnassignCourierPopup().pressButton("Unassign").isStatusType("Locating Courier")

def test_locating_courier_project_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().getSearchNData(2).fillSearchInput().pressApply().pressKebab().pressButton("Locating Courier").isLocatingCourierPopup().openCourierTypes().selectCheckbox("Monthly Active").closeDropdownByEsc().setDistance("100").pressButton("Apply").getCourierName().searchLocatedCourier().isCourierFoundByName().pressButton("Clear").openCourierTypes().selectCheckbox("Monthly Active").closeDropdownByEsc().setDistance("100").pressButton("Apply").getCourierID().searchLocatedCourier().isCourierFoundByID().pressButton("Assign Courier").isAssignCourierPopup().pressButton("Assign").openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().isCourierNameTrue().isStatusType("Courier Assigned").pressKebab().pressButton("Unassign Courier").isUnnassignCourierPopup().pressButton("Unassign").isStatusType("Locating Courier")

def test_push_note_shr_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Shared Windows").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().pressKebab().pressButton("Push Notification").isPushPopup().fillTitleText("Title @123").clickTextArea().resetTextArea().fillTextArea("Text @123").clickTitleArea().resetTextArea().pressButton("Cancel")

def test_push_note_express_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Express").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().pressKebab().pressButton("Push Notification").isPushPopup().fillTitleText("Title @123").clickTextArea().resetTextArea().fillTextArea("Text @123").clickTitleArea().resetTextArea().pressButton("Cancel")

def test_push_note_project_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().pressKebab().pressButton("Push Notification").isPushPopup().fillTitleText("Title @123").clickTextArea().resetTextArea().fillTextArea("Text @123").clickTitleArea().resetTextArea().pressButton("Cancel")

def test_reschedule_express_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Express").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().getSearchNData(2).fillSearchInput().pressApply().pressKebab().pressButton("Reschedule Route").isReschedulePopup().setNextAvailableDay().setTime().pressButton("Save").isRescheduledDay().isRescheduledTime()

def test_reschedule_project_kebab_test(page):
    login_op(page)
    RoutesPage(page).isRoutesPage().cleanFilter().openDatePicker().selectLastSevenDays().openServiceFilter().selectCheckbox("Projects").closeDropdownByEsc().openStatusFilter().selectCheckbox("Locating Courier").closeDropdownByEsc().pressApply().getSearchNData(2).fillSearchInput().pressApply().pressKebab().pressButton("Reschedule Route").isReschedulePopup().setNextAvailableDay().pressButton("Save").isRescheduledDay()
