# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     app_name: str = "GenWeatherAPI"
#     database_url: str = "postgresql://postgres:root@localhost:5432/re_tabrajhal_shv"

#     model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# settings = Settings()

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = os.getenv("ENV_FILE", ".env")


class Settings(BaseSettings):
    app_name: str = "GenWeatherAPI"

    database_url: str
    pqm_opc_url: str = "opc.tcp://172.16.51.1:4840"
    ingest_log_dir: str = "logs/ingest"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
