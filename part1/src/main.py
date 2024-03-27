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

# Third party modules
from fastapi import FastAPI

# Local modules
from . import api

app = FastAPI(
    version="1.1.0",
    title="FastAPI-MongoDB Example")

# Add used endpoints (and simplifying endpoint declarations).
app.include_router(api.ROUTER)
