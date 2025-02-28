# ePub to Audiobook Converter

A command-line application that converts ePub files into audiobooks using multiple text-to-speech engines.

## Overview

This application allows users to convert their ePub books into high-quality audiobooks that can be listened to on various devices. It supports multiple TTS engines including Fish Audio and Kokoro for natural-sounding narrations.

## Features

- Parse ePub files to extract text content
- Convert text to natural-sounding speech using multiple TTS engines:
  - Kokoro TTS - an open-weight local TTS model with 82M parameters (default)
  - Fish Audio TTS - a high-quality cloud-based TTS service
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
# Using Kokoro TTS (default)
poetry run python -m epub_to_audiobook.cli "Hello world" --output hello.wav

# Using Fish Audio TTS
poetry run python -m epub_to_audiobook.cli "Hello world" --engine fish --output hello.wav

# Convert a text file using Kokoro TTS
poetry run python -m epub_to_audiobook.cli --file mybook.txt --output mybook.mp3 --format mp3 --voice af_heart
```

For more options:

```bash
poetry run python -m epub_to_audiobook.cli --help
```

## License

MIT License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
