from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os
# Charger les variables d'environnement
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))  # Force le chemin absolu

# Définir la classe de configuration
class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"

# Créer une instance de configuration
Config = Settings()  # Correction ici
