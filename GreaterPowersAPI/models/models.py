from pydantic import BaseModel
from typing import Optional, List

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

# Modèle pour les objets de jeu
class GameItem(BaseModel):
    custom_id:int
    ASSIGNED_ARTIST: Optional[str] = None
    Name: str
    STATUS: Optional[str] = None
    Special_characteristic: Optional[str] = None
    Speed: Optional[str] = None
    rarity: Optional[str] = None
    special_restriction: Optional[str] = None

    class Config:
        # Pour exclure des champs comme _id de la sérialisation JSON
        json_schema_extra = {
            "exclude": {"_id"}
        }

# Modèle des armes héritant de GameItem
class Weapon(GameItem):
    Activation_cost: Optional[str] = None
    Arcana_Boost: Optional[str] = None
    Cooldown_in_turns: Optional[int] = None
    Tier_Minimum: Optional[str] = None
    Type: Optional[str] = None

# Modèle des mécaniques de capacité héritant de GameItem
class AbilityMechanics(BaseModel):
    custom_id:int
    Description: Optional[str] = None
    Name: Optional[str] = None
    Type: Optional[str] = None

# Modèle des améliorations de Skyship héritant de GameItem
class SkyshipUpgrades(GameItem):
    Activation_cost: Optional[str] = None
    Arcana_Requirement: Optional[str] = None
    Cooldown: Optional[str] = None
    Ineffective_Range: Optional[str] = None
    Optimal_Range: Optional[str] = None
    Tier_Restriction: Optional[str] = None
    Type: Optional[str] = None

# Modèle pour les consommables et objets non-combattants héritant de GameItem
class ConsumablesAndNoncombatItems(GameItem):
    Arcana_Restriction: Optional[str] = None
    Class_Restriction: Optional[str] = None
    Description: Optional[str] = None
    Special_Mechanic: Optional[str] = None
    Special_Restriction: Optional[str] = None

# Modèle pour les tables de capacité
class Ability(BaseModel):
    custom_id:int
    Animation: Optional[str] = None
    Arcana_Boost: Optional[str] = None
    Creator: str
    Description: str
    Duration: str
    Name: str
    Particle_Effect: str
    Power_Cost: str
    Primary_Power_type: str
    Rarity: str
    Secondary_power_type: str
    Special_Mechanic: str
    Special_restrictions: str
    speed: str
