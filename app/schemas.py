from enum import Enum

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from sqlalchemy import Boolean, Column, DateTime, Integer, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID


class Status(str, Enum):
    processed = "bearbeitet"
    unprocessed = "unbearbeitet"
    downloaded = "runtergeladen"


class UserRead(BaseUser):
    username: str
    customer: bool = True


class UserCreate(BaseUserCreate):
    username: str
    customer: bool = True


class UserUpdate(BaseUserUpdate):
    username: str
    customer: bool = True


# class ImageSchema():
#     id: str
#     name: str
#     owner: int
#     description: str
#     status: Status
#     downloaded: bool = False
#     path: str
#     upload: datetime
