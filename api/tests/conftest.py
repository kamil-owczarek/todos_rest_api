import pytest
from src.domain.model import Item, ItemBaseSchema
from src.repository.repository import AbstractRepository
from src.service.session import PostgresSession
from src.service.unit_of_work import AbstractUnitOfWork


@pytest.fixture
def test_items():
    return [
        FakeItemBaseSchema(
            {
                "id": 1,
                "title": "test title",
                "description": "test description",
                "completed": False,
            }
        ),
        FakeItemBaseSchema(
            {
                "id": 2,
                "title": "dummy title",
                "description": "dummy description",
                "completed": True,
            }
        ),
    ]


@pytest.fixture
def session_fixture(test_items):
    return FakeSession(test_items)


@pytest.fixture
def error_session_fixture(test_items, request):
    return FakeErrorSession(request.param, test_items)


@pytest.fixture
def fake_uow(test_items):
    return FakeUnitOfWork(test_items)


@pytest.fixture
def mock_postgres_connection(monkeypatch, session_fixture):
    def mock_connection(*args, **kwargs):
        return session_fixture

    monkeypatch.setattr(PostgresSession, "create_session", mock_connection)


@pytest.fixture
def mock_postgres_error_connection(monkeypatch, error_session_fixture):
    def mock_connection(*args, **kwargs):
        return error_session_fixture

    monkeypatch.setattr(PostgresSession, "create_session", mock_connection)


@pytest.fixture
def connection_dict():
    return {
        "username": "test",
        "password": "test",
        "host": "test",
        "port": 5432,
        "database_name": "test",
    }


class FakeItemBaseSchema:
    def __init__(self, data: dict):
        self.data = data

    def _asdict(self):
        return self.data


class FakeSession:
    def __init__(self, results) -> None:
        self.results = results

    def query(self, *args, **kwargs):
        return FakeCursor(self.results)

    def close(self):
        return True

    def add(self, item):
        self.results.append(item)

    def commit(self):
        return True

    def refresh(self, *args):
        return True


class FakeErrorSession:
    def __init__(self, exception, results) -> None:
        self.exception = exception
        self.results = results

    def query(self, *args, **kwargs):
        raise self.exception

    def close(self):
        return True


class FakeCursor:
    def __init__(self, results: list) -> None:
        self.results = [Item(**result._asdict()) for result in results]

    def filter(self, *args, **kwargs):
        return self

    def offset(self, *args):
        return self

    def limit(self, *args):
        return self

    def all(self):
        return self.results

    def count(self):
        return 1

    def first(self) -> Item:
        return self.results[0]

    def all(self):
        return self.results

    def update(self, *args):
        return True

    def delete(self):
        return True


class FakeRepository(AbstractRepository):
    def __init__(self, records: list):
        self.records = records

    def get_items(
        self,
        limit,
        offset,
        filter_field,
        filter_value,
    ):
        return [
            Item(**FakeItemBaseSchema._asdict()) for FakeItemBaseSchema in self.records
        ]

    def get_item(self, item_id: int):
        return Item(**self.records[item_id - 1]._asdict())

    def insert_item(self, item: ItemBaseSchema):
        self.records.append(FakeItemBaseSchema(item.__dict__))

    def update_item(self, item_id, item: ItemBaseSchema):
        self.records[item_id - 1] = FakeItemBaseSchema(item.__dict__)

    def delete_item(self, item_id):
        self.records.pop(item_id - 1)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, records: list):
        self.repository = FakeRepository(records)
