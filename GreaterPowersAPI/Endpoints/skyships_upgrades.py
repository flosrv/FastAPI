from fastapi import APIRouter, HTTPException, Path, status, Body
from typing import List, Optional,Union,Dict, Any, Annotated
from bson import ObjectId
from pymongo import ReturnDocument
from models.skyships_upgrades import SkyshipUpgradesIn, SkyshipUpgradesOut
from serializers import serialize_skyship_upgrade, serialize_skyship_upgrades
from fastapi import APIRouter, Depends, Query, Body, Path
from db.db_main import  collection_skyship_upgrades
from fastapi import HTTPException, status
from pydantic import ValidationError
from functions_for_routes import get_model_details, validate_updates

endPoint = APIRouter()

############ GET ALL #########################################################################################################################

@endPoint.get("/all/", response_model=List[SkyshipUpgradesOut])
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

############ GET BY ID ##############################################################################################################

@endPoint.get("/by_ID/{custom_id}", response_model=SkyshipUpgradesOut)
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

############ GET BY NAME ##############################################################################################################

@endPoint.get("/by_name/{name}", response_model=SkyshipUpgradesOut)
async def get_skyship_upgrade_by_name(name: str = Path(...)):
    """Retourne une amélioration de Skyship via son nom"""
    try:
        skyship_upgrade = await collection_skyship_upgrades.find_one({"Name": name})

        if not skyship_upgrade:
            raise HTTPException(status_code=404, detail=f"Skyship upgrade with name {name} not found.")

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

########### GET ATTRIBUTES BY ID ###################################################################################################

@endPoint.get("/by_ID/{custom_id}/get_attributes/", response_model=Dict[str, Any])
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
    
############ GET ATTRIBUTES BY NAME ###################################################################################################

@endPoint.get("/by_name/{name}/get_attributes/", response_model=Dict[str, Any])
async def get_skyship_upgrade_attr_by_name(
    name: str = Path(..., title="Name", description="The name of the skyship upgrade"),
    q: Annotated[List[str], Query(title="Attributes", description="List of attributes to retrieve")] = None
):
    """Retourne les attributs demandés d'une amélioration de Skyship via son nom"""
    try:
        skyship_upgrade = await collection_skyship_upgrades.find_one({"Name": name})

        if not skyship_upgrade:
            raise HTTPException(status_code=404, detail=f"Skyship Upgrade with Name {name} not found.")

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

############ PATCH ATTRIBUTES BY ID ################################################################################################

@endPoint.patch("/update_attributes/{custom_id}")
async def update_skyship_upgrade_attributes_by_id(
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

############ PATCH ATTRIBUTES BY NAME ################################################################################################

@endPoint.patch("/update_attributes/{name}")
async def update_skyship_upgrade_attributes_by_name(
    name: str = Path(..., title="Skyship Upgrade name", description="The name of the skyship upgrade"),
    updates: List[Dict[str, Any]] = Body(..., title="Updates", description="List of attributes to update")
):
    """Update attributes by name"""
    try:
        skyship_upgrade = await collection_skyship_upgrades.find_one({"Name": name})
        if not skyship_upgrade:
            raise HTTPException(status_code=404, detail=f"Skyship Upgrade with ID {name} not found.")

        update_dict = {list(update.keys())[0]: list(update.values())[0] for update in updates}
        await collection_skyship_upgrades.update_one({"Name": name}, {"$set": update_dict})

        return {"message": "Skyship Upgrade attributes updated successfully", "updated_attributes": update_dict}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

####### POST ################################################################################################################

@endPoint.post("/create/", response_model=SkyshipUpgradesOut)
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

