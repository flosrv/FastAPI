from fastapi import APIRouter, HTTPException, Path, status, Body, Depends,Query
from typing import List, Optional,Union,Dict, Any, Annotated
from bson import ObjectId
from pymongo import ReturnDocument
from models.weapons import WeaponIn, WeaponOut
from serializers import serialize_weapon, serialize_weapons
from db.db_main import collection_weapons
from pydantic import ValidationError
from functions_for_routes import get_model_details, validate_updates
from fastapi import APIRouter

endPoint = APIRouter()

########## GET ALL ##########################################################################################
@endPoint.get("/all/", response_model=List[WeaponOut])
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
        raise HTTPException(status_code=422, detail=f"Validation Error: {str(ve)}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Database Connection Issue.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Waiting Timeout.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown Server Error: {str(e)}")

########## GET BY ID ##########################################################################################

@endPoint.get("/by_ID/{custom_id}/", response_model=WeaponOut)
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

########## GET BY NAME ##########################################################################################

@endPoint.get("/by_name/{weapon_name}/",response_model=WeaponOut)
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

########## GET ATTRIBUTES BY ID ##########################################################################################

@endPoint.get("/by_ID/{custom_id}/get_attributes/", response_model=Dict[str, Any])
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

########## GET ATTRIBUTES BY NAME ##########################################################################################

@endPoint.get("/by_name/{name}/get_attributes/", response_model=Dict[str, Any])
async def get_weapon_attr_by_name(
    name: str = Path(..., title="Name", description="The name of the weapon"),
    q: Annotated[List[str], Query(title="Attributes", description="List of attributes to retrieve")] = None
):
    """Retourne les attributs demandés d'une arme via son nom"""
    try:
        weapon = await collection_weapons.find_one({"Name": name})

        if not weapon:
            raise HTTPException(status_code=404, detail=f"Weapon with name {name} not found.")

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

############# PATCH ATTRIBUTES BY ID ################################################################################################

@endPoint.patch("/update_attributes/{custom_id}")
async def update_weapon_attributes_by_id(
    custom_id: int = Path(..., title="Weapon ID", description="The ID of the weapon", gt=0),
    updates: List[Dict[str, Any]] = Body(..., title="Updates", description="List of attributes to update")
):
    """Met à jour les attributs d'une arme via son ID"""
    try:
        weapon = await collection_weapons.find_one({"custom_id": custom_id})
        if not weapon:
            raise HTTPException(status_code=404, detail=f"Weapon with ID {custom_id} not found.")

        update_dict = {list(update.keys())[0]: list(update.values())[0] for update in updates}
        await collection_weapons.update_one({"custom_id": custom_id}, {"$set": update_dict})

        return {"message": "Weapon attributes updated successfully", "updated_attributes": update_dict}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

############# PATCH ATTRIBUTES BY NAME ################################################################################################

@endPoint.patch("/update_attributes/{name}")
async def update_weapon_attributes_by_name(
    name: str = Path(..., title="Weapon name", description="The name of the weapon"),
    updates: List[Dict[str, Any]] = Body(..., title="Updates", description="List of attributes to update")
):
    """Met à jour les attributs d'une arme via son ID"""
    try:
        weapon = await collection_weapons.find_one({"Name": name})
        if not weapon:
            raise HTTPException(status_code=404, detail=f"Weapon with ID {name} not found.")

        update_dict = {list(update.keys())[0]: list(update.values())[0] for update in updates}
        await collection_weapons.update_one({"Name": name}, {"$set": update_dict})

        return {"message": "Weapon attributes updated successfully", "updated_attributes": update_dict}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

########## POST ##########################################################################################

@endPoint.post("/create/", response_model=WeaponOut)
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