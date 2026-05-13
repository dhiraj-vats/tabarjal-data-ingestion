from typing import Any

from fastapi.encoders import jsonable_encoder


def success_response(message: str, data: Any = None) -> dict[str, Any]:
    return {
        "status": True,
        "message": message,
        "data": jsonable_encoder(data),
    }


def error_response(message: str, data: Any = None) -> dict[str, Any]:
    return {
        "status": False,
        "message": message,
        "data": jsonable_encoder(data),
    }
