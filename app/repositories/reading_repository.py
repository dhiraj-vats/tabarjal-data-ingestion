from datetime import date, datetime
from decimal import Decimal

import psycopg


READING_TABLES = {
    "PQM": "tb_pqm_readings",
    "WMS": "tb_wms_readings",
    "SACU": "tb_sacu_readings",
    "INVERTER": "tb_inverter_readings",
}


class ReadingRepository:
    def __init__(self, conn: psycopg.Connection) -> None:
        self.conn = conn

    def get_day_wise_readings(
        self,
        *,
        category: str,
        reading_date: date | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict]:
        table_name = READING_TABLES[category]
        filters: list[str] = ["s.category = %(category)s"]
        params: dict[str, date | str] = {"category": category}

        if reading_date:
            filters.append("r.block_ts::date = %(reading_date)s")
            params["reading_date"] = reading_date
        if from_date:
            filters.append("r.block_ts::date >= %(from_date)s")
            params["from_date"] = from_date
        if to_date:
            filters.append("r.block_ts::date <= %(to_date)s")
            params["to_date"] = to_date

        query = f"""
            SELECT
                r.id AS reading_id,
                r.block_ts,
                s.id AS source_id,
                s.source_code,
                s.source_name,
                s.category,
                c.component_key,
                r.value
            FROM {table_name} r
            JOIN tb_source_components c ON c.id = r.src_component_id
            JOIN tb_data_sources s ON s.id = c.source_id
            WHERE {' AND '.join(filters)}
              AND r.is_deleted = FALSE
            ORDER BY r.block_ts DESC, s.source_code, c.component_key;
        """

        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return list(cur.fetchall())

    def ingest_block_reading(
        self,
        *,
        category: str,
        source_code: str,
        component_key: str,
        block_ts: datetime,
        value: Decimal,
        source: str,
    ) -> dict | None:
        table_name = READING_TABLES[category]
        params = {
            "category": category,
            "source_code": source_code,
            "component_key": component_key,
            "block_ts": block_ts,
            "value": value,
            "source": source,
        }

        mapping_query = """
            SELECT
                c.id,
                s.source_code
            FROM tb_source_components c
            JOIN tb_data_sources s ON s.id = c.source_id
            WHERE c.component_key = %(component_key)s
              AND c.is_active = TRUE
              AND s.is_active = TRUE
              AND s.category = %(category)s
              AND (
                    s.source_code = %(source_code)s::varchar
                 OR s.source_name = %(source_code)s::varchar
              )
            LIMIT 1;
        """
        soft_delete_query = """
            UPDATE {table_name}
            SET
                is_deleted = TRUE,
                updated_at = NOW()
            WHERE src_component_id = %(src_component_id)s
              AND block_ts = %(block_ts)s
              AND is_deleted = FALSE;
        """.format(table_name=table_name)
        insert_query = f"""
            INSERT INTO {table_name} (
                src_component_id,
                block_ts,
                value,
                source,
                raw_key,
                is_deleted
            )
            VALUES (
                %(src_component_id)s,
                %(block_ts)s,
                %(value)s,
                %(source)s,
                %(raw_key)s,
                FALSE
            )
            RETURNING
                id,
                src_component_id,
                block_ts,
                value,
                raw_key;
        """

        with self.conn.cursor() as cur:
            cur.execute(mapping_query, params)
            mapped_component = cur.fetchone()
            if mapped_component is None:
                return None

            params["src_component_id"] = mapped_component["id"]
            params["raw_key"] = f"{mapped_component['source_code']}.{component_key}"

            cur.execute(soft_delete_query, params)
            cur.execute(insert_query, params)
            return cur.fetchone()
