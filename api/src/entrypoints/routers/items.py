"""
Module contains FastAPI items routes.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from src.auth.token import JWTToken
from src.domain.model import Item
from src.domain.schema import ItemBaseSchema, ItemSchema
from src.service import services
from src.service.unit_of_work import PostgreSqlUnitOfWork
from src.utils.exceptions import IdNotFound

router = APIRouter(
    tags=["items"],
    prefix="/items",
    dependencies=[Depends(JWTToken())],
)


@router.get(
    "",
    response_model=list[ItemSchema],
    description="Retrieve todo items based on the provided filters.",
)
def get_items(
    limit: int = Query(20, ge=0, description="Limit page items size."),
    offset: int = Query(0, ge=0, description="Page number."),
    filter_field: str | None = Query(None, description="Filtering field name."),
    filter_value: str | bool | None = Query(None, description="Filter value."),
) -> list[Item]:
    """Retrieve Items based on provided parameters.

    :param limit: Limit page items size. Default: 20.
    :type limit: int
    :param offset: Page number. Default: 0.
    :type offset: int
    :param filter_field: Filtering field name.
    :type filter_field: str | None
    :param filter_value: Filter value.
    :type filter_value: str | bool | None

    :returns: List of Item objects.
    :rtype: list[Item]
    """

    try:
        results = services.get_items(
            limit,
            offset,
            filter_field,
            filter_value,
            uow=PostgreSqlUnitOfWork(),
        )
        if not results:
            return Response(status_code=204)
        return results
    except Exception as err:
        logging.error(f"Caught error during getting Items: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/{item_id}",
    response_model=ItemSchema,
    description="Retrieve todo item based on the provided ID.",
)
def get_item(item_id: int) -> Item:
    """Retrieve Item based on provided Id.

    :param item_id: Id of Item in table.
    :type item_id: int

    :returns: Item object.
    :rtype: Item
    """

    try:
        return services.get_item(item_id, uow=PostgreSqlUnitOfWork())
    except IdNotFound:
        raise HTTPException(
            status_code=404, detail=f"Item with ID: {item_id} not found!"
        )
    except Exception as err:
        logging.error(f"Caught error during getting Item: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post(
    "",
    description="Upload todo item with provided title, description and completed flag.",
)
def post_item(item: ItemBaseSchema):
    """Insert Item based on provided schema.

    :param item: Body of Item to insert.
    :type item: ItemBaseSchema

    :returns: Response code.
    :rtype: Response
    """

    try:
        services.insert_item(item, uow=PostgreSqlUnitOfWork())
        return Response(status_code=201)
    except Exception as err:
        logging.error(f"Caught error during inserting Item: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch(
    "/{item_id}",
    description="Update todo item based on ID.",
    dependencies=[Depends(JWTToken())],
)
def patch_item(item_id: int, item: ItemBaseSchema):
    """Update Item based on provided Id and schema.

    :param item_id: Id of Item in table to update.
    :type item_id: int
    :param item: Body of Item to update.
    :type item: ItemBaseSchema

    :returns: Response code.
    :rtype: Response
    """

    try:
        services.update_item(item_id, item, uow=PostgreSqlUnitOfWork())
        return Response(status_code=204)
    except IdNotFound:
        raise HTTPException(
            status_code=404, detail=f"Item with ID: {item_id} not found!"
        )
    except Exception as err:
        logging.error(f"Caught error during updating Item: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete(
    "/{item_id}",
    description="Delete todo item based on provided ID.",
)
def delete_item(item_id: int):
    """Delete Item based on provided Id.

    :param item_id: Id of Item in table to update.
    :type item_id: int

    :returns: Response code.
    :rtype: Response
    """

    try:
        services.delete_item(item_id, uow=PostgreSqlUnitOfWork())
        return Response(status_code=204)
    except IdNotFound:
        raise HTTPException(
            status_code=404, detail=f"Item with ID: {item_id} not found!"
        )
    except Exception as err:
        logging.error(f"Caught error during Item deletion: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
