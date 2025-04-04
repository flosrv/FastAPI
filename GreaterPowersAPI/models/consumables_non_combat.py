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

################# CONSUMABLES NON COMBAT ITEMS ##############################################################################

# Modèle pour les consommables et objets non-combattants héritant de GameItem
class ConsumablesAndNoncombatItemsIn(GameItem):
    Arcana_Restriction: Optional[str] = None
    Class_Restriction: Optional[str] = None
    Description: Optional[str] = None
    Special_Mechanic: Optional[str] = None
    Special_Restriction: Optional[str] = None

class ConsumablesAndNoncombatItemsOut(ConsumablesAndNoncombatItemsIn):
    custom_id:int