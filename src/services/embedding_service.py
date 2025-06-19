"""Service for generating embeddings using Sentence Transformers."""

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Service layer for generating text embeddings using Sentence Transformers.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initializes the Sentence Transformer model.

        Args:
            model_name (str, optional): Pre-trained embedding model name.
        """
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text):
        """
        Generates an embedding vector for the given text.

        Args:
            text (str): Text to generate an embedding for.

        Returns:
            List[float]: Embedding vector.
        """
        try:
            embedding = self.model.encode(text, convert_to_numpy=True).tolist()
            return embedding
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")
