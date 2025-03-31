from fastapi import APIRouter, HTTPException, Path, status
from typing import List
from bson import ObjectId
from models.models import Weapon
from serializers import serialize_weapon, serialize_weapons  # Importer la fonction de sérialisation
from db.db_main import client_atlas, DarkstarDb, collection_skyship_upgrades,collection_weapons,collection_abilities,collection_ability_mechanics,collection_consumables,collection_devs_data,collection_players_data

endPoint = APIRouter()

# Récupérer toutes les armes
@endPoint.get("/all_weapons", response_model=List[Weapon])
async def get_all_weapons():
    """Retourne la liste de toutes les armes"""
    # Récupérer les documents de la collection "weapons"
    weapons_cursor = collection_weapons.find({})  # Utilisation de la collection "weapons"
    
    # Convertir en liste
    weapons = await weapons_cursor.to_list(length=None)  
    
    if not weapons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No weapons found.")
    
    # Sérialisation des armes avant de les renvoyer
    serialized_weapons = [serialize_weapon(weapon) for weapon in weapons]
    
    return serialized_weapons


# Récupérer une arme via son custom_id
@endPoint.get("/get_weapon_by_custom_id/{custom_id}", response_model=Weapon)
async def get_weapon_by_custom_id(custom_id: int = Path(..., gt=0)):
    """Retourne une arme via son custom_id"""
    # Rechercher l'arme avec le custom_id
    weapon = await collection_weapons.find_one({"custom_id": custom_id})
    
    if not weapon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Weapon with custom_id {custom_id} not found.")
    
    # Sérialiser l'arme avant de la renvoyer
    return serialize_weapon(weapon)


# Créer une arme (ajouté en bonus)
@endPoint.post("/create_weapon", response_model=Weapon)
async def create_weapon(weapon: Weapon):
    try:
        # Convertir le modèle Pydantic en dictionnaire
        weapon_dict = weapon.model_dump(exclude_unset=False)  
        result = await collection_weapons.insert_one(weapon_dict)
        
        # Ajouter l'ID inséré au modèle Pydantic
        weapon.custom_id = str(result.inserted_id)  # Le custom_id est un string, on convertit l'ObjectId
        
        return weapon
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
