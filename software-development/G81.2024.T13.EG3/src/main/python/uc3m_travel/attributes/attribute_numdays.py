"""ATRIBUTE NUMDAYS FILE"""
from uc3m_travel.attributes.attribute import Attribute
from uc3m_travel.hotel_management_exception import HotelManagementException

class NumDays(Attribute):
    """NUM DAYS CLASS"""
    def __init__(self, attr_value):
        self._validation_pattern = r"(1|2|3|4|5|6|7|8|9|10)"
        self._error_message = "Numdays should be in the range 1-10"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        self.validate_numdays(attr_value)
        super()._validate(str(attr_value))
        return attr_value
    def validate_numdays(self, attr_value):
        """validates the number of days"""
        try:
            int(attr_value)
        except ValueError as ex:
            raise HotelManagementException("Invalid num_days datatype") from ex
        return attr_value
