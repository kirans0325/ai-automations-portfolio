import os
from dataclasses import dataclass
from typing import List, Tuple
from dotenv import load_dotenv
from src.chunker import DocumentChunk
from src.vector_store import VectorStore

load_dotenv()


@dataclass
class RAGResponse:
    question: str
    answer: str
    retrieved_chunks: List[Tuple[DocumentChunk, float]]
    mode: str  # "Live Cloud LLM" or "Offline Grounded Engine"


class RAGEngine:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.api_key = os.getenv("GEMINI_API_KEY")

    def answer_question(self, question: str, top_k: int = 3) -> RAGResponse:
        """Retrieves top relevant context chunks and synthesizes a grounded answer."""
        retrieved = self.vector_store.search(question, top_k=top_k)

        # Build context block
        context_blocks = []
        for chunk, score in retrieved:
            context_blocks.append(
                f"--- [Source: {chunk.source_file} | Relevance Score: {score:.2f}] ---\n{chunk.content}"
            )
        context_str = "\n\n".join(context_blocks) if context_blocks else "No relevant context found."

        if self.api_key:
            try:
                from google import genai
                client = genai.Client(api_key=self.api_key)

                prompt = f"""
You are a precise AI Knowledge Assistant.
Answer the user's question STRICTLY using the knowledge base context provided below.
If the answer cannot be determined from the context, state: "I could not find relevant information in the provided knowledge base."

KNOWLEDGE BASE CONTEXT:
{context_str}

USER QUESTION:
{question}
"""
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                return RAGResponse(
                    question=question,
                    answer=response.text.strip(),
                    retrieved_chunks=retrieved,
                    mode="Live Cloud LLM"
                )
            except Exception as e:
                pass  # Fallback to local offline synthesis

        # Local Offline Grounded Synthesis
        if not retrieved or retrieved[0][1] == 0:
            answer = "I could not find relevant information in the knowledge base documents for your question."
        else:
            top_chunk, top_score = retrieved[0]
            answer = f"Based on knowledge base document [{top_chunk.source_file}]:\n\"{top_chunk.content}\""

        return RAGResponse(
            question=question,
            answer=answer,
            retrieved_chunks=retrieved,
            mode="Offline Grounded Engine"
        )
