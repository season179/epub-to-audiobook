"""Configuration models for the ePub to Audiobook converter."""

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, validator


class Settings(BaseModel):
    """Application settings."""
    
    voice: str = Field(default="default", description="Voice to use for the audiobook")
    speed: float = Field(default=1.0, description="Speech speed", ge=0.5, le=2.0)
    output_dir: Path = Field(..., description="Directory to save the audiobook files")
    api_key: Optional[str] = Field(
        None, description="Fish Audio API key. If not provided, will look for FISH_AUDIO_API_KEY environment variable"
    )
    
    @validator("api_key", pre=True, always=True)
    def set_api_key(cls, v):
        """Set the API key from environment variable if not provided."""
        import os
        if v is None:
            return os.environ.get("FISH_AUDIO_API_KEY")
        return v


class EpubMetadata(BaseModel):
    """Metadata from an ePub file."""
    
    title: str
    author: str
    publisher: Optional[str] = None
    language: Optional[str] = None
    identifier: Optional[str] = None
    description: Optional[str] = None
    
    
class Chapter(BaseModel):
    """Chapter from an ePub file."""
    
    title: str
    content: str
    index: int


class Book(BaseModel):
    """Represents a parsed ePub book."""
    
    metadata: EpubMetadata
    chapters: list[Chapter]
    
    @property
    def total_chapters(self) -> int:
        """Get the total number of chapters."""
        return len(self.chapters)
