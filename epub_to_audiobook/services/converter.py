"""Converter for ePub files to audiobooks."""

import os
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn

from epub_to_audiobook.models.config import Book, Chapter, Settings
from epub_to_audiobook.services.epub_parser import EpubParser
from epub_to_audiobook.services.fish_audio import FishAudioService

console = Console()


class EpubConverter:
    """Converter for ePub files to audiobooks."""
    
    def __init__(self, epub_path: Path, settings: Settings):
        """Initialize the converter.
        
        Args:
            epub_path: Path to the ePub file
            settings: Application settings
        """
        self.epub_path = epub_path
        self.settings = settings
        self.output_dir = settings.output_dir
        self.epub_parser = EpubParser(epub_path)
        self.fish_audio = FishAudioService(settings)
        
    def convert(self) -> Path:
        """Convert ePub to audiobook.
        
        Returns:
            Path to the output directory
        """
        # Parse the ePub file
        book = self.epub_parser.parse()
        
        console.print(f"Converting book: [bold]{book.metadata.title}[/bold] by [bold]{book.metadata.author}[/bold]")
        
        # Create output directory with book title
        book_dir = self.output_dir / self._sanitize_filename(book.metadata.title)
        book_dir.mkdir(exist_ok=True, parents=True)
        
        # Process each chapter
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(f"Converting [bold]{len(book.chapters)}[/bold] chapters", total=len(book.chapters))
            
            for chapter in book.chapters:
                progress.update(task, description=f"Converting Chapter {chapter.index + 1}: {chapter.title}")
                
                # Process chapter text (placeholder for Phase 2)
                processed_text = self._process_text(chapter.content)
                
                # Convert text to speech (placeholder for Phase 2)
                chapter_filename = f"{chapter.index + 1:03d}_{self._sanitize_filename(chapter.title)}.mp3"
                chapter_path = book_dir / chapter_filename
                
                # TODO: In Phase 2, implement actual text-to-speech conversion
                # Placeholder for now
                # self.fish_audio.text_to_speech(processed_text, chapter_path)
                
                progress.advance(task)
        
        console.print(f"Audiobook saved to: [blue]{book_dir}[/blue]")
        return book_dir
    
    def _process_text(self, text: str) -> str:
        """Process text for conversion to speech.
        
        Args:
            text: Text to process
            
        Returns:
            Processed text
        """
        # TODO: Implement text processing in Phase 2
        # This would include:
        # - Removing unnecessary formatting and special characters
        # - Normalizing whitespace
        # - Handling dialogues, quotes, etc.
        # - Chunking text if needed
        
        return text
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a string for use as a filename.
        
        Args:
            name: String to sanitize
            
        Returns:
            Sanitized string
        """
        # Replace invalid characters with underscores
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        
        # Trim length if needed
        if len(name) > 100:
            name = name[:97] + '...'
            
        return name.strip()
