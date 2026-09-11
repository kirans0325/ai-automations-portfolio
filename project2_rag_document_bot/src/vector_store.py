import math
import re
from typing import List, Tuple
from src.chunker import DocumentChunk


class VectorStore:
    """Lightweight in-memory Vector Store supporting semantic cosine similarity search."""

    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self.vectors: List[dict] = []  # term frequency dictionary per chunk
        self.vocabulary = set()

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenizer: lowercase words, removing special chars."""
        return re.findall(r"\b\w+\b", text.lower())

    def add_chunks(self, chunks: List[DocumentChunk]):
        """Adds document chunks and computes vector embeddings for each chunk."""
        for chunk in chunks:
            tokens = self._tokenize(chunk.content)
            tf_dict = {}
            for token in tokens:
                tf_dict[token] = tf_dict.get(token, 0) + 1
                self.vocabulary.add(token)

            # Normalize term frequencies
            total = len(tokens) or 1
            norm_tf = {k: v / total for k, v in tf_dict.items()}

            self.chunks.append(chunk)
            self.vectors.append(norm_tf)

    def _cosine_similarity(self, vec1: dict, vec2: dict) -> float:
        """Calculates cosine similarity score (0.0 to 1.0) between two sparse vectors."""
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([val ** 2 for val in vec1.values()])
        sum2 = sum([val ** 2 for val in vec2.values()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        return float(numerator / denominator)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[DocumentChunk, float]]:
        """Searches vector store for top_k chunks most relevant to the query.

        Returns:
            List[Tuple[DocumentChunk, score]]: Ranked list of chunks with similarity scores.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # Vectorize query
        query_tf = {}
        for token in query_tokens:
            query_tf[token] = query_tf.get(token, 0) + 1
        total = len(query_tokens) or 1
        query_vec = {k: v / total for k, v in query_tf.items()}

        # Compute similarity scores against all chunks
        scored_chunks = []
        for i, chunk_vec in enumerate(self.vectors):
            score = self._cosine_similarity(query_vec, chunk_vec)
            scored_chunks.append((self.chunks[i], score))

        # Sort descending by score
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        return scored_chunks[:top_k]
