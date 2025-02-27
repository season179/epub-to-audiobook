#!/usr/bin/env python
"""Example script demonstrating how to use the ePub to Audiobook converter."""

import os
import sys
from pathlib import Path

from rich.console import Console

from epub_to_audiobook.models.config import Settings
from epub_to_audiobook.services.epub_parser import EpubParser
from epub_to_audiobook.services.converter import EpubConverter

console = Console()


def main():
    """Run the example script."""
    # Check if an ePub file was provided as an argument
    if len(sys.argv) < 2:
        console.print("[bold red]Error:[/bold red] Please provide the path to an ePub file.")
        console.print("Usage: python example.py /path/to/book.epub")
        return 1
    
    # Get the ePub file path
    epub_path = Path(sys.argv[1])
    
    # Check if the file exists
    if not epub_path.exists():
        console.print(f"[bold red]Error:[/bold red] File {epub_path} does not exist.")
        return 1
    
    # Check if the file is an ePub file
    if epub_path.suffix.lower() != ".epub":
        console.print(f"[bold red]Error:[/bold red] File {epub_path} is not an ePub file.")
        return 1
    
    # Create output directory
    output_dir = epub_path.parent / "audiobook_output"
    
    # Create settings
    settings = Settings(
        voice="default",
        speed=1.0,
        output_dir=output_dir,
        api_key=os.environ.get("FISH_AUDIO_API_KEY")
    )
    
    # Parse ePub file to demonstrate parsing functionality
    parser = EpubParser(epub_path)
    book = parser.parse()
    
    # Display book information
    console.print(f"Book: [bold]{book.metadata.title}[/bold]")
    console.print(f"Author: [bold]{book.metadata.author}[/bold]")
    console.print(f"Chapters: [bold]{len(book.chapters)}[/bold]")
    
    # Display first few chapters
    console.print("\nChapter preview:")
    for i, chapter in enumerate(book.chapters[:3]):
        console.print(f"Chapter {i+1}: [bold]{chapter.title}[/bold]")
        # Show a preview of the content (first 100 characters)
        preview = chapter.content[:100].replace("\n", " ").strip()
        console.print(f"  Preview: {preview}...")
    
    if len(book.chapters) > 3:
        console.print(f"... and {len(book.chapters) - 3} more chapters.")
    
    console.print("\n[bold green]Parsing completed successfully![/bold green]")
    console.print("[yellow]Note: This example script only demonstrates parsing functionality.[/yellow]")
    console.print("[yellow]The actual TTS conversion will be implemented in Phase 2.[/yellow]")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
