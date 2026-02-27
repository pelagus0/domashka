from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/ivelum"
    upstream_base_url: str = "https://news.ycombinator.com"
    proxy_base_url: str = "http://localhost:8002"


settings = Settings()

