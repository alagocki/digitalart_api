from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pydantic.schema import List

from app.Model.user import User
from app.Schema.imageschema import ImageSchema


class Status(Enum):
    open = "offen"
    closed = "erledigt"
    clarification = "in_klaerung"


class OrderSchema(BaseModel):
    topic: str
    info: str
    customer_id: str
    status: Status
    order_number: str
    basic_price: float
    additional_pic_price: float
    condition: str
    shooting_date: datetime
    images_cnt: int
    include_media: int
    images: List[ImageSchema] if List[ImageSchema] else None

    class Config:
        orm_mode = True


class OrderCreate(OrderSchema):
    pass


class OrderRead(OrderSchema):
    id: str


class OrderUpdate(OrderSchema):
    pass
