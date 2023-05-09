import logging
from abc import ABC, abstractmethod

from sqlalchemy import Row, text
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
        self.table_name = "Items"

    def get_item(self, item_id):
        try:
            sql_statement = text(
                f"SELECT * FROM {self.table_name} WHERE Id = {item_id}"
            )
            result = self.session.execute(sql_statement).fetchone()
            if not isinstance(result, Row):
                raise IdNotFound
            return Item(**result._asdict())
        except Exception as err:
            logging.error(
                f"Caught error during getting Item(Id {item_id}): {type(err)}"
            )
            raise err

    def get_items(self):
        try:
            sql_statement = text(f"SELECT * FROM {self.table_name} WHERE Id")
            result = self.session.execute(sql_statement).fetchall()
            return [Item(**item._asdict()) for item in result]
        except Exception as err:
            logging.error(f"Caught error during getting Items: {type(err)}")
            raise err

    def insert_item(self, item: Item):
        try:
            sql_statement = text(
                f"INSERT INTO {self.table_name} (title, description, completed) VALUES(:title, :description, :completed)"
            )
            self.session.execute(sql_statement, item.dict())
            self.session.commit()
            return True
        except Exception as err:
            logging.error(f"Caught error during Item upload: {err}")
            raise err

    def update_item(self, item_id, item: Item):
        try:
            sql_statement = text(
                f"UPDATE {self.table_name} SET title=:title, description=:description, completed=:completed WHERE Id = {item_id}"
            )
            self.session.execute(sql_statement, item.dict())
            self.session.commit()
            return True
        except Exception as err:
            logging.error(f"Caught error during Item(Id: {item_id}) update: {err}")
            raise err

    def delete_item(self, item_id: int):
        try:
            sql_statement = text(f"DELETE FROM {self.table_name} WHERE Id = {item_id}")
            self.session.execute(sql_statement)
            self.session.commit()
            return True
        except Exception as err:
            logging.error(f"Caught error during Item(Id: {item_id}) deletion: {err}")
            raise err
