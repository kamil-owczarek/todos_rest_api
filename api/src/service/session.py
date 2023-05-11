from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AbstractSession(ABC):
    @abstractmethod
    def create_session(self):
        raise NotImplementedError


class PostgresSession(AbstractSession):
    def __init__(self, username, password, host, database_name, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.__engine = self.__create_enginge()
        self.session = None

    def create_session(self):
        try:
            self.session = sessionmaker(
                autocommit=False, autoflush=False, bind=self.__engine
            )
            return self.session()
        except Exception:
            raise Exception

    def __create_enginge(self):
        connection_string = "postgresql://{}:{}@{}:{}/{}".format(
            self.username, self.password, self.host, self.port, self.database_name
        )
        return create_engine(connection_string)
