import unittest
import json
from UC3MTravel import hotel_management_exception
from UC3MTravel.hotel_manager import Hotel_manager
from pathlib import Path


class Test_Room_reservation_tests(unittest.TestCase):

    def setUp(self):
        # Borramos cualquier reselva previa
        ReservaFile = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/hotel_reservation.json"
        dataOutput = []
        with open(ReservaFile, "w", encoding="utf", newline="") as file:
            json.dump(dataOutput, file, indent=2)

        # Creamos una reserva
        myReservation = Hotel_manager()
        value = myReservation.Room_reservation("5555555555554444", "Peter Anguila",
                                               "66664666V", "999991999",
                                               "single", "3", "20/10/2000")


    #----------INSERTION VALID----------
    def test_room_reservation(self):
        outputFile = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/hotel_reservation.json"
        dataOutput = []
        with open(outputFile, "w", encoding="utf", newline="") as file:
            json.dump(dataOutput, file, indent=2)
        myReservation = Hotel_manager()
        value = myReservation.Room_reservation("5555555555554444", "Peter Anguila",
                                "66664666V", "999991999",
                                "single", "3", "20/10/2000")

        self.assertEqual(value, "ce2f719f218227e41b9a9e6f3d12c962")

    #---------INSERTION NOT VALID-------------
    def test_room_reservation_not_valid(self):
        myReservation = Hotel_manager()
        value = myReservation.Room_reservation("5555555555554444", "Juan Ramon",
                                "66664666V", "999991999",
                                "single", "3", "20/10/2000")

        # Duplicamos para que salte el error de que la reserva ya está hecha

        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Room_reservation("5555555555554444", "Juan Ramon",
                                "66664666V", "999991999",
                                "single", "3", "20/10/2000")

        self.assertEqual(cm.exception.message, "El cliente ya tiene esta reserva")

    #------------CREDIT CARD VALID--------------
    def test_room_reservation_credit_card_valid_1(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_credit_card(CardNumber="5105105105105100")

        self.assertEqual(value, True)

    #------------CREDIT CARD NOT VALID--------------
    def test_room_reservation_credit_card_not_valid_1(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_credit_card(CardNumber="5555555555554445")

        self.assertEqual(cm.exception.message, "El número de la tarjeta es inválido")

    def test_room_reservation_credit_card_not_valid_2(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_credit_card(CardNumber="55555F558FEFD555")

        self.assertEqual(cm.exception.message, "El número de la tarjeta es inválido")

    def test_room_reservation_credit_card_not_valid_3(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_credit_card(CardNumber="55555555555555555")

        self.assertEqual(cm.exception.message, "La longitud de la tarjeta no es válido")

    def test_room_reservation_credit_card_not_valid_4(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_credit_card(CardNumber="555555555555555")

        self.assertEqual(cm.exception.message, "La longitud de la tarjeta no es válido")

    def test_room_reservation_credit_card_not_valid_5(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_credit_card(CardNumber="55555555555555555")

        self.assertEqual(cm.exception.message, "La longitud de la tarjeta no es válido")

    def test_room_reservation_credit_card_not_valid_6(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_credit_card(CardNumber="555555555555555")

        self.assertEqual(cm.exception.message, "La longitud de la tarjeta no es válido")

    #-----------NAME AND SURNAME VALID-------------
    def test_room_reservation_name_surname_valid_1(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_name(NameSurname="JOSELU LOPEZ")

        self.assertEqual(value, True)

    def test_room_reservation_name_surname_valid_2(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_name(NameSurname="JOSE LOPEZ")

        self.assertEqual(value, True)

    def test_room_reservation_name_surname_valid_3(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_name(
            NameSurname="Dimitrius johnson de las heras amor salson molina")

        self.assertEqual(value, True)

    #----------NAME AND SURNAME NOT VALID-----------
    def test_room_reservation_name_surname_not_valid_1(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_name(NameSurname="JOSE LOPEZ28")

        self.assertEqual(cm.exception.message, "El nombre es inválido")

    def test_room_reservation_name_surname_not_valid_2(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_name(NameSurname="JOSE LOP//EZ")

        self.assertEqual(cm.exception.message, "El nombre es inválido")

    def test_room_reservation_name_surname_not_valid_3(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_name(NameSurname="Pepe")

        self.assertEqual(cm.exception.message, "El nombre es inválido")

    def test_room_reservation_name_surname_not_valid_4(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_name(
                NameSurname="Demetrious johnson de las heras amores salsón molinas")

        self.assertEqual(cm.exception.message, "El nombre es inválido")

    def test_room_reservation_name_surname_not_valid_5(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_name(NameSurname="JOSE LOPE")

        self.assertEqual(cm.exception.message, "El nombre es inválido")
    def test_room_reservation_name_surname_not_valid_6(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_name(
                NameSurname="Demetrious johnson de las heras amor salsón molinasrtysrtysty")

        self.assertEqual(cm.exception.message, "El nombre es inválido")

    #----------ID CARD VALID-----------
    def test_room_reservation_id_card_valid_1(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_DNI(DNI="12345678Z")

        self.assertEqual(value, True)

    #--------ID CARD NOT VALID-------------
    def test_room_reservation_id_card_not_valid_1(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_DNI(DNI="123456789")

        self.assertEqual(cm.exception.message, "El DNI no es válido")

    def test_room_reservation_id_card_not_valid_2(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_DNI(DNI="1932L8992")

        self.assertEqual(cm.exception.message, "El DNI no es válido")

    def test_room_reservation_id_card_not_valid_3(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_DNI(DNI="1932L")

        self.assertEqual(cm.exception.message, "La longitud del DNI no es válida")

    def test_room_reservation_id_card_not_valid_4(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_DNI(DNI="1202138ASD32P")

        self.assertEqual(cm.exception.message, "La longitud del DNI no es válida")

    def test_room_reservation_id_card_not_valid_5(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_DNI(DNI="1234567PG")

        self.assertEqual(cm.exception.message, "El DNI no es válido")

    def test_room_reservation_id_card_not_valid_6(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_DNI(DNI="1234567D")

        self.assertEqual(cm.exception.message, "La longitud del DNI no es válida")

    def test_room_reservation_id_card_not_valid_7(self):
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation = Hotel_manager()
            myReservation.Validate_DNI(DNI="123456789H")

        self.assertEqual(cm.exception.message, "La longitud del DNI no es válida")

    #----------PHONE NUMBER VALID-----------
    def test_room_reservation_phone_number_valid_1(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_number(PhoneNumber="674828930")

        self.assertEqual(value, True)

    #---------PHONE NUMBER NOT VALID----------
    def test_room_reservation_phone_number_not_valid_1(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_number(PhoneNumber="555555")

        self.assertEqual(cm.exception.message, "La longitud del número no es correcta")

    def test_room_reservation_phone_number_not_valid_2(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_number(PhoneNumber="5F5F5F5F5")

        self.assertEqual(cm.exception.message, "El número no es válido")

    def test_room_reservation_phone_number_not_valid_3(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_number(PhoneNumber="99999999")

        self.assertEqual(cm.exception.message, "La longitud del número no es correcta")

    def test_room_reservation_phone_number_not_valid_4(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_number(PhoneNumber="9999999999")

        self.assertEqual(cm.exception.message, "La longitud del número no es correcta")

    def test_room_reservation_phone_number_not_valid_5(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_number(PhoneNumber="heloo world")

        self.assertEqual(cm.exception.message, "La longitud del número no es correcta")

    def test_room_reservation_phone_number_not_valid_6(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_number(PhoneNumber="91123456")

        self.assertEqual(cm.exception.message, "La longitud del número no es correcta")

    def test_room_reservation_phone_number_not_valid_7(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_number(PhoneNumber="9112345677")

        self.assertEqual(cm.exception.message, "La longitud del número no es correcta")

    # ----------ROOM TYPE VALID-----------
    def test_room_reservation_room_type_valid_1(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_room(RoomType="single")

        self.assertEqual(value, True)

    def test_room_reservation_room_type_valid_2(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_room(RoomType="double")

        self.assertEqual(value, True)

    def test_room_reservation_room_type_valid_3(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_room(RoomType="suite")

        self.assertEqual(value, True)

    # ----------ROOM TYPE NOT VALID-----------
    def test_room_reservation_room_type_not_valid_1(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_room(RoomType="cualquiera")

        self.assertEqual(cm.exception.message, "El tipo de habitacion no es válida")

    #-----------ARRIVAL DATE VALID-----------------
    def test_room_reservation_arrival_date_valid_1(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_date(Date="09/07/2024")

        self.assertEqual(value, True)

        # ----------ARRIVAL DATE NOT VALID-----------
    def test_room_reservation_arrival_date_not_valid_1(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_date("as/fg/jklñ")

        self.assertEqual(cm.exception.message, "Fecha incorrecta")

    def test_room_reservation_arrival_date_not_valid_2(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_date("1416102024")

        self.assertEqual(cm.exception.message, "Fecha incorrecta")

    # ----------NUMDAYS VALID-----------
    def test_room_reservation_num_days_valid_1(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_numdays(NumDays=8)

        self.assertEqual(value, True)

    def test_room_reservation_num_days_valid_2(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_numdays(NumDays=10)

        self.assertEqual(value, True)

    def test_room_reservation_num_days_valid_3(self):
        myReservation = Hotel_manager()
        value = myReservation.Validate_numdays(NumDays=1)

        self.assertEqual(value, True)

    # ----------NUMDAYS NOT VALID-----------
    def test_room_reservation_num_days_not_valid_1(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_numdays("hola")

        self.assertEqual(cm.exception.message, "El número de días no es válido")

    def test_room_reservation_num_days_not_valid_2(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_numdays(-10)

        self.assertEqual(cm.exception.message, "El número de días no es válido")

    def test_room_reservation_num_days_not_valid_3(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_numdays(18)

        self.assertEqual(cm.exception.message, "El número de días no es válido")

    def test_room_reservation_num_days_not_valid_4(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_numdays(0)

        self.assertEqual(cm.exception.message, "El número de días no es válido")

    def test_room_reservation_num_days_not_valid_5(self):
        myReservation = Hotel_manager()
        with self.assertRaises(hotel_management_exception.Hotel_management_exception) as cm:
            myReservation.Validate_numdays(11)

        self.assertEqual(cm.exception.message, "El número de días no es válido")
