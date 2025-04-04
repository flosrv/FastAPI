from fastapi import APIRouter, HTTPException, Path, status, Body
from typing import List, Optional,Union,Dict, Any, Annotated
from bson import ObjectId
from pymongo import ReturnDocument
from models.models import WeaponIn, WeaponOut, AbilityIn, AbilityOut, AbilityMechIn,AbilityMechOut,SkyshipUpgradesIn
from models.models import SkyshipUpgradesOut, GameItem,UserIn,Developer, Player, ConsumablesAndNoncombatItemsIn, ConsumablesAndNoncombatItemsOut
from serializers import serialize_weapon, serialize_weapons, serialize_abilities, serialize_ability, serialize_ability_mech, serialize_ability_mechs,serialize_consumable, serialize_consumables, serialize_skyship_upgrade, serialize_skyship_upgrades
from fastapi import APIRouter, Depends,Query, Body, Path
from db.db_main import collection_weapons, collection_ability_mechanics, collection_consumables
from db.db_main import collection_skyship_upgrades, collection_abilities, collection_devs_data, collection_players_data
from fastapi import HTTPException, status
from pydantic import ValidationError
from functions_for_routes import get_model_details, validate_updates

endPoint = APIRouter()

######### WEAPONS ######################################################################################

# GET ALL
@endPoint.get("/weapons/all/", response_model=List[WeaponOut])
async def get_all_weapons():
    """Retourne la liste de toutes les armes"""
    try:
        weapons_cursor = collection_weapons.find({})
        weapons = await weapons_cursor.to_list(length=None)  

        if not weapons:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No weapons found.")

        serialized_weapons = [serialize_weapon(weapon) for weapon in weapons]
        return serialized_weapons

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible, problème de connexion à la base de données.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé pour récupérer les armes.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur inconnue: {str(e)}")

# GET BY ID
@endPoint.get("/weapons/by_ID/{custom_id}/", response_model=WeaponOut)
async def get_weapon_by_custom_id(custom_id: int = Path(..., gt=0)):
    """Retourne une arme via son custom_id"""
    try:
        weapon = await collection_weapons.find_one({"custom_id": custom_id})

        if not weapon:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Weapon with custom_id {custom_id} not found.")

        return serialize_weapon(weapon)

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible, problème de connexion à la base de données.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé pour récupérer l'arme.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur inconnue: {str(e)}")

#GET BY NAME
@endPoint.get("/weapons/by_name/{weapon_name}/",response_model=WeaponOut)
async def get_weapon_by_name(
    weapon_name: str = Path(..., title="Weapon name", description="Nom de l'arme")
):
    try:
        weapon = await collection_weapons.find_one({"Name": weapon_name})
        if not weapon:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Weapon with Name {weapon_name} not found.")
        return serialize_weapon(weapon)

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible, problème de connexion à la base de données.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé pour récupérer l'arme.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur inconnue: {str(e)}")

# GET ATTRIBUTES BY ID
@endPoint.get("/weapons/by_ID/{custom_id}/get_attributes/", response_model=Dict[str, Any])
async def get_weapon_attr_by_id(
    custom_id: int = Path(..., title="Custom ID", description="The ID of the weapon", gt=0),
    q: Annotated[List[str], Query(title="Attributes", description="List of attributes to retrieve")] = None
):
    """Retourne les attributs demandés d'une arme via son id"""
    try:
        weapon = await collection_weapons.find_one({"custom_id": custom_id})

        if not weapon:
            raise HTTPException(status_code=404, detail=f"Weapon with ID {custom_id} not found.")

        if not q:
            raise HTTPException(status_code=400, detail="Aucun attribut spécifié.")

        result_dict = {}
        for attr in q:
            if attr not in weapon:
                raise HTTPException(status_code=404, detail=f"Attribut '{attr}' non trouvé dans Weapon.")
            result_dict[attr] = weapon[attr]

        return result_dict

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

# PATCH
@endPoint.patch("/weapons/update/{custom_id}")
async def update_weapon(custom_id: int = Path(..., title="Weapon id"), updates: Dict[str, Any] = Body(...)):
    """Met à jour une arme en cherchant par `custom_id` uniquement."""
    try:
        model_details = get_model_details(WeaponIn)
        invalid_fields = validate_updates(updates, WeaponIn)

        if invalid_fields:
            raise HTTPException(status_code=422, detail={
                "message": "Certains champs sont invalides",
                "erreurs": invalid_fields,
                "champs valides": model_details
            })

        weapon = await collection_weapons.find_one({"custom_id": custom_id})

        if not weapon:
            raise HTTPException(status_code=404, detail=f"Arme avec l'identifiant '{custom_id}' non trouvée")

        await collection_weapons.update_one({"custom_id": custom_id}, {"$set": updates})

        return {
            "message": "Mise à jour réussie",
            "modifications": updates,
            "champs valides": model_details
        }

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible, problème de connexion à la base de données.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé pour la mise à jour.")
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=f"Clé manquante dans les données envoyées: {str(ke)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur inconnue: {str(e)}")

# POST
@endPoint.post("/weapons/create/", response_model=WeaponOut)
async def create_weapon(weapon_data: WeaponIn):
    try:
        max_weapon = await collection_weapons.find_one({}, sort=[("custom_id", -1)])
        new_custom_id = max_weapon["custom_id"] + 1 if max_weapon else 1

        weapon_dict = weapon_data.model_dump(exclude_unset=True)
        weapon_dict["custom_id"] = new_custom_id  

        result = await collection_weapons.insert_one(weapon_dict)
        weapon_dict["_id"] = str(result.inserted_id)  

        return WeaponOut(**weapon_dict)

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible, problème de connexion à la base de données.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé pour la création de l'arme.")
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=f"Clé manquante dans les données envoyées: {str(ke)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur inconnue: {str(e)}")

########### ABILITY MECHS #######################################################################################

# GET ALL
@endPoint.get("/ability_mechs/all/", response_model=List[AbilityMechOut])
async def get_all_ability_mechs():
    """Retourne la liste de toutes les mécaniques de capacité"""
    try:
        ability_mechs_cursor = collection_ability_mechanics.find({})
        ability_mechs = await ability_mechs_cursor.to_list(length=None)

        if not ability_mechs:
            raise HTTPException(status_code=404, detail="No ability mechs found.")

        return [serialize_ability_mech(ability_mech) for ability_mech in ability_mechs]

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible, problème de connexion.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

# GET BY NAME
@endPoint.get("/ability_mechs/by_name/{name}", response_model=AbilityMechOut)
async def get_ability_mech_by_name(name: str):
    """Retourne une mécanique de capacité via son nom"""
    try:
        ability_mech = await collection_ability_mechanics.find_one({"Name": name})

        if not ability_mech:
            raise HTTPException(status_code=404, detail=f"Ability Mech with name {name} not found.")

        return serialize_ability_mech(ability_mech)

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")
    
# GET BY ID
@endPoint.get("/ability_mechs/by_ID/{custom_id}", response_model=AbilityMechOut)
async def get_ability_mech_by_id(custom_id: int):
    """Retourne une mécanique de capacité via son id"""
    try:
        ability_mech = await collection_ability_mechanics.find_one({"custom_id": custom_id})

        if not ability_mech:
            raise HTTPException(status_code=404, detail=f"Ability Mech with name {custom_id} not found.")

        return serialize_ability_mech(ability_mech)

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

# GET ATTR BY ID
@endPoint.get("/ability_mechs/by_ID/{custom_id}/get_attributes/", response_model=Dict[str, Any])
async def get_ability_mech_attr_by_id(
    custom_id: int = Path(..., title="Custom ID", description="The ID of the ability mech", gt=0),
    q: Annotated[List[str], Query(title="Attributes", description="List of attributes to retrieve")] = None
):
    """Retourne les attributs demandés d'une mécanique de capacité via son id"""

    try:
        # Récupérer le mécanisme de capacité avec l'id
        ability_mech = await collection_ability_mechanics.find_one({"custom_id": custom_id})

        if not ability_mech:
            raise HTTPException(status_code=404, detail=f"Ability Mech with ID {custom_id} not found.")

        # Si aucun attribut demandé
        if not q:
            raise HTTPException(status_code=400, detail="Aucun attribut spécifié.")

        # Filtrer et renvoyer uniquement les attributs demandés
        result_dict = {}
        for attr in q:
            if attr not in ability_mech:
                raise HTTPException(status_code=404, detail=f"Attribut '{attr}' non trouvé dans Ability Mech.")
            result_dict[attr] = ability_mech[attr]

        return result_dict

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

# PATCH ATTRIBUTES BY ID
@endPoint.patch("/ability_mechs/update_attributes/{custom_id}")
async def update_ability_mech_attributes(
    custom_id: int = Path(..., title="Ability Mech ID", description="The ID of the ability mech", gt=0),
    updates: List[Dict[str, Any]] = Body(..., title="Updates", description="List of attributes to update")
):
    """Met à jour les attributs d'une mécanique de capacité via son ID"""
    try:
        ability_mech = await collection_ability_mechanics.find_one({"custom_id": custom_id})
        if not ability_mech:
            raise HTTPException(status_code=404, detail=f"Ability Mech with ID {custom_id} not found.")

        update_dict = {list(update.keys())[0]: list(update.values())[0] for update in updates}
        await collection_ability_mechanics.update_one({"custom_id": custom_id}, {"$set": update_dict})

        return {"message": "Ability Mech attributes updated successfully", "updated_attributes": update_dict}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# POST
@endPoint.post("/ability_mechs/create", response_model=AbilityMechOut)
async def create_ability_mech(ability_mech_data: AbilityMechIn):
    try:
        max_ability_mech = await collection_ability_mechanics.find_one({}, sort=[("custom_id", -1)])
        new_custom_id = max_ability_mech["custom_id"] + 1 if max_ability_mech else 1

        ability_mech_dict = ability_mech_data.model_dump(exclude_unset=True)
        ability_mech_dict["custom_id"] = new_custom_id  

        result = await collection_ability_mechanics.insert_one(ability_mech_dict)
        ability_mech_dict["_id"] = str(result.inserted_id)  

        return AbilityMechOut(**ability_mech_dict)

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé.")
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=f"Clé manquante: {str(ke)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

########## SKYSHIPS UPGRADES #####################################################################################

# GET ALL
@endPoint.get("/skyship_upgrades/all/", response_model=List[SkyshipUpgradesOut])
async def get_all_skyship_upgrades():
    """Retourne la liste de toutes les améliorations de Skyship"""
    try:
        skyship_upgrades_cursor = collection_skyship_upgrades.find({})
        skyship_upgrades = await skyship_upgrades_cursor.to_list(length=None)

        if not skyship_upgrades:
            raise HTTPException(status_code=404, detail="No skyship upgrades found.")

        return [serialize_skyship_upgrade(skyship_upgrade) for skyship_upgrade in skyship_upgrades]

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

# GET BY ID
@endPoint.get("/skyship_upgrades/by_ID/{custom_id}", response_model=SkyshipUpgradesOut)
async def get_skyship_upgrade_by_custom_id(custom_id: int = Path(..., gt=0)):
    """Retourne une amélioration de Skyship via son custom_id"""
    try:
        skyship_upgrade = await collection_skyship_upgrades.find_one({"custom_id": custom_id})

        if not skyship_upgrade:
            raise HTTPException(status_code=404, detail=f"Skyship upgrade with custom_id {custom_id} not found.")

        return serialize_skyship_upgrade(skyship_upgrade)

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

# GET BY NAME
@endPoint.get("/skyship_upgrades/by_name/{name}", response_model=SkyshipUpgradesOut)
async def get_skyship_upgrade_by_custom_id(name: str = Path(...)):
    """Retourne une amélioration de Skyship via son custom_id"""
    try:
        skyship_upgrade = await collection_skyship_upgrades.find_one({"Name": name})

        if not skyship_upgrade:
            raise HTTPException(status_code=404, detail=f"Skyship upgrade with custom_id {name} not found.")

        return serialize_skyship_upgrade(skyship_upgrade)

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

# GET ATTRIBUTES FOR SKYSHIP UPGRADES
@endPoint.get("/skyship_upgrades/by_ID/{custom_id}/get_attributes/", response_model=Dict[str, Any])
async def get_skyship_upgrade_attr_by_id(
    custom_id: int = Path(..., title="Custom ID", description="The ID of the skyship upgrade", gt=0),
    q: Annotated[List[str], Query(title="Attributes", description="List of attributes to retrieve")] = None
):
    """Retourne les attributs demandés d'une amélioration de Skyship via son id"""
    try:
        skyship_upgrade = await collection_skyship_upgrades.find_one({"custom_id": custom_id})

        if not skyship_upgrade:
            raise HTTPException(status_code=404, detail=f"Skyship Upgrade with ID {custom_id} not found.")

        if not q:
            raise HTTPException(status_code=400, detail="Aucun attribut spécifié.")

        result_dict = {}
        for attr in q:
            if attr not in skyship_upgrade:
                raise HTTPException(status_code=404, detail=f"Attribut '{attr}' non trouvé dans Skyship Upgrade.")
            result_dict[attr] = skyship_upgrade[attr]

        return result_dict

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

# PATCH ATTRIBUTES FOR SKYSHIP UPGRADES
@endPoint.patch("/skyship_upgrades/update_attributes/{custom_id}")
async def update_skyship_upgrade_attributes(
    custom_id: int = Path(..., title="Skyship Upgrade ID", description="The ID of the skyship upgrade", gt=0),
    updates: List[Dict[str, Any]] = Body(..., title="Updates", description="List of attributes to update")
):
    """Met à jour les attributs d'une amélioration de Skyship via son ID"""
    try:
        skyship_upgrade = await collection_skyship_upgrades.find_one({"custom_id": custom_id})
        if not skyship_upgrade:
            raise HTTPException(status_code=404, detail=f"Skyship Upgrade with ID {custom_id} not found.")

        update_dict = {list(update.keys())[0]: list(update.values())[0] for update in updates}
        await collection_skyship_upgrades.update_one({"custom_id": custom_id}, {"$set": update_dict})

        return {"message": "Skyship Upgrade attributes updated successfully", "updated_attributes": update_dict}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# POST
@endPoint.post("/skyship_upgrades/create/", response_model=SkyshipUpgradesOut)
async def create_skyship_upgrade(skyship_upgrade_data: SkyshipUpgradesIn):
    try:
        max_skyship_upgrade = await collection_skyship_upgrades.find_one({}, sort=[("custom_id", -1)])
        new_custom_id = max_skyship_upgrade["custom_id"] + 1 if max_skyship_upgrade else 1

        skyship_upgrade_dict = skyship_upgrade_data.model_dump(exclude_unset=True)
        skyship_upgrade_dict["custom_id"] = new_custom_id  

        result = await collection_skyship_upgrades.insert_one(skyship_upgrade_dict)
        skyship_upgrade_dict["_id"] = str(result.inserted_id)  

        return SkyshipUpgradesOut(**skyship_upgrade_dict)

    except HTTPException as http_err:
        raise http_err
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Erreur de validation: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service indisponible.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Temps d'attente dépassé.")
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=f"Clé manquante: {str(ke)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

########## CONSUMABLES AND NON COMBAT ITEMS #####################################################################################

# GET ALL
@endPoint.get("/consumables_and_noncombat_items/all/", response_model=List[ConsumablesAndNoncombatItemsOut])
async def get_all_consumables_and_noncombat_items():
    """Retourne la liste de tous les objets consommables et non-combattants"""
    try:
        consumables_cursor = collection_consumables.find({})
        consumables = await consumables_cursor.to_list(length=None)

        if not consumables:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No consumables and non-combat items found.")

        return [serialize_consumable(consumable) for consumable in consumables]

    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Value error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# GET BY ID
@endPoint.get("/consumables_and_noncombat_items/by_ID/{custom_id}", response_model=ConsumablesAndNoncombatItemsOut)
async def get_consumable_and_noncombat_item_by_custom_id(custom_id: int = Path(..., gt=0)):
    """Retourne un objet consommable ou non-combattant via son custom_id"""
    try:
        consumable = await collection_consumables.find_one({"custom_id": custom_id})

        if not consumable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Consumable or non-combat item with custom_id {custom_id} not found.")

        return serialize_consumable(consumable)

    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Value error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# GET BY NAME
@endPoint.get("/consumables_and_noncombat_items/by_name/{name}", response_model=ConsumablesAndNoncombatItemsOut)
async def get_consumable_by_name(name: str):
    """Retourne un consommable ou objet non-combattant via son nom"""
    try:
        consumable = await collection_consumables.find_one({"Name": name})

        if not consumable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Consumable with name {name} not found.")

        return serialize_consumable(consumable)

    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Value error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# GET ATTRIBUTES FOR CONSUMABLES AND NON-COMBAT ITEMS
@endPoint.get("/consumables_and_noncombat_items/by_ID/{custom_id}/get_attributes/", response_model=Dict[str, Any])
async def get_consumable_attr_by_id(
    custom_id: int = Path(..., title="Custom ID", description="The ID of the consumable or non-combat item", gt=0),
    q: Annotated[List[str], Query(title="Attributes", description="List of attributes to retrieve")] = None
):
    """Retourne les attributs demandés d'un consommable ou objet non-combattant via son id"""
    try:
        consumable = await collection_consumables.find_one({"custom_id": custom_id})

        if not consumable:
            raise HTTPException(status_code=404, detail=f"Consumable with ID {custom_id} not found.")

        if not q:
            raise HTTPException(status_code=400, detail="Aucun attribut spécifié.")

        result_dict = {}
        for attr in q:
            if attr not in consumable:
                raise HTTPException(status_code=404, detail=f"Attribut '{attr}' non trouvé dans Consumable.")
            result_dict[attr] = consumable[attr]

        return result_dict

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

# PATCH ATTRIBUTES FOR CONSUMABLES AND NON-COMBAT ITEMS
@endPoint.patch("/consumables_and_noncombat_items/update_attributes/{custom_id}")
async def update_consumable_attributes(
    custom_id: int = Path(..., title="Consumable ID", description="The ID of the consumable or non-combat item", gt=0),
    updates: List[Dict[str, Any]] = Body(..., title="Updates", description="List of attributes to update")
):
    """Met à jour les attributs d'un consommable ou objet non-combattant via son ID"""
    try:
        consumable = await collection_consumables.find_one({"custom_id": custom_id})
        if not consumable:
            raise HTTPException(status_code=404, detail=f"Consumable with ID {custom_id} not found.")

        update_dict = {list(update.keys())[0]: list(update.values())[0] for update in updates}
        await collection_consumables.update_one({"custom_id": custom_id}, {"$set": update_dict})

        return {"message": "Consumable attributes updated successfully", "updated_attributes": update_dict}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
# POST
@endPoint.post("/consumables_and_noncombat_items/create", response_model=ConsumablesAndNoncombatItemsOut)
async def create_consumable(consumable_data: ConsumablesAndNoncombatItemsIn):
    try:
        max_consumable = await collection_consumables.find_one({}, sort=[("custom_id", -1)])
        new_custom_id = max_consumable["custom_id"] + 1 if max_consumable else 1

        consumable_dict = consumable_data.model_dump(exclude_unset=True)
        consumable_dict["custom_id"] = new_custom_id

        result = await collection_consumables.insert_one(consumable_dict)
        consumable_dict["_id"] = str(result.inserted_id)

        return ConsumablesAndNoncombatItemsOut(**consumable_dict)

    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Value error: {str(e)}")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing key: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

######## ABILITIES ####################################################################################

# GET ALL
@endPoint.get("/abilities/all/", response_model=List[AbilityOut])
async def get_all_abilities():
    """Retourne la liste de toutes les capacités"""
    try:
        abilities_cursor = collection_abilities.find({})
        abilities = await abilities_cursor.to_list(length=None)

        if not abilities:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No abilities found.")

        serialized_abilities = [serialize_ability(ability) for ability in abilities]
        return serialized_abilities

    except HTTPException as http_ex:
        raise http_ex  # Renvoie l'erreur HTTP exacte
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")
    
# GET BY ID
@endPoint.get("/abilities/by_ID/{custom_id}", response_model=AbilityOut)
async def get_ability_by_custom_id(custom_id: int = Path(..., gt=0)):
    """Retourne une capacité via son custom_id"""
    try:
        ability = await collection_abilities.find_one({"custom_id": custom_id})
        if not ability:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ability with custom_id {custom_id} not found.")
        return serialize_ability(ability)

    except HTTPException as http_ex:
        raise http_ex
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid custom_id format.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")

# GET BY NAME
@endPoint.get("/abilities/by_name/{name}", response_model=AbilityOut)
async def get_ability_by_name(name: str):
    """Retourne une capacité via son nom"""
    try:
        ability = await collection_abilities.find_one({"Name": name})

        if not ability:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ability with name {name} not found.")

        return serialize_ability(ability)

    except HTTPException as http_ex:
        raise http_ex
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid name format.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")

# GET ATTRIBUTES FOR ABILITIES
@endPoint.get("/abilities/by_ID/{custom_id}/get_attributes/", response_model=Dict[str, Any])
async def get_ability_attr_by_id(
    custom_id: int = Path(..., title="Custom ID", description="The ID of the ability", gt=0),
    q: Annotated[List[str], Query(title="Attributes", description="List of attributes to retrieve")] = None
):
    """Retourne les attributs demandés d'une capacité via son id"""
    try:
        ability = await collection_abilities.find_one({"custom_id": custom_id})

        if not ability:
            raise HTTPException(status_code=404, detail=f"Ability with ID {custom_id} not found.")

        if not q:
            raise HTTPException(status_code=400, detail="Aucun attribut spécifié.")

        result_dict = {}
        for attr in q:
            if attr not in ability:
                raise HTTPException(status_code=404, detail=f"Attribut '{attr}' non trouvé dans Ability.")
            result_dict[attr] = ability[attr]

        return result_dict

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")

# PATCH ATTRIBUTES FOR ABILITIES
@endPoint.patch("/abilities/update_attributes/{custom_id}")
async def update_ability_attributes(
    custom_id: int = Path(..., title="Ability ID", description="The ID of the ability", gt=0),
    updates: List[Dict[str, Any]] = Body(..., title="Updates", description="List of attributes to update")
):
    """Met à jour les attributs d'une capacité via son ID"""
    try:
        ability = await collection_abilities.find_one({"custom_id": custom_id})
        if not ability:
            raise HTTPException(status_code=404, detail=f"Ability with ID {custom_id} not found.")

        update_dict = {list(update.keys())[0]: list(update.values())[0] for update in updates}
        await collection_abilities.update_one({"custom_id": custom_id}, {"$set": update_dict})

        return {"message": "Ability attributes updated successfully", "updated_attributes": update_dict}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# POST
@endPoint.post("/abilities/create", response_model=AbilityOut)
async def create_ability(ability_data: AbilityIn):
    try:
        max_ability = await collection_abilities.find_one({}, sort=[("custom_id", -1)])
        new_custom_id = max_ability["custom_id"] + 1 if max_ability else 1

        ability_dict = ability_data.model_dump(exclude_unset=True)
        ability_dict["custom_id"] = new_custom_id

        result = await collection_abilities.insert_one(ability_dict)
        ability_dict["_id"] = str(result.inserted_id)

        return AbilityOut(**ability_dict)

    except HTTPException as http_ex:
        raise http_ex
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid ability data.")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required fields.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")

#############################################################################################


