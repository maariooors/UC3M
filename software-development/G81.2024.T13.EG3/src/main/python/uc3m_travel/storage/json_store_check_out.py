"""JSON STORE RESERVATIONS FILE"""

import json
from datetime import datetime
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException


class JsonStoreCheckOut(JsonStore):
    """JSON STORE RESERVATIONS CLASS"""
    _data_list = []
    _file_name = JSON_FILES_PATH + "store_check_out.json"
    _error_message_find = "Guest is already out"

    def add_item(self, my_reservation):
        """Add item"""
        self.load_store(self._file_name)
        self._data_list.append(my_reservation)
        self.save_store(self._file_name)

    def add_checkout(self, checkout):
        """add_checkout method"""
        self.find_item(checkout["room_key"], "room_key")
        self.add_item(checkout)

    def find_roomkey_checkout(self, file_name):
        """find_roomkey_checkout method"""
        try:
            with open(file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as ex:
            raise HotelManagementException("Error: store checkin not found") from ex
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return self._data_list

    def check_room_key(self, room_key, room_key_list):
        """check_room_key method"""
        found = False
        for item in room_key_list:
            if room_key == item["_HotelStay__room_key"]:
                departure_date_timestamp = item["_HotelStay__departure"]
                found = True
        if not found:
            raise HotelManagementException("Error: room key not found")
        today = datetime.utcnow().date()
        if datetime.fromtimestamp(departure_date_timestamp).date() != today:
            raise HotelManagementException("Error: today is not the departure day")
