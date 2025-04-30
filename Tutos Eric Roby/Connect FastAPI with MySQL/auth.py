from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from models import User, Role  # Importation des modèles User et Role depuis sqlmodel
from db.database import get_db  # La fonction pour obtenir une session de la DB
import os

# Configuration du contexte pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clé secrète et algorithme pour signer les JWT
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")  # Remplacer par une vraie clé secrète en prod
ALGORITHM = "RS256"  # Utilisation de l'algorithme RS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Durée de validité du token en minutes

# OAuth2PasswordBearer pour extraire le token dans les headers Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Fonction pour hacher un mot de passe
def hash_password(password: str) -> str:
    """
    Hacher un mot de passe avant de le stocker.
    """
    return pwd_context.hash(password)


# Fonction pour vérifier un mot de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifier si le mot de passe plain text correspond à son mot de passe haché.
    """
    return pwd_context.verify(plain_password, hashed_password)


# Fonction pour générer un token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token JWT à partir des données spécifiées. 
    Si expires_delta est fourni, il définit la date d'expiration du token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Fonction pour vérifier un token JWT
def verify_token(token: str):
    """
    Vérifie la validité du token JWT, et renvoie les données décodées.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or has expired",
        )


# Fonction de dépendance pour obtenir l'utilisateur actuel à partir du token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Cette fonction extrait l'utilisateur actuel à partir du token JWT.
    """
    payload = verify_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain a valid username",
        )
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()  # Utilisation de sqlmodel ici pour exécuter la requête
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


# Fonction pour obtenir les rôles de l'utilisateur actuel
def get_current_user_roles(current_user: User = Depends(get_current_user)) -> List[str]:
    """
    Renvoie la liste des rôles de l'utilisateur actuel.
    """
    return [role.name for role in current_user.roles]


# Fonction pour vérifier si l'utilisateur a un rôle spécifique
def check_user_has_role(current_user: User, role_name: str) -> bool:
    """
    Vérifie si l'utilisateur actuel a un rôle spécifique.
    """
    return any(role.name == role_name for role in current_user.roles)
