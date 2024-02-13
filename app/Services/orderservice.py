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
from app.Services.imageservice import create_images, get_images_by_order, count_images_order, create_image

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
        status=str(data.status),
        basic_price=data.basic_price,
        additional_pic_price=data.additional_pic_price,
        condition=data.condition,
        images_cnt=data.images_cnt,
        include_media=data.include_media,
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


async def update_order_data(
        data: OrderCreate,
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(active_user),
        order_id: str = None,
):
    order_query = await db.execute(select(OrderModel).where(OrderModel.id == order_id))
    order = order_query.scalar_one()

    # exist_image_cnt = order.images_cnt if order.images_cnt else 0
    for key, value in data.dict().items():
        if key == "images_cnt":
            setattr(order, key, value) if value else None

    if data.images is not None:

        for image in data.images:
            image_in_db_query = await db.execute(
                select(ImageModel).where(ImageModel.name == image.name and ImageModel.order_id == order_id))
            image_in_db = image_in_db_query.scalar_one_or_none()
            if image_in_db:
                for key, value in image.dict().items():
                    setattr(image_in_db, key, value)
            else:
                await create_image(image, db, order_id)

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


async def update_order_data_images_delete(
        order_id: str,
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(active_user),
):
    order = await db.execute(select(OrderModel).where(OrderModel.id == order_id))
    order = order.scalar_one()

    img_cnt = await count_images_order(order_id, db)
    setattr(order, "images_cnt", list(img_cnt)[0]) if img_cnt else None

    try:
        await db.commit()
    except Exception as e:
        print(e)
        raise {"error", f"Error when saving the order {e}"}
    finally:
        await db.close()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Imagedata successfully updated"},
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
            OrderModel.additional_pic_price,
            OrderModel.basic_price,
            OrderModel.include_media,
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
            OrderModel.basic_price,
            OrderModel.condition,
            OrderModel.customer_id,
            OrderModel.images_cnt,
            OrderModel.additional_pic_price,
            OrderModel.include_media,
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
