from random import choice
from string import ascii_lowercase, digits


def generate_token() -> str:
    token = "".join(choice(ascii_lowercase + digits) for _ in range(25))
    return token
