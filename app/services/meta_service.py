import psycopg

from app.repositories.meta_repository import MetaRepository
from app.schemas.meta import MetaComponent, MetaModule, MetaResponse, MetaSource


SUPPORTED_MODULES = [
    ("PQM", "PQM"),
    ("WMS", "WMS"),
    ("SACU", "SACU"),
    ("INVERTER", "Inverter"),
]


class MetaService:
    def __init__(self, conn: psycopg.Connection) -> None:
        self.repository = MetaRepository(conn)

    def get_meta(self) -> MetaResponse:
        rows = self.repository.get_meter_components()

        modules = {
            module_key: {
                "module_key": module_key,
                "display_name": display_name,
                "meters": {},
            }
            for module_key, display_name in SUPPORTED_MODULES
        }

        for row in rows:
            module_key = row["category"]
            if module_key not in modules:
                modules[module_key] = {
                    "module_key": module_key,
                    "display_name": module_key,
                    "meters": {},
                }

            meter = modules[module_key]["meters"].setdefault(
                row["source_id"],
                {
                    "source_code": row["source_name"] or row["source_code"],
                    "category": row["category"],
                    "location": row["location"],
                    "components": [],
                },
            )

            if row["component_key"]:
                meter["components"].append(
                    MetaComponent(
                        component_key=row["component_key"],
                        display_name=row["display_name"],
                        unit=row["unit"],
                        data_type=row["data_type"],
                    )
                )

        response_modules: list[MetaModule] = []
        for module in modules.values():
            sources = [MetaSource(**meter) for meter in module["meters"].values()]
            response_modules.append(
                MetaModule(
                    module_key=module["module_key"],
                    display_name=module["display_name"],
                    sources=sources,
                )
            )

        return MetaResponse(modules=response_modules)
