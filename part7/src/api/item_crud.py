# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2024-04-26 17:38:52
     $Rev: 9
"""

# BUILTIN modules
from uuid import UUID
from typing import List

# Third party modules
from fastapi import HTTPException
from pymongo.results import DeleteResult

# Local modules
from ..db import AsyncIOMotorClientSession
from ..schemas import (ItemPayload, ItemModel, QueryArguments)


# -----------------------------------------------------------------------------
#
class ItemCrud:
    """ Item CRUD operations.

    This class implements the IRepository protocol for Item CRUD operations.

    :ivar session: Active database session.
    :type session: C{motor.motor_asyncio.AsyncIOMotorClientSession}
    """

    def __init__(self, session: AsyncIOMotorClientSession):
        """ Implicit constructor.

        :param session: Active database session.
        """
        self.session = session

    # ---------------------------------------------------------
    #
    @staticmethod
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
    async def create(self, payload: ItemPayload) -> ItemModel:
        """ Create Item in DB collection api_db.items.

        :param payload: New Item payload.
        :return: DB create response.
        :except HTTPException (400): Create failed for item_id in collection api_db.items.
        """
        db_item = ItemModel(**payload.model_dump())
        response = await self.session.client.api_db.items.insert_one(db_item.to_mongo())

        if not response.acknowledged:
            errmsg = f"Create failed for id='{db_item.id}' in api_db.items"
            raise HTTPException(status_code=400, detail=errmsg)

        return db_item

    # ---------------------------------------------------------
    #
    async def read_all(self) -> List[ItemModel]:
        """ Read all existing Items in DB collection api_db.items.

        :return: List of found Items.
        """
        result = []

        async for item in self.session.client.api_db.items.find({}):
            result.append(ItemModel.from_mongo(item))

        return result

    # ---------------------------------------------------------
    #
    async def read(self, key: UUID) -> ItemModel:
        """ Read Item for a matching index key from DB collection api_db.items.

        :param key: Index key.
        :return: Found Item.
        """
        response = await self.session.client.api_db.items.find_one({"_id": str(key)})

        return ItemModel.from_mongo(response)

    # ---------------------------------------------------------
    #
    async def query(self, arguments: QueryArguments) -> List[ItemModel]:
        """ Read all Items that match the query arguments from DB collection api_db.items.

        :param arguments: Search arguments.
        :return: List of found Items.
        """
        result = []

        async for item in self.session.client.api_db.items.find({}):

            if self._match(item, arguments):
                result.append(ItemModel.from_mongo(item))

        return result

    # ---------------------------------------------------------
    #
    async def update(self, payload: ItemModel) -> bool:
        """ Update Item in DB collection api_db.items.

        :param payload: Updated Item payload.
        :return: DB update result.
        """
        key = payload.id
        base = ItemPayload(**payload.dict())
        response = await self.session.client.api_db.items.update_one({"_id": str(key)},
                                                                     {"$set": {**base.dict()}})

        return response.raw_result['updatedExisting']

    # ---------------------------------------------------------
    #
    async def delete(self, key: UUID) -> DeleteResult:
        """ Delete Item for a matching index key from DB collection api_db.items.

        :param key: Index key.
        :return: DB delete result.
        """
        return await self.session.client.api_db.items.delete_one({"_id": str(key)})
