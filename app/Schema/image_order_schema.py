from pydantic.schema import List

from app.Schema.imageschema import ImageSchema
from app.Schema.orderschema import OrderSchema


class imageOut(ImageSchema):
    orders: List[OrderSchema]


class orderOut(OrderSchema):
    images: List[ImageSchema]
