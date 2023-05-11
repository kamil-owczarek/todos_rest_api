import json

import pytest
from fastapi.testclient import TestClient
from src.entrypoints.fastapi_app import app
from src.utils.exceptions import IdNotFound


def test_endpoint_get_item(mock_postgres_connection, auth_header):
    client = TestClient(app)
    result = client.get("/items/1", headers=auth_header)
    json_response = result.json()
    assert json_response.get("id") == 1
    assert json_response.get("title") == "test title"
    assert json_response.get("description") == "test description"
    assert json_response.get("completed") == False


def test_endpoint_get_item_missing_token(mock_postgres_connection):
    client = TestClient(app)
    result = client.get("/items/1")
    assert result.status_code == 403


def test_endpoint_get_item_invalid_token_scheme(mock_postgres_connection):
    client = TestClient(app)
    result = client.get(
        "/items/1", headers={"Authorization": "NonScheme invalid.token"}
    )
    assert result.status_code == 403


def test_endpoint_get_item_invalid_token(mock_postgres_connection):
    client = TestClient(app)
    result = client.get("/items/1", headers={"Authorization": "Bearer invalid.token"})
    assert result.status_code == 403


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_endpoint_get_item_raise_exception(
    error_session_fixture, mock_postgres_error_connection, auth_header
):
    client = TestClient(app)
    result = client.get("/items/1", headers=auth_header)
    assert result.status_code == 500


@pytest.mark.parametrize(
    "error_session_fixture", [IdNotFound], indirect=["error_session_fixture"]
)
def test_endpoint_get_item_raise_id_not_found_error(
    error_session_fixture, mock_postgres_error_connection, auth_header
):
    client = TestClient(app)
    result = client.get("/items/1", headers=auth_header)
    assert result.status_code == 404
    assert result.json().get("detail") == "Item with ID: 1 not found!"


def test_endpoint_get_items(mock_postgres_connection, auth_header):
    client = TestClient(app)
    result = client.get("/items", headers=auth_header)
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


def test_endpoint_get_items_missing_token(mock_postgres_connection):
    client = TestClient(app)
    result = client.get("/items")
    assert result.status_code == 403


def test_endpoint_get_items_invalid_token_scheme(mock_postgres_connection):
    client = TestClient(app)
    result = client.get("/items", headers={"Authorization": "NonScheme invalid.token"})
    assert result.status_code == 403


def test_endpoint_get_items_invalid_token(mock_postgres_connection):
    client = TestClient(app)
    result = client.get("/items", headers={"Authorization": "Bearer invalid.token"})
    assert result.status_code == 403


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_endpoint_get_items_raise_exception(
    error_session_fixture, mock_postgres_error_connection, auth_header
):
    client = TestClient(app)
    result = client.get("/items", headers=auth_header)
    assert result.status_code == 500


def test_endpoint_post_item(mock_postgres_connection, auth_header):
    client = TestClient(app)
    item = {"title": "new", "description": "new", "completed": True}
    result = client.post("/items", content=json.dumps(item), headers=auth_header)
    assert result.status_code == 201


def test_endpoint_post_invalid_item(mock_postgres_connection, auth_header):
    client = TestClient(app)
    item = {"title": "new", "completed": True}
    result = client.post("/items", content=json.dumps(item), headers=auth_header)
    assert result.status_code == 422


def test_endpoint_post_item_missing_token(mock_postgres_connection):
    client = TestClient(app)
    item = {"title": "new", "description": "new", "completed": True}
    result = client.post("/items", content=json.dumps(item))
    assert result.status_code == 403


def test_endpoint_post_item_invalid_token_scheme(mock_postgres_connection):
    client = TestClient(app)
    item = {"title": "new", "description": "new", "completed": True}
    result = client.post(
        "/items",
        content=json.dumps(item),
        headers={"Authorization": "NonScheme invalid.token"},
    )
    assert result.status_code == 403


def test_endpoint_post_invalid_token(mock_postgres_connection):
    client = TestClient(app)
    item = {"title": "new", "description": "new", "completed": True}
    result = client.post(
        "/items",
        content=json.dumps(item),
        headers={"Authorization": "Bearer invalid.token"},
    )
    assert result.status_code == 403


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_endpoint_post_item_raise_exception(
    error_session_fixture, mock_postgres_error_connection, auth_header
):
    client = TestClient(app)
    item = {"title": "new", "description": "new", "completed": True}
    result = client.post("/items", content=json.dumps(item), headers=auth_header)
    assert result.status_code == 500


def test_endpoint_patch_item(mock_postgres_connection, auth_header):
    client = TestClient(app)
    item = {"title": "updated", "description": "updated", "completed": False}
    result = client.patch("/items/1", content=json.dumps(item), headers=auth_header)
    assert result.status_code == 204


def test_endpoint_patch_invalid_item(mock_postgres_connection, auth_header):
    client = TestClient(app)
    item = {"description": "updated", "completed": False}
    result = client.patch("/items/1", content=json.dumps(item), headers=auth_header)
    assert result.status_code == 422


def test_endpoint_patch_item_missing_token(mock_postgres_connection):
    client = TestClient(app)
    item = {"description": "updated", "completed": False}
    result = client.patch("/items/1", content=json.dumps(item))
    assert result.status_code == 403


def test_endpoint_patch_item_invalid_token_scheme(mock_postgres_connection):
    client = TestClient(app)
    item = {"description": "updated", "completed": False}
    result = client.patch(
        "/items/1",
        content=json.dumps(item),
        headers={"Authorization": "NonScheme invalid.token"},
    )
    assert result.status_code == 403


def test_endpoint_patch_item_invalid_token(mock_postgres_connection):
    client = TestClient(app)
    item = {"description": "updated", "completed": False}
    result = client.patch(
        "/items/1",
        content=json.dumps(item),
        headers={"Authorization": "Bearer invalid.token"},
    )
    assert result.status_code == 403


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_endpoint_patch_item_raise_exception(
    error_session_fixture, mock_postgres_error_connection, auth_header
):
    client = TestClient(app)
    item = {"title": "updated", "description": "updated", "completed": False}
    result = client.patch("/items/1", content=json.dumps(item), headers=auth_header)
    assert result.status_code == 500


@pytest.mark.parametrize(
    "error_session_fixture", [IdNotFound], indirect=["error_session_fixture"]
)
def test_endpoint_patch_item_raise_id_not_found_error(
    error_session_fixture, mock_postgres_error_connection, auth_header
):
    client = TestClient(app)
    item = {"title": "updated", "description": "updated", "completed": False}
    result = client.patch("/items/1", content=json.dumps(item), headers=auth_header)
    assert result.status_code == 404


def test_endpoint_delete_item(mock_postgres_connection, auth_header):
    client = TestClient(app)
    result = client.delete("/items/1", headers=auth_header)
    assert result.status_code == 204


def test_endpoint_delete_item_missing_token(mock_postgres_connection):
    client = TestClient(app)
    result = client.delete("/items/1")
    assert result.status_code == 403


def test_endpoint_delete_item_invalid_token_scheme(mock_postgres_connection):
    client = TestClient(app)
    result = client.delete(
        "/items/1", headers={"Authorization": "NonScheme invalid.token"}
    )
    assert result.status_code == 403


def test_endpoint_delete_item_invalid_token(mock_postgres_connection):
    client = TestClient(app)
    result = client.delete(
        "/items/1", headers={"Authorization": "Bearer invalid.token"}
    )
    assert result.status_code == 403


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_endpoint_delete_item_raise_exception(
    error_session_fixture, mock_postgres_error_connection, auth_header
):
    client = TestClient(app)
    result = client.delete("/items/1", headers=auth_header)
    assert result.status_code == 500


@pytest.mark.parametrize(
    "error_session_fixture", [IdNotFound], indirect=["error_session_fixture"]
)
def test_endpoint_delete_item_raise_id_not_found_error(
    error_session_fixture, mock_postgres_error_connection, auth_header
):
    client = TestClient(app)
    result = client.delete("/items/1", headers=auth_header)
    assert result.status_code == 404
