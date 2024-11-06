"""Module for the hotel manager"""

from datetime import datetime
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.attributes.attribute_roomkey import RoomKey
from uc3m_travel.storage.json_store_check_in import JsonStoreCheckIn
from uc3m_travel.storage.json_store_check_out import JsonStoreCheckOut
from uc3m_travel.storage.json_store_reservations import JsonStoreReservations
from uc3m_travel.hotel_reservation import HotelReservation


class HotelManager:
    """Class with all the methods for managing reservations and stays"""

    def __init__(self):
        pass

    # pylint: disable=too-many-arguments
    def room_reservation(self, credit_card: str, name_surname: str, id_card: str, phone_number: str, room_type: str,
                         arrival_date: str, num_days: int) -> str:
        """manges the hotel reservation: creates a reservation and saves it into a json file"""

        my_reservation = HotelReservation(id_card=id_card,
                                          credit_card_number=credit_card,
                                          name_surname=name_surname,
                                          phone_number=phone_number,
                                          room_type=room_type,
                                          arrival=arrival_date,
                                          num_days=num_days)

        # escribo el fichero Json con todos los datos
        reservation_store = JsonStoreReservations()
        reservation_store.add_reservation(my_reservation)
        return my_reservation.localizer

    def guest_arrival(self, file_input: str) -> str:
        my_checkin = HotelStay.create_guest_arrival_from_file(file_input)

        # Ahora lo guardo en el almacen nuevo de checkin
        checkin_store = JsonStoreCheckIn()
        checkin_store.add_check_in(my_checkin)

        # escribo el fichero Json con todos los datos
        return my_checkin.room_key

    def guest_checkout(self, room_key: str) -> bool:
        """manages the checkout of a guest"""
        RoomKey(room_key)
        # check that the roomkey is stored in the checkins file
        room_key_list = JsonStoreCheckOut().find_roomkey_checkout(JSON_FILES_PATH + "store_check_in.json")

        # comprobar que esa room_key es la que me han dado
        JsonStoreCheckOut().check_room_key(room_key, room_key_list)

        checkout_store = JsonStoreCheckOut()
        checkout_store.add_checkout({"room_key": room_key, "checkout_time": datetime.timestamp(datetime.utcnow())})
        return True
