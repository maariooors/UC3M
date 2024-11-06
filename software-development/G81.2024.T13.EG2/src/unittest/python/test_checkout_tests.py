import unittest
from UC3MTravel import hotel_management_exception
from UC3MTravel.hotel_manager import Hotel_manager
from freezegun import freeze_time
from pathlib import Path
import json
import os


class Test_checkout_tests(unittest.TestCase):

    def setUp(self):
        # Nos aseguramos que está vacio
        reservas = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/hotel_reservation.json"
        reservasOutput = []
        with open(reservas, "w", encoding="utf", newline="") as file1:
            json.dump(reservasOutput, file1, indent=2)

        # Borramos el output
        output = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/hotel_stay.json"
        dataOutput = []
        with open(output, "w", encoding="utf", newline="") as file2:
            json.dump(dataOutput, file2, indent=2)

        output = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/hotel_stay.json"
        dataOutput = []
        with open(output, "w", encoding="utf", newline="") as file2:
            json.dump(dataOutput, file2, indent=2)


    # Crea el JSON de salida
    @freeze_time("20/10/2000")
    def test_guest_checkout_valid_1(self):
        myReservation = Hotel_manager()
        ID = "12345678L"
        localizer = myReservation.Room_reservation("5555555555224444", "Peter Anguila",
                                               ID, "999991999",
                                               "single", "3", "20/10/2000")

        jsonFiles = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/"
        inputFilePath = jsonFiles + "input.json"

        data = [{"Localizer": localizer, "IdCard": ID}]

        with open(inputFilePath, "w", encoding="utf-8", newline="") as b:
            json.dump(data, b, indent=2)

        room_key = myReservation.guest_arrival(inputFilePath)
        if os.path.exists(jsonFiles + "check_out.json"):
            os.remove(jsonFiles + "check_out.json")
        with freeze_time("23/10/2000"):
            result = myReservation.guest_checkout(room_key)

        self.assertEqual(result, True)

    # Normal
    @freeze_time("20/10/2000")
    def test_guest_checkout_valid_2(self):
        myReservation = Hotel_manager()
        ID = "12345673L"
        localizer = myReservation.Room_reservation("5555555555224444", "Peter Anguila",
                                               ID, "999991999",
                                               "single", "3", "20/10/2000")

        jsonFiles = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/"
        inputFilePath = jsonFiles + "input.json"

        data = [{"Localizer": localizer, "IdCard": ID}]

        with open(inputFilePath, "w", encoding="utf-8", newline="") as b:
            json.dump(data, b, indent=2)

        room_key = myReservation.guest_arrival(inputFilePath)

        with freeze_time("23/10/2000"):
            result = myReservation.guest_checkout(room_key)

        self.assertEqual(result, True)

    # Almacén con una única entrada
    @freeze_time("20/10/2000")
    def test_guest_checkout_valid_3(self):
        myReservation = Hotel_manager()
        ID = "23181902K"
        localizer = myReservation.Room_reservation("5555555555224444", "Iker Casillas el del Madrid",
                                                   ID, "123456789",
                                                   "double", "3", "20/10/2000")

        jsonFiles = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/"
        inputFilePath = jsonFiles + "input.json"
        hotelStayPath = jsonFiles + "hotel_stay.json"

        data = [{"Localizer": localizer, "IdCard": ID}]

        with open(inputFilePath, "w", encoding="utf-8", newline="") as b:
            json.dump(data, b, indent=2)

        data_stay = []

        with open(hotelStayPath, "w", encoding="utf-8", newline="") as b:
            json.dump(data_stay, b, indent=2)

        room_key = myReservation.guest_arrival(inputFilePath)

        with freeze_time("23/10/2000"):
            result = myReservation.guest_checkout(room_key)

        self.assertEqual(result, True)

    # Fecha incorrecta
    @freeze_time("20/10/2000")
    def test_guest_checkout_not_valid_1(self):
        myReservation = Hotel_manager()
        ID = "12345291j"
        localizer = myReservation.Room_reservation("5555555555224444", "Pablo Picapiedra",
                                               ID, "820173849",
                                               "double", "2", "20/10/2000")

        jsonFiles = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/"
        inputFilePath = jsonFiles + "input.json"

        data = [{"Localizer": localizer, "IdCard": ID}]

        with open(inputFilePath, "w", encoding="utf-8", newline="") as b:
            json.dump(data, b, indent=2)

        room_key = myReservation.guest_arrival(inputFilePath)

        with freeze_time("23/10/2000"): # Debería ser el 22
            with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
                myReservation.guest_checkout(room_key)

        self.assertEqual(cm.exception.message, "La fecha de salida no es válida.")

    # No str
    @freeze_time("20/10/2000")
    def test_guest_checkout_not_valid_2(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.guest_checkout(8923618936183671982739812379812379812371298)

        self.assertEqual(cm.exception.message, "La cadena de entrada no contiene un\
                                             código de habitación que pueda procesarse.")


    # No len(room_key) == 64
    @freeze_time("20/10/2000")
    def test_guest_checkout_not_valid_3(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.guest_checkout("a6b362d")

        self.assertEqual(cm.exception.message, "El código de habitación no es válido.")

    # No hexadecimal
    @freeze_time("20/10/2000")
    def test_guest_checkout_not_valid_4(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.guest_checkout("ZZZZZb537c18e2d5a49e7346b8021fca33b1d9c0c8dafe9a3b9b485a57dbed95")

        self.assertEqual(cm.exception.message, "El código de habitación no es válido.")

    # room_key que no está en el almacén
    @freeze_time("20/10/2000")
    def test_guest_checkout_not_valid_5(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.guest_checkout("9fcdbb537c18e2d5a49e7346b8021fca33b1d9c0c8dafe9a3b9b485a57dbed95")

        self.assertEqual(cm.exception.message, "El código de habitación no estaba registrado.")

    # Salida ya registrada
    @freeze_time("20/10/2000")
    def test_guest_checkout_not_valid_6(self):
        myReservation = Hotel_manager()
        ID = "77777777C"
        localizer = myReservation.Room_reservation("5555555555224444", "Cristiano Ronaldo",
                                                   ID, "666666666",
                                                   "double", "9", "20/10/2000")

        jsonFiles = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/"
        inputFilePath = jsonFiles + "input.json"

        data = [{"Localizer": localizer, "IdCard": ID}]

        with open(inputFilePath, "w", encoding="utf-8", newline="") as b:
            json.dump(data, b, indent=2)

        room_key = myReservation.guest_arrival(inputFilePath)

        with freeze_time("29/10/2000"):
            myReservation.guest_checkout(room_key)
            with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
                myReservation.guest_checkout(room_key)

        self.assertEqual(cm.exception.message, "La salida ya estaba registrada.")

    # Almacén vacío
    @freeze_time("20/10/2000")
    def test_guest_checkout_not_valid_7(self):

        myReservation = Hotel_manager()
        jsonFiles = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/"
        hotelStayPath = jsonFiles + "hotel_stay.json"

        data = []

        with open(hotelStayPath, "w", encoding="utf-8", newline="") as b:
            json.dump(data, b, indent=2)

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.guest_checkout("9fcdbb537c18e2d5a49e7346b8021fca33b1d9c0c8dafe9a3b9b485a57dbed95")

        self.assertEqual(cm.exception.message, "El código de habitación no estaba registrado.")








