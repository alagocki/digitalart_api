from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class UserRead(BaseUser):
    customer: int


class UserCreate(BaseUserCreate):
    customer: int


class UserUpdate(BaseUserUpdate):
    customer: int
