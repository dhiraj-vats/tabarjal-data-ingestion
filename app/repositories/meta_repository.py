import psycopg


class MetaRepository:
    def __init__(self, conn: psycopg.Connection) -> None:
        self.conn = conn

    def get_meter_components(self) -> list[dict]:
        query = """
            SELECT
                s.id AS source_id,
                s.source_code,
                s.source_name,
                s.category,
                s.location,
                c.id AS component_id,
                c.component_key,
                c.display_name,
                c.external_key,
                c.unit,
                c.data_type
            FROM tb_data_sources s
            LEFT JOIN tb_source_components c
                ON c.source_id = s.id
               AND c.is_active = TRUE
            WHERE s.is_active = TRUE
            ORDER BY s.category, s.source_name, c.component_key;
        """

        with self.conn.cursor() as cur:
            cur.execute(query)
            return list(cur.fetchall())
