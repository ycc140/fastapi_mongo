# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-03-01 18:03:44
     $Rev: 58
"""

# BUILTIN modules
from typing import List

# Third party modules
from loguru import logger

# local modules
from .db import Engine
from .schemas import ResourceModel


# ---------------------------------------------------------
#
async def get_mongo_status() -> List[ResourceModel]:
    """ Return MongoDb connection status.

    :return: MongoDb connection status.
    """

    try:
        await Engine.connection.server_info()
        status = True

    except BaseException as why:
        logger.critical(f'MongoDB: {why}')
        status = False

    return [ResourceModel(name='MongoDb', status=status)]
