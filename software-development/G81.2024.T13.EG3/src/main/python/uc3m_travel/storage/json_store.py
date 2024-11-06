"""JSON STORY FILE"""

import json
from uc3m_travel.hotel_management_exception import HotelManagementException


class JsonStore:
    """JsonStore class"""
    _data_list = []
    _file_name = ""
    _error_message_find = ""

    def __init__(self):
        self.load_store(self._file_name)

    def load_store(self, file_store):
        """Load json file"""
        try:
            with open(file_store, 'r', encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []

        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON FORMAT") from ex
        return self._data_list

    def add_item(self, my_reservation):
        """Add item"""
        self.load_store(self._file_name)
        self._data_list.append(my_reservation.__dict__)
        self.save_store(self._file_name)

    def save_store(self, file_store):
        """Save json file"""
        try:
            with open(file_store, 'w', encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file or file path") from ex

    def find_item(self, value, key):
        """Find item by value"""
        self.load_store(self._file_name)
        for item in self._data_list:
            if value == item[key]:
                raise HotelManagementException(self._error_message_find)
