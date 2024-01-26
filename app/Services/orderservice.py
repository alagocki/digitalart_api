from os.path import abspath
from pathlib import Path
from typing import List

from anyio.streams import file
from fastapi import Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.Classes.users import active_user
from app.Database.db import get_async_session
from app.Model.imagemodel import ImageModel
from app.Model.ordermodel import OrderModel
from app.Model.user import User
from app.Schema.orderschema import OrderCreate

from os.path import dirname, abspath, join

dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, 'CustomerFiles/')

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


async def upload_images(file_upload: UploadFile):
    # for file in files:
    global save_path
    try:
        data = await file_upload.read()
        save_path = images_path+file_upload.filename
        with open(save_path, 'wb') as f:
            f.write(data)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": Exception}
        )
    # finally:
    # file_upload.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Bild erfolgreich hochgeladen path: {save_path}"}
    )