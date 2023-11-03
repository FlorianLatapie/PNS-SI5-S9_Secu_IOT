import pretty_errors

from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import NoCardException

APPLET_AID_PREFIX = [0xa0, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46]  # APPLET AID PREFIX in Common.properties L 24
APPLET_AID = APPLET_AID_PREFIX + [0x10, 0x01]  # l 13 in build.xml
PACKAGE_AID = APPLET_AID_PREFIX + [0x10]  # l 14 in build.xml


def is_success(sw1, sw2):
    success = (sw1 == 0x90 and sw2 == 0x00)

    if not success:
        print("sw1 : ", hex(sw1))
        print("sw2 : ", hex(sw2))
    
    return success


def init_card():
    if not readers():
        print("No readers")
        exit()

    for reader in readers():
        try:
            connection = reader.createConnection()
            connection.connect()
            print(reader)
            print("ATR :", toHexString(connection.getATR()))

            # define the apdus used in this script

            # Defined in the doc : here https://www.infoworld.com/article/2076450/how-to-write-a-java-card-applet--a-developer-s-guide.html?page=2
            CLA = 0x00
            INS = 0xa4
            P1 = 0x04
            P2 = 0x00
            data = APPLET_AID
            Lc = len(data)
            apdu = [CLA, INS, P1, P2, Lc] + data

            # Select application
            print("apdu : ", apdu)
            response, sw1, sw2 = connection.transmit(apdu)

            print('response : ', response)
            print('sw1 : ', sw1, "hex", hex(sw1))
            print('sw2 : ', sw2, "hex", hex(sw2))

            # there APDU SELECTED
            if is_success(sw1, sw2):
                print("application selected")
                return connection
            else:
                print('no application selected')
                return


        except NoCardException:
            print("No card in reader")
            exit()


def change_pin(connection):
    # APDU : Modification de code PIN
    CLA = 0x00
    P1 = 0x00
    P2 = 0x00
    INS = 0x02 # j'ai modifié ici 

    data = [0x01, 0x01, 0x01, 0x01]
    Lc = len(data)
    apdu = [CLA, INS, P1, P2, Lc] + data
    response, sw1, sw2 = connection.transmit(apdu)

    print(response)

    if is_success(sw1, sw2):
        print("Code successfully changed")
    else:
        print("Error code not changed")

def main() -> int:
    print("coucou")
    connection = init_card()

    change_pin(connection)
    return 0


if __name__ == '__main__':
    main()
