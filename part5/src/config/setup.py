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

# BUILTIN modules
import site

# Third party modules
from dotenv import load_dotenv
from pydantic import BaseSettings

# Constants
MISSING_SECRET = '>>> missing SECRETS file <<<'
""" Error message for missing secrets file. """


# ---------------------------------------------------------
#
class Configuration(BaseSettings):
    """ Configuration parameters. """

    # project
    name: str
    version: str

    # database URL
    mongo_url: str = MISSING_SECRET

    class Config:
        secrets_dir = f'{site.USER_BASE}/secrets'


# ---------------------------------------------------------

# Note that the ".env" file is always implicitly loaded.
load_dotenv()

config = Configuration()
""" Configuration parameters instance. """
