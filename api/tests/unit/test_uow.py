import pytest
from src.domain.model import Item
from src.service.unit_of_work import PostgresUnitOfWork


def test_unit_of_work_return_get_item(
    mock_postgres_connection,
):
    uow = PostgresUnitOfWork()
    with uow:
        result = uow.repository.get_item(1)
    assert isinstance(result, Item)


def test_unit_of_work_return_get_items(
    mock_postgres_connection,
):
    uow = PostgresUnitOfWork()
    with uow:
        results = uow.repository.get_items(10, 0, None, None)
    assert all(isinstance(result, Item) for result in results)


def test_unit_of_work_raise_exception_when_connection_fails():
    with pytest.raises(Exception):
        uow = PostgresUnitOfWork()
        with uow:
            uow.repository.get_items()
