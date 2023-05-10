import logging
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from src.domain.model import Item, ItemBaseSchema
from src.utils.exceptions import IdNotFound


class AbstractRepository(ABC):
    @abstractmethod
    def get_items(self) -> list[Item]:
        raise NotImplementedError

    @abstractmethod
    def get_item(self, item_id: int) -> Item:
        raise NotImplementedError

    @abstractmethod
    def insert_item(self, item: ItemBaseSchema):
        raise NotImplementedError

    @abstractmethod
    def update_item(self, item_id, item: ItemBaseSchema):
        raise NotImplementedError

    @abstractmethod
    def delete_item(self, item_id):
        raise NotImplementedError


class PostgresRepository(AbstractRepository):
    def __init__(self, client_session: Session):
        self.session = client_session

    def get_item(self, item_id) -> Item:
        try:
            self.__check_if_item_exists(item_id)
            return self.session.query(Item).filter(Item.id == item_id).first()
        except IdNotFound as err:
            logging.debug(f"Item with d: {item_id} not found in database!")
            raise err
        except Exception as err:
            logging.error(f"Caught error during getting Item(Id {item_id}): {err}")
            raise err

    def get_items(self, skip: int = 0, limit: int = 100) -> list[Item]:
        try:
            return self.session.query(Item).offset(skip).limit(limit).all()
        except Exception as err:
            logging.error(f"Caught error during getting Items: {err}")
            raise err

    def insert_item(self, item: ItemBaseSchema):
        try:
            db_item = Item(**item.dict())
            self.session.add(db_item)
            self.session.commit()
            self.session.refresh(db_item)
            return db_item
        except Exception as err:
            logging.error(f"Caught error during Item upload: {err}")
            raise err

    def update_item(self, item_id, item: ItemBaseSchema):
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
