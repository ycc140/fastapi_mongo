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
from fastapi import HTTPException
from pymongo.results import DeleteResult

# Local program modules
from ..src.config.setup import config
from ..src.api import crud_items as crud
from ..src.schemas import Category, ItemModel

# This is the same as using the @pytest.mark.anyio on all test functions in the module
pytestmark = pytest.mark.anyio

# Constants
URL = "/v1/items"
""" Root endpoint URL. """
AUTH = {'Content-Type': 'application/json',
        'X-API-Key': f'{config.service_api_key}'}


# ---------------------------------------------------------
#
@pytest.mark.parametrize(
    "payload, status_code",
    [
        [None, 422],
        [['printing'], 422],
        [{"name": "Hammer", "price": 2.39}, 422],
        [{"name": "Hammer", "price": 0, "count": 20, "category": "tools"}, 422],
        [{"name": "Hammer", "price": 9.99, "count": 20, "category": "dummy"}, 422],
        [{"category": "tools", "count": 20, "price": 12.35, "name": "Wrench"}, 201],
        [{"name": "Hammer", "price": 9.99, "count": 20, "category": "unknown"}, 422],
        [{"name": "Hammer", "price": 9.99, "count": -1, "category": "consumables"}, 422],
    ]
)
async def test_create_item_payload_variants(test_app, monkeypatch,
                                            payload, status_code):
    """ Test create an item document with different payloads.

    It will test one good and the rest will test validation limits.
    """

    # ---------------------------------

    async def mock_create(_):
        """ Monkeypatch """
        return {"category": "tools", "count": 20, "price": 12.35,
                "name": "Wrench", "id": "dbb86c27-2eed-410d-881e-ad47487dd228"}

    monkeypatch.setattr(crud, "create", mock_create)

    # ---------------------------------

    response = test_app.post(URL, headers=AUTH, json=payload)
    assert response.status_code == status_code


# ---------------------------------------------------------
#
async def test_create_item_db_error(test_app, monkeypatch):
    """ Test create item document with db failure response. """

    test_data = {
        "name": "Hammer", "price": 9.99, "count": 20, "category": "tools"
    }
    request_response = "Create failed for id='dbb86c27-2eed-410d-881e-ad47487dd228' in api_db.items"

    # ---------------------------------

    async def mock_create(_):
        """ Monkeypatch """
        raise HTTPException(status_code=400, detail=request_response)

    monkeypatch.setattr(crud, "create", mock_create)

    # ---------------------------------

    response = test_app.post(URL, headers=AUTH, json=test_data)
    assert response.status_code == 400
    assert response.json()["detail"] == request_response


# ---------------------------------------------------------
#
async def test_read_all_item_documents(test_app, monkeypatch):
    """ Test read all item documents. """

    test_data = [
        {
            "count": 20,
            "price": 9.99,
            "name": "Hammer",
            "category": "tools",
            "id": "dbb86c27-2eed-410d-881e-ad47487dd228"
        },
        {
            "count": 50,
            "price": 5.99,
            "name": "Pliers",
            "category": "tools",
            "id": "32c1383a-b79e-43c1-8313-c8704382c48a"
        }
    ]

    # ---------------------------------

    async def mock_read_all():
        """ Monkeypatch """
        return test_data

    monkeypatch.setattr(crud, "read_all", mock_read_all)

    # ---------------------------------

    response = test_app.get(URL, headers=AUTH)
    assert response.status_code == 200
    assert response.json() == test_data


# ---------------------------------------------------------
#
async def test_read_item_document(test_app, monkeypatch):
    """ Test read an item document. """

    test_data = {
        "id": 'dbb86c27-2eed-410d-881e-ad47487dd228',
        "name": "Hammer", "price": 9.99, "count": 20, "category": "tools"
    }

    # ---------------------------------

    async def mock_read(_):
        """ Monkeypatch """
        return test_data

    monkeypatch.setattr(crud, "read", mock_read)

    # ---------------------------------

    response = test_app.get(f"{URL}/dbb86c27-2eed-410d-881e-ad47487dd228", headers=AUTH)
    assert response.status_code == 200
    assert response.json() == test_data


# ---------------------------------------------------------
#
async def test_read_item_index_key_error(test_app, monkeypatch):
    """ Test read item document with an incorrect index key type. """

    request_response = [
        {'ctx': {'error': 'invalid character: expected an optional prefix of '
                          '`urn:uuid:` followed by [0-9a-fA-F-], found `m` at 1'},
         'input': 'maja',
         'loc': ['path', 'item_id'],
         'msg': 'Input should be a valid UUID, invalid character: expected an '
                'optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `m` at 1',
         'type': 'uuid_parsing',
         'url': 'https://errors.pydantic.dev/2.6/v/uuid_parsing'}
    ]

    # ---------------------------------

    async def mock_read(_):
        """ Monkeypatch """
        return 0

    monkeypatch.setattr(crud, "read", mock_read)

    # ---------------------------------

    response = test_app.get(f"{URL}/maja", headers=AUTH)
    assert response.status_code == 422
    assert response.json()["detail"] == request_response


# ---------------------------------------------------------
#
async def test_read_item_unknown_error(test_app, monkeypatch):
    """ Test read item document with an unknown index key. """

    request_response = "item_id=UUID('dbb86c27-2eed-410d-881e-ad47487dd211') not found in api_db.items"

    # ---------------------------------

    async def mock_read(_):
        """ Monkeypatch """
        return 0

    monkeypatch.setattr(crud, "read", mock_read)

    # ---------------------------------

    response = test_app.get(f"{URL}/dbb86c27-2eed-410d-881e-ad47487dd211", headers=AUTH)
    assert response.status_code == 404
    assert response.json()["detail"] == request_response


# ---------------------------------------------------------
#
async def test_query_item_document(test_app, monkeypatch):
    """ Test query a item document using parameters. """

    test_request_payload = [
        ItemModel(
            id='dbb86c27-2eed-410d-881e-ad47487dd228',
            name="Hammer", price=9.99, count=20, category=Category.TOOLS,
        )
    ]
    test_response_payload = {
        "query": {
            "price": None,
            "count": None,
            "name": "Hammer",
            "category": "tools"
        },
        "selection": [
            {
                "count": 20,
                "price": 9.99,
                "name": "Hammer",
                "category": "tools",
                "id": "dbb86c27-2eed-410d-881e-ad47487dd228"
            }
        ]
    }

    # ---------------------------------

    async def mock_query(_):
        """ Monkeypatch """
        return test_request_payload

    monkeypatch.setattr(crud, "query", mock_query)

    # ---------------------------------

    response = test_app.get(f"{URL}/?name=Hammer&category=tools", headers=AUTH)
    assert response.status_code == 200
    assert response.json() == test_response_payload


# ---------------------------------------------------------
#
async def test_query_param_error(test_app, monkeypatch):
    """ Test query a item document without parameters. """

    request_response = "No query values provided in query URL"

    # ---------------------------------

    response = test_app.get(f"{URL}/", headers=AUTH)
    assert response.status_code == 406
    assert response.json()["detail"] == request_response


# ---------------------------------------------------------
#
async def test_query_invalid_category_error(test_app, monkeypatch):
    """ Test query an item document with invalid category parameter. """

    request_response = [
        {'ctx': {'expected': "'tools' or 'consumables'"},
         'input': 'powertools',
         'loc': ['query', 'category'],
         'msg': "Input should be 'tools' or 'consumables'",
         'type': 'enum'}
    ]

    # ---------------------------------

    response = test_app.get(f"{URL}/?category=powertools", headers=AUTH)
    assert response.status_code == 422
    assert response.json()["detail"] == request_response


# ---------------------------------------------------------
#
async def test_update_item_document(test_app, monkeypatch):
    """ Test update item document. """

    test_request_payload = ItemModel(
        id='dbb86c27-2eed-410d-881e-ad47487dd228',
        name="Hammer", price=9.99, count=20, category=Category.TOOLS,
    )
    test_response_payload = {
        "id": 'dbb86c27-2eed-410d-881e-ad47487dd228',
        "name": "Hammer", "price": 9.99, "count": 23, "category": "tools"
    }

    # ---------------------------------

    async def mock_read(_):
        """ Monkeypatch """
        return test_request_payload

    monkeypatch.setattr(crud, "read", mock_read)

    # ---------------------------------

    async def mock_update(_):
        """ Monkeypatch """
        return test_response_payload

    monkeypatch.setattr(crud, "update", mock_update)

    # ---------------------------------

    response = test_app.put(f"{URL}/dbb86c27-2eed-410d-881e-ad47487dd228?count=23", headers=AUTH)
    assert response.status_code == 200
    assert response.json() == test_response_payload


# ---------------------------------------------------------
#
async def test_update_item_parameter_error(test_app, monkeypatch):
    """ Test update item without query parameters. """

    response = test_app.put(f"{URL}/dbb86c27-2eed-410d-881e-ad47487dd228", headers=AUTH)
    assert response.status_code == 406
    assert response.json()["detail"] == "No query values provided in update URL"


# ---------------------------------------------------------
#
async def test_update_item_unknown_error(test_app, monkeypatch):
    """ Test update item unknown index key. """

    request_response = "item_id=UUID('dbb86c27-2eed-410d-881e-ad47487dd211') not found in api_db.items"

    # ---------------------------------

    async def mock_read(_):
        """ Monkeypatch """
        return 0

    monkeypatch.setattr(crud, "read", mock_read)

    # ---------------------------------

    response = test_app.put(f"{URL}/dbb86c27-2eed-410d-881e-ad47487dd211?count=23", headers=AUTH)
    assert response.status_code == 404
    assert response.json()["detail"] == request_response


# ---------------------------------------------------------
#
async def test_update_item_failure(test_app, monkeypatch):
    """ Test update item document with db failure response. """

    test_request_payload = ItemModel(
        id='dbb86c27-2eed-410d-881e-ad47487dd228',
        name="Hammer", price=9.99, count=20, category=Category.TOOLS,
    )
    request_response = "Failed updating item_id=UUID('dbb86c27-2eed-410d-881e-ad47487dd228') in api_db.items"

    # ---------------------------------

    async def mock_read(_):
        """ Monkeypatch """
        return test_request_payload

    monkeypatch.setattr(crud, "read", mock_read)

    # ---------------------------------

    async def mock_update(_):
        """ Monkeypatch """
        return 0

    monkeypatch.setattr(crud, "update", mock_update)

    # ---------------------------------

    response = test_app.put(f"{URL}/dbb86c27-2eed-410d-881e-ad47487dd228?count=23", headers=AUTH)
    assert response.status_code == 400
    assert response.json()["detail"] == request_response


# ---------------------------------------------------------
#
async def test_delete_item_document(test_app, monkeypatch):
    """ Test delete item document."""

    # ---------------------------------

    async def mock_delete(_):
        """ Monkeypatch """
        return DeleteResult({'n': 1}, {'ok': 1.0})

    monkeypatch.setattr(crud, "delete", mock_delete)

    # ---------------------------------

    response = test_app.delete(f"{URL}/dbb86c27-2eed-410d-881e-ad47487dd228", headers=AUTH)
    assert response.status_code == 204
    assert response.text == ''


# ---------------------------------------------------------
#
async def test_delete_item_unknown_error(test_app, monkeypatch):
    """ Test delete item document with unknown index key. """

    request_response = "item_id=UUID('dbb86c27-2eed-410d-881e-ad47487dd228') not found in api_db.items"

    # ---------------------------------

    async def mock_delete(_):
        """ Monkeypatch """
        return DeleteResult({'n': 0}, {'ok': 1.0})

    monkeypatch.setattr(crud, "delete", mock_delete)

    # ---------------------------------

    response = test_app.delete(f"{URL}/dbb86c27-2eed-410d-881e-ad47487dd228", headers=AUTH)
    assert response.status_code == 404
    assert response.json()["detail"] == request_response
