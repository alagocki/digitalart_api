from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.Classes.users import active_user
from app.Database.db import get_async_session
from app.Model.imagemodel import ImageModel
from app.Model.ordermodel import OrderModel
from app.Model.user import User
from app.Schema.orderschema import OrderCreate


async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(active_user),
):

    new_order = OrderModel(
        topic=data.topic,
        owner_id=user.id,
        customer_id=data.customer_id,
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
            downloaded=image.downloaded,
            path=image.path,
        )
        db.add(new_image)

    try:
        await db.commit()
    except Exception as e:
        raise {"error", f"Fehler beim speichern des Auftrags {e}"}
    finally:
        await db.close()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Auftrag erfolgreich angelegt"},
    )
