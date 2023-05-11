import logging
from abc import ABC

from src.repository.repository import AbstractRepository, PostgresRepository
from src.service.session import PostgresSession


class AbstractUnitOfWork(ABC):
    repository: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        logging.debug("Exiting context. Closing connection to database.")


class PostgresUnitOfWork(AbstractUnitOfWork):
    def __init__(self, connection):
        self.session = PostgresSession(**connection)

    def __enter__(self):
        try:
            self.session = self.session.create_session()
            self.repository = PostgresRepository(self.session)
            super().__enter__()
        except Exception as err:
            if self.session != None:
                self.session.close()
            raise err

    def __exit__(self, *args):
        super().__exit__(*args)
        try:
            self.session.close()
        except Exception as err:
            raise err
