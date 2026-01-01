"""
PropertyImage model for property photos
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class PropertyImage(Base):
    """PropertyImage model"""
    __tablename__ = "property_images"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    image_url = Column(String(500), nullable=False)  # Cloudinary URL
    is_primary = Column(Boolean, default=False, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    property = relationship("Property", back_populates="images")

    def __repr__(self):
        return f"<PropertyImage(id={self.id}, property_id={self.property_id}, is_primary={self.is_primary})>"
