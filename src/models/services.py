from sqlalchemy import Column, Integer, Numeric, String, Text

from .base import Base


class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, autoincrement=True)
    service_nom = Column(String(255), nullable=False)
    service_prixHeure = Column(Numeric(10, 2), nullable=False)
    service_description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Service(id={self.service_id}, nom='{self.service_nom}', prix_heure={self.service_prixHeure})>"
