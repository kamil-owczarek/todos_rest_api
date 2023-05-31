"""
Module contains Unit Of Work logic.
"""

import logging
from abc import ABC

from src.adapters.repository import AbstractRepository, PostgreSqlRepository


class AbstractUnitOfWork(ABC):
    """Base object for Unit Of Work logic."""

    repository: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        logging.debug("Exiting context. Closing connection to database.")


class PostgreSqlUnitOfWork(AbstractUnitOfWork):
    """Unit Of Work logic for PostgreSQL database."""

    def __init__(self, session):
        self.session = session

    def __enter__(self):
        try:
            self.session = self.session.create_session()
            self.repository = PostgreSqlRepository(self.session)
            super().__enter__()
        except Exception as err:
            if self.session is not None:
                self.session.close()
            raise err

    def __exit__(self, *args):
        super().__exit__(*args)
        try:
            self.session.close()
        except Exception as err:
            raise err
