from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from .base import Base


class UserClient(Base):
    __tablename__ = "UserClient"

    id = Column(Integer, primary_key=True, autoincrement=True)
    User_Id = Column(
        Integer, ForeignKey("users.User_Id", ondelete="CASCADE"), nullable=False
    )
    Client_Id = Column(
        Integer, ForeignKey("clients.ClientId", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (UniqueConstraint("User_Id", "Client_Id", name="uq_user_client"),)

    def __repr__(self):
        return f"<UserClient(User_Id={self.User_Id}, Client_Id={self.Client_Id})>"
