# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2024-04-26 17:38:52
     $Rev: 9
"""

# BUILTIN modules
import argparse

# Third party modules
import uvicorn

# Local modules
from src.config.setup import config

# ---------------------------------------------------------

if __name__ == '__main__':
    Form = argparse.ArgumentDefaultsHelpFormatter
    description = 'A utility script that let you start the app choosing reload or not.'
    parser = argparse.ArgumentParser(description=description, formatter_class=Form)
    parser.add_argument("-r", action="store_true", dest="reload", default=False,
                        help="Activate reload")
    args = parser.parse_args()

    # Define default parameters that are used by all.
    uv_config = {'app': 'src.main:app', 'log_level': config.log_level,
                 'log_config': {"disable_existing_loggers": False, "version": 1}}

    # Add the parameters that reload needs.
    if args.reload:
        uv_config |= {'reload': True}

    uvicorn.run(**uv_config)
