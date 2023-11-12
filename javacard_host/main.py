import pretty_errors

import rsa


from card_utils import get_card_connection, Card
from computer_utils import save_public_key, get_computer_commands, get_public_key_from_file, rsa_verify_bool
from utils import TEXT_ENCODING


def get_card_or_exit() -> Card:
    card = get_card_connection()
    if not card:
        print("init card failed")
        exit(1)
    print("init card success")
    return card


def print_commands(commands: dict) -> None:
    for name, func in commands.items():
        nb_args = func.__code__.co_argcount - 1
        if func.requires_auth:
            print(f"[Auth] {name}, input args : {nb_args}")
        else:
            print(f"       {name}, input args : {nb_args}")


def test_everything() -> int:
    print("main")

    print("\n--> connecting to the card ... -------------------------------------------")
    card = get_card_or_exit()

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

    # test get public key
    print("\n--> test get public key --------------------------------------------------")
    save_public_key(card, "public_key")
    public_key_from_file = get_public_key_from_file("public_key.pem")

    # test sign
    print("\n--> test sign ------------------------------------------------------------")
    text = "please sign this me !"

    signature = card.sign(text)
    print("is 1st valid :", rsa_verify_bool(text.encode(TEXT_ENCODING), bytes(signature), public_key_from_file))

    # test with long text
    long_text = "".join(["a" for _ in range(220)])

    long_text_signature = card.sign(long_text)
    print("is 2nd valid :", rsa_verify_bool(long_text.encode(TEXT_ENCODING), bytes(long_text_signature), public_key_from_file))

    return 0


def help(card: Card) -> None:
    print("Commands using the card:")
    print_commands(card.commands())
    print("Commands using the computer:")
    print_commands(get_computer_commands())


def repl() -> int:
    card = get_card_or_exit()
    help(card)

    while True:
        user_input = input("Enter command: ")
        function, *args = user_input.split(" ")
        if user_input == "exit":
            return 0
        elif user_input == "help":
            help(card)
        else:
            try:
                if function in card.commands():
                    res = card.commands()[function](*args)
                    if res is not None:
                        print("Raw response:", res)
                elif function in get_computer_commands():
                    res = get_computer_commands()[function](card, *args)
                    if res is not None:
                        print("Raw response:", res)
                else:
                    print("Command not found")
            except Exception as e:
                print("Error:", e)
    return 0


if __name__ == '__main__':
    #test_everything()
    repl()
