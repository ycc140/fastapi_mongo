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

# Third party modules
from fastapi import Depends

# Local modules
from .item_crud import ItemCrud
from ..db import Engine, AsyncIOMotorClientSession


# ---------------------------------------------------------
#
async def get_repository_crud(
        session: AsyncIOMotorClientSession = Depends(Engine.get_async_session)
) -> ItemCrud:
    """ Return Item CRUD operation instance with an active DB session.

    :param session: Active database session.
    :return: Item CRUD object with an active DB session.
    """
    return ItemCrud(session=session)
