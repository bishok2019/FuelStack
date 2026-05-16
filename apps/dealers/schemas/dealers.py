from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from ..models import Dealer


class DealerBase(BaseModel):
    name: str
    code: str
    address: Optional[str] = None
    is_active: Optional[bool] = True
    brand_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)
