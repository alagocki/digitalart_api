from pydantic import BaseModel


class CustomerAddressSchema(BaseModel):
    forename: str
    lastname: str
    street: str
    number: int
    city: str
    zip: int
    country: str
    phone: str
    customernr: int

    class Config:
        orm_mode = True


class CustomerAddressCreate(CustomerAddressSchema):
    pass


class CustomerAddressRead(CustomerAddressSchema):
    id: str


class CustomerAddressUpdate(CustomerAddressSchema):
    pass
