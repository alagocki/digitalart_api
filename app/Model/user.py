from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.Model.model import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    customer = Column(Integer(), default=0, nullable=True, autoincrement=True)

    # orders = relationship("OrderModel", backref="owner")
    # address = relationship("CustomerAddressModel", back_populates="customer")
