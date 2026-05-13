from datetime import datetime
from decimal import Decimal

import psycopg
from asyncua import Client

from app.core.config import settings
from app.repositories.reading_repository import ReadingRepository


class OpcIngestionService:
    def __init__(self, conn: psycopg.Connection) -> None:
        self.repository = ReadingRepository(conn)

    async def read_and_ingest_pqm(self, block_ts: datetime) -> dict:
        components = self.repository.get_opc_components(category="PQM")
        if not components:
            return {
                "success": 0,
                "failed": 0,
                "rejected": [],
                "message": "No active PQM OPC node mappings found",
            }

        success_count = 0
        rejected: list[dict[str, str]] = []

        try:
            async with Client(settings.pqm_opc_url) as client:
                for component in components:
                    source_code = component["source_name"] or component["source_code"]
                    component_key = component["component_key"]
                    node_id = component["external_key"]

                    try:
                        value = await client.get_node(node_id).read_value()
                        inserted = self.repository.ingest_block_reading(
                            category="PQM",
                            source_code=source_code,
                            component_key=component_key,
                            block_ts=block_ts,
                            value=Decimal(str(value)),
                            source="opc",
                        )
                        if inserted is None:
                            rejected.append(
                                {
                                    "source_code": source_code,
                                    "component_key": component_key,
                                    "node_id": node_id,
                                    "reason": "source/component mapping not found",
                                }
                            )
                            continue

                        success_count += 1
                    except Exception as exc:
                        rejected.append(
                            {
                                "source_code": source_code,
                                "component_key": component_key,
                                "node_id": node_id,
                                "reason": str(exc),
                            }
                        )
        except Exception as exc:
            return {
                "success": 0,
                "failed": len(components),
                "rejected": [
                    {
                        "source_code": component["source_name"] or component["source_code"],
                        "component_key": component["component_key"],
                        "node_id": component["external_key"],
                        "reason": f"OPC connection failed: {exc}",
                    }
                    for component in components
                ],
                "opc_url": settings.pqm_opc_url,
                "block_ts": block_ts.strftime("%Y-%m-%d %H:%M:%S"),
            }

        return {
            "success": success_count,
            "failed": len(rejected),
            "rejected": rejected,
            "opc_url": settings.pqm_opc_url,
            "block_ts": block_ts.strftime("%Y-%m-%d %H:%M:%S"),
        }
