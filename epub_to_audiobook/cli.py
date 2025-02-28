"""
Command line interface for the EPUB to Audiobook converter using Fish Audio TTS.
"""

import argparse
import sys
from pathlib import Path

from epub_to_audiobook.fish_audio import FishAudioTTS


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Convert text to speech using Fish Audio's TTS API",
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
        default=Path("output.mp3"),
    )

    parser.add_argument(
        "--reference-id",
        "-r",
        help="ID of a voice model to use",
    )

    parser.add_argument(
        "--format",
        help="Output audio format",
        choices=["mp3", "wav", "pcm"],
        default="wav",
    )

    parser.add_argument(
        "--bitrate",
        help="MP3 bitrate (only applicable if format is mp3)",
        type=int,
        choices=[64, 128, 192],
        default=128,
    )

    parser.add_argument(
        "--chunk-length",
        help="Length of each chunk in milliseconds",
        type=int,
        default=200,
        choices=range(100, 301),
        metavar="[100-300]",
    )

    parser.add_argument(
        "--no-normalize",
        help="Disable text normalization",
        action="store_true",
    )

    parser.add_argument(
        "--latency",
        help="Latency mode",
        choices=["normal", "balanced"],
        default="normal",
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

    # Create the TTS instance
    try:
        tts = FishAudioTTS()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Create the output directory if it doesn't exist
    output_dir = args.output.parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Convert the text to speech
    try:
        print("Converting text to speech...", file=sys.stderr)
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
        print(f"Audio saved to {args.output}", file=sys.stderr)
    except Exception as e:
        print(f"Error converting text to speech: {e}", file=sys.stderr)
        sys.exit(1)


def app():
    """Entry point for the CLI when installed via pip."""
    main()


if __name__ == "__main__":
    main()
