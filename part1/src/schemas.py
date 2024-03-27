# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2024-03-27 15:22:03
     $Rev: 4
"""

# BUILTIN modules
from uuid import UUID
from enum import Enum
from typing import List, Optional

# Third party modules
from uuid_extensions import uuid7
from pydantic import BaseModel, Field


# -----------------------------------------------------------------------------
#
class Category(str, Enum):
    """ Category of an item. """
    TOOLS = "tools"
    CONSUMABLES = "consumables"


# -----------------------------------------------------------------------------
#
class ItemPayload(BaseModel):
    """ Representation of an item payload in the system. """
    category: Category
    count: int
    price: float
    name: str


class ItemModel(ItemPayload):
    """ Representation of an item in the system. """
    id: UUID = Field(default_factory=uuid7)


# -----------------------------------------------------------------------------
#
class QueryArguments(BaseModel):
    """ Representation of item query arguments in the system. """
    name: Optional[str] = None
    count: Optional[int] = None
    price: Optional[float] = None
    category: Optional[Category] = None


class ItemArgumentResponse(BaseModel):
    """ Representation of an argument query response in the system. """
    query: QueryArguments
    selection: List[ItemModel]
