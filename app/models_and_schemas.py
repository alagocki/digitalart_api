from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from enum import Enum
from typing import Optional


class Roles(str, Enum):
    user = "user"
    admin = "admin"


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
