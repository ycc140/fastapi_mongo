# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-03-01 19:25:11
     $Rev: 60
"""

# BUILTIN modules
from typing import List

# Third party modules
from bson import errors
from pymongo import errors
from pydantic import UUID4
from fastapi.responses import Response
from fastapi import HTTPException, APIRouter, status, Query, Path, Depends

# Local modules
from . import crud_items as crud
from ..security import validate_authentication
from ..schemas import (Category, ItemSchema, QueryArguments,
                       ItemArgumentResponse, AlreadyExistError,
                       NotFoundError, NoArgumentsError, DbOperationFailedError)

# Constants
ROUTER = APIRouter(prefix="/v1/items", tags=["items"],
                   dependencies=[Depends(validate_authentication)])


# ---------------------------------------------------------
#
@ROUTER.post(
    "",
    response_model=ItemSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": AlreadyExistError},
        400: {"model": DbOperationFailedError}}
)
async def add_item(payload: ItemSchema) -> ItemSchema:
    """ ***Add Item to api_db.items.*** """

    try:
        successful = await crud.create(payload)

    except errors.DuplicateKeyError:
        errmsg = f"Item with id='{payload.id}' already exists in api_db.items"
        raise HTTPException(status_code=409, detail=errmsg)

    if not successful:
        errmsg = f"Create failed for id='{payload.id}' in api_db.items"
        raise HTTPException(status_code=400, detail=errmsg)

    return payload


# ---------------------------------------------------------
#
@ROUTER.get(
    "",
    response_model=List[ItemSchema],
)
async def get_all_items() -> List[ItemSchema]:
    """ ***Read all Items from api_db.items.*** """

    return await crud.read_all()


# ---------------------------------------------------------
#
@ROUTER.get(
    "/{item_id}",
    response_model=ItemSchema,
    responses={404: {"model": NotFoundError}},
)
async def query_item_by_id(item_id: UUID4) -> ItemSchema:
    """ ***Read Item for matching item_id from api_db.items.*** """

    response = await crud.read(item_id)

    if not response:
        errmsg = f"{item_id=} not found in api_db.items"
        raise HTTPException(status_code=404, detail=errmsg)

    return response


# ---------------------------------------------------------
#
@ROUTER.get(
    "/",
    response_model=ItemArgumentResponse,
    responses={406: {"model": NoArgumentsError}},
)
async def query_item_by_parameters(
        name: str | None = None,
        count: int | None = None,
        price: float | None = None,
        category: Category | None = None,
) -> ItemArgumentResponse:
    """ ***Read item(s) using URL query parameters.***

    Note that this is a non-indexed search that traverses all Items
    in the collection to find the Items that match the search criteria.
    """

    # Verify that at least one of the query parameters have a value since
    # we don't want to extract all Items, get_all_items() already does that.
    if all(info is None for info in (name, price, count, category)):
        errmsg = "No query values provided in query URL"
        raise HTTPException(status_code=406, detail=errmsg)

    arguments = QueryArguments(name=name, price=price, count=count, category=category)
    response = await crud.query(arguments)

    return ItemArgumentResponse(query=arguments, selection=response)


# ---------------------------------------------------------
#
@ROUTER.put(
    "/{item_id}",
    response_model=ItemSchema,
    responses={
        404: {"model": NotFoundError},
        406: {"model": NoArgumentsError},
        400: {"model": DbOperationFailedError}}
)
async def update_item(
        item_id: UUID4 = Path(
            title="Item ID",
            description="Unique identifier that specifies an item",
        ),
        name: str | None = Query(
            min_length=1,
            max_length=8,
            default=None,
            title="Name",
            description="New name of the item",
        ),
        count: int | None = Query(
            ge=0,
            default=None,
            title="Count",
            description="New amount of instances of this item in stock",
        ),
        price: float | None = Query(
            gt=0.0,
            default=None,
            title="Price",
            description="New price of the item in Euro",
        ),
) -> ItemSchema:
    """ ***Update Item for matching item_id in api_db.items.*** """

    # Verify that at least one of the query parameters have a value since
    # we don't want to extract all Items, get_all_items() already does that.
    if all(info is None for info in (name, price, count)):
        errmsg = "No query values provided in update URL"
        raise HTTPException(status_code=406, detail=errmsg)

    response = await crud.read(item_id)

    if not response:
        errmsg = f"{item_id=} not found in api_db.items"
        raise HTTPException(status_code=404, detail=errmsg)

    if name is not None:
        response.name = name
    if price is not None:
        response.price = price
    if count is not None:
        response.count = count

    successful = await crud.update(response)

    if not successful:
        errmsg = f"Failed updating {item_id=} in api_db.items"
        raise HTTPException(status_code=400, detail=errmsg)

    return response


# ---------------------------------------------------------
#
@ROUTER.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": NotFoundError}},
    response_description='Item was successfully deleted'
)
async def delete_item(item_id: UUID4):
    """ ***Delete Item for matching item_id from api_db.items.*** """

    response = await crud.delete(item_id)

    if response.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"{item_id=} not found in api_db.items")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
