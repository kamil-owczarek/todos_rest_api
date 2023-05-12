"""
Module stores models schema.
"""

from pydantic import BaseModel


class ItemBaseSchema(BaseModel):
    """
    ItemBaseSchema object creates based model schema for record which will be inserted to table.

    :param title: Title column record value.
    :type title: str
    :param description: Description column record value.
    :type description: str
    :param completed: Completed column record value. Default: False.
    :type completed: bool
    """

    title: str
    description: str
    completed: bool = False


class ItemSchema(ItemBaseSchema):
    """
    ItemSchema object creates based model schema for record retrieved from table.

    :param id: Id column record value.
    :type id: int
    :param title: Title column record value.
    :type title: str
    :param description: Description column record value.
    :type description: str
    :param completed: Completed column record value. Default: False.
    :type completed: bool
    """

    id: int

    class Config:
        """
        Config object control ItemSchem object behaviour.

        :param orm_mode: Define support for mapping ORM objects.
        :type orm_mode: bool
        """

        orm_mode = True
