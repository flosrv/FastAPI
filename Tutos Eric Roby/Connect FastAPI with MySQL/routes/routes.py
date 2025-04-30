from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from sqlmodel import Session, select
from auth import hash_password, verify_password, create_access_token, get_current_user, get_current_user_roles, check_user_has_role
from models import User, Role
from db.database import get_db
import logging

# Créer un routeur FastAPI
endPoint = APIRouter()

# OAuth2PasswordBearer pour extraire le token dans les headers Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialiser le logger
logger = logging.getLogger("app")

# Route pour s'inscrire (création d'un utilisateur)
@endPoint.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    username: str, 
    email: str, 
    password: str, 
    db: Session = Depends(get_db)
):
    try:
        # Vérifier si l'utilisateur existe déjà, ou si l'email est déjà enregistré
        statement = select(User).where(User.username == username | User.email == email)
        existing_user = db.exec(statement).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or Email already taken")

        # Hacher le mot de passe avant de l'enregistrer
        hashed_password = hash_password(password)  
        new_user = User(username=username, email=email, hashed_password=hashed_password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"User {username} registered successfully.")
        return {"msg": "User created successfully"}

    except Exception as e:
        logger.error(f"Error during user registration: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# Route pour se connecter (générer un token JWT)
@endPoint.post("/token", response_model=dict)
async def login_for_access_token(
    username: str, 
    password: str, 
    db: Session = Depends(get_db)
):
    try:
        # Vérifier si l'utilisateur existe
        statement = select(User).where(User.username == username)
        user = db.exec(statement).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        # Vérifier le mot de passe
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        # Créer un token
        access_token = create_access_token(data={"sub": user.username})
        logger.info(f"User {username} logged in successfully.")
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# Route protégée par authentification (requiert un token valide)
@endPoint.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# Route protégée par authentification et autorisation de rôle
@endPoint.get("/admin", response_model=str)
async def admin_only(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    try:
        if not check_user_has_role(current_user, "admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this resource"
            )

        logger.info(f"User {current_user.username} accessed admin resource.")
        return {"msg": "Welcome, Admin!"}
    
    except Exception as e:
        logger.error(f"Error in admin access: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# Route pour récupérer les rôles de l'utilisateur actuel
@endPoint.get("/users/me/roles", response_model=List[str])
async def read_user_roles(current_user: User = Depends(get_current_user)):
    try:
        roles = get_current_user_roles(current_user)
        logger.info(f"User {current_user.username} roles fetched successfully.")
        return roles

    except Exception as e:
        logger.error(f"Error fetching roles for user {current_user.username}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
