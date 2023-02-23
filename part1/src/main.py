# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: MIT

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-20 04:00:57
     $Rev: 14
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
