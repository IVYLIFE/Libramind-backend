from fastapi.responses import JSONResponse
from fastapi import status


def success_response(status_code=status.HTTP_200_OK, data=None, message="Success", meta=None):
    content = {
        "status_code": status_code,
        "status": "success",
        "message": message,
    }
    if data:
        content["data"] = data
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
