from datetime import date

import psycopg
from fastapi import APIRouter, Depends, Query

from app.core.response import success_response
from app.db.session import get_connection
from app.schemas.readings import IngestReadingRequest
from app.services.reading_service import ReadingService


router = APIRouter()


def get_day_wise_summary_for_category(
    *,
    category: str,
    date: date,
    conn: psycopg.Connection,
) -> dict:
    service = ReadingService(conn)
    data = service.get_day_wise_summary(category=category, reading_date=date)
    return success_response(f"{category} readings fetched successfully", data)


def ingest_readings_for_category(
    *,
    category: str,
    payload: IngestReadingRequest,
    conn: psycopg.Connection,
) -> dict:
    service = ReadingService(conn)
    data = service.ingest_readings(category=category, payload=payload)
    message = f"{category} readings ingested successfully" if data["failed"] == 0 else f"{category} readings ingested with failures"
    return success_response(message, data)


@router.get("/pqm/readings/day-wise")
def get_pqm_day_wise_summary(
    date: date = Query(..., description="Reading date in YYYY-MM-DD format"),
    conn: psycopg.Connection = Depends(get_connection),
) -> dict:
    return get_day_wise_summary_for_category(category="PQM", date=date, conn=conn)


@router.post("/pqm/readings/ingest")
def ingest_pqm_readings(
    payload: IngestReadingRequest,
    conn: psycopg.Connection = Depends(get_connection),
) -> dict:
    return ingest_readings_for_category(category="PQM", payload=payload, conn=conn)


@router.get("/wms/readings/day-wise")
def get_wms_day_wise_summary(
    date: date = Query(..., description="Reading date in YYYY-MM-DD format"),
    conn: psycopg.Connection = Depends(get_connection),
) -> dict:
    return get_day_wise_summary_for_category(category="WMS", date=date, conn=conn)


@router.post("/wms/readings/ingest")
def ingest_wms_readings(
    payload: IngestReadingRequest,
    conn: psycopg.Connection = Depends(get_connection),
) -> dict:
    return ingest_readings_for_category(category="WMS", payload=payload, conn=conn)


@router.get("/sacu/readings/day-wise")
def get_sacu_day_wise_summary(
    date: date = Query(..., description="Reading date in YYYY-MM-DD format"),
    conn: psycopg.Connection = Depends(get_connection),
) -> dict:
    return get_day_wise_summary_for_category(category="SACU", date=date, conn=conn)


@router.post("/sacu/readings/ingest")
def ingest_sacu_readings(
    payload: IngestReadingRequest,
    conn: psycopg.Connection = Depends(get_connection),
) -> dict:
    return ingest_readings_for_category(category="SACU", payload=payload, conn=conn)
