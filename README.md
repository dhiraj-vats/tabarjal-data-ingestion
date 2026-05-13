# GenWeatherAPI

FastAPI REST API for centralized source/component mapping and category-wise readings.

## Setup

```bash
cd D:\xampp\htdocs\RE-FNS-TABRAJAL\data-ingestion
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

## Quick Check

```http
GET http://127.0.0.1:8000/api/v1/pqm/readings/day-wise?date=2026-05-12
GET http://127.0.0.1:8000/api/v1/wms/readings/day-wise?date=2026-05-12
```

```http
GET http://127.0.0.1:8000/api/v1/meta
```

## Ingest Example

Current database has been migrated through `sql/005_generic_sources_and_wms.sql`.

```http
POST http://127.0.0.1:8000/api/v1/pqm/readings/ingest
Content-Type: application/json

{
  "source": "api",
  "sources": [
    {
      "source_code": "PQM - 01",
      "blocks": [
        {
          "block_ts": "2026-05-12 00:00:00",
          "components": {
            "total_active_power": 1300.25
          }
        }
      ]
    },
    {
      "source_code": "PQM - 02",
      "blocks": [
        {
          "block_ts": "2026-05-12 00:00:00",
          "components": {
            "total_active_power": 1008.50
          }
        }
      ]
    }
  ]
}
```

WMS example:

```http
POST http://127.0.0.1:8000/api/v1/wms/readings/ingest
Content-Type: application/json

{
  "source": "api",
  "sources": [
    {
      "source_code": "MVPS02",
      "blocks": [
        {
          "block_ts": "2026-05-12 10:00:00",
          "components": {
            "dni_wm2": 800.5,
            "ghi_w": 620.2,
            "wind_speed": 4.8
          }
        }
      ]
    }
  ]
}
```
