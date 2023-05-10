from abc import ABC, abstractmethod

from sqlalchemy import create_engine


class DatabaseConnector(ABC):
    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError


class PostgresConnector(DatabaseConnector):
    def __init__(self, username, password, host, database_name, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.connection = None

    def connect(self):
        try:
            __engine = self.__create_enginge()
            self.connection = __engine.connect()
            return self.connection
        except Exception:
            raise Exception

    def disconnect(self):
        try:
            if self.connection != None:
                self.connection.close()
        except Exception as err:
            raise err

    def __create_enginge(self):
        connection_string = "postgresql://{}:{}@{}:{}/{}".format(
            self.username, self.password, self.host, self.port, self.database_name
        )
        return create_engine(connection_string)
