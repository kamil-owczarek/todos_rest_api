"""
Module contains logic for operations on database. 
"""

import logging
from abc import ABC, abstractmethod

from sqlalchemy.orm import Query, Session
from src.domain.model import Item
from src.domain.schema import ItemBaseSchema


class AbstractRepository(ABC):
    """
    Base object for database operations.
    """

    @abstractmethod
    def get_item(self, item_id: int) -> Item:
        """Retrieve Item based on provided Id.

        :param item_id: Id of Item in table.
        :type item_id: int

        :returns: Item object.
        :rtype: Item
        """

        raise NotImplementedError

    @abstractmethod
    def get_items(
        self,
        limit: int,
        offset: int,
        filter_field: str | None,
        filter_value: str | bool | None,
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

        :returns: List of Item objects.
        :rtype: list[Item]
        """

        raise NotImplementedError

    @abstractmethod
    def insert_item(self, item: ItemBaseSchema) -> bool:
        """Insert Item based on provided schema.

        :param item: Body of Item to insert.
        :type item: ItemBaseSchema

        :returns: Operation result.
        :rtype: bool
        """

        raise NotImplementedError

    @abstractmethod
    def update_item(self, item_id: int, item: ItemBaseSchema) -> bool:
        """Update Item based on provided Id and schema.

        :param item_id: Id of Item in table to update.
        :type item_id: int
        :param item: Body of Item to update.
        :type item: ItemBaseSchema

        :returns: Operation result.
        :rtype: bool
        """

        raise NotImplementedError

    @abstractmethod
    def delete_item(self, item_id: int) -> bool:
        """Delete Item based on provided Id.

        :param item_id: Id of Item in table to update.
        :type item_id: int

        :returns: Operation result.
        :rtype: bool
        """

        raise NotImplementedError


class PostgreSqlRepository(AbstractRepository):
    """
    Object for PostgreSQL database operations.

    :param client_session: Connection session to PostgreSQL database.
    :type client_session: Session
    """

    def __init__(self, client_session: Session):
        self.session = client_session

    def get_item(self, item_id: int) -> Item:
        try:
            return self.session.query(Item).filter(Item.id == item_id).first()
        except Exception as err:
            logging.error(f"Caught error during getting Item(Id {item_id}): {err}")
            raise err

    def get_items(
        self,
        limit: int,
        offset: int,
        filter_field: str | None,
        filter_value: str | bool | None,
    ) -> list[Item]:
        def __prepare_query_filters(
            query: Query,
            filter_field: str | None,
            filter_value: str | bool | None,
        ) -> Query:
            match filter_field:
                case "title":
                    query = query.filter(Item.title.contains(filter_value))
                case "description":
                    query = query.filter(Item.description.contains(filter_value))
                case "completed":
                    query = query.filter(Item.completed == filter_value)
            return query

        try:
            query = self.session.query(Item)
            query = __prepare_query_filters(query, filter_field, filter_value)
            return query.offset(offset).limit(limit).all()
        except Exception as err:
            logging.error(f"Caught error during getting Items: {err}")
            raise err

    def insert_item(self, item: ItemBaseSchema):
        try:
            db_item = Item(**item.dict())
            self.session.add(db_item)
            self.session.commit()
            self.session.refresh(db_item)
            return True
        except Exception as err:
            logging.error(f"Caught error during Item upload: {err}")
            raise err

    def update_item(self, item_id: int, item: ItemBaseSchema):
        try:
            self.session.query(Item).filter(Item.id == item_id).update(
                {
                    Item.title: item.title,
                    Item.description: item.description,
                    Item.completed: item.completed,
                }
            )
            self.session.commit()
            return True
        except Exception as err:
            logging.error(f"Caught error during Item(Id: {item_id}) update: {err}")
            raise err

    def delete_item(self, item_id: int):
        try:
            self.session.query(Item).filter(Item.id == item_id).delete()
            self.session.commit()
            return True
        except Exception as err:
            logging.error(f"Caught error during Item(Id: {item_id}) deletion: {err}")
            raise err
