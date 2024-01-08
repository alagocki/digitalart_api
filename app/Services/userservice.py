import json

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.Classes.users import active_user
from app.Database.db import get_async_session
from app.Model.customeraddressmodel import CustomerAddressModel
from app.Model.user import User
from app.Schema.customeradressschema import CustomerAddressCreate


async def get_all_use(
        db: AsyncSession = Depends(get_async_session),
):
    users: [User] = await db.execute(select(User))
    results = [{row.User.id, row.User.email, row.User.customer} for row in users]

    return results
