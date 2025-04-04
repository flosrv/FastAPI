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

