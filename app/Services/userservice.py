import json
from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.Classes.users import active_user
from app.Database.db import get_async_session
from app.Model.customeraddressmodel import CustomerAddressModel
from app.Model.user import User
from app.Schema.customeradressschema import CustomerAddressCreate


async def get_all_customer(
        db: AsyncSession = Depends(get_async_session),
):
    users: [User] = await db.execute(
        select(User.id, User.email, User.customer, CustomerAddressModel.forename, CustomerAddressModel.lastname, CustomerAddressModel.street, CustomerAddressModel.number, CustomerAddressModel.city, CustomerAddressModel.zip)
        .join(CustomerAddressModel)
        .where(User.customer != None)
        .where(User.is_verified == True))
    results = [{row} for row in users]

    return {"users": results}
