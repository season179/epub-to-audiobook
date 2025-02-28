"""
Kokoro TTS module.

This module provides functions to convert text to speech using the Kokoro TTS model.
"""

import os
from typing import BinaryIO, List
import soundfile as sf
import numpy as np

from dotenv import load_dotenv, find_dotenv

# Attempt to load environment variables from .env file
load_dotenv(find_dotenv())


class KokoroTTS:
    """A class to handle text-to-speech conversion using the Kokoro TTS model."""

    def __init__(self, lang_code: str = "a"):
        """
        Initialize the KokoroTTS class.

        Args:
            lang_code: Language code for the TTS model.
                       'a' - American English (default)
                       'b' - British English
                       'j' - Japanese (requires misaki[ja])
                       'z' - Mandarin Chinese (requires misaki[zh])
                       'e' - Spanish
                       'f' - French
                       'h' - Hindi
                       'i' - Italian
                       'p' - Brazilian Portuguese
        """
        # Import dependencies here to avoid import errors if packages aren't installed
        try:
            from kokoro import KPipeline

            self.lang_code = lang_code
            self.pipeline = KPipeline(lang_code=lang_code)
        except ImportError:
            raise ImportError(
                "The kokoro package is required. "
                "Install it with: pip install kokoro>=0.8.2 soundfile"
            )

    def text_to_speech(
        self,
        text: str,
        output_file: BinaryIO,
        voice: str = "af_heart",
        speed: float = 1.0,
        split_pattern: str = r"\n+",
        audio_format: str = "wav",
    ) -> None:
        """
        Convert text to speech and write the audio to the specified file.

        Args:
            text: The text to convert to speech.
            output_file: A file-like object (opened in binary write mode) to write the audio to.
            voice: Voice ID to use (e.g., 'af_heart').
            speed: Speech speed multiplier (1.0 is normal speed).
            split_pattern: Regex pattern to split text into chunks.
            audio_format: Output audio format ("wav" or "mp3").
        """
        # Validate parameters
        if audio_format not in ["wav", "mp3"]:
            raise ValueError("Audio format must be one of 'wav' or 'mp3'")

        # Sample rate for Kokoro TTS is 24000 Hz
        sample_rate = 24000

        # Generate audio from the text
        try:
            # Collect all audio chunks
            audio_chunks = []
            for _, _, audio in self.pipeline(
                text, voice=voice, speed=speed, split_pattern=split_pattern
            ):
                audio_chunks.append(audio)

            # Combine all audio chunks
            if not audio_chunks:
                raise ValueError("No audio was generated")

            combined_audio = np.concatenate(audio_chunks)

            # Write the audio to the output file
            if audio_format == "wav":
                sf.write(output_file, combined_audio, sample_rate)
            elif audio_format == "mp3":
                try:
                    from pydub import AudioSegment
                    import tempfile

                    # First save as WAV to a temporary file
                    with tempfile.NamedTemporaryFile(
                        suffix=".wav", delete=False
                    ) as temp_wav:
                        temp_wav_path = temp_wav.name
                        sf.write(temp_wav_path, combined_audio, sample_rate)

                    # Convert WAV to MP3
                    audio_segment = AudioSegment.from_wav(temp_wav_path)
                    audio_segment.export(output_file, format="mp3")

                    # Clean up temporary file
                    os.unlink(temp_wav_path)

                except ImportError:
                    raise ImportError(
                        "The pydub package is required for MP3 conversion. "
                        "Install it with: pip install pydub"
                    )
        except Exception as e:
            raise RuntimeError(f"Error generating audio with Kokoro TTS: {str(e)}")

    def list_available_voices(self) -> List[str]:
        """
        List all available voices for the current language code.

        Returns:
            A list of available voice IDs.
        """
        # This is a simplified implementation as Kokoro doesn't expose a direct
        # API for this. In practice, you'd want to check what voices are actually
        # available for each language.

        # Common voices by language code
        voices_by_lang = {
            "a": ["af_heart", "af_nova", "af_calm", "af_bella"],  # American English
            "b": ["bf_calm", "bf_nova"],  # British English
            "j": ["jf_heart"],  # Japanese
            "z": ["zf_heart"],  # Chinese
            "e": ["ef_heart"],  # Spanish
            "f": ["ff_heart"],  # French
            "h": ["hf_heart"],  # Hindi
            "i": ["if_heart"],  # Italian
            "p": ["pf_heart"],  # Portuguese
        }

        return voices_by_lang.get(self.lang_code, ["af_heart"])
