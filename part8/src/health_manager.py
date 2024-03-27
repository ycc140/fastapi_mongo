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
from typing import List

# Third party modules
from loguru import logger

# local modules
from .db import Engine
from .config.setup import config
from .schemas import HealthResourceModel, HealthResponseModel


# -----------------------------------------------------------------------------
#
class HealthManager:
    """ This class handles health status reporting on used resources. """

    # ---------------------------------------------------------
    #
    @staticmethod
    async def _get_mongo_status() -> List[HealthResourceModel]:
        """ Return MongoDb connection status.

        :return: MongoDb connection status.
        """
        try:
            status = await Engine.is_db_connected()

        except BaseException as why:
            logger.critical(f'MongoDB: {why}')
            status = False

        return [HealthResourceModel(name='MongoDb', status=status)]

    # ---------------------------------------------------------
    #
    async def get_status(self) -> HealthResponseModel:
        """ Return Health status for used resources.

        :return: Service health status.
        """
        resource_items = []
        resource_items += await self._get_mongo_status()
        total_status = all(key.status for key in resource_items)

        return HealthResponseModel(status=total_status,
                                   version=config.version,
                                   name=config.service_name,
                                   resources=resource_items)
