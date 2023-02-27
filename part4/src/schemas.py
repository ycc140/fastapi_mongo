# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-26 03:35:05
     $Rev: 42
"""

# BUILTIN modules
from enum import Enum
from typing import List, Optional

# Third party modules
from pydantic import BaseModel, Field, UUID4

# Local modules
from .apidocs.openapi_documentation import query_example, item_example


# -----------------------------------------------------------------------------
# Error reporting classes.
#
class AlreadyExistError(BaseModel):
    """ Define model for a http 409 exception (Conflict). """
    detail: str = "Item already exists in DB"


class NotFoundError(BaseModel):
    """ Define model for a http 404 exception (Not Found). """
    detail: str = "Item not found in DB"


class NoArgumentsError(BaseModel):
    """ Define model for a http 400 exception (Unprocessable Entity). """
    detail: str = "No query arguments provided in URL"


class DbOperationFailedError(BaseModel):
    """ Define model for a http 400 exception (Unprocessable Entity). """
    detail: str = "DB operation failed"


# -----------------------------------------------------------------------------
#
class Category(str, Enum):
    """ Category of an item. """

    TOOLS = "tools"
    CONSUMABLES = "consumables"


# -----------------------------------------------------------------------------
# You can add metadata to attributes using the Field class.
# You can also add example data to attributes using the Field class,
# or you can add an example on a class level using the Config subclass.
# This information will also be shown in the auto-generated documentation.
#
class ItemSchema(BaseModel):
    """ Representation of an item in the system. """

    count: int = Field(ge=0, description="Number of this item in stock")
    price: float = Field(gt=0.0, description="Price of the item in Euro")
    category: Category = Field(description="Category this item belongs to")
    name: str = Field(min_length=1, max_length=8, description="Name of the item")
    id: UUID4 = Field(description="Unique identifier (UUID) that specifies this item")

    class Config:
        schema_extra = {"example": item_example}


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

    query: QueryArguments = Field(description="Dictionary containing the user's query arguments")
    selection: List[ItemSchema] = Field(description="List of items that match the query arguments")

    class Config:
        schema_extra = {"example": query_example}
