from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from apps.database import Base
from base.models import BaseModel


class Customer(BaseModel):
    __tablename__ = "customers"
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    postal_code = Column(String(20), nullable=True)
    date_of_birth = Column(String(20), nullable=True)
    gender = Column(String(10), nullable=True)
    is_active = Column(Boolean, default=True)
    user = relationship("User", back_populates="customer_profile")
