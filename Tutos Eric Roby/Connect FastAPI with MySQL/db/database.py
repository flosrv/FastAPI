from sqlmodel import Session, SQLModel, create_engine
from typing import Generator
from models.models import User, Department  # Importer les modèles User et Department
import pymysql
import json
import os

# Charger les informations de connexion depuis un fichier JSON
mysql_creds_path = r"c:\Credentials\mysql_creds.json"

def load_db_config():
    try:
        with open(mysql_creds_path, "r") as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"Erreur : Le fichier de configuration '{mysql_creds_path}' est introuvable.")
        raise
    except json.JSONDecodeError:
        print("Erreur : Le fichier de configuration JSON est mal formaté.")
        raise

config = load_db_config()

host = config["host"]
user = config["user"]
password = config["password"]
port = int(config["port"])

DATABASE = "user_management_project"

# Fonction pour créer la base de données si nécessaire
def create_database():
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            cursorclass=pymysql.cursors.DictCursor,
        )
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        print(f"Base de données '{DATABASE}' vérifiée/créée avec succès.")
    except pymysql.MySQLError as e:
        print(f"Erreur MySQL lors de la création de la base de données: {e}")
        raise
    finally:
        connection.close()

# Créer la base de données si elle n'existe pas
create_database()

# Connexion à la base de données via SQLModel
connection_string = (
    f"mysql+pymysql://{config['user']}:{config['password']}"
    f"@{config['host']}:{config['port']}/{DATABASE}"
)

# Créer le moteur SQLModel pour interagir avec la base de données
engine = create_engine(connection_string, echo=True)

# Fonction pour obtenir une session de base de données
def get_db() -> Generator[Session, None, None]:
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        print(f"Erreur lors de la récupération de la session : {e}")
        raise

# Fonction pour initialiser la base de données (création des tables)
def init_db():
    try:
        SQLModel.metadata.create_all(bind=engine)
        print("Tables créées avec succès dans la base de données.")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")
        raise

