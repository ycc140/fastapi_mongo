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
from typing import Tuple

# Third party modules
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Local modules
from .api import ROUTER
from .config.setup import config
from .custom_logging import CustomizeLogger
from .apidocs.openapi_documentation import tags_metadata, license_info

# Constants
ROOT_PATH = Path(__file__).parent
""" Root path for files. """


# ---------------------------------------------------------
#
def get_description() -> str:
    """  Return content of description Markdown file.

    :return: Markdown formatted description text.
    """

    with open(ROOT_PATH / 'apidocs' / 'description.md', 'r') as hdl:
        md_text = hdl.read()

    return md_text


# ---------------------------------------------------------
#
def create_app() -> Tuple[FastAPI, str]:
    """ Create FastAPI app structure and unified logging. """

    instance = FastAPI(
        redoc_url=None,
        title=config.name,
        version=config.version,
        license_info=license_info,
        openapi_tags=tags_metadata,
        description=get_description()
    )

    # Needed for swagger Markdown images to be displayed.
    static_path = ROOT_PATH / 'apidocs'
    instance.mount("/static", StaticFiles(directory=static_path))

    # Create app structure.
    level, custom_logger = CustomizeLogger.make_logger()
    instance.logger = custom_logger

    return instance, level


# ---------------------------------------------------------

# Create the FastAPI application.
app, log_level = create_app()

# Add created endpoints.
app.include_router(ROUTER)


# ---------------------------------------------------------
#
@app.get("/")
async def root_path():
    return {"message": f'You are visiting: {config.name} v{config.version}'}
