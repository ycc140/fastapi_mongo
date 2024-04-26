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
from typing import Protocol

# Third party modules
from pymongo.results import DeleteResult

# Local modules
from ..db import AsyncIOMotorClientSession
from ..schemas import ItemModel, ItemPayload, QueryArguments


# -----------------------------------------------------------------------------
#
class ICrudRepository(Protocol):
    """ Item CRUD Interface class.

    :ivar session: Active database session.
    """
    session: AsyncIOMotorClientSession

    async def create(self, payload: ItemPayload) -> ItemModel:
        """ Create Item in DB collection api_db.items.

        :param payload: New Item payload.
        :return: DB create response.
        :except HTTPException (400): Create failed for item_id in collection api_db.items.
        """

    async def read_all(self) -> List[ItemModel]:
        """ Read all existing Items in DB collection api_db.items.

        :return: List of found Items.
        """

    async def read(self, key: UUID) -> ItemModel:
        """ Read Item for a matching index key from DB collection api_db.items.

        :param key: Index key.
        :return: Found Item.
        """

    async def query(self, arguments: QueryArguments) -> List[ItemModel]:
        """ Read all Items that match the query arguments from DB collection api_db.items.

        :param arguments: Search arguments.
        :return: List of found Items.
        """

    async def update(self, payload: ItemModel) -> bool:
        """ Update Item in DB collection api_db.items.

        :param payload: Updated Item payload.
        :return: DB update result.
        """

    async def delete(self, key: UUID) -> DeleteResult:
        """ Delete Item for a matching index key from DB collection api_db.items.

        :param key: Index key.
        :return: DB delete result.
        """
