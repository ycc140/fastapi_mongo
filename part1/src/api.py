# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-24 20:27:01
     $Rev: 39
"""

# BUILTIN modules
from typing import List

# Third party modules
from pydantic import UUID4
from fastapi.responses import Response
from fastapi import HTTPException, APIRouter, status, Query

# Local modules
from .db import items
from .schemas import (Category, ItemSchema, QueryArguments, ItemArgumentResponse)

# Constants
ROUTER = APIRouter(prefix="/items")


# ---------------------------------------------------------
#
@ROUTER.post(
    "",
    response_model=ItemSchema,
    status_code=status.HTTP_201_CREATED,
)
def add_item(payload: ItemSchema) -> ItemSchema:
    """ ***Add Item to DB.*** """

    if payload.id not in items:
        errmsg = f"Item with id='{payload.id}' already exists in DB"
        raise HTTPException(status_code=409, detail=errmsg)

    items[payload.id] = payload

    return payload


# ---------------------------------------------------------
#
@ROUTER.get(
    "",
    response_model=List[ItemSchema]
)
def get_all_items() -> List[ItemSchema]:
    """ ***Read all Items from DB.*** """

    return list(items.values())


# ---------------------------------------------------------
#
@ROUTER.get(
    "/{item_id}",
    response_model=ItemSchema,
)
def query_item_by_id(item_id: UUID4) -> ItemSchema:
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
)
def query_item_by_parameters(
        name: str | None = None,
        count: int | None = None,
        price: float | None = None,
        category: Category | None = None,
) -> ItemArgumentResponse:
    """ ***Read item(s) using URL query parameters.*** """

    def match(item: ItemSchema) -> bool:
        """ Return all parameters match status with outer scope Item. """

        return all(
            (
                name is None or item.name == name,
                count is None or item.count == count,
                price is None or item.price == price,
                category is None or item.category is category,
            )
        )

    # Verify that at least one of the query parameters have a value since
    # we don't want to extract all Items, get_all_items() already does that.
    if all(info is None for info in (name, price, count, category)):
        errmsg = "No parameters provided for Item query"
        raise HTTPException(status_code=400, detail=errmsg)

    matching_items = [item for item in items.values() if match(item)]
    arguments = QueryArguments(name=name, price=price, count=count, category=category)

    return ItemArgumentResponse(query=arguments, selection=matching_items)


# ---------------------------------------------------------
#
@ROUTER.put(
    "/{item_id}",
    response_model=ItemSchema,
)
def update_item(
        item_id: UUID4,
        name: str | None = Query(default=None),
        count: int | None = Query(default=None),
        price: float | None = Query(default=None),
) -> ItemSchema:
    """ ***Update Item for matching item_id in DB.*** """

    if all(info is None for info in (name, price, count)):
        errmsg = "No parameters provided for Item update"
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
    response_description='Item was successfully deleted'
)
async def delete_item(item_id: UUID4):
    """ ***Delete Item for matching item_id from DB.*** """

    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"{item_id=} not found in DB")

    else:
        del items[item_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)
