# serializers.py
from typing import List
from models.models import WeaponIn, WeaponOut, Ability,AbilityMechanics,SkyshipUpgrades, GameItem,UserIn,Developer, Player, ConsumablesAndNoncombatItems
from pydantic import BaseModel
from bson import ObjectId

# Fonction pour convertir un objet MongoDB en un format sérialisé
def serialize_weapon(weapon_data: dict) -> WeaponOut:
    """
    Sérialise un objet d'arme récupéré depuis MongoDB en un modèle Pydantic.
    """
    # Si l'arme a un _id, nous le remplaçons par custom_id
    if '_id' in weapon_data:
        weapon_data['_id'] = str(weapon_data.pop('_id'))  # Convertit l'_id MongoDB en custom_id
    
    # Retourner l'objet sérialisé en utilisant le modèle Pydantic
    return WeaponOut(**weapon_data)


# Fonction pour sérialiser une liste d'armes
def serialize_weapons(weapons_data: List[dict]) -> List[WeaponOut]:
    """
    Sérialise une liste d'armes récupérées depuis MongoDB.
    """
    return [serialize_weapon(weapon) for weapon in weapons_data]
