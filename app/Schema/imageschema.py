from enum import Enum

from pydantic import BaseModel, Field
from pydantic.schema import Optional


class Status(Enum):
    unprocessed = "unbearbeitet"
    processed = "bearbeitet"
    downloaded = "runtergeladen"


class ImageSchema(BaseModel):
    name: str
    description: str
    status: Status
    downloaded: bool
    path: str

    class Config:
        orm_mode = True


class ImageCreate(ImageSchema):
    pass


class ImageRead(ImageSchema):
    id: str


class ImageUpdate(ImageSchema):
    pass
