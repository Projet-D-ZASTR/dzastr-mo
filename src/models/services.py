from sqlalchemy import Column, Integer, Numeric, String, Text

from .base import Base


class Service(Base):
    __tablename__ = "services"

    Service_Id = Column(Integer, primary_key=True, autoincrement=True)
    Service_Name = Column(String(255), nullable=False)
    Service_PriceHour = Column(Numeric(10, 2), nullable=False)
    Service_Description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Service(Service_Id={self.Service_Id}, Service_Name='{self.Service_Name}')>"
