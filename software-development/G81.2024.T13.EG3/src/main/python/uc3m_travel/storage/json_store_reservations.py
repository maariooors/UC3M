"""JSON STORE RESERVATIONS FILE"""

from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException


class JsonStoreReservations(JsonStore):
    """JSON STORE RESERVATIONS CLASS"""
    _data_list = []
    _file_name = JSON_FILES_PATH + "store_reservation.json"
    _error_message_find = "Reservation already exists"

    def check_reservation(self, localizer, id_card):
        """check_reservation method"""
        self.load_store(self._file_name)
        self.find_item(localizer, "_HotelReservation__localizer")
        self._error_message_find = "This ID card has another reservation"
        self.find_item(id_card, "_HotelReservation__id_card")

    def add_reservation(self, reservation):
        """add_reservation method"""
        self.check_reservation(reservation.localizer, reservation.id_card)
        self.add_item(reservation)

    def find_reservation_localizer(self, localizer):
        """find_reservation_localizer method"""
        self._data_list = self.load_store(self._file_name)
        self._error_message_find = "Error: localizer not found"

        for item in self._data_list:
            if localizer == item["_HotelReservation__localizer"]:
                return item
            raise HotelManagementException(self._error_message_find)
