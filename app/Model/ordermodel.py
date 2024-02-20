import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.Model.model import Base
from app.Model.relation_image_order import image_order


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
    order_number = Column(String(100), index=True, nullable=False)
    owner_id = Column(ForeignKey("user.id"), index=True, nullable=False)
    customer_id = Column(ForeignKey("user.id"), index=True, nullable=False)
    info = Column(String(500), nullable=True)
    status = Column(Text, nullable=False)
    shooting_date = Column(DateTime, nullable=True)
    basic_price = Column(Float, nullable=True)
    additional_pic_price = Column(Float, nullable=True)
    include_media = Column(Integer, nullable=True)
    condition = Column(Text, nullable=True)
    images_cnt = Column(Integer, nullable=True)
    created = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", foreign_keys="[OrderModel.owner_id]")
    customer = relationship("User", foreign_keys="[OrderModel.customer_id]")
    images = relationship("ImageModel", secondary=image_order, back_populates="orders")
