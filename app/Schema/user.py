from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class UserRead(BaseUser):
    username: str
    customer: bool = True


class UserCreate(BaseUserCreate):
    username: str
    customer: bool = True


class UserUpdate(BaseUserUpdate):
    username: str
    customer: bool = True
