from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from typing import List, Optional
from datetime import datetime

# Modèle pour le Département
class Department(SQLModel, table=True):
    __tablename__ = 'departments'

    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": True, "nullable": False})

    # Relation one-to-many avec User
    users: List["User"] = Relationship(back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name})>"

# Modèle pour le Rôle (Role) des utilisateurs
class Role(SQLModel, table=True):
    __tablename__ = 'roles'

    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": True, "nullable": False})

    # Relation many-to-many avec User (un utilisateur peut avoir plusieurs rôles)
    users: List["User"] = Relationship(back_populates="roles", link_model="UserRole")

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"

# Modèle pour l'Utilisateur (User)
class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, sa_column_kwargs={"unique": True, "nullable": False})
    email: str = Field(index=True, sa_column_kwargs={"unique": True, "nullable": False})
    hashed_password: str = Field(nullable=False)

    # Liens avec le Département
    department_id: int = Field(foreign_key="departments.id", nullable=False)
    department: Department = Relationship(back_populates="users")

    # Relation many-to-many avec Role (un utilisateur peut avoir plusieurs rôles)
    roles: List["Role"] = Relationship(back_populates="users", link_model="UserRole")

    # Relation one-to-many avec Token
    tokens: List["Token"] = Relationship(back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

# Table de liaison entre les utilisateurs et leurs rôles
class UserRole(SQLModel, table=True):
    __tablename__ = 'user_roles'

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role_id: int = Field(foreign_key="roles.id", primary_key=True)

    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"

# Modèle pour le Token JWT
class Token(SQLModel, table=True):
    __tablename__ = 'tokens'

    id: int = Field(default=None, primary_key=True)
    access_token: str = Field(nullable=False)
    refresh_token: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow, nullable=False)

    # Relier le token à l'utilisateur
    user_id: int = Field(foreign_key="users.id", nullable=False)
    user: User = Relationship(back_populates="tokens")

    __table_args__ = (
        UniqueConstraint('user_id', 'access_token', name='unique_user_access_token'),
    )

    def __repr__(self):
        return f"<Token(id={self.id}, access_token={self.access_token}, created_at={self.created_at})>"
