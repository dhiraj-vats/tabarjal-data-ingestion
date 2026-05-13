import psycopg
from fastapi import APIRouter, Depends

from app.core.response import success_response
from app.db.session import get_connection
from app.services.meta_service import MetaService


router = APIRouter()


@router.get("")
def get_meta(conn: psycopg.Connection = Depends(get_connection)) -> dict:
    service = MetaService(conn)
    data = service.get_meta()
    return success_response("Meta fetched successfully", data)
