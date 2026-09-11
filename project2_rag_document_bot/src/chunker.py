from dataclasses import dataclass
from typing import List


@dataclass
class DocumentChunk:
    chunk_id: str
    source_file: str
    content: str
    chunk_index: int


def chunk_text(text: str, source_file: str, chunk_size: int = 300, overlap: int = 50) -> List[DocumentChunk]:
    """Splits a document's raw text into smaller overlapping chunks for vector embedding.

    Args:
        text: Full raw text of the document.
        source_file: Name/path of the source file.
        chunk_size: Maximum word count per chunk.
        overlap: Number of overlapping words between consecutive chunks.

    Returns:
        List[DocumentChunk]: List of chunk objects with metadata.
    """
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    chunk_idx = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunk_content = " ".join(chunk_words)

        chunk_id = f"{source_file}_chunk_{chunk_idx}"
        chunks.append(DocumentChunk(
            chunk_id=chunk_id,
            source_file=source_file,
            content=chunk_content,
            chunk_index=chunk_idx
        ))

        chunk_idx += 1
        # Move forward by chunk_size - overlap to create overlapping windows
        start += (chunk_size - overlap)

    return chunks
