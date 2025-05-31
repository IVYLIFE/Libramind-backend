from fastapi.responses import JSONResponse
from fastapi import status
from typing import Any, Optional, Dict
from datetime import date


def format_dates_in_dict(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.strftime("%d-%m-%Y")
    return data


def serialize(item):
    if hasattr(item, "model_dump"):
        item_dict = item.model_dump()
    elif hasattr(item, "dict"):
        item_dict = item.dict()
    else:
        item_dict = item

    if isinstance(item_dict, dict):
        return format_dates_in_dict(item_dict)
    return item_dict


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
