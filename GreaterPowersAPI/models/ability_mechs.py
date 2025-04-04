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

################ ABILITY MECHS ##############################################################################

# Modèle des mécaniques de capacité héritant de GameItem
class AbilityMechIn(BaseModel):
    Description: Optional[str] = None
    Name: str
    Type: Optional[str] = None

# Modèle des mécaniques de capacité héritant de GameItem
class AbilityMechOut(AbilityMechIn):
    custom_id:int
    