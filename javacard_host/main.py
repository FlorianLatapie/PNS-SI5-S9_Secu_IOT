import pretty_errors

import rsa

import binascii

from card_utils import get_card_connection, Card
from sympy import mod_inverse


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

    # test get public key
    print("\n--> test get public key --------------------------------------------------")
    crypto_public_key = card.get_public_key()

    public_exponent = crypto_public_key[0]
    public_modulus = crypto_public_key[1]
    import_rsa_public_key = rsa.PublicKey(public_modulus, public_exponent)

    # test sign
    print("\n--> test sign ------------------------------------------------------------")
    encoding = "utf-8"
    text = "please sign me !"
    signature = card.sign(text, encoding)

    # test verify
    print("\n--> test verify ----------------------------------------------------------")
    print("sign card  ", binascii.hexlify(bytes(signature)))

    # check signature
    rsa.verify(text.encode(encoding), bytes(signature), import_rsa_public_key)


if __name__ == '__main__':
    main()
