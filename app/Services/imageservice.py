from os.path import abspath, dirname, join

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from starlette import status
from starlette.responses import JSONResponse

from app.Classes.users import active_user
from app.Database.db import get_async_session
from app.Model.imagemodel import ImageModel
from app.Model.ordermodel import OrderModel
from app.Model.user import User
from app.Schema.imageschema import ImageSchema

dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, "CustomerFiles/")


async def get_images_by_order(
        db: AsyncSession = Depends(get_async_session),
        order_id: str = None,
):
    images: [ImageModel] = await db.execute(
        select(
            ImageModel.id,
            ImageModel.name,
            ImageModel.description,
            ImageModel.status,
            ImageModel.ordered,
            ImageModel.base64encoded,
            ImageModel.blocked,
            ImageModel.file_extension
        ).where(ImageModel.order_id == order_id)
        .order_by(ImageModel.upload)
    )
    results = [{row} for row in images]

    return results


async def count_images_order(
        order_id: str, db: AsyncSession = Depends(get_async_session)
):
    image_count: [ImageModel] = await db.execute(
        select(count(ImageModel.id).label("image_count")).where(
            ImageModel.order_id == order_id
        )
    )
    result = image_count.scalar_one()

    return {result}


async def create_images(
        images: [ImageSchema],
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(active_user),
        order_id: str = None,
):
    order = await db.execute(select(OrderModel).where(OrderModel.id == order_id))
    order = order.scalar_one()

    if not order:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Order not found"},
        )

    for image in images:
        new_image = ImageModel(
            name=image.name,
            orders=order,
            description=image.description,
            status=str("unbearbeitet"),
            ordered=image.ordered,
            base64encoded=image.base64encoded,
            blocked=image.blocked,
            file_extension=image.file_extension
        )
        db.add(new_image)

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


async def create_image(
        image: ImageSchema,
        db: AsyncSession = Depends(get_async_session),
        order_id: str = None,
):
    order = await db.execute(select(OrderModel).where(OrderModel.id == order_id))
    order = order.scalar_one()

    if not order:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Order not found"},
        )

    new_image = ImageModel(
        name=image.name,
        orders=order,
        description=image.description,
        status=str("unbearbeitet"),
        ordered=image.ordered,
        base64encoded=image.base64encoded,
        blocked=image.blocked,
        file_extension=image.file_extension
    )
    db.add(new_image)

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


async def get_order(
        order_id: str,
        db: AsyncSession = Depends(get_async_session)
):
    order = await db.execute(select(OrderModel).where(OrderModel.id == order_id))
    order = order.scalar_one()

    if not order:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Order not found"},
        )

    return order


async def delete_image(
        image_id: str,
        db: AsyncSession = Depends(get_async_session)
):
    image = await db.execute(select(ImageModel).where(ImageModel.id == image_id))
    image = image.scalar_one()

    if not image:
        raise HTTPException(status_code=404, detail="Images not found")

    await db.delete(image)
    await db.commit()
    return {"ok": True}
