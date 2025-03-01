"""
Module for handling EPUB files.

This module provides functionality for extracting content from EPUB files,
such as the table of contents, text content, and metadata.
"""

import os
from typing import Dict, List, Union

from ebooklib import epub


def extract_toc(epub_path: str) -> List[Dict[str, Union[str, List]]]:
    """
    Extract the table of contents from an EPUB file.

    Args:
        epub_path: Path to the EPUB file.

    Returns:
        A list of dictionaries representing the table of contents.
        Each dictionary contains:
        - 'title': The title of the section
        - 'href': The link to the section content
        - 'level': The nesting level of the section
        - 'children': A list of child sections (if any)

    Raises:
        FileNotFoundError: If the EPUB file does not exist.
        ValueError: If the file is not a valid EPUB file.
    """
    if not os.path.exists(epub_path):
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    try:
        # Read the EPUB file
        book = epub.read_epub(epub_path)

        # Process the table of contents
        toc = book.toc

        # Function to recursively process TOC items
        def process_toc_item(item, level=0):
            result = []

            if isinstance(item, epub.Link):
                # It's a direct link
                result.append(
                    {
                        "title": item.title,
                        "href": item.href,
                        "level": level,
                        "children": [],
                    }
                )
            elif isinstance(item, tuple) and len(item) == 2:
                # It's a section with children
                section, children = item

                if isinstance(section, epub.Section):
                    # Add the section
                    section_item = {
                        "title": section.title,
                        "href": "",  # Sections might not have direct content
                        "level": level,
                        "children": [],
                    }

                    # Process children and add them to the section
                    for child in children:
                        child_items = process_toc_item(child, level + 1)
                        section_item["children"].extend(child_items)

                    result.append(section_item)
                else:
                    # Process children
                    for child in children:
                        child_items = process_toc_item(child, level)
                        result.extend(child_items)
            elif isinstance(item, list):
                # It's a list of items
                for child in item:
                    child_items = process_toc_item(child, level)
                    result.extend(child_items)

            return result

        # Process the entire TOC
        processed_toc = []
        for item in toc:
            processed_toc.extend(process_toc_item(item))

        return processed_toc

    except Exception as e:
        if "not a zip file" in str(e).lower():
            raise ValueError(f"The file is not a valid EPUB file: {epub_path}")
        raise
