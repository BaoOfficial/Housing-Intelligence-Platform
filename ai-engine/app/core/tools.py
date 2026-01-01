"""
LangChain tools for the ReAct agent
These tools allow the agent to search properties and reviews
"""
from langchain_core.tools import tool
from typing import Optional
import httpx
from .vector_db import vector_db
from ..config import settings


@tool
def search_properties(
    area: Optional[str] = None,
    property_type: Optional[str] = None,
    bedrooms: Optional[int] = None,
    min_rent: Optional[int] = None,
    max_rent: Optional[int] = None,
    limit: int = 10
) -> str:
    """
    Search for available rental properties in Lagos, Nigeria.

    Use this tool when the user asks about finding properties, homes, apartments,
    houses, duplexes, or rooms for rent.

    Args:
        area: Area/neighborhood in Lagos (e.g., "Lekki", "Ikeja", "Victoria Island", "Yaba")
        property_type: Type of property - must be one of: "apartment", "house", "duplex", "room"
        bedrooms: Number of bedrooms (e.g., 1, 2, 3, 4)
        min_rent: Minimum annual rent in Nigerian Naira (e.g., 500000 for ₦500k)
        max_rent: Maximum annual rent in Nigerian Naira (e.g., 2000000 for ₦2M)
        limit: Maximum number of results to return (default: 10)

    Returns:
        Formatted string with matching properties including title, area, price, bedrooms, bathrooms
    """
    try:
        # Build query parameters
        params = {
            "is_available": True,
            "page_size": limit
        }

        if area:
            params["area"] = area
        if property_type:
            params["property_type"] = property_type.lower()
        if bedrooms is not None:
            params["bedrooms"] = bedrooms
        if min_rent is not None:
            params["min_rent"] = min_rent
        if max_rent is not None:
            params["max_rent"] = max_rent

        # Call backend API
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                f"{settings.BACKEND_URL}/api/v1/properties",
                params=params
            )
            response.raise_for_status()
            data = response.json()

        properties = data.get("properties", [])

        if not properties:
            filter_desc = []
            if property_type:
                filter_desc.append(f"{property_type}s")
            if area:
                filter_desc.append(f"in {area}")
            if bedrooms:
                filter_desc.append(f"with {bedrooms} bedrooms")
            if max_rent:
                filter_desc.append(f"under ₦{max_rent:,.0f}")

            filters = " ".join(filter_desc) if filter_desc else "matching your criteria"
            return f"No properties found {filters}. Try adjusting your search criteria."

        # Format results for AI
        formatted_properties = []
        for i, prop in enumerate(properties, 1):
            prop_type = prop.get("property_type", "Property")
            title = prop.get("title", "Untitled")
            prop_area = prop.get("area", "Unknown")
            price = float(prop.get("rent_price", 0))  # Convert string to float
            beds = prop.get("bedrooms", 0)
            baths = prop.get("bathrooms", 0)

            formatted_properties.append(
                f"{i}. {title}\n"
                f"   Type: {prop_type} | Area: {prop_area}\n"
                f"   Bedrooms: {beds} | Bathrooms: {baths}\n"
                f"   Annual Rent: ₦{price:,.0f}\n"
            )

        result = f"Found {len(properties)} properties:\n\n" + "\n".join(formatted_properties)

        if len(properties) >= limit:
            result += f"\n\n(Showing first {limit} results. There may be more available.)"

        return result

    except httpx.HTTPError as e:
        error_msg = f"HTTP Error: {type(e).__name__}: {str(e)}"
        print(f"🔴 search_properties HTTP error: {error_msg}")
        return f"Error connecting to property database: {error_msg}"
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"🔴 search_properties error: {error_msg}")
        import traceback
        traceback.print_exc()
        return f"Error searching properties: {error_msg}"


@tool
def search_tenant_reviews(
    query: str,
    area: Optional[str] = None,
    n_results: int = 5
) -> str:
    """
    Search tenant reviews and experiences about living in different areas of Lagos.

    Use this tool when the user asks about:
    - What people say about an area
    - Tenant experiences
    - Issues like power supply, water, security, noise, landlord behavior
    - Pros and cons of living somewhere

    Args:
        query: What to search for (e.g., "power supply issues", "security in Lekki")
        area: Specific area to filter by (e.g., "Lekki", "Ikeja")
        n_results: Number of reviews to return (default: 5)

    Returns:
        Formatted string with relevant tenant reviews
    """
    try:
        # Generate embedding for the query
        from ..services.embedding_service import embedding_service
        query_embedding = embedding_service.embed_text(query)

        # Build metadata filter
        where_filter = None
        if area:
            where_filter = {"area": {"$eq": area}}

        # Query ChromaDB
        results = vector_db.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )

        # Format results
        if not results or not results.get('documents') or not results['documents'][0]:
            return f"No reviews found for query: '{query}'" + (f" in {area}" if area else "")

        documents = results['documents'][0]
        metadatas = results['metadatas'][0] if results.get('metadatas') else []
        distances = results['distances'][0] if results.get('distances') else []

        formatted_reviews = []
        for i, doc in enumerate(documents):
            metadata = metadatas[i] if i < len(metadatas) else {}
            relevance = 1 - distances[i] if i < len(distances) else 0

            review_area = metadata.get("area", "Unknown")
            rating = metadata.get("rating", "N/A")
            rent = metadata.get("rent_paid", "N/A")

            formatted_reviews.append(
                f"Review {i+1} (Area: {review_area}, Rating: {rating}/5, Rent: ₦{rent:,.0f}):\n{doc}\n"
            )

        return "\n".join(formatted_reviews)

    except Exception as e:
        return f"Error searching reviews: {str(e)}"


@tool
def get_area_statistics(area: str) -> str:
    """
    Get statistical summary of reviews for a specific area.

    Use this tool when the user asks about general information about an area,
    or wants a summary of what people say about living there.

    Args:
        area: The area name (e.g., "Lekki", "Ikeja", "Victoria Island")

    Returns:
        Statistical summary of reviews for that area
    """
    try:
        from ..services.embedding_service import embedding_service

        # Search for general reviews about the area
        query = f"living in {area}"
        query_embedding = embedding_service.embed_text(query)

        results = vector_db.query(
            query_embeddings=[query_embedding],
            n_results=20,  # Get more for statistics
            where={"area": {"$eq": area}}
        )

        if not results or not results.get('metadatas') or not results['metadatas'][0]:
            return f"No data available for {area}"

        metadatas = results['metadatas'][0]

        # Calculate statistics
        total_reviews = len(metadatas)
        ratings = [m.get("rating", 0) for m in metadatas if m.get("rating")]
        rents = [m.get("rent_paid", 0) for m in metadatas if m.get("rent_paid")]

        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        avg_rent = sum(rents) / len(rents) if rents else 0
        min_rent = min(rents) if rents else 0
        max_rent = max(rents) if rents else 0

        # Also include actual review text for the agent to analyze
        documents = results['documents'][0] if results.get('documents') else []

        summary = f"""
Statistics for {area}:
- Total Reviews: {total_reviews}
- Average Rating: {avg_rating:.1f}/5
- Average Rent: ₦{avg_rent:,.0f}
- Rent Range: ₦{min_rent:,.0f} - ₦{max_rent:,.0f}

Sample Reviews (most relevant):
"""
        # Add top 10 reviews for context
        for i, doc in enumerate(documents[:10], 1):
            metadata = metadatas[i-1] if i-1 < len(metadatas) else {}
            rating = metadata.get("rating", "N/A")
            summary += f"\n{i}. [Rating: {rating}/5] {doc[:400]}...\n"

        return summary.strip()

    except Exception as e:
        return f"Error getting statistics for {area}: {str(e)}"


@tool
def compare_areas(area1: str, area2: str) -> str:
    """
    Compare two areas based on tenant reviews.

    Use this tool when the user wants to compare two different areas
    (e.g., "Compare Lekki and Ikeja")

    Args:
        area1: First area name
        area2: Second area name

    Returns:
        Comparison of the two areas based on reviews
    """
    try:
        stats1 = get_area_statistics(area1)
        stats2 = get_area_statistics(area2)

        comparison = f"""
Comparison between {area1} and {area2}:

{area1}:
{stats1}

{area2}:
{stats2}
"""
        return comparison.strip()

    except Exception as e:
        return f"Error comparing areas: {str(e)}"


# Export all tools
AGENT_TOOLS = [
    search_properties,
    search_tenant_reviews,
    get_area_statistics,
    compare_areas,
]
