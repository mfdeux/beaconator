import pytest
from starlette.testclient import TestClient

from beaconator.backend.server import create_server
from beaconator.backend.utils.secrets import generate_jwt_token
from beaconator.config import load_config

config = load_config()
app = create_server(config)


@pytest.fixture(scope="module")
def client():
    client_inst = TestClient(app)
    yield client_inst


@pytest.fixture(scope="module")
def auth_client():
    client_inst = TestClient(app)
    token = generate_jwt_token(config.jwt_secret)
    client_inst.headers["Authorization"] = f"Bearer {token}"
    yield client_inst
