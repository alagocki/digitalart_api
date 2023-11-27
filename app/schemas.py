import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import Field


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


class Image:
    id: Optional[UUID] = Field(primary_key=True, index=True)
    name: str = Field(nullable=False, max_length=128)
    owner: int = Field(nullable=False)
    description: Optional[str] = Field(max_length=500)
    status: Status
    downloaded: Optional[int]
    path: str = Field(max_length=255)
    upload: datetime = Field(nullable=False)

