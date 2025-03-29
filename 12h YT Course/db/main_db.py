from sqlmodel import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env
load_dotenv()

# Récupérer la DATABASE_URL depuis les variables d'environnement
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing! Check your .env file.")

print(f"✅ DATABASE_URL Loaded: {DATABASE_URL}")

# Créer le moteur de la base de données avec SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Créer la session asynchrone
SessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base pour les modèles
Base = declarative_base()

# Fonction pour initialiser la BDD
async def init_db():
    async with engine.begin() as conn:
        result = await conn.execute("SELECT 'Hello';")
        print(result.all())
