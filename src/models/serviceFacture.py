from sqlalchemy import Column, Integer, String
from .base import Base


class ServiceFacture(Base):
    __tablename__ = "service_factures"

    ServiceFacture_Id = Column(Integer, primary_key=True, autoincrement=True)
    Service_Id = Column(Integer, nullable=False)
    ServiceFacture_Lot = Column(String(255), nullable=False)
    

    def __repr__(self):
        return f"<ServiceFacture(ServiceFacture_Id={self.ServiceFacture_Id}, Service_Id='{self.Service_Id}', ServiceFacture_Lot='{self.ServiceFacture_Lot}')>"
    