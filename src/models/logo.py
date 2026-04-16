from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String

from .base import Base


class Logo(Base):
    __tablename__ = "logos"

    Logo_Id = Column(Integer, primary_key=True, autoincrement=True)
    User_Id = Column(
        Integer, ForeignKey("users.User_Id", ondelete="CASCADE"), nullable=False
    )
    Logo_Data = Column(LargeBinary, nullable=False)
    Logo_Filename = Column(String(255), nullable=False)
    Logo_Sizebytes = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Logo(Logo_Id={self.Logo_Id}, User_Id={self.User_Id}, Logo_Filename='{self.Logo_Filename}')>"
