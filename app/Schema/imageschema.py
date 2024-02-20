from enum import Enum

from pydantic import BaseModel


class Status(Enum):
    unprocessed = "unbearbeitet"
    processed = "bearbeitet"
    downloaded = "runtergeladen"


class ImageSchema(BaseModel):
    name: str
    description: str
    status: Status
    ordered: bool
    base64encoded: str
    blocked: bool

    class Config:
        orm_mode = True


class ImageCreate(ImageSchema):
    pass


class ImageRead(ImageSchema):
    id: str


class ImageUpdate(ImageSchema):
    pass


class ImageUploadData(BaseModel):
    data: str
