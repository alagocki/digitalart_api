from os.path import abspath, dirname, join

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.Database.db import get_async_session
from app.Model.imagemodel import ImageModel

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
        ).where(ImageModel.order_id == order_id)
    )
    results = [{row} for row in images]

    return results
