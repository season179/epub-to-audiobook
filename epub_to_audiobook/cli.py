"""Command-line interface for the ePub to Audiobook converter."""

import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from epub_to_audiobook.models.config import Settings
from epub_to_audiobook.services.converter import EpubConverter

app = typer.Typer(help="Convert ePub files to audiobooks using Fish Audio.")
console = Console()


@app.command()
def convert(
    epub_path: Path = typer.Argument(
        ..., help="Path to the ePub file to convert", exists=True, file_okay=True, dir_okay=False
    ),
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Directory to save the audiobook files"
    ),
    voice: str = typer.Option(
        "default", "--voice", "-v", help="Voice to use for the audiobook"
    ),
    speed: float = typer.Option(
        1.0, "--speed", "-s", help="Speech speed (0.5 to 2.0)", min=0.5, max=2.0
    ),
):
    """Convert an ePub file to an audiobook."""
    if not output_dir:
        output_dir = Path(os.path.splitext(str(epub_path))[0])
    
    output_dir.mkdir(exist_ok=True, parents=True)
    
    settings = Settings(
        voice=voice,
        speed=speed,
        output_dir=output_dir,
    )
    
    console.print(f"Converting [bold]{epub_path}[/bold] to audiobook...")
    console.print(f"Using voice: [green]{voice}[/green] at speed: [green]{speed}x[/green]")
    console.print(f"Output directory: [blue]{output_dir}[/blue]")
    
    # This will be implemented in Phase 1 and 2
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing ePub file...", total=None)
        # TODO: Implement the actual conversion process
        # converter = EpubConverter(epub_path, settings)
        # converter.convert()
        
    console.print("[bold green]Conversion completed![/bold green]")


@app.command()
def version():
    """Show the application version."""
    from epub_to_audiobook import __version__
    console.print(f"ePub to Audiobook Converter v{__version__}")


if __name__ == "__main__":
    app()
