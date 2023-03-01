# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-03-01 19:25:11
     $Rev: 60
"""

# BUILTIN modules
from enum import Enum
from typing import List, Optional, Callable

# Third party modules
from pydantic import BaseModel, Field, BaseConfig, UUID4

# Local modules
from .config.setup import config
from .apidocs.openapi_documentation import (item_example,
                                            query_example,
                                            resource_example)


# ------------------------------------------------------------------------
# Error reporting classes.
#
class AlreadyExistError(BaseModel):
    """ Define model for a http 409 exception (CONFLICT). """
    detail: str = "Item already exists in DB"


class NotFoundError(BaseModel):
    """ Define model for a http 404 exception (NOT_FOUND). """
    detail: str = "Item not found in DB"


class NoArgumentsError(BaseModel):
    """ Define model for a http 406 exception (NOT_ACCEPTABLE). """
    detail: str = "No query arguments provided in URL"


class DbOperationFailedError(BaseModel):
    """ Define model for a http 400 exception (BAD_REQUEST). """
    detail: str = "DB operation failed"


class HealthStatusError(BaseModel):
    """ Define model for a http 500 exception (INTERNAL_SERVER_ERROR). """
    detail: str = "HEALTH: database connection is down"


# ------------------------------------------------------------------------
#
class MongoBase(BaseModel):
    """
    Class that handles conversions between MongoDB '_id' key
    and our own 'id' key.

    MongoDB uses `_id` as an internal default index key.
    We can use that to our advantage.
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


# -----------------------------------------------------------------------------
#
class ResourceModel(BaseModel):
    """ Define OpenAPI model for a health resources response.

    :ivar name: Resource name.
    :ivar status: Resource status
    """

    name: str
    status: bool


class HealthModel(BaseModel):
    """ Define OpenAPI model for a health response.

    :ivar name: Service name.
    :ivar status: Overall health status
    :ivar version: Service version.
    :ivar resources: Status for individual resources..
    """

    status: bool
    name: str = Field(example=config.name)
    version: str = Field(example=config.version)
    resources: List[ResourceModel] = Field(example=resource_example)
