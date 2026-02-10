from dataclasses import dataclass


@dataclass
class BankDetails:
    bankName: str = ""
    bankBranch: str = ""
    bankAccount: str = ""
    bankNationaID: str = ""
    bankFullName: str = ""

    @classmethod
    def builder(cls):
        return _BankDetailsBuilder()

    def getBankName(self):
        return self.bankName

    def getBankBranch(self):
        return self.bankBranch

    def getBankAccount(self):
        return self.bankAccount

    def getBankNationaID(self):
        return self.bankNationaID

    def getBankFullName(self):
        return self.bankFullName


class _BankDetailsBuilder:
    def __init__(self):
        self._data = BankDetails()

    def bankName(self, value):
        self._data.bankName = value
        return self

    def bankBranch(self, value):
        self._data.bankBranch = value
        return self

    def bankAccount(self, value):
        self._data.bankAccount = value
        return self

    def bankNationaID(self, value):
        self._data.bankNationaID = value
        return self

    def bankFullName(self, value):
        self._data.bankFullName = value
        return self

    def build(self):
        return self._data
