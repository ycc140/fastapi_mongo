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

# Third party modules
import uvicorn


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000,
                log_level="info", reload=True, workers=1)
