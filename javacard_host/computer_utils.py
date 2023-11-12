import rsa
import os

from card_utils import Card
from utils import command, TEXT_ENCODING


def __save_public_key(public_key: rsa.PublicKey, filename: str):
    with open(filename, "wb") as f:
        f.write(public_key.save_pkcs1())


def get_public_key_from_file(filename: str) -> rsa.PublicKey:
    if not os.path.isfile(filename):
        return None
    with open(filename, "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())


def rsa_verify_bool(message: bytes, signature: bytes, public_key: rsa.PublicKey) -> bool:
    try:
        res = rsa.verify(message, bytes(signature), public_key)
        # return res is not empty boolean value
        return bool(res)
    except rsa.pkcs1.VerificationError:
        return False


@command()
def save_public_key(card: Card, filename: str):

    public_exponent, public_modulus = card.get_public_key()
    public_key = rsa.PublicKey(public_modulus, public_exponent)

    __save_public_key(public_key, filename + ".pem")
    print("Public key saved to", filename + ".pem")

@command()
def store_signature(card: Card):
    filename = input("Enter filename (no extension): ")
    message = input("Enter message: ")

    signature = card.sign(message)
    with open(filename+".sig", "wb") as f:
        f.write(bytes(signature))
        print("Signature stored to", filename+".sig")
    with open(filename+".msg", "w") as f:
        f.write(message)
        print("Message stored to", filename+".msg")
    print("Signature stored to", filename)


@command()
def verify_signature(card: Card):
    key_filename = input("Enter public key filename (no extension): ")
    print("loading public key from", key_filename + ".pem")
    filename = input("Enter filename (no extension): ")
    print("loading signature from", filename + ".sig")
    print("loading message from", filename + ".msg")

    public_key = get_public_key_from_file(key_filename + ".pem")
    if public_key is None:
        print("Public key not found")
        return
    with open(filename+".sig", "rb") as f:
        signature = f.read()
    with open(filename+".msg", "r") as f:
        message = f.read()
    print("is valid :", rsa_verify_bool(message.encode(TEXT_ENCODING), signature, public_key))


def get_computer_commands():
    commands = {}

    # Iterate through all functions in the current module
    for name, obj in globals().items():
        if callable(obj):
            if hasattr(obj, "is_command"):
                commands[name] = obj

    return commands
