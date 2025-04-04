
from pydantic import BaseModel
from typing import Optional, List


################ GAME ASSETS ###############################################################################################

# Modèle pour les objets de jeu
class GameItem(BaseModel):
    ASSIGNED_ARTIST: Optional[str] = None
    Name: str
    STATUS: Optional[str] = None
    Special_characteristic: Optional[str] = None
    Speed: Optional[int] = None
    rarity: Optional[str] = None
    special_restriction: Optional[str] = None

# Modèle pour les tables de capacité
class AbilityIn(BaseModel):
    Animation: Optional[str] = None
    Arcana_Boost: Optional[str] = None
    Creator: Optional[str] = None
    Description: Optional[str] = None
    Duration: Optional[int] = None
    Duration_additional_infos: Optional[str] = None
    Name: str
    Particle_Effect: Optional[str] = None
    Power_Cost: Optional[str] = None
    Primary_Power_type: Optional[str] = None
    Rarity: Optional[str] = None
    Secondary_power_type: Optional[str] = None
    Special_Mechanic: Optional[str] = None
    Special_restrictions: Optional[str] = None
    speed: Optional[int] = None

class AbilityOut(AbilityIn):
    custom_id:int

