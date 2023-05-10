import logging
from abc import ABC, abstractmethod

from sqlalchemy import text
from src.domain.model import Item
from src.utils.exceptions import IdNotFound


class AbstractRepository(ABC):
    @abstractmethod
    def get_items(self):
        raise NotImplementedError

    @abstractmethod
    def get_item(self, item_id: int):
        raise NotImplementedError

    @abstractmethod
    def insert_item(self, item: Item):
        raise NotImplementedError

    @abstractmethod
    def update_item(self, item_id, item: Item):
        raise NotImplementedError

    @abstractmethod
    def delete_item(self, item_id):
        raise NotImplementedError


class PostgresRepository(AbstractRepository):
    def __init__(self, client_session):
        self.session = client_session

    def get_item(self, item_id):
        try:
            self.__check_if_item_exists(item_id)
            sql_statement = text("SELECT * FROM Items WHERE Id = :item_id")
            result = self.session.execute(
                sql_statement, {"item_id": item_id}
            ).fetchone()
            return Item(**result._asdict())
        except IdNotFound as err:
            logging.debug(f"Item with d: {item_id} not found in database!")
            raise err
        except Exception as err:
            logging.error(f"Caught error during getting Item(Id {item_id}): {err}")
            raise err

    def get_items(self):
        try:
            sql_statement = text("SELECT * FROM Items")
            result = self.session.execute(sql_statement).fetchall()
            return [Item(**item._asdict()) for item in result]
        except Exception as err:
            logging.error(f"Caught error during getting Items: {err}")
            raise err

    def insert_item(self, item: Item):
        try:
            sql_statement = text(
                "INSERT INTO Items (title, description, completed) VALUES(:title, :description, :completed)"
            )
            self.session.execute(sql_statement, item.dict())
            self.session.commit()
            return True
        except Exception as err:
            logging.error(f"Caught error during Item upload: {err}")
            raise err

    def update_item(self, item_id, item: Item):
        try:
            self.__check_if_item_exists(item_id)
            sql_statement = text(
                "UPDATE Items SET title=:title, description=:description, completed=:completed WHERE Id = :item_id"
            )
            self.session.execute(sql_statement, {**item.dict(), "item_id": item_id})
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
            sql_statement = text("DELETE FROM Items WHERE Id = :item_id")
            self.session.execute(sql_statement, {"item_id": item_id})
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
            sql_statement = text("SELECT COUNT(*) FROM Items WHERE Id = :item_id")
            result = self.session.execute(sql_statement, {"item_id": item_id}).first()
            if result[0] > 0:
                return True
            else:
                raise IdNotFound
        except IdNotFound as err:
            raise err
        except Exception as err:
            logging.error(f"Caught error during retrieving Item from database: {err}")
            raise err
