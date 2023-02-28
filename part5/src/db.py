# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-23 21:12:28
     $Rev: 34
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

client = Engine()
""" Global instance of MongoDb engine. """
connection_url = f'{config.mongo_url}'
""" Async connection URL. """


# ---------------------------------------------------------
#
async def connect_to_mongo():
    """ Initialize DB connection to MongoDb and database. """

    client.connection = AsyncIOMotorClient(connection_url)
    client.db = client.connection.api_db


# ---------------------------------------------------------
#
async def close_mongo_connection():
    """ Close DB connection. """

    client.connection.close()
