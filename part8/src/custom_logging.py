# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-03-04 13:29:26
     $Rev: 70
"""

# BUILTIN modules
import sys
import json
import logging
from pathlib import Path
from types import FrameType
from typing import Callable, Tuple, cast

# Third party modules
from loguru import logger


# ---------------------------------------------------------
#
class InterceptHandler(logging.Handler):
    """Logs to loguru from Python logging module"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name

        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2

        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info).log(
            level,
            record.getMessage()
        )


# ------------------------------------------------------------------------
#
class CustomizeLogger:
    """ Customize logger. """

    # ---------------------------------------------------------
    #
    @classmethod
    def make_logger(cls) -> Tuple[str, Callable]:
        """ Make logger.

        :return: Loglevel and customized logger object.
        """

        config = cls._load_logging_config()
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

        for logger_name in logging.root.manager.loggerDict.keys():

            if logger_name not in seen:
                seen.add(logger_name.split(".")[0])
                mod_logger = logging.getLogger(logger_name)
                mod_logger.handlers = [InterceptHandler(level=level.upper())]
                mod_logger.propagate = False

        return logger.bind(request_id=None, method=None)

    # ---------------------------------------------------------
    #
    @classmethod
    def _load_logging_config(cls,) -> dict:
        """ load logging configuration file.

        :return: Logging config file content.
        """

        cwd = Path(__file__).parent
        config_file = cwd.parent.parent / 'logging_config_dev.json'

        with open(config_file) as hdl:
            config = json.load(hdl)

        return config
