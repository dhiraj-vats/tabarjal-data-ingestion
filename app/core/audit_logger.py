import json
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi.encoders import jsonable_encoder

from app.core.config import settings


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_ingest_log_dir() -> Path:
    log_dir = Path(settings.ingest_log_dir)
    if not log_dir.is_absolute():
        log_dir = PROJECT_ROOT / log_dir
    return log_dir


def ensure_ingest_log_dir() -> Path:
    log_dir = get_ingest_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def write_ingest_log(
    *,
    category: str,
    endpoint: str,
    client_ip: str | None,
    payload: Any,
    result: dict[str, Any],
) -> None:
    hit_at = datetime.now().replace(microsecond=0)
    log_dir = ensure_ingest_log_dir() / hit_at.strftime("%Y-%m-%d")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"{category.lower()}.jsonl"
    entry = {
        "hit_at": hit_at.strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "endpoint": endpoint,
        "client_ip": client_ip,
        "payload": jsonable_encoder(payload),
        "result": jsonable_encoder(result),
    }

    with log_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")
