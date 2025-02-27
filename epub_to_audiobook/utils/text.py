"""Text processing utilities for the ePub to Audiobook converter."""

import re
from typing import List


def clean_text(text: str) -> str:
    """Clean text for TTS conversion.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might affect TTS
    text = re.sub(r'[^\w\s.,?!:;()\-\'"]', ' ', text)
    
    # Replace common abbreviations
    abbreviations = {
        'Mr.': 'Mister',
        'Mrs.': 'Misses',
        'Dr.': 'Doctor',
        'Prof.': 'Professor',
        'e.g.': 'for example',
        'i.e.': 'that is',
        'etc.': 'etcetera',
    }
    
    for abbr, full in abbreviations.items():
        text = text.replace(abbr, full)
    
    return text.strip()


def split_into_chunks(text: str, max_chunk_size: int = 1000) -> List[str]:
    """Split text into chunks for TTS processing.
    
    Args:
        text: Text to split
        max_chunk_size: Maximum size of each chunk in characters
        
    Returns:
        List of text chunks
    """
    # If text is smaller than max chunk size, return as is
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    current_chunk = ""
    
    for sentence in sentences:
        # If adding this sentence would exceed max size, add current chunk to list and start a new one
        if len(current_chunk) + len(sentence) > max_chunk_size:
            if current_chunk:  # Only add if not empty
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def normalize_text(text: str) -> str:
    """Normalize text for better TTS quality.
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    # Convert numbers to words (simplified version)
    # In a real implementation, we would use a more sophisticated library for this
    
    # Handle dates (e.g., "2022-05-15" -> "May 15, 2022")
    text = re.sub(
        r'(\d{4})-(\d{2})-(\d{2})',
        lambda m: f"{int(m.group(2))}/{int(m.group(3))}/{m.group(1)}",
        text
    )
    
    # Handle time (e.g., "14:30" -> "2:30 PM")
    text = re.sub(
        r'(\d{1,2}):(\d{2})',
        lambda m: f"{int(m.group(1))}:{m.group(2)}",
        text
    )
    
    # Handle common symbols
    text = text.replace('%', ' percent')
    text = text.replace('&', ' and ')
    text = text.replace('@', ' at ')
    text = text.replace('#', ' number ')
    text = text.replace('$', ' dollars ')
    text = text.replace('=', ' equals ')
    text = text.replace('+', ' plus ')
    text = text.replace('-', ' minus ')
    text = text.replace('*', ' times ')
    text = text.replace('/', ' divided by ')
    
    return text
