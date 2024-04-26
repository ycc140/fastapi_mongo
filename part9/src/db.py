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
from motor.motor_asyncio import (AsyncIOMotorClient,
                                 AsyncIOMotorDatabase,
                                 AsyncIOMotorClientSession)

# Local program modules
from .config.setup import config


# ---------------------------------------------------------
#
class Engine:
    """ MongoDb database async engine class.


    :type db: C{motor.motor_asyncio.AsyncIOMotorDatabase}
    :ivar db: AsyncIOMotorDatabase class instance.
    :type client: C{motor.motor_asyncio.AsyncIOMotorClient}
    :ivar client: AsyncIOMotorClient class instance.
    """
    db: AsyncIOMotorDatabase = None
    client: AsyncIOMotorClient = None

    # ---------------------------------------------------------
    #
    @classmethod
    async def connect_to_mongo(cls):
        """ Initialize DB connection to MongoDb and database. """
        cls.client = AsyncIOMotorClient(config.mongo_url)
        cls.db = cls.client.api_db

    # ---------------------------------------------------------
    #
    @classmethod
    async def close_mongo_connection(cls):
        """ Close DB connection. """
        cls.client.close()

    # ---------------------------------------------------------
    #
    @classmethod
    async def is_db_connected(cls) -> bool:
        """ Return MongoDB connection status. """
        return bool(await cls.client.server_info())

    # ---------------------------------------------------------
    #
    @classmethod
    async def get_async_session(cls) -> AsyncIOMotorClientSession:
        """ Return an active database session object from the pool.

        Note that this is a DB session generator.

        Returns:
            An active DB session.
        """
        async with await cls.client.start_session() as session:
            yield session
