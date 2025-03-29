from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
import os

# Explicitly load environment variables from the .env file
load_dotenv()

# Define your settings class
class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"

# Initialize the settings object
settings = Settings()

# Check if the DATABASE_URL is correctly loaded via Pydantic
print(settings.DATABASE_URL)
