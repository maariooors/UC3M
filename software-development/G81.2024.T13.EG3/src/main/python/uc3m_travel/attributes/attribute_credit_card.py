"""ATTRIBUTE CREDIT CARD FILE"""
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.attributes.attribute import Attribute


class CreditCard(Attribute):
    """CREDIT CARD CLASS"""
    def __init__(self, attr_value):
        self._validation_pattern = r"^[0-9]{16}"
        self._error_message = "Invalid credit card format"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        super()._validate(attr_value)
        self.validatecreditcard(attr_value)
        return attr_value

    @staticmethod
    def validatecreditcard(attr_value):
        """validates the credit card number using luhn altorithm"""
        # taken form
        # https://allwin-raju-12.medium.com/
        # credit-card-number-validation-using-luhns-algorithm-in-python-c0ed2fac6234
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(attr_value)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        if not checksum % 10 == 0:
            raise HotelManagementException("Invalid credit card number (not luhn)")
        return attr_value
