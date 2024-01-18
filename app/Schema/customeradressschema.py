from __future__ import annotations

from pydantic import BaseModel


class CustomerAddressSchema(BaseModel):
    forename: str
    lastname: str
    street: str
    number: str
    city: str
    zip: int
    country: str
    phone: str
    customer_id: str

    class Config:
        orm_mode = True


class CustomerAddressCreate(CustomerAddressSchema):
    pass


class CustomerAddressRead(CustomerAddressSchema):
    id: str


class CustomerAddressUpdate(CustomerAddressSchema):
    pass
