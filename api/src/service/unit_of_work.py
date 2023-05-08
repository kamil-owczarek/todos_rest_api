from abc import ABC, abstractmethod
from src.domain.model import Item

from src.repository.repository import AbstractRepository


class AbstractUnitOfWork(ABC):
    repository: AbstractRepository

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
