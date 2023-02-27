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
from dotenv import load_dotenv
from pydantic import BaseSettings


# ---------------------------------------------------------
#
class Configuration(BaseSettings):
    """ Configuration parameters. """

    # project
    name: str
    version: str


# ---------------------------------------------------------

# Note that the ".env" file is always implicitly loaded.
# ENV_FILE environment value is set by uvicorn configuration in file run.py.
load_dotenv()

config = Configuration()
""" Configuration parameters instance. """
