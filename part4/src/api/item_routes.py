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
from fastapi.responses import Response
from fastapi import HTTPException, APIRouter, status, Query

# Local modules
from ..db import items
from .documentation import (item_id_documentation,
                            get_query_documentation as get_query_doc,
                            put_query_documentation as put_query_doc)
from ..schemas import (Category, ItemPayload, ItemModel,
                       QueryArguments, ItemArgumentResponse,
                       DbOperationFailedError, NotFoundError, NoArgumentError)

# Constants
ROUTER = APIRouter(prefix="/v1/items", tags=["items"])


# ---------------------------------------------------------
#
@ROUTER.post(
    "",
    response_model=ItemModel,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": DbOperationFailedError}},
)
def add_item(payload: ItemPayload) -> ItemModel:
    """ ***Add Item to DB.*** """
    db_item = ItemModel(**payload.model_dump())
    items[db_item.id] = db_item

    return db_item


# ---------------------------------------------------------
#
@ROUTER.get(
    "",
    response_model=List[ItemModel]
)
def get_all_items() -> List[ItemModel]:
    """ ***Read all Items from DB.*** """

    return list(items.values())


# ---------------------------------------------------------
#
@ROUTER.get(
    "/{item_id}",
    response_model=ItemModel,
    responses={404: {"model": NotFoundError}},
)
def query_item_by_id(item_id: UUID = item_id_documentation) -> ItemModel:
    """ ***Read Item for matching item_id from DB.*** """

    if item_id not in items:
        errmsg = f"{item_id=} not found in DB"
        raise HTTPException(status_code=404, detail=errmsg)

    return items[item_id]


# ---------------------------------------------------------
#
@ROUTER.get(
    "/",
    response_model=ItemArgumentResponse,
    responses={400: {"model": NoArgumentError}},
)
def query_item_by_parameters(
        name: str = Query(**get_query_doc['name']),
        count: int = Query(**get_query_doc['count']),
        price: float = Query(**get_query_doc['price']),
        category: Category = Query(**get_query_doc['category']),
) -> ItemArgumentResponse:
    """ ***Read item(s) using URL query parameters.*** """

    def match(item: ItemModel) -> bool:
        """ Return all parameters match status with outer scope Item. """

        return all(
            (
                count is None or item.count == count,
                price is None or item.price == price,
                category is None or item.category is category,
                name is None or item.name.lower() == name.lower(),
            )
        )

    # Verify that at least one of the query parameters has a value since
    # we don't want to extract all Items (get_all_items() already does that).
    if all(info is None for info in (name, price, count, category)):
        errmsg = "No query values provided in query URL"
        raise HTTPException(status_code=400, detail=errmsg)

    matching_items = [item for item in items.values() if match(item)]
    arguments = QueryArguments(name=name, price=price, count=count, category=category)

    return ItemArgumentResponse(query=arguments, selection=matching_items)


# ---------------------------------------------------------
#
@ROUTER.put(
    "/{item_id}",
    response_model=ItemModel,
    responses={
        404: {"model": NotFoundError},
        400: {"model": NoArgumentError}}
)
def update_item(
        item_id: UUID = item_id_documentation,
        name: str = Query(**put_query_doc['name']),
        count: int = Query(**put_query_doc['count']),
        price: float = Query(**put_query_doc['price']),
) -> ItemModel:
    """ ***Update Item for matching item_id in DB.*** """

    # Verify that at least one of the query parameters has
    # a value; otherwise there's no need to do an update.
    if all(info is None for info in (name, price, count)):
        errmsg = "No query values provided in update URL"
        raise HTTPException(status_code=400, detail=errmsg)

    if item_id not in items:
        errmsg = f"{item_id=} not found in DB"
        raise HTTPException(status_code=404, detail=errmsg)

    item = items[item_id]

    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count

    return item


# ---------------------------------------------------------
#
@ROUTER.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": NotFoundError}},
    response_description='Item was successfully deleted'
)
async def delete_item(item_id: UUID = item_id_documentation):
    """ ***Delete Item for matching item_id from DB.*** """

    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"{item_id=} not found in DB")

    else:
        del items[item_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)
