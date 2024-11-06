import hashlib
from datetime import datetime


class HotelReservation:
    def __init__(self, IdCard, CreditCardNumb,
                 NameAndSurname, PhoneNumber, RoomType, NumDays, ArrivalDate):
        self.__creditcardnumber = CreditCardNumb
        self.__idcard = IdCard
        self.__arrival_date = ArrivalDate
        justnow = datetime.utcnow()
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surmane = NameAndSurname
        self.__phonenumber = PhoneNumber
        self.__roomtype = RoomType
        self.__num_days = NumDays
        self.__localizer = self.localizer

    def __str__(self):
        """return a json string with the
        elements required to calculate the localizer"""
        jsonInfo = {"id_card": self.__idcard,
                    "name_surname": self.__name_surmane,
                    "credit_card": self.__creditcardnumber,
                    "phone_number:": self.__phonenumber,
                    "arrival_date": self.__arrival_date,
                    "num_days": self.__num_days,
                    "room_type": self.__roomtype,
                    }
        return "HotelReservation:" + jsonInfo.__str__()

    @property
    def credit_card(self):
        return self.__creditcardnumber

    @credit_card.setter
    def credit_card(self, Value):
        self.__creditcardnumber = Value

    @property
    def id_card(self):
        return self.__idcard

    @id_card.setter
    def id_card(self, Value):
        self.__idcard = Value

    @property
    def localizer(self):
        """Returns the md5 signature"""
        return hashlib.md5(str(self).encode()).hexdigest()
        # return hashlib.md5(print(self)).hexdigest()

    @localizer.setter
    def localizer(self, Value):
        self.__localizer = Value
