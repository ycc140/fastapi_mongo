# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-27 15:38:13
     $Rev: 46
"""


# BUILTIN modules
import shutil
import argparse

# Third party modules
import uvicorn
from loguru import logger
from uvicorn.supervisors import Multiprocess, ChangeReload
from loguru_logging_intercept import setup_loguru_logging_intercept

# Local modules
from src.main import log_level
from src.custom_logging import logging, found_log_modules


# ---------------------------------------------------------
#
def run_uvicorn(config: uvicorn.Config, force_exit: bool = False):
    """ Same as uvicorn.run but injects loguru logging. """

    server = uvicorn.Server(config=config)
    server.force_exit = force_exit

    # Trigger Loguru hijacking.
    setup_loguru_logging_intercept(
       modules=found_log_modules(),
       level=logging.getLevelName(config.log_level.upper()))

    if config.should_reload:

        if config.workers > 1:
            logger.warning('"workers" flag is ignored '
                           'when reloading is enabled.')

        sock = config.bind_socket()
        ChangeReload(config, target=server.run, sockets=[sock]).run()

    elif config.workers > 1:
        sock = config.bind_socket()
        Multiprocess(config, target=server.run, sockets=[sock]).run()

    else:
        server.run()


# ---------------------------------------------------------

if __name__ == '__main__':

    Form = argparse.ArgumentDefaultsHelpFormatter
    description = 'A utility script that let you start the app choosing reload or not.'
    parser = argparse.ArgumentParser(description=description, formatter_class=Form)
    parser.add_argument("-r", action="store_true", dest="reload", default=False,
                        help="Activate reload")
    args = parser.parse_args()

    # Make sure the log config file is where it's needed.
    shutil.copy('../logging_config_dev.json',
                './src/config/logging_config.json')

    uv_config = {'app': 'src.main:app', 'log_level': log_level}

    # Add the parameters that reload needs.
    if args.reload:
        uv_config |= {'reload': True, 'log_config': 'src/config/uvicorn.yaml'}

    run_uvicorn(uvicorn.Config(**uv_config))
