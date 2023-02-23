# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: MIT

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-21 18:00:32
     $Rev: 24
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
ROUTER = APIRouter()


# ---------------------------------------------------------
#
@ROUTER.post(
    "/items",
    response_model=ItemSchema,
    status_code=status.HTTP_201_CREATED,
)
def add_item(payload: ItemSchema) -> ItemSchema:
    """ Add Item to DB.

    :raises HTTPException 409: When Item already exists in DB.
    """

    if payload.id not in items:
        errmsg = f"Item with id='{payload.id}' already exists in DB"
        raise HTTPException(status_code=409, detail=errmsg)

    items[payload.id] = payload

    return payload


# ---------------------------------------------------------
#
@ROUTER.get(
    "/items",
    response_model=List[ItemSchema]
)
def get_all_items() -> List[ItemSchema]:
    """ Get all items from DB. """

    return list(items.values())


# ---------------------------------------------------------
#
@ROUTER.get(
    "/items/{item_id}",
    response_model=ItemSchema,
)
def query_item_by_id(item_id: UUID4) -> ItemSchema:
    """ Extract Item for matching key from DB.

    :raises HTTPException 404: When Item is not found in DB.
    """

    if item_id not in items:
        errmsg = f"{item_id=} not found in DB"
        raise HTTPException(status_code=404, detail=errmsg)

    return items[item_id]


# ---------------------------------------------------------
#
@ROUTER.get(
    "/items/",
    response_model=ItemArgumentResponse,
)
def query_item_by_parameters(
        name: str | None = None,
        count: int | None = None,
        price: float | None = None,
        category: Category | None = None,
) -> ItemArgumentResponse:
    """ Query item(s) using URL parameters.

    :raises HTTPException 400: When no values provided for Item query.
    """

    def match(item: ItemSchema):
        """ Check if the item matches the query arguments from the outer scope. """

        return all(
            (
                name is None or item.name == name,
                count is None or item.count == count,
                price is None or item.price == price,
                category is None or item.category is category,
            )
        )

    if all(info is None for info in (name, price, count, category)):
        errmsg = "No parameters provided for Item query"
        raise HTTPException(status_code=400, detail=errmsg)

    matching_items = [item for item in items.values() if match(item)]
    arguments = QueryArguments(name=name, price=price, count=count, category=category)

    return ItemArgumentResponse(query=arguments, selection=matching_items)


# ---------------------------------------------------------
# The 'responses' keyword allows you to specify which responses a user can expect from this endpoint.
# The Query and Path classes also allow us to add documentation to query and path parameters.
#
@ROUTER.put(
    "/items/{item_id}",
    response_model=ItemSchema,
)
def update_item(
        item_id: UUID4,
        name: str | None = Query(default=None),
        count: int | None = Query(default=None),
        price: float | None = Query(default=None),
) -> ItemSchema:
    """ Update specified item in DB.

    :raises HTTPException 404: When Item not found in DB.<br>
    :raises HTTPException 400: When no values provided for Item update.
    """

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
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description='Item was successfully deleted'
)
async def delete_item(item_id: UUID4):
    """ Delete Item for matching key from DB.

    :raises HTTPException 404: When Item not found in DB.
    """

    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"{item_id=} not found in DB")

    else:
        del items[item_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)
