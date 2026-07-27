from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    github_token: str = Field(alias="GITHUB_TOKEN")
    GROQ_API_KEY: str
    GITHUB_WEBHOOK_SECRET: Optional[str] = None
    REVIEWGUARD_API_KEY: str = "dev-secret-key"
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()