# FastAPI-MongoDB example

An extensive python FastAPI example using MongoDB

## Author: Anders Wiklund

<img width="55%" align="right" src="part2/src/apidocs/fastapi_mongo.png"/>

This code repository is an extensive FAstAPI example of a RESTful API using MongoDB.

Async IO is a vital part of FastAPI, and it will be used extensively in this example.

The root of my example is derived from an example that **Arjan** has shown in a YouTube
[video](https://www.youtube.com/watch?v=SORiTsvnU28), the corresponding code is available in this
[GitHub repo](https://github.com/ArjanCodes/2023-fastapi).

This repository is structured around the **Medium** article parts.
There's one folder per part.
Each folder contains all the code you need to follow along with the examples for the corresponding part.

### Here's a brief outline of the article parts

#### [Part 1: A basic RESTful API](https://medium.com/@wilde.consult/extensive-fastapi-with-mongodb-example-part1-ceff58e16f94)

It explains the absolute basic part of the API.
It is using a dictionary as a DB just to show the concepts without too much clutter that takes away focus from what
is important.
RESTful best practices have been followed when naming endpoints and returning the proper status codes.

#### [Part 2: Extending the OpenAPI documentation in the code](https://medium.com/@wilde.consult/extensive-fastapi-with-mongodb-example-part2-22fc3255ea97)

This part shows how to expand the Swagger documentation within the code.

#### [Part 3: How to handle configuration data](https://medium.com/@wilde.consult/extensive-fastapi-with-mongodb-example-part3-b6d1a7d97692)

This part adds initial configuration handling using the Pydantic **BaseSettings** class.
Project parameters in an
.env file.
Later on, when we add database support and Authentication passwords we will use Pydantic secrets files.
In part9, we will integrate Docker secrets with Pydantic secrets.

#### [Part 4: Normalized log handling](https://medium.com/@wilde.consult/extensive-fastapi-with-mongodb-example-part4-8fa4572bbc0)

This part adds normalized log handling with color using the third party **Loguru** package.

#### [Part 5: How to use MongoDB with FastAPI](https://medium.com/@wilde.consult/extensive-fastapi-with-mongodb-example-part5-ba057abf97e5)

This part adds the usage of MongoDB. It also shows how to install MongoDB using Docker for local usage.

#### [Part 6: A health status endpoint](https://medium.com/@wilde.consult/extensive-fastapi-with-mongodb-example-part6-c88f40846684)

This part adds health status handling. It displays MongoDB connection status.

#### [Part 7: HTTP API-key Authentication](https://medium.com/@wilde.consult/extensive-fastapi-with-mongodb-example-part7-166723102498)

This part adds API-key Authentication handling.
This type of Authentication should only be used together
with TLS/SSL certificates so that the communication is encrypted between the browser and the API.

#### [Part 8: FastAPI Mock Testing](https://medium.com/@wilde.consult/extensive-fastapi-with-mongodb-example-part8-6aa6647894cb)

This part adds Mock testing of the API using the third party **pytest** package. The
"mocking" part is the MongoDB itself. This gives us much better control and makes it a lot
easier to test, for example, DB failures during create and update operations.

#### [Part 9: Docker container handling](https://medium.com/@wilde.consult/extensive-fastapi-with-mongodb-example-part9-b1cf673026b2)

This part adds docker functionality with multiple environments using a multi-build Dockerfile solution
to reduce container size.
