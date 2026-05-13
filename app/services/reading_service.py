from datetime import date

import psycopg

from app.repositories.reading_repository import ReadingRepository
from app.schemas.readings import (
    DayWiseSummaryResponse,
    IngestReadingRequest,
    ReadingBlock,
    SourceReadings,
)


class ReadingService:
    def __init__(self, conn: psycopg.Connection) -> None:
        self.repository = ReadingRepository(conn)

    def get_day_wise_summary(
        self,
        *,
        category: str,
        reading_date: date | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> DayWiseSummaryResponse:
        rows = self.repository.get_day_wise_readings(
            category=category,
            reading_date=reading_date,
            from_date=from_date,
            to_date=to_date,
        )

        sources_map: dict[tuple[int, str], dict] = {}
        total_blocks: set[tuple[int, str]] = set()
        total_components: set[tuple[int, str]] = set()

        for row in rows:
            source_key = (row["source_id"], row["source_code"])
            source = sources_map.setdefault(
                source_key,
                {
                    "source_code": row["source_name"] or row["source_code"],
                    "blocks": {},
                },
            )
            block = source["blocks"].setdefault(
                row["block_ts"].isoformat(),
                {
                    "block_ts": row["block_ts"],
                    "components": {},
                },
            )
            block["components"][row["component_key"]] = row["value"]
            total_blocks.add((row["source_id"], row["block_ts"].isoformat()))
            total_components.add((row["source_id"], row["component_key"]))

        sources: list[SourceReadings] = []
        for source in sources_map.values():
            blocks = [
                ReadingBlock(**block)
                for block in sorted(source["blocks"].values(), key=lambda item: item["block_ts"])
            ]
            sources.append(
                SourceReadings(
                    source_code=source["source_code"],
                    blocks=blocks,
                )
            )

        return DayWiseSummaryResponse(
            reading_date=reading_date,
            category=category,
            total_sources=len(sources),
            total_blocks=len(total_blocks),
            total_components=len(total_components),
            total_rows=len(rows),
            sources=sources,
        )

    def ingest_readings(self, *, category: str, payload: IngestReadingRequest) -> dict:
        success_count = 0
        rejected: list[dict[str, str]] = []

        for source_item in payload.sources:
            for block in source_item.blocks:
                component_values = (
                    block.components.items()
                    if isinstance(block.components, dict)
                    else ((item.component_key, item.value) for item in block.components)
                )
                for component_key, value in component_values:
                    inserted = self.repository.ingest_block_reading(
                        category=category,
                        source_code=source_item.source_code,
                        component_key=component_key,
                        block_ts=block.block_ts,
                        value=value,
                        source=payload.source,
                    )
                    if inserted is None:
                        rejected.append(
                            {
                                "source_code": source_item.source_code,
                                "component_key": component_key,
                                "block_ts": block.block_ts.isoformat(),
                                "reason": "meter/component mapping not found",
                            }
                        )
                        continue

                    success_count += 1

        return {
            "success": success_count,
            "failed": len(rejected),
            "rejected": rejected,
        }
