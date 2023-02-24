# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-24 14:23:17
     $Rev: 37
"""

# BUILTIN modules
from pathlib import Path

# Third party modules
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Local modules
from .api import ROUTER
from .apidocs.openapi_documentation import license_info, tags_metadata

# Constants
DOC_PATH = Path(__file__).parent / 'apidocs'
""" OpenAPI documentation root path. """


# ---------------------------------------------------------
#
def _get_description() -> str:
    """ Return content of description Markdown file.

    :return: Markdown formatted description text.
    """

    with open(DOC_PATH / 'description.md', 'r') as hdl:
        md_text = hdl.read()

    return md_text


# ---------------------------------------------------------
#
app = FastAPI(
    redoc_url=None,
    version="0.2.0",
    license_info=license_info,
    openapi_tags=tags_metadata,
    description=_get_description(),
    title="FastAPI-MongoDB Example",
)

# Needed for OpenAPI Markdown images to be displayed.
app.mount("/static", StaticFiles(directory=DOC_PATH))

# Add used endpoints and simplifying endpoint declarations.
app.include_router(ROUTER)
