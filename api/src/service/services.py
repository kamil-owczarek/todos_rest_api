from src.domain.model import Item
from src.service.unit_of_work import AbstractUnitOfWork


def get_item(item_id: int, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.get_item(item_id)


def get_items(uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.get_items()


def insert_item(item: Item, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.insert_item(item)


def update_item(item_id, item: Item, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.update_item(item_id, item)


def delete_item(item_id: int, uow: AbstractUnitOfWork):
    with uow:
        return uow.repository.delete_item(item_id)
