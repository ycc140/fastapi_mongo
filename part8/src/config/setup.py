# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-03-01 19:25:11
     $Rev: 60
"""

# BUILTIN modules
import site

# Third party modules
from dotenv import load_dotenv
from pydantic import BaseSettings

# Constants
MISSING_SECRET = '>>> missing SECRETS file <<<'
""" Error message for missing secrets file. """
MISSING_ENV = '>>> missing ENV value <<<'
""" Error message for missing values in the .env file. """


# ---------------------------------------------------------
#
class Configuration(BaseSettings):
    """ Configuration parameters. """

    # project
    name: str = MISSING_ENV
    version: str = MISSING_ENV

    # database URL
    mongo_url: str = MISSING_SECRET

    # authentication
    service_user: str = MISSING_ENV
    service_pwd: str = MISSING_SECRET

    class Config:
        secrets_dir = f'{site.USER_BASE}/secrets'


# ---------------------------------------------------------

# Note that the ".env" file is always implicitly loaded.
load_dotenv()

config = Configuration()
""" Configuration parameters instance. """
