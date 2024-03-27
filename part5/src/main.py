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
import json
from pathlib import Path
from contextlib import asynccontextmanager

# Third party modules
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Local modules
from .db import Engine
from .api import item_routes
from .config.setup import config
from .custom_logging import create_unified_logger
from .api.documentation import tags_metadata, license_info, description


# ---------------------------------------------------------
#
class Service(FastAPI):
    """ This class extends the FastAPI class for the OrderService API.

    The following functionality is added:
      - unified logging.
      - includes API router.
      - Defines a static path for images in the documentation.

    :ivar logger: Unified loguru logger object.
    :type logger: loguru.logger
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

        # Unify logging within the imported package's closure.
        self.logger = create_unified_logger()


# ---------------------------------------------------------
#
@asynccontextmanager
async def lifespan(service: Service):
    """ Define startup and shutdown application logic.

    Handle unavailable RabbitMQ server during startup.

    :param service: FastAPI service.
    """
    try:
        await startup(service)
        yield

    except BaseException as why:
        service.logger.critical(f'RabbitMQ server is unreachable: {why.args[1]}.')

    finally:
        await shutdown(service)


# ---------------------------------------------------------

app = Service(
    redoc_url=None,
    lifespan=lifespan,
    title=config.name,
    version=config.version,
    description=description,
    license_info=license_info,
    openapi_tags=tags_metadata,
    # swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
)
""" The FastAPI application instance. """

# Test log level and show Log config values for testing purposes.
app.logger.debug(f'{config.name} v{config.version} has started...')
app.logger.trace(f'config: {json.dumps(config.model_dump(), indent=2)}')


# ---------------------------------------------------------
#
async def startup(service: Service):
    """ Initialize DB connection. """
    service.logger.info('Establishing MongoDB connection...')
    await Engine.connect_to_mongo()


# ---------------------------------------------------------
#
async def shutdown(service: Service):
    """ Close DB connection. """
    service.logger.info('Disconnecting from MongoDB...')
    await Engine.close_mongo_connection()
