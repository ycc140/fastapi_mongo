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
import sys
import json
import shutil
import logging
from pathlib import Path
from typing import Callable, Tuple, Iterable

# Third party modules
from loguru import logger
from loguru_logging_intercept import (InterceptHandler)


# ---------------------------------------------------------
#
def found_log_modules() -> Iterable:
    """ Return list of found python logging modules.

    :return: List of found python logging modules.
    """
    return logging.root.manager.loggerDict.keys()


# ------------------------------------------------------------------------
#
class CustomizeLogger:
    """ Customize logger. """

    # ---------------------------------------------------------
    #
    @classmethod
    def make_logger(cls, config_file: Path) -> Tuple[str, Callable]:
        """ Make logger.

        :param config_file: Logging config file.
        :return: Loglevel and customized logger object.
        """

        config = cls._load_logging_config(config_file)
        logging_config = config.get('logger')

        return (logging_config.get('level'),
                cls._customize_logging(
                    level=logging_config.get('level'),
                    diagnose=logging_config.get('diagnose'),
                    colorize=logging_config.get('colorize'),
                    log_format=logging_config.get('format')))

    # ---------------------------------------------------------
    #
    @classmethod
    def _customize_logging(cls, level: str, diagnose: bool,
                           colorize: bool, log_format: str) -> logger:
        """ Return customized logger object.

        :param level: Logging level.
        :param diagnose: Diagnose status.
        :param colorize: Coloring status.
        :param log_format: Log format string.
        :return: customized logger object.
        """

        # Remove all existing loggers.
        logger.remove()

        # Create a basic Loguru logging config.
        logger.add(
            sys.stderr,
            enqueue=True,
            backtrace=True,
            format=log_format,
            colorize=colorize,
            diagnose=diagnose,
            level=level.upper())

        # Prepare to incorporate python standard logging.
        seen = set()
        logging.basicConfig(handlers=[InterceptHandler()], level=0)

        for logger_name in found_log_modules():

            if logger_name not in seen:
                seen.add(logger_name.split(".")[0])
                mod_logger = logging.getLogger(logger_name)
                mod_logger.handlers = [InterceptHandler(level=level.upper())]
                mod_logger.propagate = False

        return logger.bind(request_id=None, method=None)

    # ---------------------------------------------------------
    #
    @classmethod
    def _load_logging_config(cls, config_file: Path) -> dict:
        """ load logging configuration file.

        :param config_file: Logging config file.
        :return: Logging config file content.
        """

        # Copy the file if it does not already exist. When running
        # inside Docker, skip it (Docker handles that on its own).
        if not Path('/.dockerenv').exists():
            cwd = Path(__file__).parent
            log_file = cwd.parent.parent / 'logging_config_dev.json'
            shutil.copy(log_file, cwd / 'config/logging_config.json')

        with open(config_file) as hdl:
            config = json.load(hdl)

        return config
