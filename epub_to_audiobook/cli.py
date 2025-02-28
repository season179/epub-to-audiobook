"""
Command line interface for the EPUB to Audiobook converter using various TTS engines.
"""

import argparse
import sys
from pathlib import Path

from epub_to_audiobook.fish_audio import FishAudioTTS


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Convert text to speech using various TTS engines",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "text",
        help="Text to convert to speech. Use quotes for text with spaces. "
        "For longer text, use --file instead.",
        nargs="?",
    )

    parser.add_argument(
        "--file",
        "-f",
        help="Path to a text file containing the text to convert",
        type=Path,
    )

    parser.add_argument(
        "--output",
        "-o",
        help="Path to save the output audio file",
        type=Path,
        default=Path("output.wav"),
    )
    
    parser.add_argument(
        "--engine",
        help="TTS engine to use",
        choices=["fish", "kokoro"],
        default="kokoro",
    )
    
    # Fish Audio specific arguments
    fish_group = parser.add_argument_group("Fish Audio TTS options")
    fish_group.add_argument(
        "--reference-id",
        "-r",
        help="ID of a voice model to use (Fish Audio only)",
    )

    fish_group.add_argument(
        "--bitrate",
        help="MP3 bitrate for Fish Audio (only applicable if format is mp3)",
        type=int,
        choices=[64, 128, 192],
        default=128,
    )

    fish_group.add_argument(
        "--chunk-length",
        help="Length of each chunk in milliseconds (Fish Audio only)",
        type=int,
        default=200,
        choices=range(100, 301),
        metavar="[100-300]",
    )

    fish_group.add_argument(
        "--no-normalize",
        help="Disable text normalization (Fish Audio only)",
        action="store_true",
    )

    fish_group.add_argument(
        "--latency",
        help="Latency mode (Fish Audio only)",
        choices=["normal", "balanced"],
        default="normal",
    )
    
    # Kokoro TTS specific arguments
    kokoro_group = parser.add_argument_group("Kokoro TTS options")
    kokoro_group.add_argument(
        "--lang-code",
        help="Language code for Kokoro TTS",
        choices=["a", "b", "j", "z", "e", "f", "h", "i", "p"],
        default="a",
    )
    
    kokoro_group.add_argument(
        "--voice",
        help="Voice ID for Kokoro TTS",
        default="af_heart",
    )
    
    kokoro_group.add_argument(
        "--speed",
        help="Speech speed multiplier for Kokoro TTS",
        type=float,
        default=1.0,
    )
    
    kokoro_group.add_argument(
        "--split-pattern",
        help="Regex pattern to split text for Kokoro TTS",
        default=r"\n+",
    )

    parser.add_argument(
        "--format",
        help="Output audio format",
        choices=["mp3", "wav", "pcm"],
        default="wav",
    )

    args = parser.parse_args()

    # Validate input arguments
    if not args.text and not args.file:
        parser.error("Either text or --file must be provided")

    if args.text and args.file:
        parser.error("Cannot provide both text and --file")

    # Get the text to convert
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = args.text

    # Create the output directory if it doesn't exist
    output_dir = args.output.parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    
    # Use the selected TTS engine
    try:
        if args.engine == "fish":
            # Fish Audio TTS
            try:
                tts = FishAudioTTS()
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            except ImportError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
                
            print("Converting text to speech using Fish Audio...", file=sys.stderr)
            with open(args.output, "wb") as output_file:
                tts.text_to_speech(
                    text=text,
                    output_file=output_file,
                    reference_id=args.reference_id,
                    audio_format=args.format,
                    bitrate=args.bitrate,
                    chunk_length=args.chunk_length,
                    normalize=not args.no_normalize,
                    latency=args.latency,
                )
        else:
            # Kokoro TTS
            from epub_to_audiobook.kokoro_tts import KokoroTTS
            
            try:
                tts = KokoroTTS(lang_code=args.lang_code)
            except ImportError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
                
            print("Converting text to speech using Kokoro TTS...", file=sys.stderr)
            with open(args.output, "wb") as output_file:
                tts.text_to_speech(
                    text=text,
                    output_file=output_file,
                    voice=args.voice,
                    speed=args.speed,
                    split_pattern=args.split_pattern,
                    audio_format=args.format if args.format != "pcm" else "wav",
                )
                
        print(f"Audio saved to {args.output}", file=sys.stderr)
    except Exception as e:
        print(f"Error converting text to speech: {e}", file=sys.stderr)
        sys.exit(1)


def app():
    """Entry point for the CLI when installed via pip."""
    main()


if __name__ == "__main__":
    main()
