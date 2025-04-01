from fastapi import FastAPI, HTTPException
from starlette import status
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient  # Utiliser le client asynchrone
from pymongo.errors import PyMongoError
from routes import endPoint
from db.db_main import client_atlas

# 🌍 Lifecycle de l'application avec gestion asynchrone

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Test de connexion à la DB
        await client_atlas.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")

        # 🚀 Connexion à la DB au démarrage
        print("✅ Connexion à MongoDB réussie")
    except PyMongoError as e:
        print(f"❌ Erreur de connexion MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Erreur de connexion à MongoDB")
    
    yield  # ⏳ Attente de la fermeture de l'application
    
    if client_atlas:
        client_atlas.close()  # 🔻 Fermeture propre de la connexion MongoDB
        print("🚪 Connexion MongoDB fermée")

# 🏗 Création de l'application FastAPI
app = FastAPI(lifespan=lifespan)

app.include_router(endPoint)
# Exemple d'endpoint dans routes.py pour tester la connexion MongoDB
@endPoint.get("/test_connection")
async def test_connection():
    return {"message": "Connexion MongoDB réussie"}
@app.get("/welcome")
async def  welcome():
    return {"Welcome": "Visitor"}



