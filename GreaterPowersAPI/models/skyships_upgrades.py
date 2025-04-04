from pydantic import BaseModel
from typing import Optional, List


# Modèle pour les objets de jeu
class GameItem(BaseModel):
    ASSIGNED_ARTIST: Optional[str] = None
    Name: str
    STATUS: Optional[str] = None
    Special_characteristic: Optional[str] = None
    Speed: Optional[int] = None
    rarity: Optional[str] = None
    special_restriction: Optional[str] = None

################# SKYSHIPS UPGRADES ##############################################################################

# Modèle des améliorations de Skyship héritant de GameItem
class SkyshipUpgradesIn(GameItem):
    Activation_cost: Optional[str] = None
    Arcana_Requirement: Optional[str] = None
    Cooldown: Optional[int] = None
    Ineffective_Range: Optional[str] = None
    Optimal_Range: Optional[str] = None
    Tier_Restriction: Optional[int] = None
    Type: Optional[str] = None

class SkyshipUpgradesOut(SkyshipUpgradesIn):
    custom_id:int


