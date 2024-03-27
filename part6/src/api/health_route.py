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

# Third party modules
from fastapi import APIRouter
from fastapi.responses import JSONResponse

# local modules
from ..health_manager import HealthManager
from ..schemas import HealthResponseModel, HealthStatusError

# Constants
ROUTER = APIRouter(prefix="/health", tags=["Health endpoint"])
""" Health API endpoint router. """


# ---------------------------------------------------------
#
@ROUTER.get(
    '',
    response_model=HealthResponseModel,
    responses={500: {"model": HealthStatusError}},
)
async def health_check() -> JSONResponse:
    """ ***Return Health check status.*** """
    content = await HealthManager().get_status()
    response_code = (200 if content.status else 500)

    return JSONResponse(status_code=response_code,
                        content=content.model_dump())
