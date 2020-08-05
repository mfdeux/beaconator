import typing

import yaml


def load_config(path: str) -> typing.Dict:
    with open(path) as fh:
        loaded_config = yaml.safe_load(fh)

    return loaded_config


def save_config(temp_config: typing.Dict, path: str):
    with open(path) as fh:
        yaml.dump(temp_config, fh)
