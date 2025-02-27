"""Audio utilities for the ePub to Audiobook converter."""

from pathlib import Path
from typing import List, Optional

from pydub import AudioSegment


def merge_audio_files(audio_files: List[Path], output_file: Path) -> Path:
    """Merge multiple audio files into a single file.
    
    Args:
        audio_files: List of audio files to merge
        output_file: Path to the output file
        
    Returns:
        Path to the merged audio file
    """
    # Create combined audio segment
    combined = AudioSegment.empty()
    
    # Append each audio file
    for file in audio_files:
        segment = AudioSegment.from_file(file)
        combined += segment
    
    # Create directory if it doesn't exist
    output_file.parent.mkdir(exist_ok=True, parents=True)
    
    # Export to file
    combined.export(output_file, format="mp3")
    
    return output_file


def add_silence(audio_file: Path, duration_ms: int = 500, at_beginning: bool = True) -> Path:
    """Add silence to the beginning or end of an audio file.
    
    Args:
        audio_file: Path to the audio file
        duration_ms: Duration of silence in milliseconds
        at_beginning: Whether to add the silence at the beginning or end
        
    Returns:
        Path to the modified audio file
    """
    # Load audio
    audio = AudioSegment.from_file(audio_file)
    
    # Create silence
    silence = AudioSegment.silent(duration=duration_ms)
    
    # Add silence
    if at_beginning:
        modified = silence + audio
    else:
        modified = audio + silence
    
    # Export to file
    modified.export(audio_file, format="mp3", overwrite=True)
    
    return audio_file
