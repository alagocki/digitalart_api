from enum import Enum

from pydantic import BaseModel


class Status(Enum):
    unprocessed = "unbearbeitet"
    processed = "bearbeitet"
    downloaded = "runtergeladen"


class ImageSchema(BaseModel):
    name: str
    description: str
    status: str
    ordered: bool
    base64encoded: str
    blocked: bool
    file_extension: str

    class Config:
        orm_mode = True


class ImageCreate(ImageSchema):
    pass


class ImageRead(ImageSchema):
    id: str


class ImageUpdate(ImageSchema):
    pass
