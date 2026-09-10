import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


from rich.console import Console

from rich.panel import Panel
from rich.table import Table
from rich.json import JSON
from src.extractor import extract_structured_ticket

console = Console()


def print_extraction_result(source_name: str, raw_text: str, result):
    console.print(f"\n[bold cyan]======================================================[/bold cyan]")
    console.print(f"[bold yellow]📄 Processing Input:[/bold yellow] {source_name}")
    console.print(f"[bold cyan]======================================================[/bold cyan]")

    # Print raw text in box
    console.print(Panel(raw_text.strip(), title="Raw Input Text", border_style="dim"))

    # Summary table
    table = Table(title="Structured Extraction Result (Pydantic Model)", show_header=True, header_style="bold magenta")
    table.add_column("Field", style="cyan", width=22)
    table.add_column("Extracted Value", style="white")

    table.add_row("Ticket Summary", result.ticket_summary)
    table.add_row("Category", f"[bold green]{result.category.value}[/bold green]")
    
    # Priority color mapping
    priority_color = {
        "urgent": "bold red",
        "high": "red",
        "medium": "yellow",
        "low": "green"
    }.get(result.priority.value, "white")
    table.add_row("Priority", f"[{priority_color}]{result.priority.value.upper()}[/{priority_color}]")

    table.add_row("Customer Sentiment", result.customer_sentiment.value)
    table.add_row("Customer Name", result.customer_name or "N/A")
    table.add_row("Account/Invoice ID", result.account_id or "N/A")
    table.add_row("Affected Product", result.affected_product or "N/A")

    console.print(table)

    # Action Items
    if result.action_items:
        console.print("\n[bold green]📋 Recommended Action Items:[/bold green]")
        for i, item in enumerate(result.action_items, 1):
            console.print(f"  {i}. [bold yellow]{item.assignee_role}:[/bold yellow] {item.description}")

    # Exported JSON
    console.print("\n[bold blue]🔍 Validated Pydantic JSON Dump:[/bold blue]")
    console.print(JSON(result.model_dump_json()))


def main():
    sample_dir = Path(__file__).parent / "samples"
    sample_files = list(sample_dir.glob("*.txt"))

    if not sample_files:
        console.print("[red]No sample files found in samples/[/red]")
        return

    console.print("[bold green]🚀 AI Support Ticket Structured Data Extractor[/bold green]")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        console.print("[green]✓ GEMINI_API_KEY detected. Running in Live Cloud LLM Mode.[/green]\n")
    else:
        console.print("[yellow]ℹ No GEMINI_API_KEY detected. Running in Local Offline Mock Mode.[/yellow]")
        console.print("[dim](Set GEMINI_API_KEY in .env to switch to Live API Mode)[/dim]\n")

    for sample_file in sample_files:
        raw_text = sample_file.read_text(encoding="utf-8")
        result = extract_structured_ticket(raw_text)
        print_extraction_result(sample_file.name, raw_text, result)


if __name__ == "__main__":
    main()
