from typing import Optional

import pretty_errors

from smartcard.System import readers
from smartcard.Exceptions import NoCardException

from card_utils import *
from card_config import *

verbose = False


def get_card_connection() -> Optional[Card]:
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

            card = Card(connection)

            response, sw1, sw2 = card.send_command(apdu_select_applet(APPLET_AID))

            return card if is_success(sw1, sw2) else None

        except NoCardException:
            print("No card in reader")
            return None
    """
    card_type = AnyCardType()
    card_request = CardRequest(timeout=1, cardType=card_type)
    card_service = card_request.waitforcard()

    card_service.connection.connect()
    card = Card(card_service.connection)

    response, sw1, sw2 = card.send_command(apdu_select_applet(APPLET_AID))
    card.debug()

    return card
    """


def main() -> int:
    print("main")

    print("\n--> connecting to the card ... -------------------------------------------")
    card = get_card_connection()

    if not card:
        print("init card failed")
        return 1

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
