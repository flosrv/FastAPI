from fastapi import APIRouter, HTTPException, Path, status, Body
from typing import List, Optional,Union,Dict, Any, Annotated
from bson import ObjectId
from pymongo import ReturnDocument
from models.ability_mechs import AbilityMechIn, AbilityMechOut
from serializers import serialize_ability_mech, serialize_ability_mechs
from fastapi import APIRouter, Depends, Query, Body, Path
from db.db_main import  collection_ability_mechanics
from fastapi import HTTPException, status
from pydantic import ValidationError
from functions_for_routes import get_model_details, validate_updates


endPoint = APIRouter()

# GET ALL
@endPoint.get("/all/", response_model=List[AbilityMechOut])
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
@endPoint.get("/by_name/{name}", response_model=AbilityMechOut)
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
@endPoint.get("/by_ID/{custom_id}", response_model=AbilityMechOut)
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


######### GET ATTR BY ID ###################################################################################################
@endPoint.get("/by_ID/{custom_id}/get_attributes/", response_model=Dict[str, Any])
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
    

######### GET ATTR BY NAME ###################################################################################################
@endPoint.get("/by_name/{name}/get_attributes/", response_model=Dict[str, Any])
async def get_ability_mech_attr_by_name(
    name: str = Path(..., title="Name", description="The name of the ability mech"),
    q: Annotated[List[str], Query(title="Attributes", description="List of attributes to retrieve")] = None
):
    """Retourne les attributs demandés d'une mécanique de capacité via son nom"""

    try:
        # Récupérer le mécanisme de capacité avec l'id
        ability_mech = await collection_ability_mechanics.find_one({"Name": name})

        if not ability_mech:
            raise HTTPException(status_code=404, detail=f"Ability Mech with name {name} not found.")

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

############ PATCH ATTRIBUTES BY ID ################################################################################################

@endPoint.patch("/update_attributes/{custom_id}")
async def update_ability_mech_attributes_by_id(
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

############ PATCH ATTRIBUTES BY NAME ################################################################################################

@endPoint.patch("/update_attributes/{name}")
async def update_ability_mech_attributes_by_name(
    name: str = Path(..., title="Ability Mech name", description="The name of the ability mech"),
    updates: List[Dict[str, Any]] = Body(..., title="Updates", description="List of attributes to update")
):
    """Met à jour les attributs d'une mécanique de capacité via son nom"""
    try:
        ability_mech = await collection_ability_mechanics.find_one({"Name": name})
        if not ability_mech:
            raise HTTPException(status_code=404, detail=f"Ability Mech with name {name} not found.")

        update_dict = {list(update.keys())[0]: list(update.values())[0] for update in updates}
        await collection_ability_mechanics.update_one({"Name": name}, {"$set": update_dict})

        return {"message": "Ability Mech attributes updated successfully", "updated_attributes": update_dict}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

############ POST ################################################################################################

@endPoint.post("/create", response_model=AbilityMechOut)
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











