# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-03-04 13:29:26
     $Rev: 70
"""

# BUILTIN modules
from pathlib import Path

# Third party modules
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Local modules
from .api import ROUTER
from .config.setup import config
from .apidocs.openapi_documentation import tags_metadata, license_info

# Constants
DOC_PATH = Path(__file__).parent / 'apidocs'
""" OpenAPI documentation root path. """


# ---------------------------------------------------------
#
def get_description() -> str:
    """  Return content of description Markdown file.

    :return: Markdown formatted description text.
    """

    with open(DOC_PATH / 'description.md', 'r') as hdl:
        md_text = hdl.read()

    return md_text


# ---------------------------------------------------------
#
app = FastAPI(
    redoc_url=None,
    title=config.name,
    version=config.version,
    license_info=license_info,
    openapi_tags=tags_metadata,
    description=get_description()
)

# Needed for swagger Markdown images to be displayed.
app.mount("/static", StaticFiles(directory=DOC_PATH))

# Add used endpoints (and simplifying endpoint declarations).
app.include_router(ROUTER)


# ---------------------------------------------------------
#
@app.get("/")
async def root_path():
    return {"message": f'You are visiting: {config.name} v{config.version}'}
