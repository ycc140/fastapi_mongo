# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-28 19:26:05
     $Rev: 52
"""

# Third party modules
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# Local program modules
from .config.setup import config


# ---------------------------------------------------------
#
class Engine:
    """ MongoDb database async engine class.


    :type db: C{motor.motor_asyncio.AsyncIOMotorDatabase}
    :ivar db: AsyncIOMotorDatabase class instance.
    :type connection: C{motor.motor_asyncio.AsyncIOMotorClient}
    :ivar connection: AsyncIOMotorClient class instance.
    """

    db: AsyncIOMotorDatabase = None
    connection: AsyncIOMotorClient = None

    # ---------------------------------------------------------
    #
    @classmethod
    async def connect_to_mongo(cls):
        """ Initialize DB connection to MongoDb and database. """

        cls.connection = AsyncIOMotorClient(config.mongo_url)
        cls.db = cls.connection.api_db

    # ---------------------------------------------------------
    #
    @classmethod
    async def close_mongo_connection(cls):
        """ Close DB connection. """

        cls.connection.close()
