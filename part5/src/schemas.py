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

# BUILTIN modules
from uuid import UUID
from enum import Enum
from typing import List, Optional, Callable

# Third party modules
from uuid_extensions import uuid7
from pydantic import BaseModel, Field, ConfigDict

# Local modules
from .api.documentation import item_example, query_example


# ------------------------------------------------------------------------
# Error reporting classes.
#
class DbOperationFailedError(BaseModel):
    """ Define model for the http 400 exception (BAD_REQUEST). """
    detail: str = "DB operation failed"


class NotFoundError(BaseModel):
    """ Define a model for the http 404 exception (NOT_FOUND). """
    detail: str = "Item not found in DB"


class NoArgumentError(BaseModel):
    """ Define model for the http 406 exception (NOT_ACCEPTABLE). """
    detail: str = "No query arguments provided in URL"


# ------------------------------------------------------------------------
#
class MongoBase(BaseModel):
    """
    Class that handles conversions between MongoDB '_id' key
    and our own 'id' key.

    MongoDB uses `_id` as an internal default index key.
    We can use that to our advantage.
    """
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @classmethod
    def from_mongo(cls, data: dict) -> Callable:
        """ Convert "_id" (str object) into "id" (UUID object).

        :param data: Current model as a dict.
        :return: Converted MongoDB model object to current model.
        """

        if not data:
            return data

        mongo_id = data.pop('_id', None)
        return cls(**dict(data, id=mongo_id))

    def to_mongo(self, **kwargs) -> dict:
        """ Convert "id" (UUID object) into "_id" (str object).

        :param kwargs: Current DB Model parameters.
        :return: MongoDB converted object.
        """

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
    category: Category
    count: int = Field(ge=0)
    price: float = Field(gt=0.0)
    name: str = Field(min_length=1, max_length=8)


class ItemModel(ItemPayload):
    """ Representation of an item in the system. """
    model_config = ConfigDict(json_schema_extra={"example": item_example})
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
    model_config = ConfigDict(json_schema_extra={"example": query_example})
    query: QueryArguments = Field(description="Dictionary containing the user's query arguments")
    selection: List[ItemModel] = Field(description="List of items that match the query arguments")
