from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from base.models import BaseModel


class Hub(BaseModel):
    __tablename__ = "hubs"

    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    dealer_id = Column(
        Integer, ForeignKey("dealers.id", ondelete="CASCADE"), nullable=False
    )

    # relationships

    dealer = relationship("Dealer", back_populates="hubs")
