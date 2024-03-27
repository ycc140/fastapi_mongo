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
from pathlib import Path

# Third party modules
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Local modules
from .api import item_routes
from .api.documentation import tags_metadata, license_info, description


# ---------------------------------------------------------
#
class Service(FastAPI):
    """ This class extends the FastAPI class for the OrderService API.

    The following functionality is added:
      - includes API router.
      - Defines a static path for images in the documentation.
    """

    def __init__(self, *args: int, **kwargs: dict):
        """ This class adds RabbitMQ message consumption and unified logging.

        :param args: Named arguments.
        :param kwargs: Key-value pair arguments.
        """
        super().__init__(*args, **kwargs)

        # Needed for OpenAPI Markdown images to be displayed.
        static_path = Path(__file__).parent / 'static'
        self.mount("/static", StaticFiles(directory=static_path))

        # Add declared router information.
        self.include_router(item_routes.ROUTER)


# ---------------------------------------------------------

app = Service(
    redoc_url=None,
    version="1.2.0",
    description=description,
    license_info=license_info,
    openapi_tags=tags_metadata,
    title="FastAPI-MongoDB Example",
    # swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
)
""" The FastAPI application instance. """
