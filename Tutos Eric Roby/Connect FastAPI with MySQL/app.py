from fastapi import FastAPI
from routes.routes import endPoint  # Importer le routeur défini dans routes.py
from db.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Configuration de base de l'application FastAPI
logger = logging.getLogger("uvicorn")

# Définir le lifespan pour initialiser et fermer la connexion à la base de données
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialiser la base de données (création des tables si nécessaire)
    init_db()
    logger.info("Base de données initialisée avec succès.")
    yield
    # Code à exécuter après l'arrêt de l'application (ex. fermer la connexion DB, nettoyage)
    logger.info("Application fermée, nettoyage effectué.")


# Créer l'application FastAPI avec lifespan pour gérer les connexions à la DB
app = FastAPI(lifespan=lifespan)

# Ajouter le middleware CORS pour permettre les requêtes cross-origin
origins = [
    "http://localhost",  # Autoriser localhost
    "http://localhost:8000",  # Autoriser FastAPI en local
    # Tu peux ajouter ici d'autres origines autorisées si tu as un frontend externe.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Liste des origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les headers
)

# Inclure les routes définies dans routes.py
app.include_router(endPoint)

# Exemple de route pour vérifier que l'API fonctionne
@app.get("/")
def read_root():
    return {"msg": "Bienvenue dans l'API de gestion des utilisateurs"}

