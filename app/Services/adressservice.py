from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.Classes.users import active_user
from app.Database.db import get_async_session
from app.Model.customeradressmodel import CustomerAdressModel
from app.Model.user import User
from app.Schema.customeradressschema import CustomerAddressCreate


async def create_customer_address(
    data: CustomerAddressCreate,
    db: AsyncSession = Depends(get_async_session),
    customer: User = Depends(active_user),
):
    # customer = await db.execute(select(User).where(User.customer == data.customernr))
    # customer_id_db = customer.first()[0].id

    # if not customer:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Kunde mit der Nummer {data.customernr} nicht gefunden",
    #     )

    new_adress = CustomerAdressModel(
        forename=data.forename,
        lastname=data.lastname,
        street=data.street,
        number=data.number,
        city=data.city,
        zip=data.zip,
        country=data.country,
        phone=data.phone,
        customer_id=data.customer_id,
    )

    db.add(new_adress)

    try:
        await db.commit()
    except Exception as e:
        raise {"error", f"Fehler beim speichern des Auftrags {e}"}
    finally:
        await db.close()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Adresse erfolgreich angelegt"},
    )
