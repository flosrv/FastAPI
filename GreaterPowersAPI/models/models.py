from pydantic import BaseModel
from typing import Optional, List



################ PEOPLE ###############################################################################################

# Classe Person qui sera une base pour d'autres classes
class Person(BaseModel):
    name: str
    surname: str

# Classe de base pour les utilisateurs
class User(BaseModel):
    email: str

# Classe d'authentification pour les utilisateurs
class UserIn(BaseModel):
    password: str

# Classe Developer héritant de User et ajoutant des spécificités
class Developer(User, Person):  # On hérite maintenant de User et Person
    role: str
    tags: List[str]  # Change en liste de tags
    rights: Optional[str] = None

# Classe Player avec ses propriétés
class Player(BaseModel):  # Héritage de BaseModel
    level: int
    faction: Optional[str] = None
    guild: Optional[str] = None
    achievements: Optional[List[str]] = None  # Liste d'achievements
    playtime_hours: Optional[int] = None

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

################# WEAPONS ##############################################################################

# Modèle des armes héritant de GameItem
class WeaponIn(GameItem):
    Activation_cost: Optional[str] = None
    Arcana_Boost: Optional[str] = None
    Cooldown_in_turns: Optional[int] = None
    Tier_Minimum: Optional[int] = None
    Type: Optional[str] = None

class WeaponOut(WeaponIn):
    custom_id : int
    
################# ABILITY MECHS ##############################################################################

# Modèle des mécaniques de capacité héritant de GameItem
class AbilityMechIn(BaseModel):
    Description: Optional[str] = None
    Name: str
    Type: Optional[str] = None

# Modèle des mécaniques de capacité héritant de GameItem
class AbilityMechOut(AbilityMechIn):
    custom_id:int

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



