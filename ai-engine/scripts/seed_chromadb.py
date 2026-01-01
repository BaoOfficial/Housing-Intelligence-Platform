"""
Seed ChromaDB with review embeddings from MySQL
"""
import sys
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.vector_db import vector_db
from app.services.embedding_service import embedding_service

# Load backend .env for database connection
backend_env_path = Path(__file__).parent.parent.parent / "backend" / ".env"
load_dotenv(backend_env_path)

# Database connection
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "housing_intelligence")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Define Review model locally
class Review(Base):
    """Review model"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer)
    area = Column(String(100))
    rent_paid = Column(Numeric(12, 2))
    property_type = Column(String(50))
    review_text = Column(Text)
    pros = Column(Text)
    cons = Column(Text)
    rating = Column(Integer)


def seed_chromadb():
    """Seed ChromaDB with review embeddings from MySQL"""
    print("=" * 60)
    print("Starting ChromaDB Seeding...")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Fetch all reviews from MySQL
        reviews = db.query(Review).all()
        total_reviews = len(reviews)

        if total_reviews == 0:
            print("ERROR: No reviews found in MySQL database!")
            print("   Please run backend/scripts/seed_reviews.py first")
            return

        print(f"\nFound {total_reviews} reviews in MySQL")
        print(f"Generating embeddings and storing in ChromaDB...\n")

        # Prepare data for ChromaDB
        documents = []
        embeddings_list = []
        metadatas = []
        ids = []

        # Process in batches for efficiency
        batch_size = 50
        for i in range(0, total_reviews, batch_size):
            batch = reviews[i:i + batch_size]
            batch_texts = []
            batch_metadatas = []
            batch_ids = []

            for review in batch:
                # Combine review text with pros and cons
                full_text = review.review_text
                if review.pros:
                    full_text += f" Pros: {review.pros}"
                if review.cons:
                    full_text += f" Cons: {review.cons}"

                batch_texts.append(full_text)
                batch_metadatas.append({
                    "review_id": review.id,
                    "area": review.area,
                    "property_type": review.property_type or "unknown",
                    "rent_paid": float(review.rent_paid) if review.rent_paid else 0,
                    "rating": review.rating if review.rating else 0,
                    "property_id": review.property_id if review.property_id else 0
                })
                batch_ids.append(f"review_{review.id}")

            # Generate embeddings for batch
            print(f"  Processing batch {i//batch_size + 1}/{(total_reviews + batch_size - 1)//batch_size}...")
            batch_embeddings = embedding_service.embed_texts(batch_texts)

            # Add to main lists
            documents.extend(batch_texts)
            embeddings_list.extend(batch_embeddings)
            metadatas.extend(batch_metadatas)
            ids.extend(batch_ids)

        # Add all to ChromaDB
        print(f"\nStoring {len(documents)} embeddings in ChromaDB...")
        vector_db.add_documents(
            documents=documents,
            embeddings=embeddings_list,
            metadatas=metadatas,
            ids=ids
        )

        print("\n" + "=" * 60)
        print("SUCCESS: ChromaDB seeding completed successfully!")
        print("=" * 60)

        # Verify
        count = vector_db.get_collection_count()
        print(f"\nSummary:")
        print(f"  Total documents in ChromaDB: {count}")
        print(f"  Collection: {vector_db.collection_name}")
        print(f"  Data stored in: ai-engine/chroma_data/")

    except Exception as e:
        print(f"\nERROR during seeding: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_chromadb()
