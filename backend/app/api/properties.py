"""
Properties API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal

from ..database import get_db
from ..schemas.property import (
    PropertyResponse,
    PropertyListResponse,
    PropertySearchFilters
)
from ..services.property_service import PropertyService

router = APIRouter()


@router.get("", response_model=PropertyListResponse)
async def get_properties(
    area: Optional[str] = Query(None, description="Filter by area (e.g., Lekki, Ikeja)"),
    min_rent: Optional[Decimal] = Query(None, ge=0, description="Minimum rent price"),
    max_rent: Optional[Decimal] = Query(None, ge=0, description="Maximum rent price"),
    bedrooms: Optional[int] = Query(None, ge=0, description="Number of bedrooms"),
    bathrooms: Optional[int] = Query(None, ge=0, description="Number of bathrooms"),
    property_type: Optional[str] = Query(None, description="Property type (apartment, house, duplex, room)"),
    is_available: bool = Query(True, description="Filter by availability"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get list of properties with filtering and pagination

    Query Parameters:
    - area: Filter by area name (case-insensitive partial match)
    - min_rent: Minimum annual rent in Naira
    - max_rent: Maximum annual rent in Naira
    - bedrooms: Number of bedrooms
    - bathrooms: Number of bathrooms
    - property_type: Type of property
    - is_available: Only show available properties (default: true)
    - page: Page number (default: 1)
    - page_size: Items per page (default: 20, max: 100)
    """
    try:
        # Create filters object
        filters = PropertySearchFilters(
            area=area,
            min_rent=min_rent,
            max_rent=max_rent,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            property_type=property_type,
            is_available=is_available,
            page=page,
            page_size=page_size
        )

        # Get properties from database
        properties, total = PropertyService.get_properties(db, filters)

        return PropertyListResponse(
            properties=properties,
            total=total,
            page=page,
            page_size=page_size
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching properties: {str(e)}"
        )


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property_by_id(
    property_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single property by ID

    Returns full property details including images
    """
    try:
        property_obj = PropertyService.get_property_by_id(db, property_id)

        if not property_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Property with ID {property_id} not found"
            )

        return property_obj

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching property: {str(e)}"
        )
