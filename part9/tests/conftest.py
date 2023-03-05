# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-03-05 11:05:26
     $Rev: 72
"""

# Third party modules
import pytest
from requests import auth
from starlette.testclient import TestClient

# Local program modules
from ..src.main import app
from ..src.config.setup import config

# Constants
pytest.AUTH = auth.HTTPBasicAuth(config.service_user, config.service_pwd)


# ---------------------------------------------------------
#
@pytest.fixture(scope="module")
def anyio_backend():
    """ Module fixture. """

    return 'asyncio'


# ---------------------------------------------------------
#
@pytest.fixture(scope="module")
def test_app():
    """ Module fixture. """

    with TestClient(app) as test_client:
        yield test_client
