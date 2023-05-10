import pytest
from src.service.connector import PostgresConnector

from src.service.unit_of_work import AbstractUnitOfWork
from src.repository.repository import AbstractRepository
from src.domain.model import Item


@pytest.fixture
def test_items():
    return [
        FakeRow(
            {
                "id": 1,
                "title": "test title",
                "description": "test description",
            }
        ),
        FakeRow(
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

    monkeypatch.setattr(PostgresConnector, "connect", mock_connection)


@pytest.fixture
def mock_postgres_error_connection(monkeypatch, error_session_fixture):
    def mock_connection(*args, **kwargs):
        return error_session_fixture

    monkeypatch.setattr(PostgresConnector, "connect", mock_connection)


@pytest.fixture
def connection_dict():
    return {
        "username": "test",
        "password": "test",
        "host": "test",
        "port": 5432,
        "database_name": "test",
    }


class FakeRow:
    def __init__(self, data: dict):
        self.data = data

    def _asdict(self):
        return self.data


class FakeSession:
    def __init__(self, results) -> None:
        self.results = results

    def execute(self, *args, **kwargs):
        return FakeCursor(self.results)

    def commit(self):
        return True


class FakeErrorSession:
    def __init__(self, exception, results) -> None:
        self.exception = exception
        self.results = results

    def execute(self, *args, **kwargs):
        raise self.exception

    def commit():
        return True


class FakeCursor:
    def __init__(self, results) -> None:
        self.results = results

    def fetchall(self):
        return self.results

    def fetchone(self) -> FakeRow:
        return self.results[0]

    def first(self) -> tuple:
        return (1,)


class FakeRepository(AbstractRepository):
    def __init__(self, records: list):
        self.records = records

    def get_items(self):
        return [Item(**Fakerow._asdict()) for Fakerow in self.records]

    def get_item(self, item_id: int):
        return Item(**self.records[item_id - 1]._asdict())

    def insert_item(self, item: Item):
        self.records.append(FakeRow(item.__dict__))

    def update_item(self, item_id, item: Item):
        self.records[item_id - 1] = FakeRow(item.__dict__)

    def delete_item(self, item_id):
        self.records.pop(item_id - 1)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, records: list):
        self.repository = FakeRepository(records)
