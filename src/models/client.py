from sqlalchemy import Column, Integer, String

from .base import Base


class Client(Base):
    __tablename__ = "clients"

    ClientId = Column(Integer, primary_key=True, autoincrement=True)
    Client_Name = Column(String(255), nullable=False)
    Client_Entreprise = Column(String(255), nullable=False)
    Client_Email = Column(String(255), nullable=False)
    Client_Address = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Client(ClientId={self.ClientId}, Client_Name='{self.Client_Name}', Client_Entreprise='{self.Client_Entreprise}', Client_Email='{self.Client_Email}', Client_Address='{self.Client_Address}')>"
