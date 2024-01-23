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
    status: str
    images: List[ImageSchema]

    class Config:
        orm_mode = True


class OrderCreate(OrderSchema):
    pass


class OrderRead(OrderSchema):
    id: str


class OrderUpdate(OrderSchema):
    pass
