# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2024-03-27 05:39:41
     $Rev: 2
"""

# BUILTIN modules
from fastapi import Path

query_example = {
    "query": {
        "name": None,
        "count": None,
        "price": None,
        "category": "tools"
    },
    "selection": [
        {
            "count": 20,
            "price": 9.99,
            "name": "Hammer",
            "category": "tools",
            "id": "dbb86c27-2eed-410d-881e-ad47487dd228"
        },
        {
            "count": 100,
            "price": 1.99,
            "name": "Nails",
            "category": "consumables",
            "id": "3c65943f6-a376-4265-98bb-5b13ed6a54c8"
        }
    ]
}

item_example = {
    "count": 50,
    "price": 5.99,
    "name": "Pliers",
    "category": "tools",
    "id": "32c1383a-b79e-43c1-8313-c8704382c48a"
}

license_info = {
    "name": "License: Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
}

tags_metadata = [
    {
        "name": "Items",
        "description": "Manage the lifecycle of the item "
                       "stock and their base price in Euro.",
    },
    {
        "name": "Health endpoint",
        "description": "A health check that return "
                       "the MongoDB connection status.",
    }
]

item_id_documentation = Path(
    ...,
    description='A unique identifier for an existing Item.<br>'
                '*Example: `dbb86c27-2eed-410d-881e-ad47487dd228`*.',
)
""" OpenAPI item ID documentation. """

get_query_documentation = {
    "name": {'default': None, 'min_length': 1, 'max_length': 8,
             'description': 'Name of the item.<br>'
                            '*Example: `Pliers`*.'},
    "count": {'default': None, 'ge': 0,
              'description': 'Number of this item in stock.<br>'
                             '*Example: `125`*.'},
    "price": {'default': None, 'gt': 0.0,
              'description': 'Price of the item in Euro.<br>'
                             '*Example: `12.45`*.'},
    "category": {'default': None,
                 'description': 'Category this item belongs to.'},
}
""" OpenAPI item GET query parameters documentation. """

put_query_documentation = {
    "name": {'default': None, 'min_length': 1, 'max_length': 8,
             'description': "New name of this item.<br>"
                            "*Example: `Hammer`*."},
    "count": {'default': None, 'ge': 0,
              'description': "New number of this item in stock.<br>"
                             "*Example: `100`*."},
    "price": {'default': None, 'gt': 0.0,
              'description': "New price of the item in Euro.<br>"
                             "*Example: `25.10`*."},
}
""" OpenAPI item PUT query parameters documentation. """

description = """
<img width="35%" align="right" src="/static/fastapi_mongo.png"/>

### Extensive example on how to use FastAPI and MongoDB to create a RESTful API.

**The following status codes are returned:**
  - Successful codes:
    - **200**: for all GET and PUT operations.
    - **201**: for POST operation.
    - **204**: for DELETE operation.

  - Failing codes:
    - **400**: POST or PUT operations failed with a DB error.
    - **400**: No query arguments provided in URL when at least one is required.
    - **401**: Access is denied on protected endpoints without proper authentication.
    - **404**: Search key _item_id_ is not found in the DB.
    - **406**: No query arguments provided in URL.
    - **500**: HEALTH: database connection is down.
"""
