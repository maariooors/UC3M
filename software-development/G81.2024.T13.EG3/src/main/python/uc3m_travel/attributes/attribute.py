"""ATRIBUTE FILE"""
import re
from uc3m_travel.hotel_management_exception import HotelManagementException


class Attribute:
    """Attribute class"""
    def __init__(self):
        self._validation_pattern = ""
        self._error_message = ""
        self._attr_value = ""

    def _validate(self, attr_value):
        """Validate attribute value"""
        myregex = re.compile(self._validation_pattern)
        res = myregex.fullmatch(attr_value)
        if not res:
            raise HotelManagementException(self._error_message)
        return attr_value


    @property
    def value(self):
        """Value property"""
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = attr_value
