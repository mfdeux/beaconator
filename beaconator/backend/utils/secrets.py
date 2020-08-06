import secrets
import string
import typing

import jwt


class InvalidToken(Exception):
    pass


def generate_jwt_token(secret: str) -> str:
    encoded_jwt = jwt.encode({"usage": "authentication"}, secret, algorithm="HS256")
    return encoded_jwt.decode("utf-8")


def validate_jwt_token(token: str, secret: str) -> typing.Optional[typing.Dict]:
    try:
        jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        raise InvalidToken


def make_temporary_password() -> str:
    return make_random_token(24)


def make_jwt_secret() -> str:
    return make_random_token(60)


def make_random_token(char_length: int = 24) -> str:
    return "".join(
        secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(char_length)
    )
