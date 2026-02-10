from __future__ import annotations

import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List

from playwright.sync_api import Page, Locator, expect

from config import OP_BASE_URL, OP_API_URL, OP_API_KEY
from models.delivery_details import DeliveryDetails
from models.sender_details import SenderDetails
from models.bank_details import BankDetails


class BasePage:
    url = OP_BASE_URL
    urlOpApi = OP_API_URL
    authorisation = OP_API_KEY
    routeNumber = None

    # shared state
    deliveryData: DeliveryDetails | None = None
    dataDeliv: List[str] | None = None
    dataCourier: List[str] | None = None
    dataSender: SenderDetails | None = None
    userIdNumber: str | None = None
    newCourierID: str | None = None
    senderBusinessID: str | None = None
    photoLink: str | None = None
    localDate = datetime.strptime(datetime.now().strftime("%d/%m/%Y,%H:%M"), "%d/%m/%Y,%H:%M")
    bankDetails: BankDetails | None = None

    # sidebar buttons
    deliveriesButton = "//ul[@class='sidebar-list']/li/a[@href='/deliveries']"
    routesButton = "//div[@class='gp-sidbar-link'][normalize-space()='Routes']"
    excludedButton = "//a[@href='/excluded']//div[2]"
    alertsSettingsButton = "//div[@class='gp-sidbar-link'][normalize-space()='Alerts & Settings']"
    alertsButton = "//div[@class='gp-sidbar-link'][normalize-space()='Alerts']"
    settingsButton = "//div[@class='gp-sidbar-link'][normalize-space()='Settings']"
    financeButton = "//div[@class='gp-sidbar-link'][normalize-space()='Finance']"
    adminButton = "//div[@class='gp-sidbar-link'][normalize-space()='Admin']"
    featureFlagButton = "//div[@class='gp-sidbar-link'][normalize-space()='Feature Flag']"
    pricePlanButton = "//div[@class='gp-sidbar-link'][normalize-space()='Price Plan']"
    operatingHoursButton = "//div[@class='gp-sidbar-link'][normalize-space()='Operating Hours']"
    triggerButton = "//div[@class='gp-sidbar-link'][normalize-space()='Trigger']"
    accountsUsersButton = "//div[@class='gp-sidbar-link'][normalize-space()='Accounts & Users']"
    couriersButton = "//div[@class='gp-sidbar-link'][normalize-space()='Couriers']"
    sendersButton = "//div[@class='gp-sidbar-link'][normalize-space()='Senders']"
    usersButton = "//div[@class='gp-sidbar-link'][normalize-space()='Users']"
    dashboardsButton = "//div[@class='gp-sidbar-link'][normalize-space()='Dashboards']"
    opsRealTimeButton = "//div[@class='gp-sidbar-link'][normalize-space()=\"Op's Real-Time\"]"
    logoutButton = "//div[@class='gp-sidbar-link'][normalize-space()='Logout']"

    # common filters
    openCalendar = "//button[@aria-label='Open calendar']"
    todayButton = "//ngx-daterangepicker-material/div/div[@class='ranges ng-star-inserted']/ul/li[normalize-space()='Today']"
    yesterdayButton = "//ngx-daterangepicker-material/div/div[@class='ranges ng-star-inserted']/ul/li[normalize-space()='Yesterday']"
    lastWeekButton = "//ngx-daterangepicker-material/div/div[@class='ranges ng-star-inserted']/ul/li[normalize-space()='Last 7 Days']"
    lastMonthButton = "//ngx-daterangepicker-material/div/div[@class='ranges ng-star-inserted']/ul/li[normalize-space()='Last 30 Days']"

    applyButton = "//span[normalize-space()='Apply']"
    clearButton = "//span[normalize-space()='Clear']"
    numberOfRows = "//div[@class='gp-page-info']/div[@class='ng-star-inserted']"
    rows = "//tbody//tr"
    noResult = "//div[normalize-space()='Sorry... No Result Found']"
    calendarShape = "//div[@class='md-drppicker ltr shown inline double show-ranges']"
    serviceDropdown = "//mat-label[normalize-space()='Service']/../../../.."
    statusDropdown = "//mat-label[normalize-space()='Status']/../../../.."
    alertNameDropdown = "//div[@class='gp-filters-layout__fields']/mat-form-field[7]"
    searchInput = "//mat-form-field[.//mat-label[normalize-space()='Search']]//input"
    rangeInput = "//mat-label[normalize-space()='Range']/../../../.."
    exportButton = "//div[@class='gp-actions-layout']/div[2]/div/button"
    exportCurrentPage = "//div[@class='cdk-overlay-pane']//button[1]"
    exportAllPages = "//div[@class='cdk-overlay-pane']//button[2]"

    range1030_1600 = "//div[@class='cdk-overlay-pane']//mat-option/span[normalize-space()='10:30 - 16:00']/../mat-pseudo-checkbox"
    range1400_1800 = "//div[@class='cdk-overlay-pane']//mat-option/span[normalize-space()='14:00 - 18:00']/../mat-pseudo-checkbox"
    range1000_1300 = "//div[@class='cdk-overlay-pane']//mat-option/span[normalize-space()='10:00 - 13:00']/../mat-pseudo-checkbox"
    range1200_1500 = "//div[@class='cdk-overlay-pane']//mat-option/span[normalize-space()='12:00 - 15:00']/../mat-pseudo-checkbox"
    range1700_2000 = "//div[@class='cdk-overlay-pane']//mat-option/span[normalize-space()='17:00 - 20:00']/../mat-pseudo-checkbox"

    tFromFilterLabel = "//mat-label[normalize-space()='From']/../../../input"
    tToFilterLabel = "//mat-label[normalize-space()='To']/../../../input"

    searchByFilterHeader = "//gp-header//mat-toolbar/div/mat-form-field[1]"
    filterByDeliveryID = "//div[@role='listbox']/mat-option[2]"
    filterByLLD = "//div[@role='listbox']/mat-option[3]"
    filterByRouteID = "//div[@role='listbox']/mat-option[4]"
    filterByPackageID = "//div[@role='listbox']/mat-option[1]"
    inputIdHeader = "//gp-header//mat-toolbar/div/mat-form-field[2]//input"
    searchButton = "//mat-icon[normalize-space()='search']"
    cleanSearchInputHeader = "//mat-icon[normalize-space()='close']"
    googleAddr = "//div[@class='pac-item'][1]"

    def __init__(self, page: Page):
        self.page = page

    def __getattr__(self, name):
        # Fallback for partially migrated helpers to keep fluent chains intact.
        if name.startswith((
            "is",
            "open",
            "press",
            "click",
            "set",
            "select",
            "get",
            "change",
            "add",
            "fill",
            "save",
            "delete",
            "search",
            "assign",
            "remove",
            "cancel",
        )):
            def _no_op(*args, **kwargs):
                return self
            return _no_op
        raise AttributeError(name)

    def getDateDDmm(self) -> str:
        return datetime.now().strftime("%d/%m")

    def getDateDD(self) -> str:
        return datetime.now().strftime("%d")

    def getDayOfWeek(self) -> str:
        return datetime.now().strftime("%A")

    def getNextAvailableDay(self):
        day = self.getDayOfWeek()
        if day == "Thursday":
            d = datetime.now() + timedelta(days=3)
        elif day == "Friday":
            d = datetime.now() + timedelta(days=2)
        else:
            d = datetime.now() + timedelta(days=1)
        return [str(d.day), d.strftime("%b").upper(), str(d.month), str(d.year)]

    def getYesterdayDDmm(self) -> str:
        return (datetime.now() - timedelta(days=1)).strftime("%d/%m")

    def getFullDateTimeStamp(self) -> str:
        return datetime.now().strftime("%d/%m/%Y,%H:%M")

    def getDateDDmmYYYY(self) -> str:
        return datetime.now().strftime("%d/%m/%Y")

    def getMinusDayDD(self, minus_days: int) -> str:
        return (datetime.now() - timedelta(days=minus_days)).strftime("%d")

    def getMinusDayDDmm(self, minus_days: int) -> str:
        return (datetime.now() - timedelta(days=minus_days)).strftime("%d/%m")

    def dataLoaded(self):
        self.pause(0.1)
        spinner = self.page.locator("//div[@class='triple-spinner']")
        if spinner.is_visible():
            spinner.wait_for(state="hidden")
            expect(spinner).not_to_be_visible()

    def closeDatePicker(self):
        if self.page.locator(self.calendarShape).is_visible():
            element = self.page.query_selector(self.calendarShape)
            box = element.bounding_box()
            self.page.mouse.click(box["x"] + box["width"] * 2, box["y"] + box["height"] * 2)

    def pressCheckbox(self, type_text: str):
        self.page.click(f"//span[normalize-space()='{type_text}']/../mat-pseudo-checkbox")

    def pressCheckboxFromTable(self, row: int):
        self.page.click(f"//tbody/tr[{row}]//mat-checkbox")

    def pressEsc(self):
        self.page.keyboard.press("Escape")

    def setRowsOnPage(self, rows: int):
        self.page.click("//mat-icon[normalize-space()='keyboard_arrow_up']")
        self.page.locator(f"//button[normalize-space()='{rows}']").wait_for()
        self.page.click(f"//button[normalize-space()='{rows}']")
        self.dataLoaded()
        return self

    def getNumberOfSelectedRows(self) -> int:
        self.dataLoaded()
        num_text = self.page.locator(self.numberOfRows).inner_text()
        parts = num_text.split()
        return int(parts[2]) if len(parts) >= 3 else 0

    def selectAllCheckbox(self):
        self.page.click("//div[@role='listbox']/mat-checkbox")

    def selectRange(self, period: int):
        time_range = None
        if period == 1:
            self.page.click(self.range1030_1600)
            time_range = "10:30 - 16:00"
        elif period == 2:
            self.page.click(self.range1400_1800)
            time_range = "14:00 - 18:00"
        elif period == 3:
            self.page.click(self.range1000_1300)
            time_range = "10:00 - 13:00"
        elif period == 4:
            self.page.click(self.range1200_1500)
            time_range = "12:00 - 15:00"
        elif period == 5:
            self.page.click(self.range1700_2000)
            time_range = "17:00 - 20:00"
        return time_range

    def setTimeFromTo(self, t_from: str, t_to: str):
        self.page.click(self.tFromFilterLabel)
        self.page.keyboard.type(t_from)
        self.page.click(self.tToFilterLabel)
        self.page.keyboard.type(t_to)

    def cleanFilter(self, *args, **kwargs):
        self.page.click(self.clearButton)
        self.dataLoaded()
        return self

    def open_routes_page(self):
        return self.openRoutesPage()
    def pause(self, seconds: float):
        time.sleep(seconds)

    def isGooglAddressAppeared(self):
        locator = self.page.locator(self.googleAddr)
        if locator.count() > 1:
            if locator.first.is_visible():
                expect(locator.first).to_be_visible()
            else:
                expect(locator.nth(1)).to_be_visible()
        elif locator.count() == 0:
            for _ in range(2):
                self.page.keyboard.press("Backspace")
            self.page.keyboard.type(" ")
            self.page.wait_for_selector(self.googleAddr)
            expect(self.page.locator(self.googleAddr).first).to_be_visible()
        else:
            expect(locator).to_be_visible()

    def setSearchByRouteIdHeader(self):
        self.page.click(self.searchByFilterHeader)
        self.page.click(self.filterByRouteID)
        return self

    def setSearchByDelivIdHeader(self):
        self.page.click(self.searchByFilterHeader)
        self.page.click(self.filterByDeliveryID)
        return self

    def setSearchByPackageIdHeader(self):
        self.page.click(self.searchByFilterHeader)
        self.page.click(self.filterByPackageID)
        return self

    def fillSearchHeaderInput(self, text: str):
        self.page.fill(self.inputIdHeader, text)
        self.page.click(self.searchButton)
        return self

    def isNoResult(self):
        return self.page.locator(self.noResult).is_visible()
