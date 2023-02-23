# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: MIT

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-18 00:27:47
     $Rev: 1
"""

# Third party modules
import uvicorn


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000,
                log_level="info", reload=True, workers=1)
