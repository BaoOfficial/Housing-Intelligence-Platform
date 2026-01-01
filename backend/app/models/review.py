"""
Review model for tenant experiences and feedback
"""
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Review(Base):
    """Review model"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True)
    contributor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    area = Column(String(100), index=True, nullable=False)
    rent_paid = Column(Numeric(12, 2), nullable=True)
    property_type = Column(String(50), nullable=True)
    review_text = Column(Text, nullable=False)
    pros = Column(Text, nullable=True)
    cons = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 rating
    is_anonymous = Column(Boolean, default=True, nullable=False)
    chromadb_id = Column(String(100), nullable=True)  # Reference to ChromaDB document
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    property = relationship("Property", back_populates="reviews")
    contributor = relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, area={self.area}, rating={self.rating})>"
