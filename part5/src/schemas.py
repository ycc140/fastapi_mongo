# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-28 19:26:05
     $Rev: 52
"""

# BUILTIN modules
from enum import Enum
from typing import List, Optional, Callable

# Third party modules
from pydantic import BaseModel, Field, BaseConfig, UUID4

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
    """ Define model for a http 406 exception (Not Acceptable). """
    detail: str = "No query arguments provided in URL"


class DbOperationFailedError(BaseModel):
    """ Define model for a http 400 exception (Bad Request). """
    detail: str = "DB operation failed"


# -----------------------------------------------------------------------------
#
class MongoBase(BaseModel):
    """ Class that handles conversions between MongoDB '_id' key and our own 'id' key.

    MongoDB uses `_id` as an internal default index key. We can use that to our advantage.
    """

    class Config(BaseConfig):
        """ basic config. """
        orm_mode = True
        allow_population_by_field_name = True

    # noinspection PyArgumentList
    @classmethod
    def from_mongo(cls, data: dict) -> Callable:
        """ Convert "_id" (str object) into "id" (UUID object). """

        if not data:
            return data

        mongo_id = data.pop('_id', None)
        return cls(**dict(data, id=mongo_id))

    def to_mongo(self, **kwargs) -> dict:
        """ Convert "id" (UUID object) into "_id" (str object). """

        parsed = self.dict(**kwargs)

        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = str(parsed.pop('id'))

        return parsed


# -----------------------------------------------------------------------------
#
class Category(str, Enum):
    """ Category of an item. """

    TOOLS = "tools"
    CONSUMABLES = "consumables"


# -----------------------------------------------------------------------------
#
class ItemPayload(MongoBase):
    """ Representation of an item payload in the system. """

    count: int = Field(ge=0, description="Number of this item in stock")
    price: float = Field(gt=0.0, description="Price of the item in Euro")
    category: Category = Field(description="Category this item belongs to")
    name: str = Field(min_length=1, max_length=8, description="Name of the item")


class ItemSchema(ItemPayload):
    """ Representation of an item in the system. """

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
