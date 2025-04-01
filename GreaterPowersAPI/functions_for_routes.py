from models.models import WeaponIn, WeaponOut, AbilityIn, AbilityOut, AbilityMechIn,AbilityMechOut,SkyshipUpgradesIn
from models.models import SkyshipUpgradesOut, GameItem,UserIn,Developer, Player, ConsumablesAndNoncombatItemsIn, ConsumablesAndNoncombatItemsOut
from pydantic import BaseModel
from typing import Dict, Any
import os, sys


def get_model_details(model: type[BaseModel]) -> Dict[str, str]:
    """
    Retourne un dictionnaire contenant les champs valides du modèle et leurs types attendus.
    
    :param model: Modèle Pydantic
    :return: Dictionnaire {nom_du_champ: type_attendu}
    """
    return {field_name: str(field_info.annotation) for field_name, field_info in model.__pydantic_fields__.items()}

# Fonction de validation des mises à jour
def validate_updates(updates: Dict[str, Any], model: BaseModel) -> Dict[str, str]:
    """
    Vérifie si les champs modifiés existent bien dans le modèle et si leurs valeurs sont du bon type.

    :param updates: Dictionnaire des mises à jour à valider.
    :param model: Modèle Pydantic à vérifier.
    :return: Dictionnaire avec les champs invalides et leurs erreurs.
    """
    # Récupérer les détails du modèle
    model_details = get_model_details(model)

    invalid_fields = {}
    for field, value in updates.items():
        if field not in model_details:
            invalid_fields[field] = f"⚠️ Champ inconnu"
        else:
            expected_type = model_details[field]
            # Vérification du type avec le modèle Pydantic
            expected_type = expected_type.replace('typing.Optional[', '').replace(']', '')  # Gestion des Optional
            if not isinstance(value, eval(expected_type)):
                invalid_fields[field] = f"⚠️ Type incorrect, attendu: {expected_type}"

    return invalid_fields