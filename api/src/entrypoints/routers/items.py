"""
Module contains FastAPI items routes.
"""


from fastapi import APIRouter, Depends, Query, Response
from src.adapters.session import PostgreSqlSession
from src.domain.model import Item
from src.domain.schema import ItemBaseSchema, ItemSchema
from src.service_layer import services
from src.service_layer.unit_of_work import PostgreSqlUnitOfWork

router = APIRouter(tags=["items"], prefix="/items")


def uow():
    """
    Unit of work dependency.
    """
    try:
        session = PostgreSqlSession()
        return PostgreSqlUnitOfWork(session)
    except Exception as err:
        raise err


@router.get(
    "",
    response_model=list[ItemSchema],
    description="Retrieve todo items based on the provided filters.",
    responses={
        204: {"description": "No Content"},
        403: {"description": "Invalid token"},
    },
)
def get_items(
    limit: int = Query(20, ge=0, description="Limit page items size."),
    offset: int = Query(0, ge=0, description="Page number."),
    filter_field: str | None = Query(None, description="Filtering field name."),
    filter_value: str | bool | None = Query(None, description="Filter value."),
    uow_session=Depends(uow),
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

    return services.get_items(
        limit,
        offset,
        filter_field,
        filter_value,
        uow=uow_session,
    )


@router.get(
    "/{item_id}",
    response_model=ItemSchema,
    description="Retrieve todo item based on the provided ID.",
    responses={
        403: {"description": "Invalid token"},
        404: {"description": "ID not found!"},
    },
)
def get_item(item_id: int, uow_session=Depends(uow)) -> Item:
    """Retrieve Item based on provided Id.

    :param item_id: Id of Item in table.
    :type item_id: int

    :returns: Item object.
    :rtype: Item
    """

    return services.get_item(item_id, uow=uow_session)


@router.post(
    "",
    description="Upload todo item with provided title, description and completed flag.",
    responses={
        201: {"description": "Created"},
        403: {"description": "Invalid token"},
    },
)
def post_item(item: ItemBaseSchema, uow_session=Depends(uow)):
    """Insert Item based on provided schema.

    :param item: Body of Item to insert.
    :type item: ItemBaseSchema

    :returns: Response code.
    :rtype: Response
    """

    services.insert_item(item, uow=uow_session)
    return Response(status_code=201)


@router.patch(
    "/{item_id}",
    description="Update todo item based on ID.",
    responses={
        204: {"description": "Not Content"},
        403: {"description": "Invalid token"},
    },
)
def patch_item(item_id: int, item: ItemBaseSchema, uow_session=Depends(uow)):
    """Update Item based on provided Id and schema.

    :param item_id: Id of Item in table to update.
    :type item_id: int
    :param item: Body of Item to update.
    :type item: ItemBaseSchema

    :returns: Response code.
    :rtype: Response
    """

    services.update_item(item_id, item, uow=uow_session)
    return Response(status_code=204)


@router.delete(
    "/{item_id}",
    description="Delete todo item based on provided ID.",
    responses={
        204: {"description": "Not Content"},
        403: {"description": "Invalid token"},
    },
)
def delete_item(item_id: int, uow_session=Depends(uow)):
    """Delete Item based on provided Id.

    :param item_id: Id of Item in table to update.
    :type item_id: int

    :returns: Response code.
    :rtype: Response
    """

    services.delete_item(item_id, uow=uow_session)
    return Response(status_code=204)
