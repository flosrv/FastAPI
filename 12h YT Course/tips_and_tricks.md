# Quand FastAPI charge indéfiniment, et que le code est correct, toujours checker si le port à utiliser n'est pas déjà utilisé
C:\Users\f.gionnane>netstat -ano | findstr :8000

  TCP    127.0.0.1:8000         0.0.0.0:0              LISTENING       17852
  TCP    127.0.0.1:8000         0.0.0.0:0              LISTENING       11104

  TCP    127.0.0.1:8000         127.0.0.1:51904        CLOSE_WAIT      17852

  TCP    127.0.0.1:51904        127.0.0.1:8000         FIN_WAIT_2      5892
  TCP    127.0.0.1:52075        127.0.0.1:8000         ESTABLISHED     5892

# Ici on a un probleme avec le port 8000 et on voit qu'il est déjà occupé par deux processus. Tuons les !
taskkill /PID 17852 /F
taskkill /PID 11104 /F
Opération réussie : le processus avec PID 11104 a été terminé.

Ensuite on réessaie par ex:
http://127.0.0.1:8000/api/v1/books
Ca doit marcher  !


# 📌 **Tips & Tricks pour l'utilisation de FastAPI & Pydantic (Version 0.115.12 / 2.10.6)**

### 🔹 **1. Modèles Pydantic - Structuration et Validation**

#### ✅ **Utilisation de Pydantic pour la Validation**
Pydantic permet de définir des modèles qui valident et sérialisent les données de manière fluide. Cela assure une validation des données côté serveur.

```python
from pydantic import BaseModel

class Weapon(BaseModel):
    name: str
    activation_cost: str
    cooldown_in_turns: float
    special_characteristic: str
    speed: float
```

**Astuce :** Utiliser des types `Optional` pour les champs qui peuvent être nuls.
```python
from typing import Optional
class Weapon(BaseModel):
    name: str
    cooldown_in_turns: Optional[float] = None
```

#### ✅ **Validation de données imbriquées**
Si vous avez des objets imbriqués (par exemple, un objet `user` dans un `profile`), vous pouvez les valider automatiquement.

```python
class User(BaseModel):
    username: str
    email: str

class Profile(BaseModel):
    user: User
    age: int
```

#### ✅ **Configurer des erreurs de validation personnalisées**
Pydantic vous permet de définir des erreurs personnalisées en utilisant des méthodes de validation.

```python
from pydantic import validator

class Weapon(BaseModel):
    name: str
    activation_cost: str

    @validator('activation_cost')
    def validate_activation_cost(cls, v):
        if not v.isdigit():
            raise ValueError('Activation cost must be numeric')
        return v
```

---

### 🔹 **2. Sécurisation de votre API**

#### ✅ **Authentification basée sur JWT**
L'authentification par token (JWT) est couramment utilisée dans des applications comme des jeux en ligne pour sécuriser les routes. Voici un exemple simple pour l'implémentation :

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
```

**Astuce :** Toujours sécuriser les clés JWT en les stockant dans des variables d'environnement et éviter de les hardcoder dans votre code.

---

### 🔹 **3. Utilisation des Routes avec MongoDB (ou autre BDD NoSQL)**

#### ✅ **Connexion à MongoDB**
Utiliser une bibliothèque comme `motor` pour la connexion asynchrone à MongoDB.

```python
from motor.motor_asyncio import AsyncIOMotorClient

@app.on_event("startup")
async def startup_db():
    app.mongodb_client = AsyncIOMotorClient("mongodb://localhost:27017")
    app.db = app.mongodb_client["game_db"]
```

#### ✅ **Opérations CRUD avec MongoDB**
Une fois la connexion établie, vous pouvez effectuer des opérations CRUD de manière fluide.

```python
@app.post("/weapons")
async def create_weapon(weapon: Weapon):
    weapon_dict = weapon.dict()
    result = await app.db.weapons.insert_one(weapon_dict)
    return {"status": "success", "id": str(result.inserted_id)}

@app.put("/weapons/{weapon_id}")
async def update_weapon(weapon_id: str, weapon: Weapon):
    update_result = await app.db.weapons.update_one({"_id": ObjectId(weapon_id)}, {"$set": weapon.dict()})
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return {"status": "success", "message": "Weapon updated successfully"}
```

#### ✅ **Indexation de données pour des requêtes rapides**
Indexez vos collections pour optimiser les recherches. Cela réduit la latence des requêtes dans les systèmes de production.

```python
@app.on_event("startup")
async def setup_indexes():
    await app.db.weapons.create_index([("name", pymongo.ASCENDING)])
```

---

### 🔹 **4. Gestion des Erreurs et Debugging**

#### ✅ **Gestion centralisée des erreurs**
Utiliser FastAPI pour personnaliser le gestionnaire d’erreurs, ce qui permet de centraliser et normaliser les réponses en cas d'erreur.

```python
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Custom error: {exc.detail}"}
    )
```

**Astuce :** Ajoutez des logs détaillés à chaque étape critique du processus pour faciliter le debugging en production.

#### ✅ **Logging avec FastAPI**
L'intégration du logging dans votre API peut vous permettre de suivre les événements en temps réel.

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    logger.info("Received a request at root")
    return {"message": "Hello, World!"}
```

---

### 🔹 **5. Tests Unitaires et Intégration**

#### ✅ **Tests avec pytest**
Testez vos routes et modèles avec `pytest` pour garantir que tout fonctionne avant de déployer en production.

```python
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_create_weapon():
    response = client.post("/weapons", json={"name": "Test Weapon", "activation_cost": "1i/att"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "id": "some_id"}
```

**Astuce :** Utiliser `TestClient` pour tester les requêtes en interne sans avoir à démarrer un serveur complet.

---

### 🔹 **6. Optimisation de la Performance**

#### ✅ **Réponse asynchrone avec FastAPI**
Utilisez les méthodes asynchrones pour effectuer des opérations longues sans bloquer les autres requêtes.

```python
@app.get("/async_example")
async def async_example():
    await asyncio.sleep(2)  # Simulate a delay, like a database call
    return {"message": "This is an async route"}
```

#### ✅ **Cachez les réponses fréquentes**
Utilisez des solutions comme Redis pour mettre en cache les données fréquemment demandées et améliorer les performances.

```python
import redis

cache = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.get("/cached_weapon/{weapon_id}")
async def get_cached_weapon(weapon_id: str):
    cached_weapon = cache.get(weapon_id)
    if cached_weapon:
        return {"weapon": cached_weapon}
    weapon = await app.db.weapons.find_one({"_id": ObjectId(weapon_id)})
    cache.set(weapon_id, weapon)
    return {"weapon": weapon}
```

---

### 🔹 **7. Bonnes Pratiques et Sécurité**

#### ✅ **Limiter les Requêtes pour éviter le DDoS**
Utiliser un middleware pour limiter les requêtes par seconde et éviter les attaques DDoS.

```python
from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await FastAPILimiter.init(redis)

@app.get("/limited_route")
@limiter.limit("5/minute")
async def limited_route():
    return {"message": "This route is limited to 5 requests per minute."}
```

#### ✅ **Protection contre les attaques XSS et CSRF**
Dès que vous traitez des entrées de l'utilisateur (comme des textes, des fichiers ou des paramètres dans l'URL), assurez-vous de les valider pour éviter les attaques par injection.

```python
from fastapi import Request

@app.post("/submit_form")
async def submit_form(request: Request):
    form_data = await request.form()
    # Validation et échappement des entrées utilisateur
    return {"message": "Form submitted successfully"}
```

---

### 🔹 **8. Documentation et Maintenance**

#### ✅ **Génération automatique de la documentation**
FastAPI génère automatiquement de la documentation pour vos API via Swagger UI et Redoc, assurant ainsi une documentation toujours à jour.

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int, query_param: str = None):
    """
    Documentation pour cette route
    - `item_id`: ID de l'item à récupérer
    - `query_param`: Paramètre de requête facultatif
    """
    return {"item_id": item_id, "query_param": query_param}
```

---

**Astuce finale :**  
Investissez du temps pour maintenir une bonne structure de projet et un processus de test rigoureux. Cela vous aidera à éviter les problèmes en production et à livrer des applications fiables.

