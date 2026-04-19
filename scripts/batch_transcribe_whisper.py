"""
batch_transcribe_whisper.py — Whisper-based local transcription for voice dataset creation.

Audio never leaves the local machine. No API keys or cloud credentials required.

Usage:
    python scripts/batch_transcribe_whisper.py \
        --input-dir test_data/wavs_export_audacity \
        --output-csv test_data/transcripts.csv \
        --model base \
        --language en

Language code note:
    --language takes an ISO 639-1 code (e.g. 'en', 'fr', 'mi' for Māori) because
    that is what Whisper expects. The project's metadata `language` field uses
    ISO 639-3 (e.g. 'eng', 'fra', 'mri' for Māori). Translate between the two
    when filling metadata. MMS (see 03b_transcribe_mms.ipynb) uses ISO 639-3
    directly, so no translation is needed on that pathway.
"""

import argparse
import csv
import os
import sys

from tqdm import tqdm


def transcribe(input_dir: str, output_csv: str, model_name: str, language: str | None) -> None:
    try:
        import whisper
    except ImportError:
        print("openai-whisper is not installed. Run: uv sync --extra dev", file=sys.stderr)
        sys.exit(1)

    wav_files = sorted(
        f for f in os.listdir(input_dir) if f.lower().endswith(".wav")
    )
    if not wav_files:
        print(f"No WAV files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    # Resume: skip file_ids already present in the output CSV. Lets the operator
    # re-run after an interruption without re-transcribing completed files.
    already_done: set[str] = set()
    if os.path.exists(output_csv):
        with open(output_csv, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            already_done = {row["file_id"] for row in reader if row.get("file_id")}

    pending = [f for f in wav_files if os.path.splitext(f)[0] not in already_done]
    if already_done:
        print(f"Resuming: {len(already_done)} already transcribed, {len(pending)} remaining.")
    if not pending:
        print(f"All files already transcribed in {output_csv}. Nothing to do.")
        return

    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    write_header = not os.path.exists(output_csv) or os.path.getsize(output_csv) == 0
    with open(output_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file_id", "transcript"])
        if write_header:
            writer.writeheader()

        for filename in tqdm(pending, desc="Transcribing"):
            file_id = os.path.splitext(filename)[0]
            filepath = os.path.join(input_dir, filename)

            options = {}
            if language:
                options["language"] = language

            result = model.transcribe(filepath, **options)
            writer.writerow({"file_id": file_id, "transcript": result["text"].strip()})
            f.flush()

    print(f"Transcriptions written to {output_csv}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Transcribe WAV files using local Whisper inference. "
            "No audio is sent to any external service."
        )
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing WAV files to transcribe",
    )
    parser.add_argument(
        "--output-csv",
        required=True,
        help="Path to output CSV (file_id, transcript)",
    )
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        help="Whisper model size (default: base). Use large-v3 for final production pass.",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="ISO 639-1 language code (e.g. 'en', 'fr', 'mi' for Māori). "
             "Note: the project's metadata `language` field uses ISO 639-3 "
             "(e.g. 'mri' for Māori) — translate when filling metadata. "
             "Leave unset for automatic detection.",
    )
    args = parser.parse_args()
    transcribe(args.input_dir, args.output_csv, args.model, args.language)


if __name__ == "__main__":
    main()
