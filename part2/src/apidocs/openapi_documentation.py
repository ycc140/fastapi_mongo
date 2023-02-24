# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: MIT

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-24 11:24:16
     $Rev: 36
"""

query_example = {
    "query": {
        "name": None,
        "count": None,
        "price": None,
        "category": "tools"
    },
    "selection": [
        {
            "name": "Hammer",
            "price": 9.99,
            "category": "tools",
            "count": 20,
            "id": "dbb86c27-2eed-410d-881e-ad47487dd228"
        },
        {
            "name": "Pliers",
            "price": 5.99,
            "category": "tools",
            "count": 50,
            "id": "32c1383a-b79e-43c1-8313-c8704382c48a"
        }
    ]
}

item_example = {
    "name": "Pliers",
    "price": 5.99,
    "category": "tools",
    "count": 50,
    "id": "32c1383a-b79e-43c1-8313-c8704382c48a"
}

license_info = {
    "name": "License: Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
}

tags_metadata = [
    {
        "name": "items",
        "description": "Manage the lifecycle of order items.",
    },
]
