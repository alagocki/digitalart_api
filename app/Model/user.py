from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.Model.image import Image
from app.Model.model import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String(30))
    customer = Column(Boolean())

    images = relationship("Image", back_populates="owner")
