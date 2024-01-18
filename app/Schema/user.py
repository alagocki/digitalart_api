from typing import Optional

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class UserRead(BaseUser):
    customer: Optional[int] = None


class UserCreate(BaseUserCreate):
    customer: Optional[int] = None


class UserUpdate(BaseUserUpdate):
    customer: Optional[int] = None
