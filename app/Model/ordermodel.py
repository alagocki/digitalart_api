import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.Model.model import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
        unique=True,
    )
    topic = Column(String(100), index=True, nullable=False)
    owner_id = Column(ForeignKey("user.id"), index=True, nullable=False)
    info = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="orders")
    images = relationship("ImageModel", back_populates="orders")
