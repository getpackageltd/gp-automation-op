from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.deliveries_page import DeliveriesPage
from pages.routes_page import RoutesPage


class FinancePage(BasePage):
    financeBreadcrumbs = "//gp-breadcrumbs//a[@href='/finance/courier-withdrawls']"
    searchByInput = "//div[@class='gp-filters-layout__fields']//span//mat-label/../../../input"

    courierDateTable = "//tbody/tr/td[2]"
    courierServTypeTable = "//tbody/tr/td[3]"
    courierRouteTable = "//tbody/tr/td[4]/a"
    courierAccountIdTable = "//tbody/tr/td[5]/a"
    courierTaxIdTable = "//tbody/tr/td[6]"
    courierAmountTable = "//tbody/tr/td[7]/span"
    courierPaymentStatusTable = "//tbody/tr/td[9]"
    courierRegionTable = "//tbody/tr/td[10]"

    sendersChargeLinesButton = "//a[@routerlink='/finance/senders-charge-lines']"

    senderChargeDateTable = courierDateTable
    senderChargeAccNameTable = courierServTypeTable
    senderChargeAccIdTable = "//tbody/tr/td[4]"
    senderChargeAccTypeTable = "//tbody/tr/td[5]"
    senderChargeUserNameTable = courierTaxIdTable
    senderChargeUserIdTable = "//tbody/tr/td[7]"
    senderChargeBranchIdTable = "//tbody/tr/td[8]"
    senderChargeBranchNameTable = courierPaymentStatusTable
    senderChargeServTypeTable = courierRegionTable + "/div"
    senderChargeRouteIdTable = "//tbody/tr/td[11]/a"
    senderChargeDelivIdTable = "//tbody/tr/td[12]/a"
    senderChargePackIdTable = "//tbody/tr/td[13]"
    senderChargePackSizeTable = "//tbody/tr/td[14]"
    senderChargePickAddrTable = "//tbody/tr/td[15]"
    senderChargeDropAddrTable = "//tbody/tr/td[16]"
    senderChargeDropOffDateTable = "//tbody/tr/td[17]"
    senderChargeDropNoteTable = "//tbody/tr/td[18]"
    senderChargeDistanceTable = "//tbody/tr/td[19]"
    senderChargeDelivStatusTable = "//tbody/tr/td[20]"
    senderChargeNumOfStopsTable = "//tbody/tr/td[21]"
    senderChargeIdReturnTable = "//tbody/tr/td[24]"
    senderChargeAdminRemarksTable = "//tbody/tr/td[25]"
    senderChargePriceNoTaxTable = "//tbody/tr/td[27]/span"
    senderChargePayMethTable = "//tbody/tr/td[28]"
    senderChargeDescriptionTable = "//tbody/tr/td[29]"
    senderChargePayStatTable = "//tbody/tr/td[30]"
    senderChargeInvoiceTable = "//tbody/tr/td[31]/div/a"
    senderChargeRegionTable = "//tbody/tr/td[33]"

    def isFinancePage(self):
        self.page.wait_for_url(self.url + "/finance/courier-withdrawls")
        self.page.mouse.click(20, 20)
        expect(self.page.locator(self.financeBreadcrumbs)).to_be_visible()
        return self

    def openDeliveriesPage(self):
        self.page.click(self.deliveriesButton)
        return DeliveriesPage(self.page)

    def openRoutesPage(self):
        self.page.click(self.routesButton)
        return RoutesPage(self.page)

    def openSenderChargeLines(self):
        self.page.click(self.sendersChargeLinesButton)
        self.dataLoaded()
        return self

    def isCourierPayout(self):
        data = self.deliveryData
        expect(self.page.locator(self.courierDateTable)).to_contain_text(data.getTimePickUp())
        expect(self.page.locator(self.courierServTypeTable)).to_contain_text(data.getServiceType())
        expect(self.page.locator(self.courierRouteTable)).to_contain_text(data.getRouteId())
        expect(self.page.locator(self.courierAccountIdTable)).to_contain_text(data.getCourierData().accountId)
        expect(self.page.locator(self.courierAmountTable)).to_contain_text(data.getCourierPrice())
        expect(self.page.locator(self.courierPaymentStatusTable)).to_contain_text("Pending")
        expect(self.page.locator(self.courierRegionTable)).to_contain_text("GetPackage Israel")
        return self

    def isSenderChargeLine(self):
        data = self.deliveryData
        if "Credit Card" in self.page.inner_text(self.senderChargePayMethTable):
            while "Charge Created" in self.page.inner_text(self.senderChargePayStatTable):
                self.page.click(self.applyButton)
                self.pause(2)
            expect(self.page.locator(self.senderChargePayStatTable)).to_contain_text("Pending")
        else:
            expect(self.page.locator(self.senderChargePayStatTable)).to_contain_text("Pending")

        expect(self.page.locator(self.senderChargePriceNoTaxTable)).to_contain_text(data.getSenderPrice())
        expect(self.page.locator(self.senderChargeDropAddrTable)).to_contain_text(data.getDropOffAddress())
        expect(self.page.locator(self.senderChargePickAddrTable)).to_contain_text(data.getPickUpAddress())
        expect(self.page.locator(self.senderChargePackSizeTable)).to_contain_text(data.getPackageSize())
        expect(self.page.locator(self.senderChargePackIdTable)).to_contain_text(data.getPackageId())
        expect(self.page.locator(self.senderChargeDelivIdTable)).to_contain_text(data.getDeliveryId())
        expect(self.page.locator(self.senderChargeRouteIdTable)).to_contain_text(data.getRouteId())
        expect(self.page.locator(self.senderChargeServTypeTable)).to_contain_text(data.getServiceType())
        expect(self.page.locator(self.senderChargeDateTable)).to_contain_text(data.getTimePickUp())
        return self

    def findByRouteID(self):
        self.page.fill(self.searchByInput, self.deliveryData.getRouteId())
        self.page.click(self.applyButton)
        self.dataLoaded()
        return self
