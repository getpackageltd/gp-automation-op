from dataclasses import dataclass


@dataclass
class CourierDetails:
    cFirstName: str = ""
    cLastName: str = ""
    cEmail: str = ""
    cNationalId: str = ""
    cPhone: str = ""
    cPassword: str = ""
    cAddress: str = ""
    cRegion: int = 0
    cCity: str = ""
    cVehicle: int = 0
    cTaxStat: int = 0
    cLanguage: int = 0
    accountId: str = ""
    taxId: str = ""

    @classmethod
    def builder(cls):
        return _CourierDetailsBuilder()

    def getCFirstName(self):
        return self.cFirstName

    def getCLastName(self):
        return self.cLastName

    def getCEmail(self):
        return self.cEmail

    def getCNationalId(self):
        return self.cNationalId

    def getCPhone(self):
        return self.cPhone

    def getCPassword(self):
        return self.cPassword

    def getCAddress(self):
        return self.cAddress

    def getCRegion(self):
        return self.cRegion

    def getCCity(self):
        return self.cCity

    def getCVehicle(self):
        return self.cVehicle

    def getCTaxStat(self):
        return self.cTaxStat

    def getCLanguage(self):
        return self.cLanguage


class _CourierDetailsBuilder:
    def __init__(self):
        self._data = CourierDetails()

    def cFirstName(self, value):
        self._data.cFirstName = value
        return self

    def cLastName(self, value):
        self._data.cLastName = value
        return self

    def cEmail(self, value):
        self._data.cEmail = value
        return self

    def cNationalId(self, value):
        self._data.cNationalId = value
        return self

    def cPhone(self, value):
        self._data.cPhone = value
        return self

    def cPassword(self, value):
        self._data.cPassword = value
        return self

    def cAddress(self, value):
        self._data.cAddress = value
        return self

    def cRegion(self, value):
        self._data.cRegion = value
        return self

    def cCity(self, value):
        self._data.cCity = value
        return self

    def cVehicle(self, value):
        self._data.cVehicle = value
        return self

    def cTaxStat(self, value):
        self._data.cTaxStat = value
        return self

    def cLanguage(self, value):
        self._data.cLanguage = value
        return self

    def build(self):
        return self._data
