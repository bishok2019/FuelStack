from typing import Optional

from pydantic import BaseModel, ConfigDict


class InventoryBase(BaseModel):
    dealer_id: int
    hub_id: int
    brand_id: int
    filled_quantity: Optional[int] = 0
    empty_quantity: Optional[int] = 0
    reserved_quantity: Optional[int] = 0
    damaged_quantity: Optional[int] = 0
    low_stock_threshold: Optional[int] = 10
    is_active: Optional[bool] = True


class InventoryCreate(InventoryBase):
    pass  # Inherits all fields from InventoryBase


class InventoryUpdate(BaseModel):
    filled_quantity: Optional[int] = None
    empty_quantity: Optional[int] = None
    reserved_quantity: Optional[int] = None
    damaged_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    is_active: Optional[bool] = None


class InventoryList(InventoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class InventoryRetrieve(InventoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
