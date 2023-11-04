from smartcard.util import toHexString

from card_config import *
from scrape_eftlab import get_sw_description


def is_success(sw1, sw2):
    success = (sw1 == 0x90 and sw2 == 0x00)

    if not success:
        import inspect
        import os
        file_path = inspect.stack()[1].filename
        file_name = os.path.basename(file_path)
        caller = inspect.stack()[1].function
        line_no = inspect.stack()[1].lineno
        print(f"Error from file {file_name} in function \"{caller}\" at line {line_no}")
        print(get_sw_description(sw1, sw2))

    return success


def command(auth=False):
    def decorator(func):
        func.is_command = True
        func.requires_auth = auth
        return func

    return decorator


class APDU:
    def __init__(self, cla, ins, p1, p2, data=None, receive_length=0):
        self.cla = cla
        self.ins = ins
        self.p1 = p1
        self.p2 = p2

        # if type(data) == int:
        if data is int:
            data = [data]
        # check if data is a list of int or int
        if data and not all(isinstance(x, int) for x in data):
            raise ValueError("data must be a list of numbers (int, hex) or a single number (int, hex)")

        if data:
            self.data = data
            self.lc = len(data)
        else:
            self.receive_length = receive_length

    def get_apdu(self):
        if hasattr(self, 'data'):
            return [self.cla, self.ins, self.p1, self.p2, self.lc] + self.data
        else:
            return [self.cla, self.ins, self.p1, self.p2, self.receive_length]

    def __str__(self):
        return self.get_apdu().__str__()


def apdu_select_applet(applet_aid: str) -> APDU:
    # Defined in the doc here :
    # https://www.infoworld.com/article/2076450/how-to-write-a-java-card-applet--a-developer-s-guide.html?page=2
    return APDU(0x00, 0xa4, 0x04, 0x00, applet_aid)


class Card:
    def __init__(self, connection):
        self.connection = connection

    def send_command(self, apdu: APDU):
        response, sw1, sw2 = self.connection.transmit(apdu.get_apdu())

        if sw1 == SW1_RETRY_WITH_LE:
            return self.send_command(
                APDU(apdu.cla, apdu.ins, apdu.p1, apdu.p2, receive_length=sw2)
            )
        if sw1 == SW1_RETRY_WITH_GET_RESPONSE_61 or sw1 == SW1_RETRY_WITH_GET_RESPONSE_9F:
            # if it does not work use 0xa0 for CLA (first applet AID prefix)
            return self.send_command(
                APDU(apdu.cla, INS_GET_RESPONSE, apdu.p1, apdu.p2, receive_length=sw2)
            )
        return response, sw1, sw2

    @command()
    def debug(self) -> bytes:
        print("Debug")
        apdu = APDU(APPLET_CLA, INS_DEBUG, 0, 0)
        response, sw1, sw2 = self.send_command(apdu)

        if is_success(sw1, sw2):
            print("Debug yes !")
            print("Debug :", toHexString(response))
            print(bytes(response))
        else:
            print("Debug no !")

        return response

    @command(auth=True)
    def change_pin(self, new_pin: str) -> bool:
        if len(new_pin) != PIN_LENGTH:
            print("Pin must be 4 digits")
            return False

        # byte array of the new pin
        data = [int(c) for c in new_pin]

        response, sw1, sw2 = self.send_command(APDU(APPLET_CLA, INS_MODIFY_PIN, 0, 0, data))

        success = is_success(sw1, sw2)
        print("Code successfully changed") if success else print("Error code not changed")
        return success

    @command()
    def login(self, pin: str) -> bool:

        if len(pin) != PIN_LENGTH:
            print("Pin must be 4 digits")
            return False

        # byte array of the pin
        data = [int(c) for c in pin]

        response, sw1, sw2 = self.send_command(APDU(APPLET_CLA, INS_LOGIN, 0, 0, data))

        success = is_success(sw1, sw2)
        print("Successfully logged in") if success else print("Error logging in")
        return success

    @command(auth=True)
    def sign(self, message: str) -> bytes:
        # byte array of the message
        data = [ord(c) for c in message]

        response, sw1, sw2 = self.send_command(APDU(APPLET_CLA, INS_SIGN_MESSAGE, 0, 0, data))

        if is_success(sw1, sw2):
            print("Successfully signed message")
            print("Signature :", toHexString(response))
            print("Signature :", bytes(response))
        else:
            print("Error signing message")

        return response

    @command()
    def factory_reset(self) -> bool:
        response, sw1, sw2 = self.send_command(APDU(APPLET_CLA, INS_FACTORY_RESET, 0, 0))

        success = is_success(sw1, sw2)
        print("Factory reset successful") if success else print("Error factory reset")
        return success

    @command()
    def get_public_key(self) -> bytes:
        response, sw1, sw2 = self.send_command(APDU(APPLET_CLA, INS_SEND_PUBLIC_KEY, 0, 0))

        if is_success(sw1, sw2):
            print("Successfully got public key")
            print("Public key :", toHexString(response))
            print("Public key :", bytes(response))
        else:
            print("Error getting public key")

        return response
