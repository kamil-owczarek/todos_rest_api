from src.domain.schema import ItemBaseSchema
from src.service.unit_of_work import AbstractUnitOfWork


def get_item(item_id: int, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.get_item(item_id)


def get_items(
    limit: int,
    offset: int,
    filter_field: str | None,
    filter_value: str | bool | None,
    uow: AbstractUnitOfWork,
):
    with uow:
        return uow.repository.get_items(limit, offset, filter_field, filter_value)


def insert_item(item: ItemBaseSchema, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.insert_item(item)


def update_item(item_id: int, item: ItemBaseSchema, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.update_item(item_id, item)


def delete_item(item_id: int, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.delete_item(item_id)
