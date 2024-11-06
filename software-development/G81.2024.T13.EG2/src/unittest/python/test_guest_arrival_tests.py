import unittest
import json
from pathlib import Path
#from UC3MTravel.hotel_management_exception import Hotel_management_exception
from UC3MTravel import hotel_management_exception
from UC3MTravel.hotel_manager import Hotel_manager
from freezegun import freeze_time


class Test_guest_arrival_tests(unittest.TestCase):
    def setUp(self):
        # Nos aseguramos que está vacio
        reservas = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/hotel_reservation.json"
        reservasOutput = []
        with open(reservas, "w", encoding="utf", newline="") as file1:
            json.dump(reservasOutput, file1, indent=2)

        # Borramos el output
        outputFile = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/hotel_stay.json"
        dataOutput = []
        with open(outputFile, "w", encoding="utf", newline="") as file2:
            json.dump(dataOutput, file2, indent=2)

        # Hacemos una reserva
        myReservation = Hotel_manager()
        myReservation.Room_reservation("5555555555554444", "Peter Anguila",
                                               "66664666V", "999991999",
                                               "single", "3", "20/10/2000")

    # -------VALID TEST-----------
    @freeze_time("20/10/2000")
    def test_guest_arrival_valid_1(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input25.json"
        Reserva = Hotel_manager()

        Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(Room_key, "8da6b3518ee23f7cc189cf86fc20e67ede88a4a41acee0b2c5ab9793ede19088")

    # ---------NOT VALID------------
    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_1(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input1.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_2(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input2.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_3(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input25.json"
        Reserva = Hotel_manager()

        Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(Room_key, "8da6b3518ee23f7cc189cf86fc20e67ede88a4a41acee0b2c5ab9793ede19088")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_4(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input4.json"
        Reserva = Hotel_manager()

        with self.assertRaises(KeyError):
            Reserva.guest_arrival(inputFilePath)

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_5(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input5.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_6(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input6.json"
        Reserva = Hotel_manager()

        with self.assertRaises(KeyError):
            Reserva.guest_arrival(inputFilePath)

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_7(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input7.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_8(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input8.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_9(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input9.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_10(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input10.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_11(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input11.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_12(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input12.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_13(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input13.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_14(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input14.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_15(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input15.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_16(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input16.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El archivo no tiene formato JSON")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_17(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input17.json"
        Reserva = Hotel_manager()

        with self.assertRaises(KeyError):
            Reserva.guest_arrival(inputFilePath)

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_18(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input18.json"
        Reserva = Hotel_manager()

        with self.assertRaises(KeyError):
            Reserva.guest_arrival(inputFilePath)

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_19(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input19.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El localizador no es valido")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_20(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input20.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El localizador no es valido")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_21(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input21.json"
        Reserva = Hotel_manager()

        with self.assertRaises(KeyError):
            Reserva.guest_arrival(inputFilePath)

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_22(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input22.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El código de habitación no es válido")

    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_23(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input23.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El código de habitación no es válido")


    @freeze_time("20/10/2000")
    def test_guest_arrival_not_valid_24(self):
        inputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/RF2/input24.json"
        Reserva = Hotel_manager()

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            Room_key = Reserva.guest_arrival(inputFilePath)

        self.assertEqual(cm.exception.message, "El DNI no es válido")
