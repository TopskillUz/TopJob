import getpass
import pathlib
from typing import Optional, Any
from uuid import UUID

import requests
from pydantic import PostgresDsn, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings

if getpass.getuser() == "yakubov":
    env_filename = ".env.dev"
else:
    env_filename = ".env.prod"

ENV_FILE_PATH = f"{pathlib.Path(__file__).parents[3]}/deploy/{env_filename}"


class Settings(BaseSettings):
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"
    SVC_PORT: int
    DEBUG: Optional[int] = False
    TOPSKILL_BASE_URL: Optional[AnyHttpUrl] = "https://topskill.uz"
    TOPSKILL_ADMIN_USERNAME: str
    TOPSKILL_ADMIN_PASSWORD: str
    SECRET_KEY: str

    # JWT
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    JWT_ALGORITHM: str
    REFRESH_TOKEN_EXPIRES_IN: Optional[int] = 60 * 24 * 10  # 10 days
    ACCESS_TOKEN_EXPIRES_IN: Optional[int] = 3600  # 60 minutes

    # Pool connection
    DB_POOL_SIZE: int = 83
    WEB_CONCURRENCY: int = 9
    POOL_SIZE: int = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

    # Database
    DATABASE: Optional[str] = 'postgres'
    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_USER: str
    DATABASE_NAME: str
    DATABASE_HOST: str

    SYNC_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SYNC_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v

        return str(PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=values.data.get("DATABASE_USER"),
            password=values.data.get("DATABASE_PASSWORD"),
            host=values.data.get("DATABASE_HOST"),
            port=int(values.data.get("DATABASE_PORT")),
            path=f"{values.data.get('DATABASE_NAME') or ''}",
        ))

    # Redis
    REDIS_HOST: str
    REDIS_PORT: str

    BACKEND_CORS_ORIGINS: str

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str) -> list[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        raise ValueError(v)

    class Config:
        env_file = ENV_FILE_PATH


settings = Settings()
