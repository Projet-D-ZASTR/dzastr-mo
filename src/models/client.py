from sqlalchemy import Column, ForeignKey, Integer, String

from .base import Base


class Client(Base):
    __tablename__ = "clients"

    Client_Id = Column(Integer, primary_key=True, autoincrement=True)
    User_Id = Column(
        Integer, ForeignKey("users.User_Id", ondelete="CASCADE"), nullable=False
    )
    Client_Name = Column(String(255), nullable=False)
    Client_Entreprise = Column(String(255), nullable=False)
    Client_Email = Column(String(255), nullable=False)
    Client_Address = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Client(Client_Id={self.Client_Id}, Client_Name='{self.Client_Name}')>"
