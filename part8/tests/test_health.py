# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2024-03-28 01:20:39
     $Rev: 8
"""

# Third party modules
import pytest
from starlette.testclient import TestClient
from httpx import AsyncClient, ASGITransport

# This is the same as using the @pytest.mark.anyio
# on all test functions in the module
pytestmark = pytest.mark.anyio


# ---------------------------------------------------------
#
async def test_normal_health(test_app: TestClient):
    """ Test successful health endpoint.

    :param test_app: TestClient instance.
    """
    transport = ASGITransport(app=test_app.app)

    async with AsyncClient(transport=transport,
                           base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()['status'] is True


# ---------------------------------------------------------
#
async def test_health_error(test_app: TestClient):
    """ Test failed health endpoint.

    :param test_app: TestClient instance.
    """
    transport = ASGITransport(app=test_app.app)

    async with AsyncClient(transport=transport,
                           base_url="http://dummy") as client:
        response = await client.get("/health")

    assert response.status_code == 500
    assert response.json()['status'] is False
