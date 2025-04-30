from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from db import SessionLocal  # Importation de la session pour la base de données
from models.users import Users  # Importation du modèle Users
from passlib.context import CryptContext  # Pour la gestion du hachage de mot de passe
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # Pour la gestion de l'authentification OAuth2
from jose import jwt, JWTError  # Pour la gestion de JWT (JSON Web Tokens)
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, create_engine
import json


path_to_mysql_creds = r"c:\Credentials\mysql_creds.json"

with open (path_to_mysql_creds, 'r') as file:
    content = json.load(file)
    mysql_user = content["user"]
    mysql_password = content["password"]
    mysql_port = content["port"]
    mysql_host = content["host"]

mysql_user = "flosrv"
password = "Nesrine123"
host = "localhost"
port = 3306
database_darkstar = "Darkstar_Games"
Directors_table = 'Darkstar_Directors'

# Connect to the database
engine_darkstar = create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{database_darkstar}", isolation_level ='AUTOCOMMIT')

# Définition de l'endpoint 'auth' avec un préfixe /auth
endpoint = APIRouter(
    prefix='/auth',  # Toutes les routes commenceront par /auth
    tags=['auth']  # Tag pour regrouper les routes liées à l'authentification
)

# Clé secrète utilisée pour signer les JWT (en production, la clé doit être sécurisée)
SECRET = "ginngfdsf54f464dd6th468hthd58e7d7g7h8rx8c4cs46e4he8the6th"
ALGORITHM = "HS256"  # L'algorithme utilisé pour signer le JWT (ici HMAC avec SHA-256)

# Initialisation de l'objet CryptContext pour le hachage des mots de passe
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Instance d'OAuth2PasswordBearer qui nous permet de gérer la sécurité OAuth2 avec un token JWT
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# Modèle Pydantic pour la création d'un utilisateur
class CreateUserRequests(BaseModel):
    username: str  # Nom d'utilisateur
    password: str  # Mot de passe de l'utilisateur
    email: str  # Email de l'utilisateur

# Modèle Pydantic pour la réponse du token (JWT) après une authentification réussie
class Token(BaseModel):
    access_token: str  # Le token d'accès JWT
    token_type: str  # Type de token, ici "bearer"

# Fonction pour obtenir une session de base de données (DB)
def get_db():
    db = SessionLocal()  # Crée une instance de session DB
    try:
        yield db  # Récupère la session de DB à utiliser dans la route
    finally:
        db.close()  # Ferme la session DB une fois la requête traitée

# Alias de type pour la session DB dans les dépendances FastAPI
db_dependency = Annotated[Session, Depends(get_db)]

# Route pour créer un utilisateur (POST /auth)
@endpoint.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequests):
    # Création d'une instance Users avec les données de la requête
    create_user_model = Users(
        username=create_user_request.username,  # Récupère le nom d'utilisateur
        email=create_user_request.email,  # Récupère l'email
        hashed_password=bcrypt_context.hash(create_user_request.password)  # Hache le mot de passe avec bcrypt
    )

    # Ajoute l'utilisateur à la session DB
    db.add(create_user_model)
    
    # Commits les changements dans la DB pour enregistrer l'utilisateur
    db.commit()

    # Après l'ajout de l'utilisateur, la fonction se termine sans retour explicite
    # Le code HTTP 201 est renvoyé avec un statut de création réussie.







