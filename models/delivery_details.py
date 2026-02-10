from dataclasses import dataclass
from models.courier_details import CourierDetails
from models.sender_details import SenderDetails
from models.user_details import UserDetails


@dataclass
class DeliveryDetails:
    deliveryId: str = ""
    routeId: str = ""
    packageId: str = ""
    serviceType: str = ""
    courierData: CourierDetails | None = None
    senderData: SenderDetails | None = None
    userData: UserDetails | None = None
    status: str = ""
    pickUpAddress: str = ""
    dropOffAddress: str = ""
    timePickUp: str = ""
    timeDropOff: str = ""
    courierPrice: str = ""
    senderPrice: str = ""
    packageSize: str = ""

    @classmethod
    def builder(cls):
        return _DeliveryDetailsBuilder()

    def getDeliveryId(self):
        return self.deliveryId

    def getRouteId(self):
        return self.routeId

    def getPackageId(self):
        return self.packageId

    def getServiceType(self):
        return self.serviceType

    def getCourierData(self):
        return self.courierData

    def getSenderData(self):
        return self.senderData

    def getUserData(self):
        return self.userData

    def getStatus(self):
        return self.status

    def getPickUpAddress(self):
        return self.pickUpAddress

    def getDropOffAddress(self):
        return self.dropOffAddress

    def getTimePickUp(self):
        return self.timePickUp

    def getTimeDropOff(self):
        return self.timeDropOff

    def getCourierPrice(self):
        return self.courierPrice

    def getSenderPrice(self):
        return self.senderPrice

    def getPackageSize(self):
        return self.packageSize


class _DeliveryDetailsBuilder:
    def __init__(self):
        self._data = DeliveryDetails()

    def build(self):
        return self._data
