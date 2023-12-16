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
    downloaded: bool = False
    path: str

    class Config:
        orm_mode = True
