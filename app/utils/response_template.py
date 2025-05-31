from fastapi.responses import JSONResponse
from fastapi import status
from typing import Any, Optional, Dict

from app.utils.utils import serialize


def success_response(
    status_code: int = status.HTTP_200_OK,
    data: Optional[Any] = None,
    message: str = "Success",
    meta: Optional[Dict[str, Any]] = None
) -> JSONResponse:

    content = {
        "status_code": status_code,
        "status": "success",
        "message": message,
    }

    if data is not None:
        if isinstance(data, list):
            content["data"] = [serialize(d) for d in data]
        else:
            content["data"] = serialize(data)

    if meta:
        content["meta"] = meta

    return JSONResponse(status_code=status_code, content=content)



def error_response(status_code=status.HTTP_400_BAD_REQUEST, detail=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "status": "error",
            "detail": detail,
        }
    )
