import json

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from app.db import User, create_db_and_tables, get_async_session, Image
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import active_user, auth_backend, fastapi_users

app = FastAPI(
    title="Andreas Lagocki | DigitalArt",
)
app.include_router(fastapi_users.get_auth_router(auth_backend), tags=["Authentication"])
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), tags=["Authentication"]
)
app.include_router(fastapi_users.get_reset_password_router(), tags=["Authentication"])
app.include_router(fastapi_users.get_verify_router(UserRead), tags=["Authentication"])
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), tags=["User"], prefix="/users"
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/user/images", tags=["User"])
async def user_images_route(user: User = Depends(active_user)):
    return {"message", f"Alle Bilder von {user.username} mit {user.email}"}


@app.get("/user/images/{image_id}", tags=["User"])
async def user_image_route(image_id: int, user: User = Depends(active_user)):
    return {"message", f"Bild {image_id} von {user.username} mit {user.email}"}


@app.get("/images/all", tags=["Content"])
async def all_images_route(db: AsyncSession = Depends(get_async_session)):
    images : [Image] = await db.execute(select(Image).order_by(Image.upload))
    results = [list(row) for row in images]
    return {'results': results}


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
