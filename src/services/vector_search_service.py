"""Service for managing schema embedding operations in Chroma."""

from repositories.chroma_repository import ChromaRepository


class VectorSearchService:
    """
    Service layer for managing vector search operations in Chroma.
    """

    def __init__(self, chroma_repo: ChromaRepository):
        """
        Initializes the VectorSearchService with a Chroma repository.

        Args:
            chroma_repo (ChromaRepository): Chroma repository instance.
        """
        self.chroma_repo = chroma_repo

    def add_schema_embedding(self, doc_id, schema_text, embedding_vector):
        """
        Adds a schema embedding document to the vector database.

        Args:
            doc_id (str): Unique document identifier.
            schema_text (str): Schema text document.
            embedding_vector (List[float]): Embedding vector.
        """
        try:
            self.chroma_repo.add_embedding(doc_id, schema_text, embedding_vector)
        except Exception as e:
            raise Exception(f"Failed to add schema embedding: {str(e)}")

    def search_similar_schemas(self, embedding_vector, top_k=3):
        """
        Searches for similar schema embeddings in the vector database.

        Args:
            embedding_vector (List[float]): Embedding vector to compare.
            top_k (int, optional): Number of similar results to retrieve. Defaults to 3.

        Returns:
            dict: Matching results containing documents, distances, and IDs.
        """
        try:
            results = self.chroma_repo.query_similar_schemas(embedding_vector, top_k)
            return results
        except Exception as e:
            raise Exception(f"Failed to search similar schemas: {str(e)}")

    def delete_schema_embedding(self, doc_id):
        """
        Deletes a specific schema embedding from the vector database.

        Args:
            doc_id (str): Document identifier.
        """
        try:
            self.chroma_repo.delete_embedding(doc_id)
        except Exception as e:
            raise Exception(f"Failed to delete schema embedding: {str(e)}")
