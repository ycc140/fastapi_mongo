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

# Third party modules
from fastapi import FastAPI

# Local modules
from .api import ROUTER

app = FastAPI(
    version="0.1.0",
    title="FastAPI-MongoDB Example")

# Add used endpoints (and simplifying endpoint declarations).
app.include_router(ROUTER)
