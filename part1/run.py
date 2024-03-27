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
import argparse
from contextlib import suppress

# Third party modules
import uvicorn

if __name__ == "__main__":
    Form = argparse.ArgumentDefaultsHelpFormatter
    description = 'A utility script that let you start the app choosing reload or not.'
    parser = argparse.ArgumentParser(description=description, formatter_class=Form)
    parser.add_argument("-r", action="store_true", dest="reload", default=False,
                        help="Activate reload")
    args = parser.parse_args()

    # Define default parameters that are used by all.
    uv_config = {'app': 'src.main:app', 'log_level': "debug"}

    # Add the parameters that reload needs.
    if args.reload:
        uv_config |= {'reload': True}

    with suppress(KeyboardInterrupt):
        uvicorn.run(**uv_config)
