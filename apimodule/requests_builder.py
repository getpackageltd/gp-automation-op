import json
import os
import random

from config import RESOURCES_DIR


class RequestsBuilder:
    _addresses = None

    def _load_addresses(self):
        if self._addresses is not None:
            return
        path = os.path.join(RESOURCES_DIR, "addrtelaviv.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        addresses = []
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            street = props.get("addr:street")
            number = props.get("addr:housenumber")
            if street and number:
                addresses.append(f"{street}, {number}, תל אביב-יפו")
        self._addresses = addresses

    def getRandomeAddress(self):
        self._load_addresses()
        if not self._addresses:
            return "תל אביב-יפו"
        return random.choice(self._addresses)
