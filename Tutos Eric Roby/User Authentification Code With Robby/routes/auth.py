from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from db import get_db
from models.users import Users
from schemas.user import CreateUserRequest, Token
from core.security import hash_password, create_access_token

# Création du router FastAPI pour les routes d'authentification
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Route pour créer un utilisateur
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: Session = Depends(get_db), create_user_request: CreateUserRequest = Depends()):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(Users).filter(Users.username == create_user_request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Cet utilisateur existe déjà")

    # Créer un nouvel utilisateur
    new_user = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        hashed_password=hash_password(create_user_request.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "Utilisateur créé avec succès"}

# Route pour générer un token JWT après login
@router.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(Users).filter(Users.username == form_data.username).first()
    
    if not user or not hash_password.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
