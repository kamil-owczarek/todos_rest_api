"""
Module stores ORM models.
"""


from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Item(Base):
    """
    Item object creates ORM model for record in Items table.

    :param id: Id column record value. Id column is primary key.
    :type id: Column
    :param title: Title column record value.
    :type title: Column
    :param description: Description column record value.
    :type description: Column
    :param completed: Completed column record value.
    :type completed: Column
    """

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, index=True, default=False)
