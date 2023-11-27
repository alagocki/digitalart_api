import uuid

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import Boolean, Column, Integer, SmallInteger, String,DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import schemas

DATABASE_URL = "postgresql+asyncpg://digitalart:digitalart@db:5432/digitalart"

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String(30))
    customer = Column(Boolean())


class Image(Base):
    __tablename__ = "Image"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(128))
    owner = Column(Integer)
    description = Column(String(500))
    status = Column(String(20))
    downloaded = Column(SmallInteger)
    path = Column(String(255))
    upload = Column(DateTime)


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session=session, user_table=User)
