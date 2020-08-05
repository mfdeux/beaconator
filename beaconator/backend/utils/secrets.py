import secrets
import string

import jwt


class InvalidToken(Exception):
    pass


TEMP_PASSWORD = "tDkZMLvsao93Cm5I9FZbwqPH"
JWT_SECRET = "cQ0MFXdo2CrvBtReB10cey0NMaB4oize76RFZ43FqxpKnXtMEZrY3U0qUV1X"


def generate_jwt_token(secret: str):
    encoded_jwt = jwt.encode({"usage": "authentication"}, secret, algorithm="HS256")
    return encoded_jwt


def validate_jwt_token(token: str, secret: str):
    try:
        jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        raise InvalidToken


def make_temporary_password():
    return make_random_token(24)


def make_jwt_secret():
    return make_random_token(60)


def make_random_token(char_length: int = 24):
    return "".join(
        secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(char_length)
    )