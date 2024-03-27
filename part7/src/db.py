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

# Third party modules
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# Local program modules
from .config.setup import config


# ---------------------------------------------------------
#
class Engine:
    """ MongoDb database async engine class.


    :ivar db: AsyncIOMotorDatabase class instance.
    :type db: motor.motor_asyncio.AsyncIOMotorDatabase
    :ivar connection: AsyncIOMotorClient class instance.
    :type connection: motor.motor_asyncio.AsyncIOMotorClient
    """
    db: AsyncIOMotorDatabase = None
    connection: AsyncIOMotorClient = None

    # ---------------------------------------------------------
    #
    @classmethod
    async def connect_to_mongo(cls):
        """ Initialize DB connection to MongoDb and database.

        Setting server connection timeout to 5 (default is 30) seconds.
        """
        cls.connection = AsyncIOMotorClient(config.mongo_url,
                                            serverSelectionTimeoutMS=5000)
        cls.db = cls.connection.api_db

    # ---------------------------------------------------------
    #
    @classmethod
    async def close_mongo_connection(cls):
        """ Close DB connection. """
        cls.connection.close()

    # ---------------------------------------------------------
    #
    @classmethod
    async def is_db_connected(cls) -> bool:
        """ Return MongoDB connection status. """
        return bool(cls.connection.server_info())
