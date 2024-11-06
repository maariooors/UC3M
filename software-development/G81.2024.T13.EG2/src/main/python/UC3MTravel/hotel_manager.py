import json
import string
from json import JSONDecodeError
from pathlib import Path
import datetime
from UC3MTravel.hotel_management_exception import Hotel_management_exception
from UC3MTravel.hotel_reservation import HotelReservation
from UC3MTravel.hotel_stay import HotelStay



class Hotel_manager:
    """Class Hotel_Manager"""

    def __init__(self):
        pass

    def Validate_credit_card(self, CardNumber: str):
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        if len(CardNumber) != 16:
            raise (Hotel_management_exception
                   ("La longitud de la tarjeta no es válido"))
        modify = CardNumber
        for i in range(len(CardNumber) - 2, -1, -2):
            try:
                a = int(CardNumber[i]) * 2
            except ValueError as ex:
                raise Hotel_management_exception("El número de la tarjeta es inválido") from ex

            modify = modify[:i] + str(a) + modify[(i + 1):]

        sumador = 0
        for i in range(0, len(modify) - 1):
            sumador += int(modify[i])

        ultimoNumero = (sumador * 9) % 10
        if ultimoNumero != int(CardNumber[-1]):
            raise (Hotel_management_exception
                   ("El número de la tarjeta es inválido"))

        return True

    def Validate_name(self, NameSurname: str):
        if 10 > len(NameSurname) or len(NameSurname) > 50:  # Si la longitud no es corecta
            raise Hotel_management_exception("El nombre es inválido")
        for _, char in enumerate(NameSurname):
            if char not in string.ascii_letters and char != " ":
                raise Hotel_management_exception("El nombre es inválido")
        return True

    def Validate_DNI(self, DNI: str):
        """Para comprobar que el DNI es valido evaluamos los primeros
        8 dígitos del DNI y los convertimos a número, si la conversión sale bien
        evaluaremos el último dígito para ver si es una letra. En caso
        de que alguna de estas dos pruebas falle, invocaremos un error"""
        if len(DNI) != 9:
            raise Hotel_management_exception("La longitud del DNI no es válida")

        try:
            int(DNI[:8])
        except ValueError as ex:
            raise Hotel_management_exception("El DNI no es válido") from ex

        # Si el siguiente código da error significa que el último caracter del DNI es una letra

        if DNI[-1] not in string.ascii_letters:
            raise Hotel_management_exception("El DNI no es válido")

        return True

    def Validate_number(self, PhoneNumber: str):

        if len(PhoneNumber) != 9:
            raise Hotel_management_exception("La longitud del número no es correcta")

        try:
            int(PhoneNumber)
        except ValueError as ex:
            raise Hotel_management_exception("El número no es válido") from ex
        return True

    def Validate_room(self, RoomType: str):
        rooms = ["single", "double", "suite"]

        if RoomType.lower() not in rooms:
            raise Hotel_management_exception("El tipo de habitacion no es válida")

        return True

    def Validate_date(self, Date: str):
        numbers = "0123456789"
        if len(Date) != 10:
            raise Hotel_management_exception("Fecha incorrecta")
        for i, char in enumerate(Date):

            if i in (2, 5):
                if char != "/":
                    raise Hotel_management_exception("Fecha incorrecta")

            else:
                if char not in numbers:
                    raise Hotel_management_exception("Fecha incorrecta")
        return True

    def Validate_numdays(self, NumDays: str):
        try:
            a = int(NumDays)
        except ValueError as ex:
            raise Hotel_management_exception("El número de días no es válido") from ex
        if a < 1 or a > 10:
            raise Hotel_management_exception("El número de días no es válido")
        return True

    def Room_reservation(self, CreditCard: str, NameSurname: str, IdCard: str,
                         PhoneNumber: str, RoomType: str, NumDays: str, ArrivalDate: str):

        self.Validate_credit_card(CreditCard)  # Comprobamos si la tarjeta es válida
        self.Validate_name(NameSurname)  # Comprobamos si el nombre es valido
        self.Validate_DNI(IdCard)  # Comprobamos si en DNI es válido
        self.Validate_number(PhoneNumber)  # Comprobamos si el número es válido
        self.Validate_room(RoomType)  # Comprobamos si el tipo de habitación es valida
        self.Validate_date(ArrivalDate)  # Comprobamos si la fecha es válida
        self.Validate_numdays(NumDays)

        reservation = HotelReservation(IdCard, CreditCard, NameSurname,
                                       PhoneNumber, RoomType, NumDays, ArrivalDate)

        # Llamo la ruta del fichero almacén, donde almacenaremos todas las reservas

        localizer = reservation.localizer # Me guardo el localizer

        jsonFilesPath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/"
        fileStore = jsonFilesPath + "hotel_reservation.json"
        # print(fileStore)

        # Comprobamos que dicho fichero existe
        try:
            with open(fileStore, "r", encoding="utf-8", newline="") as file:
                dataList = json.load(file)
        except FileNotFoundError:
            dataList = []
        except json.JSONDecodeError as ex:
            raise Hotel_management_exception("JSON Decode Error - Wrong JSON Format") from ex

        # Escribir datos en el JSON

        try:
            with open(fileStore, "w", encoding="utf", newline="") as file:
                found = False
                for _, data in enumerate(dataList):
                    info = data['_HotelReservation__localizer']
                    if info == reservation.localizer:
                        found = True
                        break
                if not found:
                    dataList.append(reservation.__dict__)
                    json.dump(dataList, file, indent=2)

                else:
                    json.dump(dataList, file, indent=2)
                    raise Hotel_management_exception("El cliente ya tiene esta reserva")


        except FileNotFoundError as ex:
            raise Hotel_management_exception("Wrong file or file path") from ex

        # Si ha llegado aquí habrá ido bien
        return localizer

    def guest_arrival(self, InputFile: str):
        jsonFilesPath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/"
        fileStore = jsonFilesPath + "hotel_reservation.json"

        # Comprobamos que la estructura del JSON es correcta

        try:
            with open(InputFile, "r", encoding="utf", newline="") as file1:
                try:
                    dataList1 = json.load(file1)
                except JSONDecodeError as ex:
                    raise Hotel_management_exception("El archivo no tiene "
                                                     "formato JSON") from ex

                for _, data1 in enumerate(dataList1):
                    info1 = data1['Localizer']
                    if len(info1) != 32: #Si la longitud no es de 32
                        raise Hotel_management_exception("El localizador no es valido")

                    for _, char in enumerate(info1):
                        if char not in string.hexdigits:
                            # Si no tiene todos sus valores hexadecimales
                            raise Hotel_management_exception("El código de habitación "
                                                             "no es válido")

                    info2 = data1['IdCard']
                    # Validamos el DNI
                    self.Validate_DNI(info2)

        except FileNotFoundError as ex2:
            raise Hotel_management_exception("Wrong file or file path") from ex2

        # Miramos si el Guest tiene reserva, y si no se han modificado datos por el camino
        try:
            with open(InputFile, "r", encoding="utf", newline="") as file1:
                dataList1 = json.load(file1)
            with open(fileStore, "r", encoding="utf", newline="") as file2:
                dataList2 = json.load(file2)

            found = False
            for _, data1 in enumerate(dataList1):
                info1Localizer = data1['Localizer']
                info1IdCard = data1['IdCard']
                for _, data2 in enumerate(dataList2):
                    info2Localizer = data2['_HotelReservation__localizer']
                    info2IdCard = data2['_HotelReservation__idcard']

                    # Generamos una nueva reserva temporal para ver si coincide los localizer
                    # y así determinal si se han modificado valores por el camino

                    if (info1Localizer == info2Localizer) and (info1IdCard == info2IdCard):
                        new = HotelReservation(data2["_HotelReservation__idcard"],
                                               data2["_HotelReservation__creditcardnumber"],
                                               data2["_HotelReservation__name_surmane"],
                                               data2["_HotelReservation__phonenumber"],
                                               data2["_HotelReservation__roomtype"],
                                               data2["_HotelReservation__num_days"],
                                               data2["_HotelReservation__arrival_date"])
                        # Insertamos la nueva información
                        if info1Localizer == new.localizer:
                            # Si los localizer coinciden, insertamos la nueva información
                            found = True

                            # Comprobamos las fechas

                            fechaLlegadaJson = data2["_HotelReservation__arrival_date"]
                            fecha = datetime.datetime.today().date()
                            # En los unittest se fijará a una en concreto
                            fechaLlegada = fecha.strftime("%d/%m/%Y")

                            if not fechaLlegadaJson == fechaLlegada:
                                raise Hotel_management_exception("La fecha de llegada "
                                                                 "no se corresponde")

                            # Insertamos toda la nueva información

                            estancia = HotelStay(data2["_HotelReservation__idcard"],
                                                 data2["_HotelReservation__localizer"],
                                                 data2["_HotelReservation__num_days"],
                                                 data2["_HotelReservation__roomtype"])

                            # Me guardo la roomKey generada para evitar insertar duplicados
                            roomKey = estancia.room_key

                            outputFilePath = (str(Path.home()) + "/PycharmProjects/"
                                                                 "G81.2024.T13.EG2/src/"
                                                                 "JsonFiles/")
                            outputFile = outputFilePath + "hotel_stay.json"
                            # Comprobamos que dicho fichero existe
                            try:
                                with open(outputFile, "r", encoding="utf-8", newline="") as a:
                                    dataOutput = json.load(a)
                            except FileNotFoundError:
                                dataOutput = []
                            except json.JSONDecodeError as ex:
                                raise Hotel_management_exception("JSON Decode Error "
                                                                 "- Wrong JSON Format") from ex

                            # Escribir datos en el JSON

                            try:
                                with open(outputFile, "w", encoding="utf", newline="") as file:
                                    # Comprobamos que las roomKey no están duplicadas
                                    found1 = False
                                    for _, data in enumerate(dataOutput):
                                        info = data["_HotelStay__room_key"]
                                        if info == roomKey:
                                            found1 = True
                                            break
                                    if not found1:
                                        dataOutput.append(estancia.__dict__)
                                        json.dump(dataOutput, file, indent=2)
                                    else:
                                        json.dump(dataOutput, file, indent=2)
                                        raise Hotel_management_exception(
                                            "La roomKey ya estaba generada")

                            except FileNotFoundError as ex:
                                raise Hotel_management_exception(
                                    "Wrong file or file path") from ex
                        else:
                            raise Hotel_management_exception(
                                "Los datos de la reserva han sido modificados")

                if not found:
                    raise Hotel_management_exception("No existe la reserva")

                # Si ha llegado aquí habrá ido bien
                return roomKey
        except FileNotFoundError as ex:
            raise Hotel_management_exception("Wrong file or file path") from ex


    def guest_checkout(self, RoomKey: str):

        if not isinstance(RoomKey, str):
            raise Hotel_management_exception("La cadena de entrada no contiene un\
                                             código de habitación que pueda procesarse.")
        if len(RoomKey) != 64:  # Si la longitud no es de 64
            raise Hotel_management_exception("El código de habitación no es válido.")

        for _, char in enumerate(RoomKey):
            if char not in string.hexdigits:
                # Si no tiene todos sus valores hexadecimales
                raise Hotel_management_exception("El código de habitación no es válido.")

        jsonFilesPath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/"
        fileStay = jsonFilesPath + "hotel_stay.json"

        # abro el almacén de estancias
        try:
            with open(fileStay, "r", encoding="utf", newline="") as file:
                try:
                    dataList = json.load(file)
                except JSONDecodeError as ex1:
                    raise Hotel_management_exception(
                        "Error de procesamiento interno al procesar el código ") from ex1

        except FileNotFoundError as ex2:
            raise Hotel_management_exception(
                "Error de procesamiento interno al procesar el código.") from ex2

        # busco la clave introducida iterando en el almacén
        found = False
        for _, data in enumerate(dataList):
            if RoomKey == data['_HotelStay__room_key']:
                found = True
                fechaPrevista = data['_HotelStay__departure']
                # si la fecha de salida del almacén no corresponde con la fecha actual, error
                if fechaPrevista != datetime.datetime.timestamp(datetime.datetime.utcnow()):
                    raise Hotel_management_exception("La fecha de salida no es válida.")
                checkout = {"room_key": data['_HotelStay__room_key'],
                            "fecha_checkout": fechaPrevista}
                break
        if not found:
            raise Hotel_management_exception("El código de habitación no estaba registrado.")

        outputFilePath = str(Path.home()) + "/PycharmProjects/G81.2024.T13.EG2/src/JsonFiles/"
        outputFile = outputFilePath + "check_out.json"

        try:
            with open(outputFile, "r", encoding="utf-8", newline="") as output:
                dataOutput = json.load(output)
        except FileNotFoundError:
            dataOutput = []
        except json.JSONDecodeError as ex:
            raise Hotel_management_exception(
                "Error de procesamiento interno al procesar el código.") from ex

        try:
            with open(outputFile, "w", encoding="utf", newline="") as file:
                # Comprobamos que no está repetido el checkout
                found1 = False
                for _, data in enumerate(dataOutput):
                    info = data['room_key']
                    if info == RoomKey:
                        found1 = True
                        break

                # si no lo encontramos añadimos la nueva salida
                if not found1:
                    dataOutput.append(checkout)
                    json.dump(dataOutput, file, indent=2)
                else:
                    json.dump(dataOutput, file, indent=2)
                    raise Hotel_management_exception("La salida ya estaba registrada.")

        except FileNotFoundError as ex:
            raise Hotel_management_exception(
                "Error de procesamiento interno al procesar el código.") from ex

        return True

    def ReaddatafromJSON(self, Fi):

        try:
            with open(Fi, encoding="utf-8") as f:
                # with open(Fi) as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise Hotel_management_exception("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise (Hotel_management_exception
                   ("JSON Decode Error - Wrong JSON Format")) from e

        try:
            c = data["CreditCard"]
            p = data["phoneNumber"]
            req = HotelReservation(IdCard="12345678Z", CreditCardNumb=c,
                                   NameAndSurname="John Doe", PhoneNumber=p,
                                   RoomType="single", NumDays=3, ArrivalDate="01/01/1999")
        except KeyError as e:
            raise (Hotel_management_exception
                   ("JSON Decode Error - Invalid JSON Key")) from e
        if not self.Validate_credit_card(c):
            raise Hotel_management_exception("Invalid credit card number")

        # Close the file
        return req
