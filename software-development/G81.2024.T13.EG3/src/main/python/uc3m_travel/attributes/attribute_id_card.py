"""ATTRIBUTE ID CARD FILE"""

from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.attributes.attribute import Attribute


class IdCard(Attribute):
    """IdCard class"""
    def __init__(self, attr_value):
        self._validation_pattern = r'^[0-9]{8}[A-Z]{1}$'
        self._error_message = "Invalid IdCard format"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        super()._validate(attr_value)
        if not self.validate_dni(attr_value):
            raise HotelManagementException("Invalid IdCard letter")
        return attr_value

    @staticmethod
    def validate_dni(attr_value):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        c = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
             "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
             "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
             "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        v = int(attr_value[0:8])
        r = str(v % 23)
        return attr_value[8] == c[r]
