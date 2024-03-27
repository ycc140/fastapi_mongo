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
from os import environ
from pathlib import Path

# Third party modules
from pydantic_settings import (BaseSettings, SettingsConfigDict)

# Constants
ENVIRONMENT = environ.get('ENVIRONMENT')
""" Current platform environment. """
MISSING_ENV = '>>> missing ENV value <<<'
""" Error message for missing values in the .env file. """


# ---------------------------------------------------------
#
class Configuration(BaseSettings):
    """ Configuration parameters. """
    model_config = SettingsConfigDict(env_file_encoding='utf-8',
                                      env_file=Path(__file__).parent / '.env')

    # Project parameters.
    name: str = MISSING_ENV
    version: str = MISSING_ENV
    service_name: str = MISSING_ENV

    # Logging parameters.
    log_level: str = MISSING_ENV
    log_format: str = MISSING_ENV
    log_diagnose: bool = ENVIRONMENT != 'prod'


# ---------------------------------------------------------

config = Configuration()
""" Configuration parameters instance. """
