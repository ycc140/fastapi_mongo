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
import os
import json
import argparse
from pathlib import Path
from configparser import ConfigParser

# Constants.
CWD = Path(__file__).parent
""" Defines the current working directory. """
ADJUSTED_LEVELS = {'TRACE': 'DEBUG', 'SUCCESS': 'INFO'}
""" Adjusted log levels for gunicorn. """


# ---------------------------------------------------------
#
def _create_uvicorn_file(log_config: dict):
    """ Create an uvicorn.json log configuration file.

    Create a new uvicorn log config file based upon the uvicorn template
    file, updated with the log level from the global log config file for
    all available loggers.

    @param log_config: Global log config data.
    """

    level = log_config['logger']['level'].upper()

    # Get uvicorn log template reference.
    with open(f"{CWD}/uvicorn.template") as hdl:
        template = json.load(hdl)

    # Set current log level from global log configuration.
    for item in ('uvicorn.error', 'uvicorn.access'):

        # Make sure any loggers exist before trying an update.
        if 'loggers' in template and item in template['loggers']:
            template['loggers'][item]['level'] = level

    # Store updated uvicorn log configuration.
    with open(f'{CWD.parent.parent}/uvicorn.json', 'w') as hdl:
        json.dump(template, hdl, indent=4)


# ---------------------------------------------------------
#
def _create_gunicorn_file(log_config: dict):
    """ Create a gunicorn.conf log configuration file.

    Create a new gunicorn log config file based upon the gunicorn template
    file, updated with the log level from the global log config file for
    all available loggers.

    @param log_config: Global log config data.
    """

    ini_config = ConfigParser()
    level = log_config['logger']['level'].upper()

    # Get gunicorn log template reference.
    ini_config.read(f"{CWD}/gunicorn.template")

    # Set current log level from global log configuration.
    for section in ('logger_root', 'logger_gunicorn.error', 'logger_gunicorn.access'):

        # gunicorn only accepts default python log levels, so we
        # need to handle the extra log levels that Loguru have defined.
        if section in ini_config:
            ini_config.set(section, 'level', ADJUSTED_LEVELS.get(level, level))

    # Store updated gunicorn log configuration.
    with open(f'{CWD.parent.parent}/gunicorn.conf', 'w') as hdl:
        ini_config.write(hdl)


# ---------------------------------------------------------
#
def create_config_files(log_config: str):
    """ Create uvicorn and gunicorn log configuration files.

    Create a new uvicorn log config file based upon the uvicorn template
    file, updated with the log level from the global log config file.

    Create a new gunicorn log config file based upon the gunicorn template
    file, updated with the log level from the global log config file.

    @param log_config: Name of log config file.
    """

    # Look for environment variable that's only is defined in Docker.
    location = os.getenv('BUILD_ENV', 'dev')

    # Get global log file configuration.
    with open(f"{CWD.parent.parent}/{log_config}") as hdl:
        config = json.load(hdl)

    if location == 'prod':
        _create_gunicorn_file(config)

    else:
        _create_uvicorn_file(config)


# ---------------------------------------------------------

if __name__ == '__main__':

    Form = argparse.ArgumentDefaultsHelpFormatter
    description = 'A utility script that let you start the app choosing reload or not.'
    parser = argparse.ArgumentParser(description=description, formatter_class=Form)
    parser.add_argument("file", help="Specify log config file")
    args = parser.parse_args()

    create_config_files(args.file)
