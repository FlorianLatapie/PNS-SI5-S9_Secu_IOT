from typing import Any

import pretty_errors

from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import NoCardException

from card_utils import *
from card_config import *

verbose = False


def apdu_select_applet(applet_aid: str) -> list:
    # Defined in the doc : here https://www.infoworld.com/article/2076450/how-to-write-a-java-card-applet--a-developer-s-guide.html?page=2
    CLA = 0x00
    INS = 0xa4
    P1 = 0x04
    P2 = 0x00
    Data_field = applet_aid
    Lc = len(Data_field)  # length of Data_field
    return [CLA, INS, P1, P2, Lc] + Data_field  # append Data_field to the list


def get_card_connection() -> Card | None:
    if not readers():
        print("No readers")
        return None

    for reader in readers():
        try:
            connection = reader.createConnection()
            connection.connect()

            if verbose:
                print(reader)
                print("ATR :", toHexString(connection.getATR()))

            apdu = apdu_select_applet(APPLET_AID)
            response, sw1, sw2 = connection.transmit(apdu)

            return Card(connection) if is_success(sw1, sw2) else None

        except NoCardException:
            print("No card in reader")
            return None


def main() -> int:
    print("main")

    print("\n--> connecting to the card ... -------------------------------------------")
    card = get_card_connection()

    if not card:
        print("init card failed")
        return 1
    else:
        print("init card success")

    # test debug infos
    print("\n--> test debug infos -----------------------------------------------------")
    card.debug()

    # test login + change pin
    print("\n--> test login + change pin ----------------------------------------------")
    card.login("1234")
    card.change_pin("1111")
    card.login("1111")

    # test factory reset
    print("\n--> test factory reset ---------------------------------------------------")
    card.factory_reset()
    card.login("1234")

    # test sign
    print("\n--> test sign ------------------------------------------------------------")
    card.sign("please sign me !")

    # test get public key
    print("\n--> test get public key --------------------------------------------------")
    card.get_public_key()

    return 0


if __name__ == '__main__':
    main()
