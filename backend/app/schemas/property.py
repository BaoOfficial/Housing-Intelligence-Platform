"""
Pydantic schemas for Property-related requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class PropertyImageSchema(BaseModel):
    """Schema for property image"""
    id: int
    property_id: int
    image_url: str
    is_primary: bool
    uploaded_at: datetime

    class Config:
        from_attributes = True


class LandlordContactSchema(BaseModel):
    """Schema for landlord contact information"""
    full_name: str
    phone_number: Optional[str] = None
    email: str

    class Config:
        from_attributes = True


class PropertyBase(BaseModel):
    """Base property schema"""
    title: str
    description: Optional[str] = None
    area: str
    address: Optional[str] = None
    property_type: str
    bedrooms: int
    bathrooms: int
    rent_price: Decimal
    is_available: bool = True


class PropertyResponse(PropertyBase):
    """Schema for property response"""
    id: int
    landlord_id: Optional[int] = None
    landlord: Optional[LandlordContactSchema] = None  # Landlord contact info
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    images: List[PropertyImageSchema] = []

    class Config:
        from_attributes = True


class PropertyListResponse(BaseModel):
    """Schema for paginated property list"""
    properties: List[PropertyResponse]
    total: int
    page: int
    page_size: int


class PropertySearchFilters(BaseModel):
    """Schema for property search filters"""
    area: Optional[str] = None
    min_rent: Optional[Decimal] = Field(None, ge=0)
    max_rent: Optional[Decimal] = Field(None, ge=0)
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[int] = Field(None, ge=0)
    property_type: Optional[str] = None
    is_available: bool = True
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
