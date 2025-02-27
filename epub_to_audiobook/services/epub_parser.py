"""Parser for ePub files."""

import io
from pathlib import Path
from typing import List, Optional

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from rich.console import Console

from epub_to_audiobook.models.config import Book, Chapter, EpubMetadata

console = Console()


class EpubParser:
    """Parser for ePub files."""
    
    def __init__(self, epub_path: Path):
        """Initialize the parser.
        
        Args:
            epub_path: Path to the ePub file
        """
        self.epub_path = epub_path
        
    def parse(self) -> Book:
        """Parse the ePub file.
        
        Returns:
            A Book object containing the metadata and chapters
        """
        console.print(f"Parsing ePub file: [bold]{self.epub_path}[/bold]")
        
        book = epub.read_epub(str(self.epub_path))
        
        # Extract metadata
        metadata = self._extract_metadata(book)
        
        # Extract chapters
        chapters = self._extract_chapters(book)
        
        console.print(f"Found [bold]{len(chapters)}[/bold] chapters")
        
        return Book(
            metadata=metadata,
            chapters=chapters
        )
    
    def _extract_metadata(self, book: epub.EpubBook) -> EpubMetadata:
        """Extract metadata from the ePub book.
        
        Args:
            book: The parsed ePub book
            
        Returns:
            EpubMetadata object
        """
        title = book.get_metadata("DC", "title")[0][0] if book.get_metadata("DC", "title") else "Unknown Title"
        
        # Extract author if available, otherwise use "Unknown Author"
        author = "Unknown Author"
        if book.get_metadata("DC", "creator"):
            author = book.get_metadata("DC", "creator")[0][0]
        
        # Extract optional metadata
        publisher = book.get_metadata("DC", "publisher")[0][0] if book.get_metadata("DC", "publisher") else None
        language = book.get_metadata("DC", "language")[0][0] if book.get_metadata("DC", "language") else None
        identifier = book.get_metadata("DC", "identifier")[0][0] if book.get_metadata("DC", "identifier") else None
        description = book.get_metadata("DC", "description")[0][0] if book.get_metadata("DC", "description") else None
        
        return EpubMetadata(
            title=title,
            author=author,
            publisher=publisher,
            language=language,
            identifier=identifier,
            description=description
        )
    
    def _extract_chapters(self, book: epub.EpubBook) -> List[Chapter]:
        """Extract chapters from the ePub book.
        
        Args:
            book: The parsed ePub book
            
        Returns:
            List of Chapter objects
        """
        chapters = []
        index = 0
        
        # Get the spine items, which represent the reading order
        spine_items = [book.get_item_with_id(item_id) for item_id in book.spine]
        
        for item in spine_items:
            # Skip if not a document
            if not isinstance(item, epub.EpubHtml):
                continue
            
            # Check if content is HTML
            if not item.get_content():
                continue
            
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            
            # Get title from heading tags or use the item title
            title = self._extract_title(soup, item)
            
            # Extract text content from HTML
            text_content = self._extract_text(soup)
            
            # Skip chapters with no significant content
            if not text_content or len(text_content.strip()) < 100:
                continue
            
            # Add chapter
            chapters.append(
                Chapter(
                    title=title,
                    content=text_content,
                    index=index
                )
            )
            index += 1
            
        return chapters
    
    def _extract_title(self, soup: BeautifulSoup, item: epub.EpubHtml) -> str:
        """Extract title from HTML content.
        
        Args:
            soup: BeautifulSoup object
            item: ePub item
            
        Returns:
            Title of the chapter
        """
        # Try to find heading elements
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            if heading.text.strip():
                return heading.text.strip()
        
        # Use item title if available
        if hasattr(item, 'title') and item.title:
            return item.title
        
        # Default title
        return f"Chapter {item.id}"
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract text content from HTML.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Text content
        """
        # Remove script and style elements
        for element in soup(['script', 'style']):
            element.extract()
        
        # Get text
        text = soup.get_text()
        
        # Process text: normalize whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
