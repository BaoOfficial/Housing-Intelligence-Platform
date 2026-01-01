"""
Property model for housing listings
"""
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class PropertyType(str, enum.Enum):
    """Property type enumeration"""
    APARTMENT = "apartment"
    HOUSE = "house"
    DUPLEX = "duplex"
    ROOM = "room"


class Property(Base):
    """Property model"""
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    landlord_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    area = Column(String(100), index=True, nullable=False)  # e.g., "Lekki", "Ikeja"
    address = Column(String(500), nullable=True)
    property_type = Column(Enum(PropertyType), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    rent_price = Column(Numeric(12, 2), nullable=False)  # Annual rent in Naira
    is_available = Column(Boolean, default=True, nullable=False)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    landlord = relationship("User", back_populates="properties")
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="property")

    def __repr__(self):
        return f"<Property(id={self.id}, title={self.title}, area={self.area}, rent={self.rent_price})>"
