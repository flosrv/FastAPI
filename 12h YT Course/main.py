from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

# Charger l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing! Check your .env file.")

print(f"✅ DATABASE_URL Loaded: {DATABASE_URL}")  # Debugging

# Créer le moteur de base de données
engine = create_async_engine(DATABASE_URL, echo=True)

# Fonction pour initialiser la base de données
async def init_db():
    async with engine.begin() as conn:
        # Utilisation de text() pour une requête SQL brute exécutable
        statement = text("SELECT 'Hello';")
        result = await conn.execute(statement)
        print(result.all())  # Affiche le résultat de la requête

# Session asynchrone pour interagir avec la BDD
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)
