from fastapi import APIRouter, HTTPException, Path, status, Body
from typing import List, Optional,Union,Dict, Any, Annotated
from bson import ObjectId
from pymongo import ReturnDocument
from serializers import serialize_abilities, serialize_ability
from fastapi import APIRouter, Depends, Query, Body, Path
from db.db_main import collection_abilities
from fastapi import HTTPException, status
from pydantic import ValidationError
from models.abilities import AbilityIn, AbilityOut

endPoint = APIRouter()

########## GET ALL #####################################################################################################################
@endPoint.get("/all/", response_model=List[AbilityOut])
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
    

################### GET BY ID ############################################################################################################
@endPoint.get("/by_ID/{custom_id}", response_model=AbilityOut)
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


################## GET BY NAME ############################################################################################################
@endPoint.get("/by_name/{name}", response_model=AbilityOut)
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

######### GET ATTRIBUTES BY ID ###################################################################################################

@endPoint.get("/by_ID/{custom_id}/get_attributes/", response_model=Dict[str, Any])
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

######### GET ATTRIBUTES BY NAME ###################################################################################################

@endPoint.get("/by_name/{name}/get_attributes/", response_model=Dict[str, Any])
async def get_ability_attr_by_name(
    name: str = Path(..., title="Name", description="The name of the ability"),
    q: Annotated[List[str], Query(title="Attributes", description="List of attributes to retrieve")] = None
):
    """Retourne les attributs demandés d'une capacité via son nom"""
    try:
        ability = await collection_abilities.find_one({"Name": name})

        if not ability:
            raise HTTPException(status_code=404, detail=f"Ability with name {name} not found.")

        if not q:
            raise HTTPException(status_code=400, detail="Aucun attribut spécifié.")

        result_dict = {}
        for attr in q:
            if attr not in ability:
                raise HTTPException(status_code=404, detail=f"Attribut '{name}' non trouvé dans Ability.")
            result_dict[attr] = ability[attr]

        return result_dict

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue: {str(e)}")
    
############# PATCH ATTRIBUTES BY ID ############################################################################################################

@endPoint.patch("/update_attributes/{custom_id}")
async def update_ability_attributes_by_id(
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

############# PATCH ATTRIBUTES BY NAME ############################################################################################################

@endPoint.patch("/update_attributes/{name}")
async def update_ability_attributes_by_name(
    name: str = Path(..., title="Ability name", description="The name of the ability"),
    updates: List[Dict[str, Any]] = Body(..., title="Updates", description="List of attributes to update")
):
    """Met à jour les attributs d'une capacité via son nom"""
    try:
        ability = await collection_abilities.find_one({"Name": name})
        if not ability:
            raise HTTPException(status_code=404, detail=f"Ability with name {name} not found.")

        update_dict = {list(update.keys())[0]: list(update.values())[0] for update in updates}
        await collection_abilities.update_one({"Name": name}, {"$set": update_dict})

        return {"message": "Ability attributes updated successfully", "updated_attributes": update_dict}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

########## POST ##################################################################################################################################
@endPoint.post("/create", response_model=AbilityOut)
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