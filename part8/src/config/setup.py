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
import site
from os import environ
from pathlib import Path

# Third party modules
from pydantic import Field
from pydantic_settings import (BaseSettings, SettingsConfigDict)

# Constants
ENVIRONMENT = environ.get('ENVIRONMENT')
""" Current platform environment. """
MISSING_ENV = '>>> missing ENV value <<<'
""" Error message for missing values in the .env file. """
MISSING_SECRET = '>>> missing SECRETS file <<<'
""" Error message for missing secrets file. """
SECRETS_DIR = f'{site.USER_BASE}/secrets'
""" This is where your secrets are stored locally. """


# ---------------------------------------------------------
#
class Configuration(BaseSettings):
    """ Configuration parameters. """
    model_config = SettingsConfigDict(secrets_dir=SECRETS_DIR,
                                      env_file_encoding='utf-8',
                                      env_file=Path(__file__).parent / '.env')

    # project
    name: str = MISSING_ENV
    version: str = MISSING_ENV
    service_name: str = MISSING_ENV

    # Logging parameters.
    log_level: str = MISSING_ENV
    log_format: str = MISSING_ENV
    log_diagnose: bool = ENVIRONMENT != 'prod'

    # database URL
    mongo_url: str = Field(MISSING_SECRET, alias=f'mongo_url_{ENVIRONMENT}')

    # authentication
    service_api_key: str = MISSING_SECRET


# ---------------------------------------------------------

config = Configuration()
""" Configuration parameters instance. """
