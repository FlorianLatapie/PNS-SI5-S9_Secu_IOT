import pretty_errors
from Crypto.PublicKey.RSA import *
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1
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
    crypto_public_key = construct((public_modulus, public_exponent))
    import_rsa_public_key = rsa.PublicKey(public_modulus, public_exponent)

    # test get private key
    print("\n--> test get private key -------------------------------------------------")
    private_key = card.get_private_key()
    private_p = private_key[0]
    private_q = private_key[1]
    private_exponent_d = mod_inverse(public_exponent, (private_p - 1) * (private_q - 1))
    crypto_private_key = construct((public_modulus, public_exponent, private_exponent_d, private_p, private_q))
    import_rsa_private_key = rsa.PrivateKey(public_modulus, public_exponent, private_exponent_d, private_p, private_q)

    # test sign
    print("\n--> test sign ------------------------------------------------------------")
    encoding = "utf-8"
    text = "please sign eee !"
    signature = card.sign(text, encoding)
    signature2 = card.sign2(text, encoding)
    # test verify
    print("\n--> test verify ----------------------------------------------------------")

    digest = SHA1.new()
    digest.update(text.encode(encoding))
    crypto_signature = pkcs1_15.new(crypto_private_key).sign(digest)

    sha_card = card.sha1(text, encoding)
    print("sha card", binascii.hexlify(bytes(sha_card)))
    print("sha lib ", binascii.hexlify(bytes(digest.digest())))

    import_rsa_signature = rsa.sign(text.encode(encoding), import_rsa_private_key, "SHA-1")

    print("sign card  ", binascii.hexlify(bytes(signature)))
    print("sign card2 ", binascii.hexlify(bytes(signature2)))
    print("sign crypto", binascii.hexlify(bytes(crypto_signature)))
    print("sign import", binascii.hexlify(bytes(import_rsa_signature)))

    # check signature
    rsa.verify(text.encode(encoding), bytes(signature), import_rsa_public_key)
    is_signature_valid = pkcs1_15.new(crypto_public_key).verify(digest, bytes(signature))


if __name__ == '__main__':
    main()
