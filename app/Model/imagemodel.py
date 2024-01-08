import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.Model.model import Base


class ImageModel(Base):
    __tablename__ = "images"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
        unique=True,
    )
    name = Column(String(128), index=True, nullable=False)
    order_id = Column(ForeignKey("orders.id"), index=True, nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False)
    downloaded = Column(SmallInteger, nullable=False)
    path = Column(String(255), nullable=False)
    upload = Column(DateTime, default=datetime.utcnow, nullable=False)

    orders = relationship("OrderModel", back_populates="images")
