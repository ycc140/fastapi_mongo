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
from uvicorn import run


if __name__ == "__main__":

    run(port=8000,
        workers=1,
        reload=True,
        use_colors=True,
        host="127.0.0.1",
        log_level="trace",
        app="src.main:app")
