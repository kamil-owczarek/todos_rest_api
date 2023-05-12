from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings


class AbstractSession(ABC):
    @abstractmethod
    def create_session(self):
        raise NotImplementedError


class PostgresSession(AbstractSession):
    def __init__(self):
        self.username = settings.db_user
        self.password = settings.db_password
        self.host = settings.db_host
        self.port = settings.db_port
        self.database_name = settings.db_name
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
