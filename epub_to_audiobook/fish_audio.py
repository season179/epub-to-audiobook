"""
Fish Audio Text-to-Speech module.

This module provides functions to convert text to speech using Fish Audio's API.
"""

import os
from typing import BinaryIO

from dotenv import load_dotenv, find_dotenv

# Attempt to load environment variables from .env file
load_dotenv(find_dotenv())


class FishAudioTTS:
    """A class to handle text-to-speech conversion using Fish Audio's API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the FishAudioTTS class.

        Args:
            api_key: The Fish Audio API key. If not provided, it will be loaded from the
                     FISH_AUDIO_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("FISH_AUDIO_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Either pass it to the constructor or set the "
                "FISH_AUDIO_API_KEY environment variable."
            )

        # Import here to avoid import errors if the package isn't installed
        try:
            from fish_audio_sdk import Session

            self.session = Session(self.api_key)
        except ImportError:
            raise ImportError(
                "The fish_audio_sdk package is required. "
                "Install it with: pip install fish-audio-sdk"
            )

    def text_to_speech(
        self,
        text: str,
        output_file: BinaryIO,
        reference_id: str = "b545c585f631496c914815291da4e893",
        audio_format: str = "wav",
        bitrate: int = 128,
        chunk_length: int = 200,
        normalize: bool = True,
        latency: str = "normal",
    ) -> None:
        """
        Convert text to speech and write the audio to the specified file.

        Args:
            text: The text to convert to speech.
            output_file: A file-like object (opened in binary write mode) to write the audio to.
            reference_id: ID of a voice model to use.
            audio_format: Output audio format ("mp3", "wav", or "pcm").
            bitrate: MP3 bitrate (64, 128, or 192).
            chunk_length: Length of each chunk in milliseconds (100-300).
            normalize: Whether to normalize the text (recommended for better stability).
            latency: Latency mode ("normal" or "balanced").
        """
        from fish_audio_sdk import TTSRequest

        # Validate parameters
        if audio_format not in ["mp3", "wav", "pcm"]:
            raise ValueError("Audio format must be one of 'mp3', 'wav', or 'pcm'")

        if bitrate not in [64, 128, 192]:
            raise ValueError("MP3 bitrate must be one of 64, 128, or 192")

        if not (100 <= chunk_length <= 300):
            raise ValueError("Chunk length must be between 100 and 300")

        if latency not in ["normal", "balanced"]:
            raise ValueError("Latency must be one of 'normal' or 'balanced'")

        # Create the TTS request
        request = TTSRequest(
            text=text,
            reference_id=reference_id,
            format=audio_format,
            mp3_bitrate=bitrate,
            chunk_length=chunk_length,
            normalize=normalize,
            latency=latency,
        )

        # Process the request and write the audio to the output file
        for chunk in self.session.tts(request):
            output_file.write(chunk)

    def apply_phoneme_control(self, text: str, phonemes: dict) -> str:
        """
        Apply phoneme control to specific words in the text.

        Args:
            text: The original text.
            phonemes: A dictionary mapping words to their phonetic representation.

        Returns:
            The text with phoneme control tags applied.
        """
        for word, phoneme in phonemes.items():
            replacement = f"<|phoneme_start|>{phoneme}<|phoneme_end|>"
            text = text.replace(word, replacement)
        return text
