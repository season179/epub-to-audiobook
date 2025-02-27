"""Tests for text utilities."""

import pytest

from epub_to_audiobook.utils.text import clean_text, split_into_chunks, normalize_text


def test_clean_text():
    """Test the clean_text function."""
    input_text = "Hello,  world! This is a test. Mr. Smith is here."
    expected = "Hello, world! This is a test. Mister Smith is here."
    
    assert clean_text(input_text) == expected


def test_split_into_chunks():
    """Test the split_into_chunks function."""
    # Create a long text with many sentences
    sentences = ["This is sentence " + str(i) + "." for i in range(100)]
    long_text = " ".join(sentences)
    
    # Split into chunks
    chunks = split_into_chunks(long_text, max_chunk_size=200)
    
    # Assert each chunk is less than or equal to max_chunk_size
    for chunk in chunks:
        assert len(chunk) <= 200
    
    # Assert all text is preserved (accounting for whitespace differences)
    original_text = " ".join(long_text.split())
    chunked_text = " ".join(" ".join(chunks).split())
    assert original_text == chunked_text


def test_normalize_text():
    """Test the normalize_text function."""
    input_text = "Meeting at 14:30 on 2022-05-15. Cost: $100 & 50% of expenses."
    expected = "Meeting at 14:30 on 5/15/2022. Cost:  dollars 100  and  50 percent of expenses."
    
    assert normalize_text(input_text) == expected
