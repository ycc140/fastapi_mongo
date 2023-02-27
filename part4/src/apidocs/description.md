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
    - **409**: Duplicate error, the _item_id_ already exists in the DB.
    - **500**: Hm, I don't know what this is, but it's not good...
