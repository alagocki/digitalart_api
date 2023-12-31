import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.Model.model import Base


class CustomerAddressModel(Base):
    __tablename__ = "addresses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
        unique=True,
    )
    forename = Column(String(125), index=True, nullable=False)
    lastname = Column(String(125), index=True, nullable=False)
    street = Column(String(125), index=True, nullable=False)
    number = Column(Integer(), index=True, nullable=False)
    city = Column(String(125), index=True, nullable=False)
    zip = Column(Integer(), index=True, nullable=False)
    country = Column(String(125), index=True, nullable=True)
    phone = Column(String(20), index=True, nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(ForeignKey("user.id"), index=True, nullable=False)

    customer = relationship("User", back_populates="address")
