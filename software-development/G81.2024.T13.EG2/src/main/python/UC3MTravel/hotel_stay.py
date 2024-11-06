''' Class HotelStay (GE2.2) '''
from datetime import datetime
import hashlib


class HotelStay():
    def __init__(self, IdCard, Localizer, NumDays, RoomType):
        self.__alg = "SHA-256"
        self.__type = RoomType
        self.__idcard = IdCard
        self.__localizer = Localizer
        justnow = datetime.utcnow()
        self.__arrival = datetime.timestamp(justnow)
        # timestamp is represented in seconds.miliseconds
        # to add the number of days we must express numdays in seconds
        self.__departure = self.__arrival + (int(NumDays) * 24 * 60 * 60)
        self.__room_key = self.room_key

#    def __signature_string(self):
#       """Composes the string to be used for generating the
#      key for the room"""
#       return "{alg:" + self.__alg + ",typ:" + self.__type + ",localizer:" + \
#        self.__localizer + ",arrival:" + self.__arrival + \
#       "departure:" + self.__departure + "}"


    def __str__(self):
        """return a json string with the
        elements required to calculate the localizer"""
        jsonInfo = {"alg": self.__alg,
                    "typ": self.__type,
                    "localizer":  self.__localizer,
                    "arrival:": self.__arrival,
                    "departure": self.__departure,
                    }
        return "{" + jsonInfo.__str__() + "}"

    @property
    def id_card(self):
        """Property that represents the product_id of the patient"""
        return self.__idcard

    @id_card.setter
    def is_card(self, Value):
        self.__idcard = Value

    @property
    def localizer(self):
        """Property that represents the order_id"""
        return self.__localizer

    @localizer.setter
    def localizer(self, Value):
        self.__localizer = Value

    @property
    def arrival(self):
        """Property that represents the phone number of the client"""
        return self.__arrival

    @property
    def room_key(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(str(self).encode()).hexdigest()

    @room_key.setter
    def room_key(self, Value):
        self.__room_key = Value

    @property
    def departure(self):
        """Returns the issued at value"""
        return self.__departure

    @departure.setter
    def departure(self, Value):
        self.__departure = Value
