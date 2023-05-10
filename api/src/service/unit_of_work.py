from abc import ABC
from src.service.connector import PostgresConnector
from src.repository.repository import AbstractRepository, PostgresRepository
import logging


class AbstractUnitOfWork(ABC):
    repository: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        logging.debug("Exiting context. Closing connection to database.")


class PostgresUnitOfWork(AbstractUnitOfWork):
    def __init__(self, connection: dict):
        self.session_factory = PostgresConnector(**connection)

    def __enter__(self):
        try:
            self.session = self.session_factory.connect()
            self.repository = PostgresRepository(self.session)
            super().__enter__()
        except Exception as err:
            if self.session_factory.connection != None:
                self.session_factory.connection.close()
            raise err

    def __exit__(self, *args):
        super().__exit__(*args)
        try:
            self.session_factory.disconnect()
        except Exception as err:
            raise err
