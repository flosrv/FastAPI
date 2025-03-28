from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

class Settings(BaseSettings):
    DATABASE_URL : str

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra="ignore")