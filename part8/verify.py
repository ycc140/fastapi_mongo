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
import asyncio
from pprint import pprint

# Third party modules
from httpx import ConnectError, ReadTimeout, AsyncClient

# Local program modules
from src.config.setup import config

# Constants
AUTH = {'Content-Type': 'application/json',
        'X-API-Key': f'{config.service_api_key}'}


# ---------------------------------------------------------
#
async def process(use_auth: bool = False):
    """ Process requests. """

    async with AsyncClient() as client:
        response = await client.get(url='http://localhost:8000/v1/items',
                                    headers=(AUTH if use_auth else None),
                                    timeout=(9.05, 60))

    if response.status_code == 200:
        print(f'\nTRUE =>')
        pprint(response.json())

    else:
        print(f'\nFALSE => \nstatus: {response.status_code}, error: {response.text}')


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
