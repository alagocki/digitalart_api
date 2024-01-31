from os.path import abspath, dirname, join

from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from starlette.responses import JSONResponse

from app.Classes.users import active_user
from app.Database.db import get_async_session
from app.Model.customeradressmodel import CustomerAdressModel
from app.Model.imagemodel import ImageModel
from app.Model.ordermodel import OrderModel
from app.Model.user import User
from app.Schema.orderschema import OrderCreate
from app.Services.imageservice import get_images_by_order

dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, "CustomerFiles/")


async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
):
    new_order = OrderModel(
        topic=data.topic,
        owner_id=user.id,
        customer_id=data.customer_id,
        order_number=data.order_number,
        shooting_date=data.shooting_date,
        info=data.info,
        status=data.status,
    )
    db.add(new_order)

    for image in data.images:
        new_image = ImageModel(
            name=image.name,
            orders=new_order,
            description=image.description,
            status="unbearbeitet",
            ordered=image.ordered,
            base64encoded=image.base64encoded,
        )
        db.add(new_image)

    try:
        await db.commit()
    except Exception as e:
        print(e)
        raise {"error", f"Fehler beim speichern des Auftrags {e}"}
    finally:
        await db.close()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Auftrag erfolgreich angelegt"},
    )


async def get_all_order(
    db: AsyncSession = Depends(get_async_session),
):
    orders: [OrderModel] = await db.execute(
        select(
            OrderModel.id,
            OrderModel.topic,
            OrderModel.status,
            OrderModel.info,
            OrderModel.order_number,
            OrderModel.shooting_date,
            CustomerAdressModel.forename,
            CustomerAdressModel.lastname,
            count(ImageModel.id).label("image_count"),
        )
        .group_by(
            OrderModel.id,
            OrderModel.topic,
            OrderModel.status,
            OrderModel.info,
            OrderModel.order_number,
            CustomerAdressModel.forename,
            CustomerAdressModel.lastname,
        )
        .join(User, onclause=OrderModel.customer_id == User.id)
        .join(
            CustomerAdressModel,
            onclause=OrderModel.customer_id == CustomerAdressModel.customer_id,
        )
        .join(ImageModel, onclause=ImageModel.order_id == OrderModel.id)
        .where(User.customer is not None)
        .where(User.is_verified == True)
    )
    results = [{row} for row in orders]

    return {"data": results}


async def get_single_order_by_id(
    db: AsyncSession = Depends(get_async_session),
    order_id: str = None,
):
    order: [OrderModel] = await db.execute(
        select(
            OrderModel.id,
            OrderModel.topic,
            OrderModel.status,
            OrderModel.info,
            OrderModel.order_number,
            OrderModel.shooting_date,
            CustomerAdressModel.forename,
            CustomerAdressModel.lastname,
        )
        .join(User, onclause=OrderModel.customer_id == User.id)
        .join(
            CustomerAdressModel,
            onclause=OrderModel.customer_id == CustomerAdressModel.customer_id,
        )
        .where(User.customer is not None)
        .where(User.is_verified == True)
        .where(OrderModel.id == order_id)
    )
    result = order.all()

    images = await get_images_by_order(db, order_id)
    result.append(images)

    return {"order": result}
