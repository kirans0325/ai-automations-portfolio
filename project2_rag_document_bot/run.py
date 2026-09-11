import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Ensure UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.chunker import chunk_text
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine

console = Console()


def initialize_rag_system(docs_dir: Path) -> RAGEngine:
    """Reads documents, chunks text, populates vector store, and initializes RAG engine."""
    vector_store = VectorStore()
    doc_files = list(docs_dir.glob("*.txt"))

    if not doc_files:
        console.print("[bold red]No document files found in docs/[/bold red]")
        sys.exit(1)

    total_chunks = 0
    for doc_file in doc_files:
        content = doc_file.read_text(encoding="utf-8")
        chunks = chunk_text(content, source_file=doc_file.name, chunk_size=100, overlap=20)
        vector_store.add_chunks(chunks)
        total_chunks += len(chunks)

    console.print(f"[bold green]✓ Loaded {len(doc_files)} documents into Vector Store ({total_chunks} total chunks indexed).[/bold green]\n")
    return RAGEngine(vector_store)


def ask_and_print(rag_engine: RAGEngine, question: str):
    console.print(f"[bold cyan]======================================================[/bold cyan]")
    console.print(f"[bold yellow]❓ Question:[/bold yellow] {question}")
    console.print(f"[bold cyan]======================================================[/bold cyan]")

    response = rag_engine.answer_question(question, top_k=2)

    # Print retrieved chunks table
    table = Table(title="🔍 Retrieved Vector Chunks (Top Match)", show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="cyan", width=6)
    table.add_column("Source Document", style="yellow", width=25)
    table.add_column("Similarity Score", style="green", width=16)
    table.add_column("Retrieved Chunk Preview", style="white")

    for idx, (chunk, score) in enumerate(response.retrieved_chunks, 1):
        preview = chunk.content[:100] + "..." if len(chunk.content) > 100 else chunk.content
        table.add_row(f"#{idx}", chunk.source_file, f"{score:.4f}", preview)

    console.print(table)

    # Print Grounded LLM Answer
    console.print(Panel(response.answer, title=f"🤖 Grounded Answer ({response.mode})", border_style="bold green"))


def main():
    docs_dir = Path(__file__).parent / "docs"
    console.print("[bold green]🚀 Launching Project 2: RAG Document QA Bot[/bold green]")
    
    rag_engine = initialize_rag_system(docs_dir)

    # Sample demo questions
    demo_questions = [
        "What is the remote work equipment setup stipend amount?",
        "How do I setup automated report exports in Analytics Hub?",
        "What should I do if the API returns HTTP 429 rate limit error?"
    ]

    for q in demo_questions:
        ask_and_print(rag_engine, q)


if __name__ == "__main__":
    main()
