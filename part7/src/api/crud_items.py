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
from fastapi import HTTPException
from pymongo.results import DeleteResult

# Local modules
from ..db import Engine
from ..schemas import (ItemPayload, ItemModel, QueryArguments)


# ---------------------------------------------------------
#
def _match(item: dict, args: QueryArguments) -> bool:
    """ Check if the item matches the query arguments.

    Note that there is a check in the API layer that verifies that at
    least one of the query parameters has a value, so we don't need
    to do that here.

    :param item: Item object from the DB.
    :param args: URL query arguments.
    :return: Match status.
    """
    return all(
        (
            args.price is None or item['price'] == args.price,
            args.count is None or item['count'] == args.count,
            args.name is None or item['name'].lower() == args.name.lower(),
            args.category is None or item['category'] == args.category.value,
        )
    )


# ---------------------------------------------------------
#
async def create(payload: ItemPayload) -> ItemModel:
    """ Create Item in DB collection api_db.items.

    :param payload: New Item payload.
    :return: DB create response.
    :except HTTPException (400): Create failed for item_id in collection api_db.items.
    """
    db_item = ItemModel(**payload.model_dump())
    response = await Engine.db.items.insert_one(db_item.to_mongo())

    if not response.acknowledged:
        errmsg = f"Create failed for id='{db_item.id}' in api_db.items"
        raise HTTPException(status_code=400, detail=errmsg)

    return db_item


# ---------------------------------------------------------
#
async def read_all() -> List[ItemModel]:
    """ Read all existing Items in DB collection api_db.items.

    :return: List of found Items.
    """
    result = []

    async for item in Engine.db.items.find({}):
        result.append(ItemModel.from_mongo(item))

    return result


# ---------------------------------------------------------
#
async def read(key: UUID) -> ItemModel:
    """ Read Item for a matching index key from DB collection api_db.items.

    :param key: Index key.
    :return: Found Item.
    """
    response = await Engine.db.items.find_one({"_id": str(key)})

    return ItemModel.from_mongo(response)


# ---------------------------------------------------------
#
async def query(arguments: QueryArguments) -> List[ItemModel]:
    """ Read all Items that match the query arguments from DB collection api_db.items.

    :param arguments: Search arguments.
    :return: List of found Items.
    """
    result = []

    async for item in Engine.db.items.find({}):

        if _match(item, arguments):
            result.append(ItemModel.from_mongo(item))

    return result


# ---------------------------------------------------------
#
async def update(payload: ItemModel) -> bool:
    """ Update Item in DB collection api_db.items.

    :param payload: Updated Item payload.
    :return: DB update result.
    """
    key = payload.id
    base = ItemPayload(**payload.dict())
    response = await Engine.db.items.update_one({"_id": str(key)},
                                                {"$set": {**base.dict()}})

    return response.raw_result['updatedExisting']


# ---------------------------------------------------------
#
async def delete(key: UUID) -> DeleteResult:
    """ Delete Item for a matching index key from DB collection api_db.items.

    :param key: Index key.

    :return: DB delete result.
    """
    return await Engine.db.items.delete_one({"_id": str(key)})
