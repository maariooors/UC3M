"""JSON STORE RESERVATIONS FILE"""

import json
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException


class JsonStoreCheckIn(JsonStore):
    """JSON STORE RESERVATIONS CLASS"""
    _data_list = []
    _file_name = JSON_FILES_PATH + "store_check_in.json"
    _error_message_find = "Guest is already out"

    def add_check_in(self, reservation):
        """add_check_in method"""
        self.find_item(reservation.room_key, "_HotelStay__room_key")
        self.add_item(reservation)

    def read_input_data_from_file(self, input_list):
        """read_input_data_from_file method"""
        try:
            my_localizer = input_list["Localizer"]
            my_id_card = input_list["IdCard"]
        except KeyError as e:
            raise HotelManagementException("Error - Invalid Key in JSON") from e
        return my_id_card, my_localizer

    def read_input_file(self, file_input):
        """read_input_file method"""
        try:
            with open(file_input, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as ex:
            raise HotelManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return input_list
