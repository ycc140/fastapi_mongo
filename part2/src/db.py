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

# Local modules
from uuid import UUID
from .schemas import Category, ItemModel

# In this version, fake MongoDB usage.
#
items = {
    UUID('dbb86c27-2eed-410d-881e-ad47487dd228'): ItemModel(
        id=UUID('dbb86c27-2eed-410d-881e-ad47487dd228'),
        name="Hammer", price=9.99, count=20, category=Category.TOOLS,
    ),
    UUID('32c1383a-b79e-43c1-8313-c8704382c48a'): ItemModel(
        id=UUID('32c1383a-b79e-43c1-8313-c8704382c48a'),
        name="Pliers", price=5.99, count=20, category=Category.TOOLS,
    ),
    UUID('c65943f6-a376-4265-98bb-5b13ed6a54c8'): ItemModel(
        id=UUID('c65943f6-a376-4265-98bb-5b13ed6a54c8'),
        name="Nails", price=1.99, count=100, category=Category.CONSUMABLES,
    ),
}
