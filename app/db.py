import uuid
from enum import Enum

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "postgresql+asyncpg://digitalart:digitalart@db:5432/digitalart"

Base = declarative_base()


class Status(str, Enum):
    processed = "bearbeitet"
    unprocessed = "unbearbeitet"
    downloaded = "runtergeladen"


class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String(30))
    customer = Column(Boolean())
    images = relationship("Image", back_populates="owner")


class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(128))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    owner = relationship("User", back_populates="images")
    description = Column(String(500))
    status = Column(String(20), default=Status.unprocessed)
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
