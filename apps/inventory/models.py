from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from apps.dealers.models.brand import Brand
from apps.dealers.models.dealer import Dealer
from apps.dealers.models.hub import Hub
from base.models import BaseModel


class Inventory(BaseModel):
    __tablename__ = "inventories"

    dealer_id = Column(
        Integer,
        ForeignKey("dealers.id", ondelete="CASCADE"),
    )

    hub_id = Column(
        Integer,
        ForeignKey("hubs.id", ondelete="CASCADE"),
        nullable=False,
    )

    brand_id = Column(
        Integer,
        ForeignKey("brands.id", ondelete="CASCADE"),
        nullable=False,
    )

    filled_quantity = Column(
        Integer,
        default=0,
        nullable=False,
    )

    empty_quantity = Column(
        Integer,
        default=0,
        nullable=False,
    )

    reserved_quantity = Column(
        Integer,
        default=0,
        nullable=False,
    )

    damaged_quantity = Column(
        Integer,
        default=0,
        nullable=False,
    )

    low_stock_threshold = Column(
        Integer,
        default=10,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    # relationships
    hub = relationship(Hub, back_populates="inventories")
    brand = relationship(Brand, back_populates="inventories")
    dealer = relationship(Dealer, back_populates="inventories")
