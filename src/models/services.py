from sqlalchemy import Column, Integer, String, Numeric, Text
from .base import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    prix_heure = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Service(id={self.id}, nom='{self.nom}', prix_heure={self.prix_heure})>"
