"""
Database seeding script
Populates database with dummy property and review data for Lagos
"""
import sys
from pathlib import Path
import random
from decimal import Decimal

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Property, PropertyType, PropertyImage, Review, User, UserRole

# Pre-computed bcrypt hash for "password123"
# This avoids runtime bcrypt issues during seeding
DEFAULT_PASSWORD_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS7sFJ6FS"

# Lagos areas with typical characteristics
LAGOS_AREAS = {
    "Lekki": {"rent_range": (800000, 5000000), "coords": (6.4474, 3.5528)},
    "Ikeja": {"rent_range": (400000, 2500000), "coords": (6.6018, 3.3515)},
    "Victoria Island": {"rent_range": (1500000, 8000000), "coords": (6.4281, 3.4219)},
    "Yaba": {"rent_range": (300000, 1500000), "coords": (6.5074, 3.3719)},
    "Surulere": {"rent_range": (350000, 1800000), "coords": (6.4969, 3.3537)},
    "Ikoyi": {"rent_range": (2000000, 10000000), "coords": (6.4550, 3.4284)},
    "Ajah": {"rent_range": (400000, 2000000), "coords": (6.4698, 3.5699)},
    "Gbagada": {"rent_range": (350000, 1600000), "coords": (6.5426, 3.3840)},
    "Maryland": {"rent_range": (400000, 2200000), "coords": (6.5729, 3.3633)},
    "Festac": {"rent_range": (350000, 1400000), "coords": (6.4667, 3.2833)},
}

# Property title templates
PROPERTY_TITLES = {
    PropertyType.APARTMENT: [
        "Modern {} Bedroom Apartment in {}",
        "Spacious {} Bedroom Flat in {}",
        "Luxury {} Bedroom Apartment - {}",
        "Well-Finished {} Bedroom Flat in {}",
        "Serviced {} Bedroom Apartment in {}",
    ],
    PropertyType.HOUSE: [
        "{} Bedroom Detached House in {}",
        "Beautiful {} Bedroom Bungalow - {}",
        "Executive {} Bedroom House in {}",
        "{} Bedroom Family Home - {}",
        "Standalone {} Bedroom House in {}",
    ],
    PropertyType.DUPLEX: [
        "Luxury {} Bedroom Duplex in {}",
        "Executive {} Bedroom Duplex - {}",
        "Modern {} Bedroom Duplex in {}",
        "Fully Detached {} Bedroom Duplex - {}",
        "Tastefully Finished {} Bedroom Duplex in {}",
    ],
    PropertyType.ROOM: [
        "Self-Contained Room in {}",
        "Spacious Single Room in {}",
        "Well-Furnished Room - {}",
        "Comfortable Room in Shared Apartment - {}",
        "Self-Con with Kitchen in {}",
    ],
}

# Property descriptions
PROPERTY_DESCRIPTIONS = [
    "This property features modern finishes, ample parking space, and 24/7 security. Located in a serene environment with easy access to major roads.",
    "Well-maintained property with standby generator, water supply, and good drainage system. Close to shopping malls and schools.",
    "Newly renovated property with contemporary design. Features include fitted kitchen, wardrobes, and tiled floors throughout.",
    "Spacious and airy property in a gated estate. Amenities include swimming pool, gym, and children's playground.",
    "Property comes with prepaid meter, water heater, and air conditioning units. Excellent security and estate management.",
    "Located in a peaceful neighborhood with good road network. Property is well-ventilated with large windows and balconies.",
    "This property offers great value for money with modern fittings and a functional layout. Estate has 24-hour power supply.",
    "Beautiful property with garden space and car park. The area is well-developed with hospitals, banks, and restaurants nearby.",
]

# Sample Cloudinary image URLs (placeholders - will be replaced with actual images)
SAMPLE_IMAGES = [
    "https://res.cloudinary.com/demo/image/upload/v1/apartment_1.jpg",
    "https://res.cloudinary.com/demo/image/upload/v1/apartment_2.jpg",
    "https://res.cloudinary.com/demo/image/upload/v1/house_1.jpg",
    "https://res.cloudinary.com/demo/image/upload/v1/house_2.jpg",
    "https://res.cloudinary.com/demo/image/upload/v1/duplex_1.jpg",
]

# Sample landlord data with Nigerian names and phone numbers
LANDLORD_DATA = [
    {"name": "Chukwudi Okonkwo", "phone": "08012345678", "email": "chukwudi.okonkwo@gmail.com"},
    {"name": "Aisha Bello", "phone": "08023456789", "email": "aisha.bello@gmail.com"},
    {"name": "Oluwaseun Adeyemi", "phone": "08034567890", "email": "seun.adeyemi@gmail.com"},
    {"name": "Ngozi Eze", "phone": "08045678901", "email": "ngozi.eze@gmail.com"},
    {"name": "Ibrahim Yusuf", "phone": "08056789012", "email": "ibrahim.yusuf@gmail.com"},
    {"name": "Funmilayo Ogundipe", "phone": "08067890123", "email": "funmi.ogundipe@gmail.com"},
    {"name": "Emeka Nwosu", "phone": "08078901234", "email": "emeka.nwosu@gmail.com"},
    {"name": "Zainab Mohammed", "phone": "08089012345", "email": "zainab.mohammed@gmail.com"},
    {"name": "Tunde Bakare", "phone": "08090123456", "email": "tunde.bakare@gmail.com"},
    {"name": "Blessing Okeke", "phone": "08101234567", "email": "blessing.okeke@gmail.com"},
    {"name": "Babatunde Olaleye", "phone": "08112345678", "email": "babatunde.olaleye@gmail.com"},
    {"name": "Chioma Nnamdi", "phone": "08123456789", "email": "chioma.nnamdi@gmail.com"},
    {"name": "Yusuf Abdullahi", "phone": "08134567890", "email": "yusuf.abdullahi@gmail.com"},
    {"name": "Folake Adenike", "phone": "08145678901", "email": "folake.adenike@gmail.com"},
    {"name": "Chinedu Okafor", "phone": "08156789012", "email": "chinedu.okafor@gmail.com"},
]


def seed_landlords(db):
    """Create landlord users with contact information"""
    print(f"\n[LANDLORDS] Seeding {len(LANDLORD_DATA)} landlords...")

    landlords = []

    for landlord_data in LANDLORD_DATA:
        landlord = User(
            email=landlord_data["email"],
            password_hash=DEFAULT_PASSWORD_HASH,  # password123
            role=UserRole.LANDLORD,
            full_name=landlord_data["name"],
            phone_number=landlord_data["phone"],
            is_verified=True
        )
        db.add(landlord)
        db.flush()  # Get the ID immediately
        landlords.append(landlord)

    db.commit()
    print(f"[SUCCESS] Created {len(landlords)} landlords with contact info!")
    return landlords


def seed_properties(db, landlords, num_properties=250):
    """Seed properties table with Lagos property data"""
    print(f"\n[PROPERTIES] Seeding {num_properties} properties...")

    properties_created = 0

    for _ in range(num_properties):
        # Random area
        area = random.choice(list(LAGOS_AREAS.keys()))
        area_info = LAGOS_AREAS[area]

        # Random property type (weighted distribution)
        prop_type_weights = [0.6, 0.2, 0.1, 0.1]  # apartment, house, duplex, room
        prop_type = random.choices(
            list(PropertyType),
            weights=prop_type_weights,
            k=1
        )[0]

        # Bedrooms based on property type
        if prop_type == PropertyType.ROOM:
            bedrooms = 1
            bathrooms = 1
        elif prop_type == PropertyType.APARTMENT:
            bedrooms = random.choices([1, 2, 3, 4], weights=[0.2, 0.4, 0.3, 0.1])[0]
            bathrooms = random.choices([1, 2, 3], weights=[0.3, 0.5, 0.2])[0]
        else:  # house or duplex
            bedrooms = random.choices([3, 4, 5], weights=[0.4, 0.4, 0.2])[0]
            bathrooms = random.choices([2, 3, 4], weights=[0.4, 0.4, 0.2])[0]

        # Generate rent based on area and property type
        min_rent, max_rent = area_info["rent_range"]

        # Adjust rent based on bedrooms
        rent_multiplier = 1 + ((bedrooms - 1) * 0.3)
        adjusted_min = int(min_rent * rent_multiplier)
        adjusted_max = int(max_rent * rent_multiplier)

        rent_price = Decimal(random.randint(adjusted_min, adjusted_max))

        # Generate title
        if prop_type == PropertyType.ROOM:
            title = random.choice(PROPERTY_TITLES[prop_type]).format(area)
        else:
            title = random.choice(PROPERTY_TITLES[prop_type]).format(bedrooms, area)

        # Availability (70% available)
        is_available = random.random() < 0.7

        # Coordinates (slight variation from area center)
        lat, lng = area_info["coords"]
        latitude = Decimal(str(lat + random.uniform(-0.02, 0.02)))
        longitude = Decimal(str(lng + random.uniform(-0.02, 0.02)))

        # Assign to random landlord
        landlord = random.choice(landlords)

        # Create property
        property_obj = Property(
            landlord_id=landlord.id,  # Link to landlord
            title=title,
            description=random.choice(PROPERTY_DESCRIPTIONS),
            area=area,
            address=f"{random.randint(1, 50)} {random.choice(['Street', 'Road', 'Avenue', 'Close'])}, {area}, Lagos",
            property_type=prop_type,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            rent_price=rent_price,
            is_available=is_available,
            latitude=latitude,
            longitude=longitude,
        )

        db.add(property_obj)
        db.flush()  # Get the ID

        # Add 3-5 images per property
        num_images = random.randint(3, 5)
        for i in range(num_images):
            image = PropertyImage(
                property_id=property_obj.id,
                image_url=random.choice(SAMPLE_IMAGES),
                is_primary=(i == 0)  # First image is primary
            )
            db.add(image)

        properties_created += 1

        if properties_created % 20 == 0:
            print(f"  -> Created {properties_created} properties...")

    db.commit()
    print(f"[SUCCESS] Created {properties_created} properties!")


def main():
    """Main seeding function"""
    print("=" * 50)
    print("Starting Database Seeding...")
    print("=" * 50)

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_properties = db.query(Property).count()
        existing_users = db.query(User).count()

        if existing_properties > 0 or existing_users > 0:
            response = input(f"\n[WARNING] Found {existing_users} users and {existing_properties} properties. Continue anyway? (yes/no): ")
            if response.lower() != "yes":
                print("Seeding cancelled.")
                return

        # Seed landlords FIRST
        landlords = seed_landlords(db)

        # Seed properties and assign to landlords
        seed_properties(db, landlords, num_properties=80)

        print("\n" + "=" * 50)
        print("[SUCCESS] Database seeding completed successfully!")
        print("=" * 50)

        # Print summary
        total_landlords = db.query(User).filter(User.role == UserRole.LANDLORD).count()
        total_properties = db.query(Property).count()
        available_properties = db.query(Property).filter(Property.is_available == True).count()
        total_images = db.query(PropertyImage).count()

        print(f"\nSummary:")
        print(f"  Total Landlords: {total_landlords}")
        print(f"  Total Properties: {total_properties}")
        print(f"  Available: {available_properties}")
        print(f"  Total Images: {total_images}")
        print(f"\nNote: All landlords have contact info (phone + email)")

    except Exception as e:
        print(f"\n[ERROR] Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
