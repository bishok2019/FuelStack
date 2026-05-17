from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerCreate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
