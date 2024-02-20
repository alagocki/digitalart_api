from sqlalchemy import Column, ForeignKey, Table

from app.Model.model import Base

image_order = Table(
    "image_order",
    Base.metadata,
    Column("image_id", ForeignKey("images.id"), primary_key=True),
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
)
