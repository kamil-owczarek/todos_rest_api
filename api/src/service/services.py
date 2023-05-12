"""
Module contains service layer implementation.
"""

from src.domain.model import Item
from src.domain.schema import ItemBaseSchema
from src.service.unit_of_work import AbstractUnitOfWork


def get_item(item_id: int, uow: AbstractUnitOfWork) -> Item:
    """Retrieve Item based on provided Id.

    :param item_id: Id of Item in table.
    :type item_id: int
    :param uow: Unit of Work.
    :type: AbstractUnitOfWork

    :returns: Item object.
    :rtype: Item
    """

    with uow:
        return uow.repository.get_item(item_id)


def get_items(
    limit: int,
    offset: int,
    filter_field: str | None,
    filter_value: str | bool | None,
    uow: AbstractUnitOfWork,
) -> list[Item]:
    """Retrieve Items based on provided parameters.

    :param limit: Limit page items size.
    :type limit: int
    :param offset: Page number.
    :type offset: int
    :param filter_field: Filtering field name.
    :type filter_field: str | None
    :param filter_value: Filter value.
    :type filter_value: str | bool | None
    :param uow: Unit of Work.
    :type: AbstractUnitOfWork

    :returns: List of Item objects.
    :rtype: list[Item]
    """

    with uow:
        return uow.repository.get_items(limit, offset, filter_field, filter_value)


def insert_item(item: ItemBaseSchema, uow: AbstractUnitOfWork) -> bool:
    """Insert Item based on provided schema.

    :param item: Body of Item to insert.
    :type item: ItemBaseSchema
    :param uow: Unit of Work.
    :type: AbstractUnitOfWork

    :returns: Operation result.
    :rtype: bool
    """

    with uow:
        return uow.repository.insert_item(item)


def update_item(item_id: int, item: ItemBaseSchema, uow: AbstractUnitOfWork) -> bool:
    """Update Item based on provided Id and schema.

    :param item_id: Id of Item in table to update.
    :type item_id: int
    :param item: Body of Item to update.
    :type item: ItemBaseSchema
    :param uow: Unit of Work.
    :type: AbstractUnitOfWork

    :returns: Operation result.
    :rtype: bool
    """

    with uow:
        return uow.repository.update_item(item_id, item)


def delete_item(item_id: int, uow: AbstractUnitOfWork) -> bool:
    """Delete Item based on provided Id.

    :param item_id: Id of Item in table to update.
    :type item_id: int
    :param uow: Unit of Work.
    :type: AbstractUnitOfWork

    :returns: Operation result.
    :rtype: bool
    """

    with uow:
        return uow.repository.delete_item(item_id)
