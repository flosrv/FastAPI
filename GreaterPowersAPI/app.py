from fastapi import FastAPI, HTTPException
from starlette import status  
from contextlib import asynccontextmanager
from db.db_main import client_atlas, DarkstarDb  # Connexion MongoDB
from models.models import Weapon, GameItem, Developer, User
from models.models import Player, SkyshipUpgrades, ConsumablesAndNoncombatItems, AbilityMechanics, Ability
from pymongo.errors import PyMongoError
from starlette.responses import JSONResponse
import json
from routes import endPoint


# 🌍 Lifecycle de l'application
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        client_atlas.admin.command('ping')
        print("✅ Connexion à MongoDB réussie")
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB: {e}")
    yield
    client_atlas.close()
    print("🚪 Connexion MongoDB fermée")

# 🏗 Création de l'application FastAPI
app = FastAPI(lifespan=lifespan)
app.include_router(endPoint)


@app.get("/welcome")
async def  welcome():
    return {"Welcome": "Visitor"}