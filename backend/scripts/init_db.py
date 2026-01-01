"""
Database initialization script
Creates all tables in MySQL database
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine, Base
from app.models import User, Property, PropertyImage, Review


def init_db():
    """Create all database tables"""
    print("Creating database tables...")

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - properties")
        print("  - property_images")
        print("  - reviews")

    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise


def drop_all_tables():
    """Drop all database tables (use with caution!)"""
    response = input("⚠️  This will drop all tables. Are you sure? (yes/no): ")
    if response.lower() == "yes":
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped!")
    else:
        print("Operation cancelled.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database initialization")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all tables before creating (dangerous!)"
    )

    args = parser.parse_args()

    if args.drop:
        drop_all_tables()

    init_db()
