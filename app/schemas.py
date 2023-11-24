from enum import Enum
from typing import Optional

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from sqlmodel import Field, SQLModel


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


class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner: Optional[int] = Field(default=None, foreign_key="user.id")
    description: str = Field(default=None)
    status: Status
    downloaded: int = Field(default=0)
    path: str = Field(default=None)
