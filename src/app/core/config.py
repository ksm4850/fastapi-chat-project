import os
from os import environ
from pathlib import Path
from typing import Any, List
from urllib.parse import quote

from pydantic import (
    AnyHttpUrl,
    FieldValidationInfo,
    PostgresDsn,
    RedisDsn,
    field_validator,
)
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "JWT_SECRET_KEY"
    JWT_TOKEN_EXPIRE_MINUTES: int = 3000
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 3000
    TEST: bool = False
    DEBUG: bool = False
    SQL_PRINT: bool = False

    PROJECT_NAME: str = "FastApi-Chat"
    VERSION: str = "1.0.0"

    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "1234"
    POSTGRES_DB: str = "chat"
    POSTGRES_PORT: int = 5432

    REDIS_SERVER: str = "127.0.0.1"
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""
    REDIS_PORT: int = 6379
    REDIS_EXPIRE_TIME: int = 86400

    REDIS_URI: str | None = None

    # MONGO_DB_NAME: str = ""
    # MONGO_URL: str = ""
    # MONGO_MAX_CONNECTIONS: int = None
    # MONGO_MIN_CONNECTIONS: int = None

    POSTGRES_SCHEMA: str = "public"
    SQLALCHEMY_DATABASE_URI: str | None = None
    SQLALCHEMY_TEST_DATABASE_URI: PostgresDsn | None = None

    if os.name == "nt":  # 윈도우
        TEMPLATE_DIR: str = "./src/templates"
    elif os.name == "posix":  # 리눅스 또는 macOS
        TEMPLATE_DIR: str = "/fastapi-chat-project/src/templates"
    else:
        TEMPLATE_DIR: str = str(Path(__file__).parent / "src" / "templates")  # 기본값

    # noinspection PyMethodParameters
    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: str | None, values: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.data.get("POSTGRES_USER"),
                password=quote(values.data.get("POSTGRES_PASSWORD")),
                host=values.data.get("POSTGRES_SERVER"),
                port=values.data.get("POSTGRES_PORT"),
                path=f"{values.data.get('POSTGRES_DB') or ''}",
            )
        )

    # noinspection PyMethodParameters
    @field_validator("REDIS_URI")
    def redis_connection(cls, v: str | None, values: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return str(
            RedisDsn.build(
                scheme="redis",
                username=values.data.get("REDIS_USER"),
                password=quote(values.data.get("REDIS_PASSWORD")),
                host=values.data.get("REDIS_SERVER"),
                port=values.data.get("REDIS_PORT"),
                path=f"{values.data.get('REDIS_DB') or ''}",
            )
        )

    class Config:
        case_sensitive = True
        env_file = "../../.env"


class LocalConfig(Config):
    DEBUG: bool = True
    SQL_PRINT: bool = True

    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_SCHEMA: str = "public"

    REDIS_SERVER: str = "127.0.0.1"


class TestConfig(Config):
    TEST: bool = True

    POSTGRES_SERVER: str = "127.0.0.1"

    REDIS_SERVER: str = "127.0.0.1"


class ProdConfig(Config):
    pass


def get_config():
    c = dict(prod=ProdConfig, test=TestConfig, local=LocalConfig)
    return c[environ.get("API_ENV", "local")]()
