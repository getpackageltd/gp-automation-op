from dataclasses import dataclass


@dataclass
class BranchDetails:
    branchName: str = ""
    branchNumber: str = ""
    branchAddress: str = ""
    branchComment: str = ""
    branchContactName: str = ""
    branchContactPhone: str = ""
    branchGpId: str = ""

    @classmethod
    def builder(cls):
        return _BranchDetailsBuilder()

    def setBranchName(self, value):
        self.branchName = value

    def setBranchNumber(self, value):
        self.branchNumber = value

    def setBranchAddress(self, value):
        self.branchAddress = value

    def setBranchComment(self, value):
        self.branchComment = value

    def setBranchContactName(self, value):
        self.branchContactName = value

    def setBranchContactPhone(self, value):
        self.branchContactPhone = value

    def setBranchGpId(self, value):
        self.branchGpId = value

    def getBranchName(self):
        return self.branchName

    def getBranchNumber(self):
        return self.branchNumber

    def getBranchAddress(self):
        return self.branchAddress

    def getBranchComment(self):
        return self.branchComment

    def getBranchContactName(self):
        return self.branchContactName

    def getBranchContactPhone(self):
        return self.branchContactPhone

    def getBranchGpId(self):
        return self.branchGpId


class _BranchDetailsBuilder:
    def __init__(self):
        self._data = BranchDetails()

    def branchName(self, value):
        self._data.branchName = value
        return self

    def branchNumber(self, value):
        self._data.branchNumber = value
        return self

    def branchAddress(self, value):
        self._data.branchAddress = value
        return self

    def branchComment(self, value):
        self._data.branchComment = value
        return self

    def branchContactName(self, value):
        self._data.branchContactName = value
        return self

    def branchContactPhone(self, value):
        self._data.branchContactPhone = value
        return self

    def build(self):
        return self._data
