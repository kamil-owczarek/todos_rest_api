import pytest
from src.domain.model import Item
from src.service.unit_of_work import PostgresUnitOfWork


def test_unit_of_work_return_get_item(mock_postgres_connection, connection_dict):
    uow = PostgresUnitOfWork(connection_dict)
    with uow:
        result = uow.repository.get_item(1)
    assert isinstance(result, Item)


def test_unit_of_work_return_get_items(mock_postgres_connection, connection_dict):
    uow = PostgresUnitOfWork(connection_dict)
    with uow:
        results = uow.repository.get_items(limit=10, offset=0)
    assert all(isinstance(result, Item) for result in results)


def test_unit_of_work_raise_exception_when_connection_fails(connection_dict):
    with pytest.raises(Exception):
        uow = PostgresUnitOfWork(connection_dict)
        with uow:
            uow.repository.get_items()
