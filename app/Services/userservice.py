import json
from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.Classes.users import active_user
from app.Database.db import get_async_session
from app.Model.customeradressmodel import CustomerAdressModel
from app.Model.user import User
from app.Schema.customeradressschema import CustomerAddressCreate


async def get_all_customer(
    db: AsyncSession = Depends(get_async_session),
):
    users: [User] = await db.execute(
        select(
            User.id,
            User.email,
            User.customer,
            CustomerAdressModel.forename,
            CustomerAdressModel.lastname,
            CustomerAdressModel.street,
            CustomerAdressModel.number,
            CustomerAdressModel.city,
            CustomerAdressModel.zip,
        )
        .join(CustomerAdressModel)
        .where(User.customer != None)
        .where(User.is_verified == True)
    )
    results = [{row} for row in users]

    return {"data": results}


async def get_single_userdata_by_id(
    db: AsyncSession = Depends(get_async_session), user: User = Depends(active_user)
):
    userdata: [User] = await db.execute(
        select(
            User.id,
            User.email,
            User.customer,
            User.is_superuser,
            CustomerAdressModel.forename,
            CustomerAdressModel.lastname,
            CustomerAdressModel.street,
            CustomerAdressModel.number,
            CustomerAdressModel.city,
            CustomerAdressModel.zip,
        )
        .join(CustomerAdressModel, onclause=User.id == CustomerAdressModel.customer_id)
        .where(User.customer != None)
        .where(User.is_verified == True)
        .where(User.id == user.id)
    )
    result = userdata.first()
    # results = [{row} for row in userdata]
    return {"data": result}
