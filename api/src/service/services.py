from src.domain.model import ItemBaseSchema
from src.service.unit_of_work import AbstractUnitOfWork


def get_item(item_id: int, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.get_item(item_id)


def get_items(limit, offset, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.get_items(limit, offset)


def insert_item(item: ItemBaseSchema, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.insert_item(item)


def update_item(item_id, item: ItemBaseSchema, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.update_item(item_id, item)


def delete_item(item_id: int, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.delete_item(item_id)
