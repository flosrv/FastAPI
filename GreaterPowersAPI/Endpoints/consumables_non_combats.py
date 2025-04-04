from fastapi import APIRouter, HTTPException, Path, status, Body
from typing import List, Optional,Union,Dict, Any, Annotated
from bson import ObjectId
from pymongo import ReturnDocument
from models.consumables_non_combat import ConsumablesAndNoncombatItemsIn, ConsumablesAndNoncombatItemsOut
from serializers import serialize_consumable, serialize_consumables
from fastapi import APIRouter, Depends, Query, Body, Path
from db.db_main import  collection_consumables
from fastapi import HTTPException, status
from pydantic import ValidationError
from functions_for_routes import get_model_details, validate_updates

endPoint = APIRouter()

# GET ALL
@endPoint.get("/all/", response_model=List[ConsumablesAndNoncombatItemsOut])
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
@endPoint.get("/by_ID/{custom_id}", response_model=ConsumablesAndNoncombatItemsOut)
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

##################### GET BY NAME ####################################################################################################

@endPoint.get("/by_name/{name}", response_model=ConsumablesAndNoncombatItemsOut)
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

########### GET ATTRIBUTES BY ID ##########################################################################################
@endPoint.get("/by_ID/{custom_id}/get_attributes/", response_model=Dict[str, Any])
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

########### GET ATTRIBUTES BY NAME ##########################################################################################
@endPoint.get("/by_name/{name}/get_attributes/", response_model=Dict[str, Any])
async def get_consumable_attr_by_name(
    name: str = Path(..., title="Name", description="The name of the consumable or non-combat item"),
    q: Annotated[List[str], Query(title="Attributes", description="List of attributes to retrieve")] = None
):
    """Retourne les attributs demandés d'un consommable ou objet non-combattant via son nom"""
    try:
        consumable = await collection_consumables.find_one({"Name": name})

        if not consumable:
            raise HTTPException(status_code=404, detail=f"Consumable with ID {name} not found.")

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

############# PATCH ATTRIBUTES BY ID ########################################################################

@endPoint.patch("/update_attributes/{custom_id}")
async def update_consumable_attributes_by_id(
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

############### PATCH ATTRIBUTES BY NAME ##################################################################################

@endPoint.patch("/update_attributes/{name}")
async def update_consumable_attributes_by_name(
    name: str = Path(..., title="Consumable name", description="The name of the consumable or non-combat item"),
    updates: List[Dict[str, Any]] = Body(..., title="Updates", description="List of attributes to update")
):
    """Met à jour les attributs d'un consommable ou objet non-combattant via son nom"""
    try:
        consumable = await collection_consumables.find_one({"Name": name})
        if not consumable:
            raise HTTPException(status_code=404, detail=f"Consumable with ID {name} not found.")

        update_dict = {list(update.keys())[0]: list(update.values())[0] for update in updates}
        await collection_consumables.update_one({"Name": name}, {"$set": update_dict})

        return {"message": "Consumable attributes updated successfully", "updated_attributes": update_dict}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    

########## POST ##############################################################################################################

@endPoint.post("/create", response_model=ConsumablesAndNoncombatItemsOut)
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