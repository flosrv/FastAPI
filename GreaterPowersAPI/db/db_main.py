from pymongo.server_api import ServerApi
import json
from motor.motor_asyncio import AsyncIOMotorClient


# Charger les informations de connexion
mongo_creds = r"c:\Credentials\mongo_creds.json"

with open(mongo_creds, 'r') as file:
    content = json.load(file)
    mongo_password = content["password"]
    mongo_user = content["user"]

# Construire l'URI de connexion pour MongoDB Atlas
uri_atlas = f"mongodb+srv://{mongo_user}:{mongo_password}@myfirstmongodbcluster.mde7n.mongodb.net/?appName=MyFirstMongoDbCluster"

# Créer le client MongoDB
client_atlas = AsyncIOMotorClient(uri_atlas, server_api=ServerApi('1'))

# Sélectionner la base de données
DarkstarDb = client_atlas.DarkstarDb

# Dictionnaire des collections
collection_weapons = DarkstarDb["WEAPONS"]
collection_ability_mechanics = DarkstarDb["Ability_mechanics"]
collection_consumables = DarkstarDb["Consumables_and_noncombat_items"]
collection_skyship_upgrades = DarkstarDb["Skyship_Upgrades"]
collection_abilities = DarkstarDb["Abilities_Table"]
collection_devs_data = DarkstarDb["devs_data"]
collection_players_data = DarkstarDb["players_data"]


# Vérification de la connexion
try:
    client_atlas.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
