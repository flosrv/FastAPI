from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

# Charger les credentials depuis un fichier JSON
path_to_mysql_creds = r"c:\Credentials\mysql_creds.json"

with open(path_to_mysql_creds, 'r') as file:
    content = json.load(file)
    mysql_user = content["user"]
    mysql_password = content["password"]
    mysql_port = content["port"]
    mysql_host = content["host"]

database_darkstar = "Darkstar_Games"

# Connexion MySQL
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{database_darkstar}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, isolation_level='AUTOCOMMIT')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance pour obtenir la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
