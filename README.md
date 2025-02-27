# ePub to Audiobook Converter

A command-line application that converts ePub files into audiobooks using Fish Audio's text-to-speech technology.

## Overview

This application allows users to convert their ePub books into high-quality audiobooks that can be listened to on various devices. It leverages Fish Audio's advanced text-to-speech capabilities to create natural-sounding narrations.

## Features

- Parse ePub files to extract text content
- Convert text to natural-sounding speech using Fish Audio
- Support for adjusting voice parameters (speed, pitch, voice selection)
- Save output as MP3 files
- Progress tracking for long conversions
- Support for chapter-by-chapter conversion

## Technical Requirements

- Python 3.11+
- Poetry for dependency management
- Fish Audio for text-to-speech synthesis
- Pydantic for data validation and settings management

## Development Plan

### Phase 1: Project Setup and ePub Parsing

1. Set up project structure and configuration
   - Initialize Poetry project
   - Configure dependencies
   - Set up basic CLI structure

2. Implement ePub parsing
   - Extract metadata (title, author, chapters)
   - Extract text content from ePub files
   - Handle different ePub formats and structures

### Phase 2: Text Processing and Fish Audio Integration

3. Implement text processing
   - Clean and prepare text for TTS conversion
   - Split content into appropriate chunks for processing
   - Handle formatting, special characters, and dialogue

4. Integrate with Fish Audio
   - Set up API authentication
   - Implement text-to-speech conversion
   - Support voice selection and customization

### Phase 3: Audio Processing and Output

5. Implement audio processing
   - Save audio segments
   - Merge audio segments into chapters
   - Add metadata to audio files

6. Create progress tracking and user feedback
   - Display conversion progress
   - Handle errors gracefully
   - Provide estimated completion time

### Phase 4: Refinement and Additional Features

7. Optimize performance
   - Implement parallel processing for faster conversion
   - Add caching mechanisms

8. Add advanced features
   - Support for customizing output format
   - Add ability to resume interrupted conversions
   - Support for batch processing of multiple books

## Installation & Usage

(To be added as development progresses)

## License

(To be determined)
