from os.path import abspath, dirname, join

from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.Classes.users import active_user
from app.Database.db import get_async_session
from app.Model.customeradressmodel import CustomerAdressModel
from app.Model.imagemodel import ImageModel
from app.Model.ordermodel import OrderModel
from app.Model.user import User
from app.Schema.orderschema import OrderCreate
from app.Services.imageservice import create_images, get_images_by_order

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
        price=data.price,
        condition=data.condition,
        images_cnt=data.images_cnt,
    )
    db.add(new_order)

    if data.images is not None:
        lastOrder = await db.execute(
            select(OrderModel).where(OrderModel.order_number == data.order_number)
        )
        lastOrderData = lastOrder.scalar_one()

        await create_images(data.images, db, user, lastOrderData.id)

    try:
        await db.commit()
    except Exception as e:
        print(e)
        raise {"error", f"Error when saving the order {e}"}
    finally:
        await db.close()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Order successfully created"},
    )


async def update_order_images(
    data: OrderCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
    order_id: str = None,
):
    order = await db.execute(select(OrderModel).where(OrderModel.id == order_id))
    order = order.scalar_one()

    exist_image_cnt = order.images_cnt if order.images_cnt else 0
    for key, value in data.dict().items():
        if key == "images_cnt":
            setattr(order, key, exist_image_cnt + value) if value else None

    if data.images is not None:
        await create_images(data.images, db, user, order_id)

    try:
        await db.commit()
    except Exception as e:
        print(e)
        raise {"error", f"Error when saving the order {e}"}
    finally:
        await db.close()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Order successfully created"},
    )


async def get_all_order(
    db: AsyncSession = Depends(get_async_session),
):
    global images_cnt
    orders: [OrderModel] = await db.execute(
        select(
            OrderModel.id,
            OrderModel.topic,
            OrderModel.status,
            OrderModel.info,
            OrderModel.order_number,
            OrderModel.shooting_date,
            OrderModel.images_cnt,
            CustomerAdressModel.forename,
            CustomerAdressModel.lastname,
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
            OrderModel.price,
            OrderModel.condition,
            OrderModel.customer_id,
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
