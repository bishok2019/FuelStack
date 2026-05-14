from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from base.models import BaseModel


class Dealer(BaseModel):
    __tablename__ = "dealers"

    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    address = Column(String(255), nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # relationships
    hubs = relationship("Hub", back_populates="dealer", cascade="all, delete-orphan")
    inventories = relationship(
        "Inventory", back_populates="dealer", cascade="all, delete-orphan"
    )
