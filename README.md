# ePub to Audiobook Converter

A command-line application that converts ePub files into audiobooks using multiple text-to-speech engines.

## Overview

This application allows users to convert their ePub books into high-quality audiobooks that can be listened to on various devices. It supports multiple TTS engines including Fish Audio and Kokoro for natural-sounding narrations.

## Features

- Parse ePub files to extract text content
- Convert text to natural-sounding speech using multiple TTS engines:
  - Fish Audio TTS - a high-quality cloud-based TTS service
  - Kokoro TTS - an open-weight local TTS model with 82M parameters
- Support for adjusting voice parameters (speed, pitch, voice selection)
- Save output as MP3 or WAV files
- Progress tracking for long conversions
- Support for chapter-by-chapter conversion
- Multiple language support (with Kokoro TTS)

## Technical Requirements

- Python 3.11+
- Poetry for dependency management
- For Fish Audio TTS:
  - Fish Audio API key
  - Internet connection
- For Kokoro TTS:
  - espeak-ng (for phoneme conversion)
  - Sufficient RAM for running ML models
- Pydantic for data validation and settings management

## TTS Engines

### Fish Audio

Fish Audio is a cloud-based TTS service that provides high-quality voice synthesis. To use it, you'll need:
- A Fish Audio API key (set as `FISH_AUDIO_API_KEY` environment variable)
- Internet connection

### Kokoro

Kokoro is an open-weight TTS model with 82 million parameters that runs locally. Features:
- No API key required
- Multiple language support:
  - English (American and British)
  - Japanese
  - Chinese (Mandarin)
  - Spanish
  - French
  - Hindi
  - Italian
  - Portuguese (Brazilian)
- Customizable voice options
- Adjustable speech speed

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

### Phase 2: Text Processing and TTS Integration

3. Implement text processing
   - Clean and prepare text for TTS conversion
   - Split content into appropriate chunks for processing
   - Handle formatting, special characters, and dialogue

4. Integrate with TTS Engines
   - Implement Fish Audio integration (cloud-based TTS)
   - Implement Kokoro integration (local open-source TTS)
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

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/epub-to-audiobook.git
cd epub-to-audiobook

# Install dependencies
poetry install

# For Kokoro TTS, install espeak-ng
# On macOS:
brew install espeak-ng

# On Ubuntu/Debian:
# sudo apt-get install espeak-ng
```

### Usage

Basic usage:

```bash
# Using Fish Audio TTS (default)
poetry run python -m epub_to_audiobook.cli "Hello world" --output hello.wav

# Using Kokoro TTS
poetry run python -m epub_to_audiobook.cli "Hello world" --engine kokoro --output hello.wav

# Convert a text file using Kokoro TTS
poetry run python -m epub_to_audiobook.cli --file mybook.txt --engine kokoro --output mybook.mp3 --format mp3 --voice af_heart
```

For more options:

```bash
poetry run python -m epub_to_audiobook.cli --help
```

## License

(To be determined)
