# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-24 19:51:37
     $Rev: 38
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
            "count": 20,
            "price": 9.99,
            "name": "Hammer",
            "category": "tools",
            "od": "dbb86c27-2eed-410d-881e-ad47487dd228"
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
        "name": "items",
        "description": "Manage the lifecycle of the item "
                       "stock and their base price in Euro.",
    },
]
