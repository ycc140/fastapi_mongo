# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-03-01 19:25:11
     $Rev: 60
"""

# BUILTIN modules
import asyncio
from pprint import pprint

# Third party modules
from httpx import ConnectError, ReadTimeout, BasicAuth, AsyncClient

# Local program modules
from src.config.setup import config

# Constants
AUTH = BasicAuth(username=config.service_user, password=config.service_pwd)


# ---------------------------------------------------------
#
async def process(use_auth: bool = False):

    async with AsyncClient() as client:
        response = await client.get(url='http://localhost:8000/v1/items',
                                    headers={'Content-Type': 'application/json'},
                                    timeout=(9.05, 60), auth=(AUTH if use_auth else None))

    if response.status_code == 200:
        print(f'\nTRUE =>')
        pprint(response.json())

    else:
        print(f'\nFALSE => \nstatus: {response.status_code}, error: {response.json()}')


# ---------------------------------------------------------
#
async def test():
    try:
        await process()
        await process(use_auth=True)

    # You will end up here if you have not started the API server program (run.py).
    except ConnectError as why:
        print(f'ERROR => {why}')

    # You can test this by changing the read timeout value from 60 seconds to 0.01.
    except ReadTimeout as why:
        print(f'TIMEOUT => {why}')


# ---------------------------------------------------------

if __name__ == "__main__":

    asyncio.run(test())
