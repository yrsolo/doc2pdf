from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    port: int = Field(default=8080, alias="PORT")
    gotenberg_base_url: str = Field(default="http://localhost:3000", alias="GOTENBERG_BASE_URL")
    shared_token: str | None = Field(default=None, alias="SHARED_TOKEN")
    gotenberg_timeout_sec: int = Field(default=120, alias="GOTENBERG_TIMEOUT_SEC")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
