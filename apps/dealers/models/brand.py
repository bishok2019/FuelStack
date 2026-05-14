from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from base.models import BaseModel


class Brand(BaseModel):
    __tablename__ = "brands"

    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # relationships
    inventories = relationship("Inventory", back_populates="brand")
