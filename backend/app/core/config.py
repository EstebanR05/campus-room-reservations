from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Campus Room Reservations API"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "base_datos_docu"


settings = Settings()
