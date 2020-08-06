import datetime
import json
import typing

import pytest
from starlette.testclient import TestClient

from beaconator.backend import dao, schemas
from beaconator.backend.server import app
from beaconator.backend.utils.images import image_queries


def test_index(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


def test_login_wrong_password(client: TestClient):
    response = client.post("/api/login", data=json.dumps({"password": "wrongpass"}))
    assert response.status_code == 401


def test_login_right_password(client: TestClient):
    response = client.post(
        "/api/login", data=json.dumps({"password": "tDkZMLvsao93Cm5I9FZbwqPH"})
    )
    assert response.status_code == 200
    assert "token" in response.json()


def test_get_codes_unauth(client: TestClient):
    response = client.get("/api/codes")
    assert response.status_code == 401


def test_get_codes(auth_client: TestClient, monkeypatch):
    """
    Test GET codes endpoint

    """
    test_data = [
        {
            "id": 1,
            "name": "Test Code",
            "code": "UA-TEST-CODE-123",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "active": True,
        },
        {
            "id": 2,
            "name": "Test Code",
            "code": "UA-TEST-CODE-123",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "active": True,
        },
    ]

    def mock_get(db=None, id=None, skip=None, limit=None):
        return test_data

    monkeypatch.setattr(dao, "get_ga_codes", mock_get)

    response = auth_client.get("/api/codes")
    assert response.status_code == 200
    assert len(response.json()) == len(test_data)


def test_get_code_unauth(client: TestClient):
    response = client.get("/api/codes/1")
    assert response.status_code == 401


def test_get_code(auth_client: TestClient, monkeypatch):
    """
    Test GET code endpoint

    """
    test_data = {
        "id": 1,
        "name": "Test Code",
        "code": "UA-TEST-CODE-123",
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "active": True,
    }

    def mock_get(db=None, id=None):
        return test_data

    monkeypatch.setattr(dao, "get_ga_code", mock_get)

    response = auth_client.get("/api/codes/1")
    assert response.status_code == 200
    assert response.json()["id"] == test_data["id"]


def test_get_code_incorrect_id(auth_client: TestClient, monkeypatch):
    def mock_get(db=None, id=None):
        return None

    monkeypatch.setattr(dao, "get_ga_code", mock_get)

    response = auth_client.get("/api/codes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Code not found"


def test_create_code_unauth(client: TestClient):
    response = client.post("/api/codes", data=json.dumps({"title": "something"}))
    assert response.status_code == 401


def test_create_code(auth_client: TestClient, monkeypatch):
    test_request_payload = {"name": "Test Code", "code": "UA-TEST-CODE-123"}
    test_response_payload = {
        "id": 1,
        "name": "Test Code",
        "code": "UA-TEST-CODE-123",
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "active": True,
    }

    def mock_post(db=None, item=None):
        return test_response_payload

    monkeypatch.setattr(dao, "create_ga_code", mock_post)

    response = auth_client.post("/api/codes", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert "id" in response.json()


def test_create_code_invalid_json(auth_client: TestClient):
    response = auth_client.post("/api/codes", data=json.dumps({"title": "something"}))
    assert response.status_code == 422


def test_update_code_unauth(client: TestClient):
    response = client.patch("/api/codes/1", data=json.dumps({"title": "something"}))
    assert response.status_code == 401


def test_update_code(auth_client: TestClient, monkeypatch):
    test_update_data = {"name": "HelloThere", "active": False}

    def mock_put(db=None, id=None, item=None):
        return 1

    monkeypatch.setattr(dao, "update_ga_code", mock_put)

    test_data = {
        "id": 1,
        "name": "HelloThere",
        "code": "UA-TEST-CODE-123",
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "active": False,
    }

    def mock_get(db=None, id=None):
        return test_data

    monkeypatch.setattr(dao, "get_ga_code", mock_get)

    response = auth_client.patch("/api/codes/1", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert "id" in response.json()


def test_update_code_invalid(auth_client: TestClient, monkeypatch):
    test_update_data = {"created_at": "Hello"}

    def mock_put(db=None, id=None, item=None):
        return 1

    monkeypatch.setattr(dao, "update_ga_code", mock_put)

    response = auth_client.patch("/api/codes/1", data=json.dumps(test_update_data))
    assert response.status_code == 422


def test_delete_code_unauth(client: TestClient):
    response = client.delete("/api/codes/1")
    assert response.status_code == 401


def test_delete_code(auth_client: TestClient, monkeypatch):
    def mock_delete(db=None, id=None):
        return 1

    monkeypatch.setattr(dao, "delete_ga_code", mock_delete)

    response = auth_client.delete("/api/codes/1")
    assert response.status_code == 204
    assert response.json() == None


def test_delete_code_incorrect_id(auth_client: TestClient, monkeypatch):
    def mock_get(db=None, id=None):
        return 0

    monkeypatch.setattr(dao, "delete_ga_code", mock_get)

    response = auth_client.delete("/api/codes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Code not found"


def test_get_properties_unauth(client: TestClient):
    response = client.get("/api/properties")
    assert response.status_code == 401


def test_get_properties(auth_client: TestClient, monkeypatch):
    """
    Test GET codes endpoint

    """
    test_data = [
        {
            "id": 1,
            "name": "Test Property",
            "code": "testcode",
            "ga_code_id": 1,
            "ga_code": {
                "id": 1,
                "name": "Test Code",
                "code": "UA-TEST-CODE-123",
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
                "active": True,
            },
            "image": "pixel",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "active": True,
        },
        {
            "id": 2,
            "name": "Test Property",
            "code": "testcode",
            "ga_code_id": 1,
            "ga_code": {
                "id": 1,
                "name": "Test Code",
                "code": "UA-TEST-CODE-123",
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
                "active": True,
            },
            "image": "pixel",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "active": True,
        },
    ]

    def mock_get(db=None, id=None, skip=None, limit=None):
        return test_data

    monkeypatch.setattr(dao, "get_properties", mock_get)

    response = auth_client.get("/api/properties")
    assert response.status_code == 200
    assert len(response.json()) == len(test_data)


def test_get_property_unauth(client: TestClient):
    response = client.get("/api/properties/1")
    assert response.status_code == 401


def test_get_property(auth_client: TestClient, monkeypatch):
    """
    Test GET code endpoint

    """
    test_data = {
        "id": 1,
        "name": "Test Property",
        "code": "testcode",
        "ga_code_id": 1,
        "ga_code": {
            "id": 1,
            "name": "Test Code",
            "code": "UA-TEST-CODE-123",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "active": True,
        },
        "image": "pixel",
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "active": True,
    }

    def mock_get(db=None, id=None):
        return test_data

    monkeypatch.setattr(dao, "get_property", mock_get)

    response = auth_client.get("/api/properties/1")
    assert response.status_code == 200
    assert response.json()["id"] == test_data["id"]


def test_get_perperty_incorrect_id(auth_client: TestClient, monkeypatch):
    def mock_get(db=None, id=None):
        return None

    monkeypatch.setattr(dao, "get_property", mock_get)

    response = auth_client.get("/api/properties/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Property not found"


def test_create_property_unauth(client: TestClient):
    response = client.post("/api/properties", data=json.dumps({"title": "something"}))
    assert response.status_code == 401


def test_create_property(auth_client: TestClient, monkeypatch):
    test_request_payload = {"name": "Test Property", "ga_code_id": 1, "image": "pixel"}
    test_response_payload = {
        "id": 1,
        "name": "Test Property",
        "code": "testcode",
        "ga_code_id": 1,
        "ga_code": {
            "id": 1,
            "name": "Test Code",
            "code": "UA-TEST-CODE-123",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "active": True,
        },
        "image": "pixel",
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "active": True,
    }

    def mock_post(db=None, item=None):
        return test_response_payload

    monkeypatch.setattr(dao, "create_property", mock_post)

    response = auth_client.post(
        "/api/properties", data=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert "id" in response.json()


def test_create_property_invalid_json(auth_client: TestClient):
    response = auth_client.post(
        "/api/properties", data=json.dumps({"title": "something"})
    )
    assert response.status_code == 422


# need to build out
def test_update_property_unauth(client: TestClient):
    response = client.patch(
        "/api/properties/1", data=json.dumps({"title": "something"})
    )
    assert response.status_code == 401


def test_update_property(auth_client: TestClient, monkeypatch):
    test_update_data = {"name": "HelloThere", "active": False}

    def mock_put(db=None, id=None, item=None):
        return 1

    monkeypatch.setattr(dao, "update_property", mock_put)

    test_data = {
        "id": 1,
        "name": "HelloThere",
        "code": "testcode",
        "ga_code_id": 1,
        "ga_code": {
            "id": 1,
            "name": "Test Code",
            "code": "UA-TEST-CODE-123",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "active": True,
        },
        "image": "pixel",
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "active": False,
    }

    def mock_get(db=None, id=None):
        return test_data

    monkeypatch.setattr(dao, "get_property", mock_get)

    response = auth_client.patch("/api/properties/1", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert "id" in response.json()


def test_update_property_invalid(auth_client: TestClient, monkeypatch):
    test_update_data = {"created_at": "Hello"}

    def mock_put(db=None, id=None, item=None):
        return 1

    monkeypatch.setattr(dao, "update_property", mock_put)

    response = auth_client.patch("/api/properties/1", data=json.dumps(test_update_data))
    assert response.status_code == 422


def test_delete_property_unauth(client: TestClient):
    response = client.delete("/api/properties/1")
    assert response.status_code == 401


def test_delete_property(auth_client: TestClient, monkeypatch):
    def mock_delete(db=None, id=None):
        return 1

    monkeypatch.setattr(dao, "delete_property", mock_delete)

    response = auth_client.delete("/api/properties/1")
    assert response.status_code == 204
    assert response.json() == None


def test_delete_property_incorrect_id(auth_client: TestClient, monkeypatch):
    def mock_get(db=None, id=None):
        return 0

    monkeypatch.setattr(dao, "delete_property", mock_get)

    response = auth_client.delete("/api/properties/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Property not found"


@pytest.mark.parametrize(
    "name, info", [[name, info] for name, info in image_queries.items()],
)
def test_api_images(client: TestClient, name: str, info: typing.Dict):
    response = client.get(f"/api/other/images?type={name}")
    assert response.status_code == 200
    assert response.headers["content-type"] == info.get("media_type")


# get_image
