import os
import typing

import pydantic
import yaml

from .backend.utils.secrets import make_jwt_secret, make_temporary_password


class Config(pydantic.BaseModel):
    database_uri: str = "sqlite:///data.db"
    docs_url: typing.Optional[str] = None
    redoc_url: typing.Optional[str] = None
    serve_admin: bool = True
    admin_path: str = "/admin"
    password: typing.Optional[str] = "tDkZMLvsao93Cm5I9FZbwqPH"
    jwt_secret: typing.Optional[
        str
    ] = "cQ0MFXdo2CrvBtReB10cey0NMaB4oize76RFZ43FqxpKnXtMEZrY3U0qUV1X"


def load_config(path: typing.Optional[str] = None) -> Config:
    if path:
        with open(path) as fh:
            loaded_config = yaml.safe_load(fh)
            config = Config(**loaded_config)
    else:
        config = Config()

    if not config.password:
        config.password = make_temporary_password()
        print(config.password)
    if not config.jwt_secret:
        config.jwt_secret = make_jwt_secret()

    os.environ["BEACONATOR__DB_URI"] = config.database_uri
    os.environ["BEACONATOR__PASSWORD"] = config.password
    os.environ["BEACONATOR__JWT_SECRET"] = config.jwt_secret

    return config


def save_config(temp_config: typing.Dict, path: str):
    with open(path) as fh:
        yaml.dump(temp_config, fh)
