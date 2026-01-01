"""
Script to populate property images with a large, diverse pool of images
Each property gets 3-5 images (exterior + interior shots)
"""
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.property import Property
from app.models.property_image import PropertyImage

# Large pool of curated Unsplash images organized by property type and room type
IMAGE_POOLS = {
    'apartment': {
        'exterior': [
            'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800',  # Modern building
            'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800',  # Apartment complex
            'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800',  # City apartment
            'https://images.unsplash.com/photo-1515263487990-61b07816b324?w=800',  # High rise
            'https://images.unsplash.com/photo-1460317442991-0ec209397118?w=800',  # Balcony view
            'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800',  # Modern exterior
            'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800',  # Glass building
            'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800',  # Urban apartment
        ],
        'living_room': [
            'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800',  # Cozy living room
            'https://images.unsplash.com/photo-1567016432779-094069958ea5?w=800',  # Modern living
            'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800',  # Bright living
            'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800',  # Sofa area
            'https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800',  # Contemporary
            'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=800',  # Minimalist
            'https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800',  # Spacious
            'https://images.unsplash.com/photo-1505693314120-0d443867891c?w=800',  # Elegant
        ],
        'kitchen': [
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800',  # Modern kitchen
            'https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800',  # White kitchen
            'https://images.unsplash.com/photo-1565538810643-b5bdb714032a?w=800',  # Contemporary
            'https://images.unsplash.com/photo-1556912167-f556f1f39fdf?w=800',  # Bright kitchen
            'https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=800',  # Elegant
            'https://images.unsplash.com/photo-1600489000022-c2086d79f9d4?w=800',  # Spacious
        ],
        'bedroom': [
            'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800',  # Modern bedroom
            'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800',  # Cozy bed
            'https://images.unsplash.com/photo-1615529328331-f8917597711f?w=800',  # Bright bedroom
            'https://images.unsplash.com/photo-1616137466211-f939a420be84?w=800',  # Minimalist
            'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800',  # Contemporary
            'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800',  # Elegant
        ],
        'bathroom': [
            'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800',  # Modern bathroom
            'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800',  # Luxury bath
            'https://images.unsplash.com/photo-1629079447777-1e605162dc87?w=800',  # Contemporary
            'https://images.unsplash.com/photo-1604709177225-055f99402ea3?w=800',  # Bright bathroom
        ],
    },
    'house': {
        'exterior': [
            'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800',  # Modern house
            'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800',  # Family house
            'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800',  # Beautiful house
            'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800',  # Contemporary
            'https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?w=800',  # Suburban
            'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800',  # White house
            'https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=800',  # Modern exterior
            'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800',  # Villa
        ],
        'living_room': [
            'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800',  # Spacious living
            'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800',  # Elegant
            'https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=800',  # Cozy
            'https://images.unsplash.com/photo-1600121848594-d8644e57abab?w=800',  # Modern
            'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800',  # Bright
            'https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800',  # Contemporary
        ],
        'kitchen': [
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800',  # Modern kitchen
            'https://images.unsplash.com/photo-1600489000022-c2086d79f9d4?w=800',  # Spacious
            'https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800',  # White kitchen
            'https://images.unsplash.com/photo-1600573472591-ee6b68d14c68?w=800',  # Island kitchen
        ],
        'bedroom': [
            'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800',  # Master bedroom
            'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800',  # Spacious bed
            'https://images.unsplash.com/photo-1615529328331-f8917597711f?w=800',  # Bright
            'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800',  # Elegant
        ],
    },
    'duplex': {
        'exterior': [
            'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800',  # Modern duplex
            'https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800',  # Luxury duplex
            'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800',  # Contemporary
            'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800',  # Modern exterior
            'https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?w=800',  # Suburban
            'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800',  # Upscale
        ],
        'living_room': [
            'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800',  # Double height
            'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800',  # Spacious
            'https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=800',  # Elegant
            'https://images.unsplash.com/photo-1600121848594-d8644e57abab?w=800',  # Modern
        ],
        'kitchen': [
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800',  # Modern
            'https://images.unsplash.com/photo-1600489000022-c2086d79f9d4?w=800',  # Spacious
            'https://images.unsplash.com/photo-1600573472591-ee6b68d14c68?w=800',  # Island
        ],
        'bedroom': [
            'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800',  # Master
            'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800',  # Spacious
            'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800',  # Elegant
        ],
    },
    'room': {
        'bedroom': [
            'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800',  # Single room
            'https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800',  # Bedroom
            'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800',  # Cozy room
            'https://images.unsplash.com/photo-1615529328331-f8917597711f?w=800',  # Bright room
            'https://images.unsplash.com/photo-1616137466211-f939a420be84?w=800',  # Minimalist
            'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800',  # Contemporary
        ],
        'interior': [
            'https://images.unsplash.com/photo-1566195992011-5f6b21e539aa?w=800',  # Study area
            'https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=800',  # Workspace
            'https://images.unsplash.com/photo-1600121848594-d8644e57abab?w=800',  # Interior
        ],
    }
}


def get_random_images_for_property(property_type: str, num_images: int = 4) -> list:
    """
    Get random images for a property, mixing different room types

    Args:
        property_type: Type of property (apartment, house, duplex, room)
        num_images: Number of images to return (default 4)

    Returns:
        List of image URLs
    """
    pool = IMAGE_POOLS.get(property_type, IMAGE_POOLS['apartment'])

    images = []

    # For non-room properties, mix exterior and interior shots
    if property_type in ['apartment', 'house', 'duplex']:
        # Always start with an exterior shot
        if 'exterior' in pool and pool['exterior']:
            images.append(random.choice(pool['exterior']))

        # Add interior shots (living room, kitchen, bedroom, bathroom)
        interior_types = [k for k in pool.keys() if k != 'exterior']
        random.shuffle(interior_types)

        for room_type in interior_types:
            if len(images) >= num_images:
                break
            if pool[room_type]:
                images.append(random.choice(pool[room_type]))
    else:
        # For rooms, just pick random bedroom/interior shots
        all_images = []
        for room_type in pool.keys():
            all_images.extend(pool[room_type])

        random.shuffle(all_images)
        images = all_images[:num_images]

    # Ensure we have the requested number of images
    while len(images) < num_images and images:
        images.append(random.choice(images))

    return images[:num_images]


def update_all_property_images():
    """Update all properties with diverse, realistic images"""
    db = SessionLocal()

    try:
        # Get all properties
        properties = db.query(Property).all()
        print(f"Updating images for {len(properties)} properties...")

        # Delete all existing images
        db.query(PropertyImage).delete()
        db.commit()
        print("Cleared all existing images")

        # Add new images for each property
        total_images = 0
        for prop in properties:
            prop_type = prop.property_type.value.lower()

            # Get 3-5 random images for this property
            num_images = random.randint(3, 5)
            image_urls = get_random_images_for_property(prop_type, num_images)

            # Create PropertyImage records
            for idx, url in enumerate(image_urls):
                image = PropertyImage(
                    property_id=prop.id,
                    image_url=url,
                    is_primary=(idx == 0)  # First image is primary
                )
                db.add(image)
                total_images += 1

        db.commit()
        print(f"✅ Successfully added {total_images} images to {len(properties)} properties!")
        print(f"📊 Average: {total_images / len(properties):.1f} images per property")

        # Show sample
        print("\n📸 Sample property images:")
        sample_props = properties[:3]
        for prop in sample_props:
            images = db.query(PropertyImage).filter(PropertyImage.property_id == prop.id).all()
            print(f"\n{prop.title} ({prop.property_type.value}):")
            print(f"  - {len(images)} images")
            for img in images:
                print(f"    • {img.image_url[:60]}...")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🏠 Property Image Updater")
    print("=" * 50)
    update_all_property_images()
