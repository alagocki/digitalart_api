from fastapi import Depends, FastAPI

from app.db import User, create_db_and_tables
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


@app.get("/customer")
async def customer_route(user: User = Depends(active_user)):
    return {"message", f"Hallo von {user.username} mit {user.email}"}


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
