"""
Stub de la table `users` — appartient à dzastr-auth (Sequelize).
Déclarée ici uniquement pour que SQLAlchemy puisse résoudre les FK
(clients.User_Id, invoices.User_Id) lors du create_all au démarrage.
"""

from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class UserStub(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    User_Id = Column(Integer, primary_key=True, autoincrement=True)
    User_Username = Column(String(80), nullable=False)
    User_Role = Column(String(50), nullable=False, default="user")
    User_Password = Column(String(255), nullable=False)
    User_Email = Column(String(80), nullable=False, unique=True)
    User_Entreprise = Column(String(80), nullable=True)
    User_Address = Column(String(255), nullable=True)
    User_IsEntrepreneur = Column(Boolean, nullable=False, default=False)