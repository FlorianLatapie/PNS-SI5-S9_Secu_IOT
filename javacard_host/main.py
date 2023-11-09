import hashlib

import pretty_errors

from card_utils import get_card_connection, Card
import rsa

def get_card_or_exit() -> Card:
    card = get_card_connection()
    if not card:
        print("init card failed")
        exit(1)
    print("init card success")
    return card

def main() -> int:
    print("main")

    print("\n--> connecting to the card ... -------------------------------------------")
    card = get_card_or_exit()
    """
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
    """

    card.login("1234")

    # test sign
    print("\n--> test sign ------------------------------------------------------------")
    text = "please sign me !"
    signature = card.sign(text)

    # test get public key
    print("\n--> test get public key --------------------------------------------------")
    public_key = card.get_public_key() # returns exponent and modulus
    print(public_key)

    # test verify signature
    print("\n--> test verify signature ------------------------------------------------")

    rsa_pkey = rsa.PublicKey(*public_key[::-1])
    try:
        my_message = text.encode("utf-8")
        rsa.verify(my_message, signature, rsa_pkey)
        print("Signature verified")
    except Exception as e:
        print("Signature not verified:\n", e)
    return 0


if __name__ == '__main__':
    main()
