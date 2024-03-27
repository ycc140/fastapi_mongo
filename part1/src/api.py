# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2024-03-27 15:22:03
     $Rev: 4
"""

# BUILTIN modules
from uuid import UUID
from typing import List

# Third party modules
from fastapi.responses import Response
from fastapi import HTTPException, APIRouter, status, Query

# Local modules
from .db import items
from .schemas import (Category, ItemPayload, ItemModel,
                      QueryArguments, ItemArgumentResponse)

# Constants
ROUTER = APIRouter(prefix="/items")


# ---------------------------------------------------------
#
@ROUTER.post(
    "",
    response_model=ItemModel,
    status_code=status.HTTP_201_CREATED,
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
)
def query_item_by_id(item_id: UUID) -> ItemModel:
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
    response_model=ItemModel,
)
def update_item(
        item_id: UUID,
        name: str | None = Query(default=None),
        count: int | None = Query(default=None),
        price: float | None = Query(default=None),
) -> ItemModel:
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
async def delete_item(item_id: UUID):
    """ ***Delete Item for matching item_id from DB.*** """
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"{item_id=} not found in DB")

    else:
        del items[item_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)
