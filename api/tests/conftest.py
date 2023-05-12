import pytest
from src.auth.token_handler import create_token
from src.azure import key_vault
from src.domain.model import Item
from src.domain.schema import ItemBaseSchema
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
def auth_header():
    token = create_token()
    header = {"Authorization": f"Bearer {token['access_token']}"}
    return header


@pytest.fixture
def fake_key_vault_client(monkeypatch):
    monkeypatch.setattr(key_vault, "SecretClient", FakeSecretClient)


class FakeItemBaseSchema:
    def __init__(self, data: dict):
        self.data = data

    def _asdict(self):
        return self.data


class FakeCursor:
    def __init__(self, results: list[FakeItemBaseSchema]):
        self.results = [Item(**result._asdict()) for result in results]

    def filter(self, *args, **kwargs):
        return self

    def offset(self, *args):
        return self

    def limit(self, *args):
        return self

    def all(self) -> list[Item]:
        return self.results

    def count(self):
        return 1

    def first(self) -> Item:
        return self.results[0]

    def update(self, *args) -> bool:
        return True

    def delete(self) -> bool:
        return True


class FakeSession:
    def __init__(self, results: list[FakeItemBaseSchema]):
        self.results = results

    def query(self, *args, **kwargs) -> FakeCursor:
        return FakeCursor(self.results)

    def close(self) -> bool:
        return True

    def add(self, item):
        self.results.append(item)

    def commit(self) -> bool:
        return True

    def refresh(self, *args) -> bool:
        return True


class FakeErrorSession:
    def __init__(self, exception: Exception, results: list[FakeItemBaseSchema]):
        self.exception = exception
        self.results = results

    def query(self, *args, **kwargs) -> Exception:
        raise self.exception

    def close(self) -> bool:
        return True


class FakeRepository(AbstractRepository):
    def __init__(self, records: list[FakeItemBaseSchema]):
        self.records = records

    def get_items(
        self,
        limit: int,
        offset: int,
        filter_field: str | None,
        filter_value: str | bool | None,
    ) -> list[Item]:
        return [
            Item(**FakeItemBaseSchema._asdict()) for FakeItemBaseSchema in self.records
        ]

    def get_item(self, item_id: int) -> Item:
        return Item(**self.records[item_id - 1]._asdict())

    def insert_item(self, item: ItemBaseSchema):
        self.records.append(FakeItemBaseSchema(item.__dict__))

    def update_item(self, item_id: int, item: ItemBaseSchema):
        self.records[item_id - 1] = FakeItemBaseSchema(item.__dict__)

    def delete_item(self, item_id: int):
        self.records.pop(item_id - 1)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, records: list[FakeItemBaseSchema]):
        self.repository = FakeRepository(records)


class FakeKeyVaultSecret:
    def __init__(self, value) -> None:
        self.value = value


class FakeSecretClient:
    def __init__(self, vault_url: str, *args, **kwargs) -> None:
        self.vault_url = self.__check_url(vault_url)
        self.secrets = {
            "fake_secret_1": FakeKeyVaultSecret("fake_value_1"),
            "fake_secret_2": FakeKeyVaultSecret("fake_value_2"),
        }

    def get_secret(self, secret_name: str) -> FakeKeyVaultSecret:
        return self.secrets.get(secret_name)

    @staticmethod
    def __check_url(vault_url: str) -> str:
        if vault_url.startswith("https://"):
            return vault_url
        else:
            raise Exception
