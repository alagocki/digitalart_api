import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, SmallInteger, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.Model import *
from app.Model.model import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
        unique=True,
    )
    name = Column(String(128))
    owner_id = Column(ForeignKey("user.id"), nullable=False)
    description = Column(String(500))
    status = Column(String(20))
    downloaded = Column(SmallInteger)
    path = Column(String(255))
    upload = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="images")
