import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = Field(default=8080, alias="PORT")
    gotenberg_base_url: str = Field(default="http://127.0.0.1:3000", alias="GOTENBERG_BASE_URL")
    shared_token: str | None = Field(default=None, alias="SHARED_TOKEN")
    gotenberg_timeout_sec: int = Field(default=120, alias="GOTENBERG_TIMEOUT_SEC")
    cors_allow_origins: str = Field(default="*", alias="CORS_ALLOW_ORIGINS")
    lockbox_enabled: bool = Field(default=False, alias="LOCKBOX_ENABLED")
    lockbox_id: str | None = Field(default=None, alias="LOCKBOX_ID")
    lockbox_endpoint: str | None = Field(default=None, alias="LOCKBOX_ENDPOINT")
    lockbox_iam_token: str | None = Field(default=None, alias="LOCKBOX_IAM_TOKEN")
    aws_access_key_id: str | None = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(default=None, alias="AWS_SECRET_ACCESS_KEY")
    object_storage_endpoint: str = Field(
        default="https://storage.yandexcloud.net",
        alias="OBJECT_STORAGE_ENDPOINT",
    )
    object_storage_region: str = Field(default="ru-central1", alias="OBJECT_STORAGE_REGION")
    object_storage_bucket: str = Field(default="dtm-presets", alias="OBJECT_STORAGE_BUCKET")
    object_storage_prefix: str = Field(default="doc2pdf", alias="OBJECT_STORAGE_PREFIX")
    object_storage_presign_ttl_sec: int = Field(
        default=3600,
        alias="OBJECT_STORAGE_PRESIGN_TTL_SEC",
    )
    mvp_token_ttl_sec: int = Field(default=3600, alias="MVP_TOKEN_TTL_SEC")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

def _normalize_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _load_lockbox_env() -> None:
    lockbox_id = os.getenv("LOCKBOX_ID") or os.getenv("lockbox_id")
    if lockbox_id:
        os.environ["LOCKBOX_ID"] = lockbox_id

    if not lockbox_id or not _normalize_bool(os.getenv("LOCKBOX_ENABLED")):
        return

    from src.services.lockbox_client import load_lockbox_payload

    payload = load_lockbox_payload(lockbox_id)
    for key in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "SHARED_TOKEN"):
        if key in payload and not os.getenv(key):
            os.environ[key] = payload[key]


_load_lockbox_env()
settings = Settings()
