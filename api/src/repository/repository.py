from abc import ABC, abstractmethod
from src.domain.model import Item
from sqlalchemy import create_engine, text


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
    def __init__(self, username, password, host, database_name, table_name, port=5432):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.table_name = table_name
        self.__engine = self.__create_enginge()

    def __create_enginge(self):
        connection_string = "postgresql://{}:{}@{}:{}/{}".format(
            self.username, self.password, self.host, self.port, self.database_name
        )
        return create_engine(connection_string)

    def get_item(self, item_id):
        sql_statement = text(f"SELECT * FROM {self.table_name} WHERE Id = {item_id}")
        with self.__engine.connect() as conn:
            result = conn.execute(sql_statement).fetchone()
        return Item(**result._asdict())

    def get_items(self):
        sql_statement = text(f"SELECT * FROM {self.table_name}")
        with self.__engine.connect() as conn:
            result = conn.execute(sql_statement).fetchall()
        return [Item(**item._asdict()) for item in result]

    def insert_item(self, item: Item):
        sql_statement = text(
            f"INSERT INTO {self.table_name} (title, description, completed) VALUES(:title, :description, :completed)"
        )
        with self.__engine.connect() as conn:
            try:
                conn.execute(sql_statement, item.dict())
                conn.commit()
                return True
            except Exception as err:
                raise err

    def update_item(self, item_id, item: Item):
        sql_statement = text(
            f"UPDATE {self.table_name} SET title=:title, description=:description, completed=:completed WHERE Id = {item_id}"
        )
        with self.__engine.connect() as conn:
            try:
                conn.execute(sql_statement, item.dict())
                conn.commit()
                return True
            except Exception as err:
                raise err

    def delete_item(self, item_id: int):
        sql_statement = text(f"DELETE FROM {self.table_name} WHERE Id = {item_id}")
        with self.__engine.connect() as conn:
            try:
                conn.execute(sql_statement)
                conn.commit()
                return True
            except Exception as err:
                raise err
