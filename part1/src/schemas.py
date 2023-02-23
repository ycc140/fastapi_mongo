# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-23 21:12:28
     $Rev: 34
"""

# BUILTIN modules
from enum import Enum
from typing import List, Optional

# Third party modules
from pydantic import BaseModel, UUID4


# -----------------------------------------------------------------------------
#
class Category(str, Enum):
    """ Category of an item. """

    TOOLS = "tools"
    CONSUMABLES = "consumables"


class ItemSchema(BaseModel):
    """ Representation of an item in the system. """

    id: UUID4
    name: str
    count: int
    price: float
    category: Category


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
    selection: List[ItemSchema]
