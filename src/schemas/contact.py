from pydantic import BaseModel, Field, EmailStr
from datetime import date


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    second_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone_number: str = Field(min_length=6, max_length=21)
    birth_date: date  # YYYY-MM-DD


class ContactUpdate(ContactSchema):
    ...


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    second_name: str
    email: EmailStr
    phone_number: str
    birth_date: date

    class Config:
        from_attributes = True
