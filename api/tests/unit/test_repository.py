import pytest
from src.adapters.repository import PostgreSqlRepository
from src.domain.model import Item
from src.domain.schema import ItemBaseSchema
from src.utils.exceptions import IdNotFound


def test_get_item(session_fixture):
    repository = PostgreSqlRepository(session_fixture)
    result = repository.get_item(1)
    assert isinstance(result, Item)
    assert result.id == 1
    assert result.title == "test title"
    assert result.description == "test description"
    assert result.completed == False


@pytest.mark.parametrize(
    "error_session_fixture", [IdNotFound], indirect=["error_session_fixture"]
)
def test_get_item_raise_id_not_found(error_session_fixture):
    with pytest.raises(IdNotFound):
        repository = PostgreSqlRepository(error_session_fixture)
        repository.get_item(1)


def test_get_items(session_fixture):
    repository = PostgreSqlRepository(session_fixture)
    results = repository.get_items(10, 0, None, None)
    assert [isinstance(result, Item) for result in results]
    assert results[0].id == 1
    assert results[0].title == "test title"
    assert results[0].description == "test description"
    assert results[0].completed == False
    assert results[1].id == 2
    assert results[1].title == "dummy title"
    assert results[1].description == "dummy description"
    assert results[1].completed == True


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_gets_item_raise_exception(error_session_fixture):
    with pytest.raises(Exception):
        repository = PostgreSqlRepository(error_session_fixture)
        repository.get_items()


def test_insert_item(session_fixture):
    repository = PostgreSqlRepository(session_fixture)
    item = ItemBaseSchema(**{"title": "new", "description": "new", "completed": True})
    result = repository.insert_item(item)
    assert result == True


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_insert_item_raise_exception(error_session_fixture):
    with pytest.raises(Exception):
        repository = PostgreSqlRepository(error_session_fixture)
        item = ItemBaseSchema(
            **{"title": "new", "description": "new", "completed": True}
        )
        repository.insert_item(item)


def test_update_item(session_fixture):
    repository = PostgreSqlRepository(session_fixture)
    item = ItemBaseSchema(**{"title": "new", "description": "new", "completed": True})
    results = repository.update_item(1, item)
    assert results == True


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_update_item_raise_exception(error_session_fixture):
    with pytest.raises(Exception):
        repository = PostgreSqlRepository(error_session_fixture)
        item = Item(**{"title": "new", "description": "new", "completed": True})
        repository.update_item(1, item)


def test_delete_item(session_fixture):
    repository = PostgreSqlRepository(session_fixture)
    results = repository.delete_item(1)
    assert results == True


@pytest.mark.parametrize(
    "error_session_fixture", [Exception], indirect=["error_session_fixture"]
)
def test_delete_item_raise_exception(error_session_fixture):
    with pytest.raises(Exception):
        repository = PostgreSqlRepository(error_session_fixture)
        repository.delete_item(1)
