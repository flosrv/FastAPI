from sqlmodel import Session
from models.models import User, Department
from faker import Faker
from db.database import engine, get_db, init_db
from passlib.context import CryptContext

# Configuration du hachage des mots de passe avec Passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fonction pour hacher le mot de passe
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Fonction pour créer les départements fictifs
def create_departments(session: Session, departments: list):
    for dept in departments:
        department = Department(name=dept)
        session.add(department)
    session.commit()
    print("Départements ajoutés avec succès.")

# Fonction d'exemple pour générer des utilisateurs répartis sur 5 départements
def create_users_example():
    fake = Faker()
    departments = ['Ressources Humaines', 'Informatique', 'Marketing', 'Finance', 'Ventes']
    
    # Créer les départements
    with Session(engine) as session:
        create_departments(session, departments)
        
        # Créer 100 utilisateurs répartis entre les départements
        for _ in range(100):
            # Génére des données d'employés fictifs
            department_name = fake.random.choice(departments)
            department = session.query(Department).filter(Department.name == department_name).first()
            
            hashed_pwd = hash_password(fake.password(length=12))  # Hachage du mot de passe avant de le stocker
            new_user = User(
                username=fake.user_name(),
                email=fake.email(),
                hashed_password=hashed_pwd,
                department_id=department.id
            )
            session.add(new_user)

        session.commit()
        print("100 utilisateurs ajoutés avec succès.")

# Fonction d'initialisation des données
def initialize_data():
    with Session(engine) as session:
        # Créer les départements et les utilisateurs
        create_users_example()
        print("Données initiales insérées avec succès.")
