from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DEBUG: bool = False

    SQLITE_PATH: str = "./data/app_database.db"

    DATABASE_CONNECTION_STRING: str = "sqlite:///data/app_database.db"

    PAGINATION_PAGE_MAX_LIMIT: int = 20


settings = Settings()
