"""
segment_on_silence.py — Split a WAV file on silence and export segments.

Outputs numbered WAV files and a Label Track.txt compatible with Audacity,
so the result integrates with the rest of the Audacity-based workflow.

Usage:
    python scripts/segment_on_silence.py \
        --input recording.wav \
        --output-dir test_data/wavs_export_audacity \
        --min-silence-len 700 \
        --silence-thresh -40
"""

import argparse
import os
import sys


def segment(
    input_path: str,
    output_dir: str,
    min_silence_len: int,
    silence_thresh: int,
    keep_silence: int,
) -> None:
    try:
        from pydub import AudioSegment
        from pydub.silence import split_on_silence
    except ImportError:
        print("pydub is not installed. Run: uv pip install pydub", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {input_path}...")
    audio = AudioSegment.from_wav(input_path)

    print(
        f"Splitting on silence (min_silence_len={min_silence_len}ms, "
        f"silence_thresh={silence_thresh}dBFS)..."
    )
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence,
    )

    if not chunks:
        print("No segments found. Try lowering --silence-thresh or --min-silence-len.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    label_lines = []
    cursor_ms = 0

    for i, chunk in enumerate(chunks, start=1):
        filename = f"{i}.wav"
        filepath = os.path.join(output_dir, filename)
        chunk.export(filepath, format="wav")

        start_s = cursor_ms / 1000.0
        end_s = (cursor_ms + len(chunk)) / 1000.0
        label_lines.append(f"{start_s:.6f}\t{end_s:.6f}\t{i}")
        cursor_ms += len(chunk)

    label_path = os.path.join(output_dir, "Label Track.txt")
    with open(label_path, "w", encoding="utf-8") as f:
        f.write("\n".join(label_lines) + "\n")

    print(f"Exported {len(chunks)} segments to {output_dir}/")
    print(f"Label file written to {label_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split a WAV file on silence and export Audacity-compatible segments."
    )
    parser.add_argument("--input", required=True, help="Input WAV file path")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to write segment WAVs and Label Track.txt",
    )
    parser.add_argument(
        "--min-silence-len",
        type=int,
        default=700,
        help="Minimum silence length in milliseconds to split on (default: 700)",
    )
    parser.add_argument(
        "--silence-thresh",
        type=int,
        default=-40,
        help="Silence threshold in dBFS (default: -40). Lower = more sensitive.",
    )
    parser.add_argument(
        "--keep-silence",
        type=int,
        default=200,
        help="Milliseconds of silence to keep at the start/end of each chunk (default: 200)",
    )
    args = parser.parse_args()
    segment(
        args.input,
        args.output_dir,
        args.min_silence_len,
        args.silence_thresh,
        args.keep_silence,
    )


if __name__ == "__main__":
    main()
