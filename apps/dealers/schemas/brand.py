from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class BrandBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    model_config = ConfigDict(from_attributes=True)
