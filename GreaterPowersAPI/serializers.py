from typing import List, Optional
from models.models import (
    WeaponOut, AbilityOut, AbilityMechOut, SkyshipUpgradesOut, ConsumablesAndNoncombatItemsOut
)
from bson import ObjectId

def safe_get(data: dict, key: str, default=None):
    """Retourne data[key] si présent, sinon retourne default."""
    return data.get(key, default)

def handle_null_value(value):
    """Vérifie si la valeur est 'null' (en tant que chaîne), et renvoie None si c'est le cas."""
    if value == "null":
        return None
    return value

############## WEAPONS #########################################################################################################

def serialize_weapon(weapon_data: dict) -> WeaponOut:
    if weapon_data == "null":
        return None  # Gestion des cas où weapon_data est None

    weapon_data['_id'] = str(weapon_data.pop('_id', None))  # Convertit l'_id MongoDB en string ou None
    # Convertir chaque valeur si elle est 'null' en None
    return WeaponOut(**{key: handle_null_value(safe_get(weapon_data, key)) for key in WeaponOut.model_fields})

def serialize_weapons(weapons_data: List[dict]) -> List[WeaponOut]:
    return [serialize_weapon(weapon) for weapon in weapons_data if weapon]

############## ABILITY MECHS ###################################################################################################

def serialize_ability_mech(ability_mech_data: dict) -> AbilityMechOut:
    if ability_mech_data == "null":
        return None

    ability_mech_data['_id'] = str(ability_mech_data.pop('_id', None))
    # Convertir chaque valeur si elle est 'null' en None
    return AbilityMechOut(**{key: handle_null_value(safe_get(ability_mech_data, key)) for key in AbilityMechOut.model_fields})

def serialize_ability_mechs(ability_mechs_data: List[dict]) -> List[AbilityMechOut]:
    return [serialize_ability_mech(ability_mech) for ability_mech in ability_mechs_data if ability_mech]

############## SKYSHIPS UPGRADES ##############################################################################################

def serialize_skyship_upgrade(skyship_upgrade_data: dict) -> SkyshipUpgradesOut:
    if skyship_upgrade_data == "null":
        return None

    skyship_upgrade_data['_id'] = str(skyship_upgrade_data.pop('_id', None))
    # Convertir chaque valeur si elle est 'null' en None
    return SkyshipUpgradesOut(**{key: handle_null_value(safe_get(skyship_upgrade_data, key)) for key in SkyshipUpgradesOut.model_fields})

def serialize_skyship_upgrades(skyship_upgrades_data: List[dict]) -> List[SkyshipUpgradesOut]:
    return [serialize_skyship_upgrade(skyship_upgrade) for skyship_upgrade in skyship_upgrades_data if skyship_upgrade]

############## CONSUMABLES AND NON-COMBAT ITEMS ###############################################################################

def serialize_consumable(consumable_data: dict) -> ConsumablesAndNoncombatItemsOut:
    if consumable_data == "null":
        return None

    consumable_data['_id'] = str(consumable_data.pop('_id', None))
    # Convertir chaque valeur si elle est 'null' en None
    return ConsumablesAndNoncombatItemsOut(**{key: handle_null_value(safe_get(consumable_data, key)) for key in ConsumablesAndNoncombatItemsOut.model_fields})

def serialize_consumables(consumables_data: List[dict]) -> List[ConsumablesAndNoncombatItemsOut]:
    return [serialize_consumable(consumable) for consumable in consumables_data if consumable]

############## ABILITIES ######################################################################################################

def serialize_ability(ability_data: dict) -> AbilityOut:
    if ability_data == "null":
        return None

    ability_data['_id'] = str(ability_data.pop('_id', None))
    # Convertir chaque valeur si elle est 'null' en None
    return AbilityOut(**{key: handle_null_value(safe_get(ability_data, key)) for key in AbilityOut.model_fields})

def serialize_abilities(abilities_data: List[dict]) -> List[AbilityOut]:
    return [serialize_ability(ability) for ability in abilities_data if ability]
