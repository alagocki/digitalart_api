from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from enum import Enum
from typing import Optional


class Roles(str, Enum):
    user = "user"
    admin = "admin"


class Status(str, Enum):
    processed = "bearbeitet"
    unprocessed = "bearbeitet"
    downloaded = "runtergeladen"


class BaseUser(SQLModel):
    email: EmailStr
    username: str
    is_active: bool = False
    role: Roles


class User(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


class UserSchema(BaseUser):
    password: str


class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner: Optional[int] = Field(default=None, foreign_key="user.id")
    description: str = Field(default=None)
    status: Status
    downloaded: int = Field(default=0)
    path: str = Field(default=None)
