# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-03-02 22:00:59
     $Rev: 63
"""

# BUILTIN modules
import secrets

# Third party modules
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# local modules
from .config.setup import config

# Constants
SECURITY = HTTPBasic()
""" HTTP basic authentication object. """


# ---------------------------------------------------------
#
def validate_authentication(credentials: HTTPBasicCredentials = Depends(SECURITY)):
    """ Validate authentication.

    Security is based on HTTP Basic Auth.

    This should only be used for the simplest cases. For example when you are
    running in a network placed behind a firewall and there's no access from
    Internet to the internal network.

    :param credentials: Authentication credentials.
    :raise HTTPException: 401 => When incorrect username or password is supplied.
    """

    correct_password = secrets.compare_digest(credentials.password, config.service_pwd)
    correct_username = secrets.compare_digest(credentials.username, config.service_user)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"})
