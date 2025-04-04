from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "ginngfdsf54f464dd6th468hthd58e7d7g7h8rx8c4cs46e4he8the6th"
ALGORITHM = "HS256"

# Contexte pour le hachage de mot de passe
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fonction pour hacher un mot de passe
def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)

# Fonction pour vérifier un mot de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

# Fonction pour créer un JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
