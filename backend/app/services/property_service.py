"""
Property service for database operations
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from decimal import Decimal
from ..models.property import Property, PropertyType
from ..models.property_image import PropertyImage
from ..schemas.property import PropertySearchFilters


class PropertyService:
    """Service for property-related database operations"""

    @staticmethod
    def get_property_by_id(db: Session, property_id: int) -> Optional[Property]:
        """
        Get a single property by ID with images and landlord

        Args:
            db: Database session
            property_id: Property ID

        Returns:
            Property object or None
        """
        return (
            db.query(Property)
            .options(joinedload(Property.images), joinedload(Property.landlord))
            .filter(Property.id == property_id)
            .first()
        )

    @staticmethod
    def get_properties(
        db: Session,
        filters: PropertySearchFilters
    ) -> tuple[List[Property], int]:
        """
        Get properties with filters and pagination

        Args:
            db: Database session
            filters: Search filters

        Returns:
            Tuple of (list of properties, total count)
        """
        # Base query with images and landlord
        query = db.query(Property).options(joinedload(Property.images), joinedload(Property.landlord))

        # Apply filters
        if filters.area:
            query = query.filter(Property.area.ilike(f"%{filters.area}%"))

        if filters.property_type:
            query = query.filter(Property.property_type == filters.property_type)

        if filters.bedrooms is not None:
            query = query.filter(Property.bedrooms == filters.bedrooms)

        if filters.bathrooms is not None:
            query = query.filter(Property.bathrooms == filters.bathrooms)

        if filters.min_rent is not None:
            query = query.filter(Property.rent_price >= filters.min_rent)

        if filters.max_rent is not None:
            query = query.filter(Property.rent_price <= filters.max_rent)

        if filters.is_available is not None:
            query = query.filter(Property.is_available == filters.is_available)

        # Get total count before pagination
        total_count = query.count()

        # Apply pagination
        offset = (filters.page - 1) * filters.page_size
        properties = query.offset(offset).limit(filters.page_size).all()

        return properties, total_count

    @staticmethod
    def search_properties_by_area(
        db: Session,
        area: str,
        limit: int = 10
    ) -> List[Property]:
        """
        Simple search for properties by area (for AI context)

        Args:
            db: Database session
            area: Area name
            limit: Maximum number of results

        Returns:
            List of properties
        """
        return (
            db.query(Property)
            .options(joinedload(Property.images), joinedload(Property.landlord))
            .filter(Property.area.ilike(f"%{area}%"))
            .filter(Property.is_available == True)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_properties_context_for_ai(
        db: Session,
        area: Optional[str] = None,
        property_type: Optional[str] = None,
        min_rent: Optional[Decimal] = None,
        max_rent: Optional[Decimal] = None,
        bedrooms: Optional[int] = None,
        limit: int = 10
    ) -> List[dict]:
        """
        Get property data formatted for AI context

        Args:
            db: Database session
            area: Area filter
            property_type: Property type filter (apartment, house, duplex, room)
            min_rent: Minimum rent filter
            max_rent: Maximum rent filter
            bedrooms: Bedrooms filter
            limit: Maximum number of results

        Returns:
            List of property dictionaries with essential info
        """
        query = db.query(Property).options(joinedload(Property.images), joinedload(Property.landlord)).filter(Property.is_available == True)

        if area:
            query = query.filter(Property.area.ilike(f"%{area}%"))

        if property_type:
            # Convert string to PropertyType enum
            try:
                prop_type_enum = PropertyType[property_type.upper()]
                query = query.filter(Property.property_type == prop_type_enum)
            except KeyError:
                pass  # Invalid property type, skip filter

        if min_rent is not None:
            query = query.filter(Property.rent_price >= min_rent)

        if max_rent is not None:
            query = query.filter(Property.rent_price <= max_rent)

        if bedrooms is not None:
            query = query.filter(Property.bedrooms == bedrooms)

        properties = query.limit(limit).all()

        # Format for AI
        return [
            {
                "id": prop.id,
                "title": prop.title,
                "area": prop.area,
                "property_type": prop.property_type.value,
                "bedrooms": prop.bedrooms,
                "bathrooms": prop.bathrooms,
                "rent_price": float(prop.rent_price),
                "address": prop.address,
                "images": [{"image_url": img.image_url} for img in prop.images] if prop.images else [],
                "landlord": {
                    "full_name": prop.landlord.full_name,
                    "phone_number": prop.landlord.phone_number,
                    "email": prop.landlord.email
                } if prop.landlord else None,
            }
            for prop in properties
        ]
