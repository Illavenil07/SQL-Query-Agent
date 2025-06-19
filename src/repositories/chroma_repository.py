"""Repository for Chroma vector database operations."""

import chromadb
from chromadb.config import Settings


class ChromaRepository:
    """
    Manages vector database operations for storing and querying schema embeddings.
    """

    def __init__(self):
        """
        Initializes Chroma client and schema collection.
        """
        self.client = chromadb.Client(Settings())
        self.collection_name = "db_schema"
        self.collection = self._get_or_create_collection(self.collection_name)

    def _get_or_create_collection(self, name):
        """
        Retrieves existing or creates a new Chroma collection.

        Args:
            name (str): Collection name.

        Returns:
            Collection object.
        """
        try:
            return self.client.get_or_create_collection(name)
        except Exception as e:
            raise Exception(f"Failed to create or fetch Chroma collection: {str(e)}")

    def add_embedding(self, doc_id, document_text, embedding_vector):
        """
        Adds a schema embedding document to the vector database.

        Args:
            doc_id (str): Unique document identifier.
            document_text (str): Original schema text.
            embedding_vector (List[float]): Embedding vector.
        """
        try:
            self.collection.add(
                ids=[doc_id],
                documents=[document_text],
                embeddings=[embedding_vector]
            )
        except Exception as e:
            raise Exception(f"Failed to add embedding: {str(e)}")

    def query_similar_schemas(self, embedding_vector, top_k=3):
        """
        Retrieves top-k similar schema documents from the vector database.

        Args:
            embedding_vector (List[float]): Embedding vector to compare.
            top_k (int, optional): Number of similar results to retrieve. Defaults to 3.

        Returns:
            List of matched document metadata.
        """
        try:
            results = self.collection.query(
                query_embeddings=[embedding_vector],
                n_results=top_k,
                include=["documents", "distances", "metadatas"]
            )
            return results
        except Exception as e:
            raise Exception(f"Failed to query similar schemas: {str(e)}")

    def delete_embedding(self, doc_id):
        """
        Deletes a document embedding from the collection.

        Args:
            doc_id (str): Document identifier to delete.
        """
        try:
            self.collection.delete(ids=[doc_id])
        except Exception as e:
            raise Exception(f"Failed to delete embedding: {str(e)}")
