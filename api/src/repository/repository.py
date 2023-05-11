import logging
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session, Query
from src.domain.model import Item
from src.domain.schema import ItemBaseSchema
from src.utils.exceptions import IdNotFound


class AbstractRepository(ABC):
    @abstractmethod
    def get_item(self, item_id: int) -> Item:
        raise NotImplementedError

    @abstractmethod
    def get_items(
        self,
        limit: int,
        offset: int,
        filter_field: str | None,
        filter_value: str | bool | None,
    ) -> list[Item]:
        raise NotImplementedError

    @abstractmethod
    def insert_item(self, item: ItemBaseSchema) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_item(self, item_id: int, item: ItemBaseSchema) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_item(self, item_id: int) -> bool:
        raise NotImplementedError


class PostgresRepository(AbstractRepository):
    def __init__(self, client_session: Session):
        self.session = client_session

    def get_item(self, item_id: int) -> Item:
        try:
            self.__check_if_item_exists(item_id)
            return self.session.query(Item).filter(Item.id == item_id).first()
        except IdNotFound as err:
            logging.debug(f"Item with d: {item_id} not found in database!")
            raise err
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
        try:
            query = self.session.query(Item)
            query = self.__prepare_query_filters(query, filter_field, filter_value)
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
            self.__check_if_item_exists(item_id)
            self.session.query(Item).filter(Item.id == item_id).update(
                {
                    Item.title: item.title,
                    Item.description: item.description,
                    Item.completed: item.completed,
                }
            )
            self.session.commit()
            return True
        except IdNotFound as err:
            logging.debug(f"Item with d: {item_id} not found in database!")
            raise err
        except Exception as err:
            logging.error(f"Caught error during Item(Id: {item_id}) update: {err}")
            raise err

    def delete_item(self, item_id: int):
        try:
            self.__check_if_item_exists(item_id)
            self.session.query(Item).filter(Item.id == item_id).delete()
            self.session.commit()
            return True
        except IdNotFound as err:
            logging.debug(f"Item with d: {item_id} not found in database!")
            raise err
        except Exception as err:
            logging.error(f"Caught error during Item(Id: {item_id}) deletion: {err}")
            raise err

    def __check_if_item_exists(self, item_id: int) -> bool:
        try:
            result = self.session.query(Item).filter(Item.id == item_id).count()
            if result > 0:
                return True
            else:
                raise IdNotFound
        except IdNotFound as err:
            raise err
        except Exception as err:
            logging.error(f"Caught error during retrieving Item from database: {err}")
            raise err

    def __prepare_query_filters(
        self, query: Query, filter_field: str | None, filter_value: str | bool | None
    ) -> Query:
        match filter_field:
            case "title":
                query = query.filter(Item.title.contains(filter_value))
            case "description":
                query = query.filter(Item.description.contains(filter_value))
            case "completed":
                query = query.filter(Item.completed == filter_value)
        return query
