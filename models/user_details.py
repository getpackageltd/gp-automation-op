from dataclasses import dataclass


@dataclass
class UserDetails:
    userName: str = ""
    userStatus: str = ""
    userId: str = ""
    phoneNumber: str = ""
    email: str = ""
    dateCreate: str = ""

    @classmethod
    def builder(cls):
        return _UserDetailsBuilder()

    def getUserName(self):
        return self.userName

    def getUserStatus(self):
        return self.userStatus

    def getUserId(self):
        return self.userId

    def getDateCreate(self):
        return self.dateCreate


class _UserDetailsBuilder:
    def __init__(self):
        self._data = UserDetails()

    def userName(self, value):
        self._data.userName = value
        return self

    def userStatus(self, value):
        self._data.userStatus = value
        return self

    def userId(self, value):
        self._data.userId = value
        return self

    def dateCreate(self, value):
        self._data.dateCreate = value
        return self

    def build(self):
        return self._data
