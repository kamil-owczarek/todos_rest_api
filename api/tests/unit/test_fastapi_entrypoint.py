import json

import pytest
from fastapi.testclient import TestClient
from src.entrypoints.fastapi_app import app
from src.utils.exceptions import IdNotFound


def test_endpoint_get_item(mock_postgres_connection):
    client = TestClient(app)
    result = client.get("/items/1")
    json_response = result.json()
    assert json_response.get("id") == 1
    assert json_response.get("title") == "test title"
    assert json_response.get("description") == "test description"
    assert json_response.get("completed") == False


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_endpoint_get_item_raise_exception(
    error_session_fixture, mock_postgres_error_connection
):
    client = TestClient(app)
    result = client.get("/items/1")
    assert result.status_code == 500


@pytest.mark.parametrize(
    "error_session_fixture", [IdNotFound], indirect=["error_session_fixture"]
)
def test_endpoint_get_item_raise_id_not_found_error(
    error_session_fixture, mock_postgres_error_connection
):
    client = TestClient(app)
    result = client.get("/items/1")
    assert result.status_code == 404
    assert result.json().get("detail") == "Item with ID: 1 not found!"


def test_endpoint_get_items(mock_postgres_connection):
    client = TestClient(app)
    result = client.get("/items")
    json_response = result.json()
    assert len(json_response) == 2
    assert json_response[0].get("id") == 1
    assert json_response[0].get("title") == "test title"
    assert json_response[0].get("description") == "test description"
    assert json_response[0].get("completed") == False
    assert json_response[1].get("id") == 2
    assert json_response[1].get("title") == "dummy title"
    assert json_response[1].get("description") == "dummy description"
    assert json_response[1].get("completed") == True


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_endpoint_get_items_raise_exception(
    error_session_fixture, mock_postgres_error_connection
):
    client = TestClient(app)
    result = client.get("/items")
    assert result.status_code == 500


def test_endpoint_post_item(mock_postgres_connection):
    client = TestClient(app)
    item = {"title": "new", "description": "new", "completed": True}
    result = client.post("/items", content=json.dumps(item))
    assert result.status_code == 201


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_endpoint_post_item_raise_exception(
    error_session_fixture, mock_postgres_error_connection
):
    client = TestClient(app)
    item = {"title": "new", "description": "new", "completed": True}
    result = client.post("/items", content=json.dumps(item))
    assert result.status_code == 500


def test_endpoint_patch_item(mock_postgres_connection):
    client = TestClient(app)
    item = {"title": "updated", "description": "updated", "completed": False}
    result = client.patch("/items/1", content=json.dumps(item))
    assert result.status_code == 204


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_endpoint_patch_item_raise_exception(
    error_session_fixture, mock_postgres_error_connection
):
    client = TestClient(app)
    item = {"title": "updated", "description": "updated", "completed": False}
    result = client.patch("/items/1", content=json.dumps(item))
    assert result.status_code == 500


def test_endpoint_delete_item(mock_postgres_connection):
    client = TestClient(app)
    result = client.delete("/items/1")
    assert result.status_code == 204


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_endpoint_delete_item_raise_exception(
    error_session_fixture, mock_postgres_error_connection
):
    client = TestClient(app)
    result = client.delete("/items/1")
    assert result.status_code == 500
