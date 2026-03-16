from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = Field(default=8080, alias="PORT")
    gotenberg_base_url: str = Field(default="http://localhost:3000", alias="GOTENBERG_BASE_URL")
    shared_token: str | None = Field(default=None, alias="SHARED_TOKEN")
    gotenberg_timeout_sec: int = Field(default=120, alias="GOTENBERG_TIMEOUT_SEC")
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

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
