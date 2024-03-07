import json

from fastapi import Body, Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from app.Classes.users import active_user, auth_backend, fastapi_users
from app.Database.db import create_db_and_tables, get_async_session
from app.Model.imagemodel import ImageModel
from app.Model.user import User
from app.Schema.customeradressschema import CustomerAddressCreate
from app.Schema.imageschema import ImageSchema, ImageToOrder, ImageUploadData
from app.Schema.orderschema import OrderCreate
from app.Schema.user import UserCreate, UserRead, UserUpdate
from app.Services.adressservice import create_customer_address
from app.Services.imageservice import create_images, delete_image, image_to_order
from app.Services.orderservice import (
    create_order,
    get_all_order,
    get_order_images,
    get_orders_by_user_id,
    get_single_order_by_id,
    update_order_data_images_delete,
)
from app.Services.userservice import get_all_customer, get_single_userdata_by_id

app = FastAPI(
    title="Andreas Lagocki | DigitalArt",
    description="This is the backend for the Andreas Lagocki | DigitalArt website",
    version="1.0.0",
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

origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/images/all", tags=["Images"])
async def all_images_route(db: AsyncSession = Depends(get_async_session)):
    images: [ImageModel] = await db.execute(
        select(ImageModel).order_by(ImageModel.upload)
    )
    results = [row.ImageModel for row in images]
    return {"images": results}


@app.post("/images/create", tags=["Images"])
async def create_images_route(
    images: ImageUploadData,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
):
    jsonData = json.loads(images.data)
    await create_images(jsonData, db)


@app.post("/image/assign/order", tags=["Images"])
async def add_order_image(
    data: ImageToOrder,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
):
    return await image_to_order(data, db)


@app.delete("/image/delete/{image_id}/{order_id}", tags=["Images"])
async def delete_image_route(
    image_id: str,
    order_id: str,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
):
    await delete_image(image_id, db)
    await update_order_data_images_delete(order_id, db, user)
    return {"message": f"Image {image_id} deleted from order successfully"}


@app.get("/user/images", tags=["User"])
async def user_images_route(user: User = Depends(active_user)):
    return {"message", f"Alle Bilder von {user.username} mit {user.email}"}


@app.get("/user/images/{image_id}", tags=["User"])
async def user_image_route(image_id: int, user: User = Depends(active_user)):
    return {"message", f"Bild {image_id} von {user.username} mit {user.email}"}


@app.post("/user/adress", tags=["User"])
async def user_adress_route(
    data: CustomerAddressCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
):
    return await create_customer_address(data, db, user)


@app.get("/user/all", tags=["User"])
async def all_users_route(
    db: AsyncSession = Depends(get_async_session), user: User = Depends(active_user)
):
    return await get_all_customer(db)


@app.get(
    "/user/single", tags=["User"], description="Returns all data from the current user"
)
async def user_data_route(
    db: AsyncSession = Depends(get_async_session), user: User = Depends(active_user)
):
    return await get_single_userdata_by_id(db, user)


@app.post("/order/create", tags=["Orders"])
async def create_order_route(
    data: OrderCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
):
    return await create_order(data, db, user)


@app.post("/order/update/{order_id}", tags=["Orders"])
async def update_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
    order_id: str = None,
):
    pass
    # return await update_order_data(data, db, user, order_id)


@app.get("/order/all", tags=["Orders"])
async def all_orders_route(
    db: AsyncSession = Depends(get_async_session), user: User = Depends(active_user)
):
    return await get_all_order(db)


@app.get("/order/images/{order_id}", tags=["Orders"])
async def order_images(
    db: AsyncSession = Depends(get_async_session),
    order_id: str = None,
    user: User = Depends(active_user),
):
    return await get_order_images(db, order_id)


@app.get("/order/{order_id}", tags=["Orders"])
async def all_orders_route(
    order_id: str,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
):
    return await get_single_order_by_id(db, order_id)


@app.get("/order/user/{user_id}", tags=["Orders"])
async def all_orders_by_user_route(
    user_id: str,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
):
    return await get_orders_by_user_id(db, user_id)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    print("Database created")
