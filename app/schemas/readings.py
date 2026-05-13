from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, field_serializer, field_validator


BLOCK_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


class BlockComponentValue(BaseModel):
    component_key: str
    value: Decimal
    reading_id: int | None = None


class ReadingBlock(BaseModel):
    block_ts: datetime
    components: dict[str, Decimal] | list[BlockComponentValue]

    @field_validator("block_ts", mode="before")
    @classmethod
    def parse_block_ts(cls, value: datetime | str) -> datetime | str:
        if isinstance(value, str):
            return datetime.strptime(value, BLOCK_TIMESTAMP_FORMAT)
        return value

    @field_serializer("block_ts")
    def serialize_block_ts(self, value: datetime) -> str:
        return value.strftime(BLOCK_TIMESTAMP_FORMAT)


class SourceReadings(BaseModel):
    source_code: str
    blocks: list[ReadingBlock]


class DayWiseSummaryResponse(BaseModel):
    reading_date: date | None = None
    category: str
    total_sources: int
    total_blocks: int
    total_components: int
    total_rows: int
    sources: list[SourceReadings]


class IngestReadingRequest(BaseModel):
    source: str = "api"
    sources: list[SourceReadings]


class IngestedReading(BaseModel):
    id: int
    meter_component_id: int
    block_ts: datetime
    value: Decimal
    raw_key: str

    @field_serializer("block_ts")
    def serialize_block_ts(self, value: datetime) -> str:
        return value.strftime(BLOCK_TIMESTAMP_FORMAT)


class IngestReadingResponse(BaseModel):
    accepted: int
    rejected: list[dict[str, str]]
    readings: list[IngestedReading]
