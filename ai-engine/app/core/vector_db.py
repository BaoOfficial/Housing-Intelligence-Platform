"""
ChromaDB connection and management
"""
import chromadb
from chromadb.config import Settings
from pathlib import Path
from ..config import settings


class VectorDB:
    """ChromaDB client wrapper"""

    def __init__(self):
        """Initialize ChromaDB client (embedded mode)"""
        # Store ChromaDB data locally in ai-engine/chroma_data
        chroma_path = Path(__file__).parent.parent.parent / "chroma_data"
        chroma_path.mkdir(exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(chroma_path),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection_name = settings.CHROMADB_COLLECTION

    def get_or_create_collection(self):
        """Get or create the reviews collection"""
        return self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Tenant reviews and experiences for Lagos housing"}
        )

    def add_documents(self, documents, embeddings, metadatas, ids):
        """Add documents to the collection"""
        collection = self.get_or_create_collection()
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_embeddings, n_results=10, where=None):
        """
        Query the collection

        Args:
            query_embeddings: List of query embedding vectors
            n_results: Number of results to return
            where: Optional metadata filter

        Returns:
            Query results from ChromaDB
        """
        collection = self.get_or_create_collection()
        return collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where
        )

    def delete_collection(self):
        """Delete the collection (use with caution!)"""
        try:
            self.client.delete_collection(name=self.collection_name)
            print(f"✅ Collection '{self.collection_name}' deleted")
        except Exception as e:
            print(f"❌ Error deleting collection: {e}")

    def get_collection_count(self):
        """Get the number of documents in the collection"""
        try:
            collection = self.get_or_create_collection()
            return collection.count()
        except Exception as e:
            print(f"❌ Error getting count: {e}")
            return 0


# Global instance
vector_db = VectorDB()
