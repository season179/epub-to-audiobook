#!/usr/bin/env python3
"""
Example script demonstrating how to use the epub_handler module to extract
and print the table of contents from an EPUB file.

Usage:
    python epub_toc_example.py /path/to/your/book.epub
"""

import os
import sys
from pprint import pprint

# Add the parent directory to the Python path to import the project module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from epub_to_audiobook.epub_handler import extract_toc


def print_toc_item(item, indent=0):
    """Print a TOC item with proper indentation."""
    indent_str = "  " * indent
    print(f"{indent_str}• {item['title']}")

    if item["href"]:
        print(f"{indent_str}  Link: {item['href']}")

    # Print children with increased indentation
    for child in item["children"]:
        print_toc_item(child, indent + 1)


def main():
    """Main function to demonstrate the epub_handler module."""
    if len(sys.argv) < 2:
        print(f"Usage: python {os.path.basename(__file__)} /path/to/your/book.epub")
        sys.exit(1)

    epub_path = sys.argv[1]

    try:
        print(f"Extracting table of contents from: {epub_path}")
        print("-" * 50)

        # Extract the table of contents
        toc = extract_toc(epub_path)

        # Print TOC in a readable format
        if toc:
            print("Table of Contents:")
            for item in toc:
                print_toc_item(item)
        else:
            print("No table of contents found in the EPUB file.")

        print("-" * 50)
        print(f"Total entries: {len(toc)}")

        # Also print the raw TOC data structure
        print("\nRaw TOC data structure:")
        pprint(toc)

    except FileNotFoundError:
        print(f"Error: The file '{epub_path}' does not exist.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
