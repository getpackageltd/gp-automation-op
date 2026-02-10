from dataclasses import dataclass


@dataclass
class SenderDetails:
    sAccountName: str = ""
    sOwnerName: str = ""
    sEmail: str = ""
    sPhone: str = ""
    sAddress: str = ""
    sPayMethod: str = ""
    sTaxId: str = ""
    finName: str = ""
    sBillingEmail: str = ""
    sCreditCard: str = ""
    senderId: str = ""
    createdAt: str = ""
    lastOrder: str = ""
    accStatus: str = ""
    accType: str = ""
    userId: str = ""

    @classmethod
    def builder(cls):
        return _SenderDetailsBuilder()

    def setSenderId(self, value):
        self.senderId = value

    def setSAccountName(self, value):
        self.sAccountName = value

    def setCreatedAt(self, value):
        self.createdAt = value

    def setLastOrder(self, value):
        self.lastOrder = value

    def setAccStatus(self, value):
        self.accStatus = value

    def setSOwnerName(self, value):
        self.sOwnerName = value

    def setAccType(self, value):
        self.accType = value

    def setSPayMethod(self, value):
        self.sPayMethod = value

    def setSAddress(self, value):
        self.sAddress = value

    def setSEmail(self, value):
        self.sEmail = value

    def setSPhone(self, value):
        self.sPhone = value

    def setSBillingEmail(self, value):
        self.sBillingEmail = value

    def setSCreditCard(self, value):
        self.sCreditCard = value

    def setSTaxId(self, value):
        self.sTaxId = value

    def setFinName(self, value):
        self.finName = value

    def setAccStatus(self, value):
        self.accStatus = value

    def setAccType(self, value):
        self.accType = value

    def getSenderId(self):
        return self.senderId

    def getSAccountName(self):
        return self.sAccountName

    def getCreatedAt(self):
        return self.createdAt

    def getLastOrder(self):
        return self.lastOrder

    def getAccStatus(self):
        return self.accStatus

    def getSOwnerName(self):
        return self.sOwnerName

    def getAccType(self):
        return self.accType

    def getSPayMethod(self):
        return self.sPayMethod

    def getSAddress(self):
        return self.sAddress

    def getSEmail(self):
        return self.sEmail

    def getSPhone(self):
        return self.sPhone

    def getSBillingEmail(self):
        return self.sBillingEmail

    def getSCreditCard(self):
        return self.sCreditCard

    def getSTaxId(self):
        return self.sTaxId

    def getFinName(self):
        return self.finName

    def getAccStatus(self):
        return self.accStatus

    def getAccType(self):
        return self.accType


class _SenderDetailsBuilder:
    def __init__(self):
        self._data = SenderDetails()

    def build(self):
        return self._data
