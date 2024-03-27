# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2024-03-27 05:38:56
     $Rev: 1
"""

# BUILTIN modules
from uuid import UUID
from typing import List

# Third party modules
from fastapi import Depends
from fastapi.responses import Response
from fastapi import HTTPException, APIRouter, status, Query

# Local modules
from . import crud_items as crud
from ..security import validate_authentication
from .documentation import (item_id_documentation,
                            get_query_documentation as get_query_doc,
                            put_query_documentation as put_query_doc)
from ..schemas import (Category, ItemPayload, ItemModel, QueryArguments,
                       ItemArgumentResponse, DbOperationFailedError,
                       NotFoundError, NoArgumentError)

# Constants
ROUTER = APIRouter(prefix="/v1/items", tags=["Items"],
                   dependencies=[Depends(validate_authentication)])


# ---------------------------------------------------------
#
@ROUTER.post(
    "",
    response_model=ItemModel,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": DbOperationFailedError}}
)
async def add_item(payload: ItemPayload) -> ItemModel:
    """  ***Add Item to api_db.items.***

    :param payload: A new item to be added.
    :return: Supplied item.
    """
    return await crud.create(payload)


# ---------------------------------------------------------
#
@ROUTER.get(
    "",
    response_model=List[ItemModel],
)
async def get_all_items() -> List[ItemModel]:
    """ ***Read all Items from api_db.items.***

    :return: All items in the database.
    """
    return await crud.read_all()


# ---------------------------------------------------------
#
@ROUTER.get(
    "/{item_id}",
    response_model=ItemModel,
    responses={404: {"model": NotFoundError}},
)
async def query_item_by_id(item_id: UUID = item_id_documentation) -> ItemModel:
    """ ***Read Item for matching item_id from api_db.items.***

    :param item_id: Item identifier.
    :return: Found item.
    """
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
    responses={406: {"model": NoArgumentError}},
)
async def query_item_by_parameters(
        name: str = Query(**get_query_doc['name']),
        count: int = Query(**get_query_doc['count']),
        price: float = Query(**get_query_doc['price']),
        category: Category = Query(**get_query_doc['category']),
) -> ItemArgumentResponse:
    """ ***Read item(s) using URL query parameters.***

    Note that this is a non-indexed search that traverses all Items
    in the collection to find the Items that match the search criteria.

    :param name: Possible name parameter.
    :param count: Possible count parameter.
    :param price: Possible price parameter.
    :param category: Possible category parameter.
    :return: Found item.
    """
    # Verify that at least one of the query parameters has a value since
    # we don't want to extract all Items (get_all_items() already does that).
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
    response_model=ItemModel,
    responses={
        404: {"model": NotFoundError},
        406: {"model": NoArgumentError},
        400: {"model": DbOperationFailedError}}
)
async def update_item(
        item_id: UUID = item_id_documentation,
        name: str = Query(**put_query_doc['name']),
        count: int = Query(**put_query_doc['count']),
        price: float = Query(**put_query_doc['price']),
) -> ItemModel:
    """ ***Update Item for matching item_id in api_db.items.***

    :param item_id: Item identifier.
    :param name: Possible name for the item.
    :param count: Possible count for the item.
    :param price: Possible price for the item.
    :return: Updated item.
    """
    # Verify that at least one of the query parameters has
    # a value; otherwise there's no need to do an update.
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
async def delete_item(item_id: UUID = item_id_documentation):
    """ ***Delete Item for matching item_id from api_db.items.***

    :param item_id: Item identifier.
    :return: No response content (custom for a deleted item).
    """
    response = await crud.delete(item_id)

    if response.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"{item_id=} not found in api_db.items")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
