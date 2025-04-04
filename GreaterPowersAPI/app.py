from fastapi import FastAPI, HTTPException
from starlette import status
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient  # Utiliser le client asynchrone
from pymongo.errors import PyMongoError
from routes import endPoint
from db.db_main import client_atlas
from Endpoints.weapons import endPoint as weapons_endpoints
from Endpoints.abilities import endPoint as abilities_endpoints
from Endpoints.consumables_non_combats import endPoint as consumables_non_combat_endpoints
from Endpoints.ability_mechs import endPoint as ability_mechs_endpoints
from Endpoints.skyships_upgrades import endPoint as skyships_upgrades_endpoints




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

# Inclusion des routers
app.include_router(weapons_endpoints, prefix="/weapons", tags=["weapons"])
app.include_router(abilities_endpoints, prefix="/abilities", tags=["abilities"])
app.include_router(consumables_non_combat_endpoints, prefix="/consumables_non_combat", tags=["consumables_non_combat"])
app.include_router(ability_mechs_endpoints, prefix="/ability_mechs", tags=["ability_mechs"])
app.include_router(skyships_upgrades_endpoints, prefix="/skyships_upgrades", tags=["skyships_upgrades"])

#app.include_router(endPoint)
# Exemple d'endpoint dans routes.py pour tester la connexion MongoDB
@endPoint.get("/test_connection")
async def test_connection():
    return {"message": "Connexion MongoDB réussie"}
@app.get("/welcome")
async def  welcome():
    return {"Welcome": "Visitor"}



