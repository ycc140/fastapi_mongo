# FastAPI-MongoDB example
An extensive python FastAPI example using MongoDB

<img width="55%" align="right" src="part2/static/fastapi_mongo.png"/>

## Author: Anders Wiklund

This code repository is an extensive FAstAPI example of a RESTful API using MongoDB. 

Async IO is a vital part of FastAPI, and it will be used extensively in this example.

The root of my example is derived from an example that **Arjan** have shown in a YouTube 
[video](https://www.youtube.com/watch?v=SORiTsvnU28), the corresponding code is available in this 
[GitHub repo](https://github.com/ArjanCodes/2023-fastapi). 

This repository is structured around the **Medium** article parts. There's one folder per part. Each folder 
contains all the code you need to follow along with the examples for the corresponding part.

### Here's a brief outline of the article parts

#### Part 1: A basic RESTful API
It explains the absolute basic part of the API. It is using a dictionary as a DB just to show the concepts 
without too much clutter that takes away focus from what is important. RESTful best practices have been 
followed when naming endpoints and returning the proper status codes.

#### Part 2: Extending the OpenAPI documentation in the code
This part show how to expand the Swagger documentation within the code.

#### Part 3: How to handle configuration data
This part adds configuration handling using the Pydantic **BaseSettings** class. Passwords and other 
secret values are stored as environment values in the OS. 

#### Part 4: Normalized log handling
This part adds normalized log handling with color using the third party **Loguru** package.

#### Part 5: How to use MongoDB with FastAPI
This part adds the usage of MongoDB. It also shows how to install MongoDB using Docker for local usage.

#### Part 6: A health status endpoint
This part adds health status handling. It displays MongoDB connection status. In this part the project 
desciption is moved into a separate file so that the Markdown functionality can be used.

#### Part 7: Basic Authentication
This part adds simple Basic Authentication handling. This type of Authentication should only be used in 
a non-public API that is not exposed to Internet. A good explanation of this, and what type to use where 
is described in an excellent book [Microservice APIs](https://www.manning.com/books/microservice-apis). 
Code examples for this book can be found in 
[appendic C](https://github.com/abunuwas/microservice-apis/tree/master/appendix_c/orders). There are also a number 
of YouTube [videos](https://www.youtube.com/@pinillos/videos) from the author that might be interesting to watch if 
that is your _cup of tea_.

#### Part 8: FastAPI Mock Testing
This part adds Mock testing of the API using the third party **pytest** package. The 
"mocking" part is the MongoDB itself. This gives us much better control and makes it a lot
easier to test, for example DB failures during create and update operations.

#### Part 9: Docker container handling
This part adds docker functionality with multiple environments using multi-build Dockerfile solution 
to reduce container size.
