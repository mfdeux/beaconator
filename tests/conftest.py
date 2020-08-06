import pytest
from starlette.testclient import TestClient

from beaconator.backend.server import app
from beaconator.backend.utils.secrets import JWT_SECRET, generate_jwt_token


@pytest.fixture(scope="module")
def client():
    client_inst = TestClient(app)
    yield client_inst


@pytest.fixture(scope="module")
def auth_client():
    client_inst = TestClient(app)
    token = generate_jwt_token(JWT_SECRET)
    client_inst.headers["Authorization"] = f"Bearer {token}"
    yield client_inst
