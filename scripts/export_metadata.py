"""
export_metadata.py — Convert Audition or Audacity marker files into CARE-aligned metadata CSV.

Replaces markersfile_to_metadata.py. Merges transcript/filename data from the
marker file with CARE fields from a pre-filled metadata template, then outputs
a full metadata CSV. Optionally also exports an LJSpeech-format metadata.csv.

Usage:
    # Audacity workflow
    python scripts/export_metadata.py audacity

    # Audition workflow with custom paths
    python scripts/export_metadata.py audition \\
        --wavs-export-path test_data/wavs_export_audition/ \\
        --input-filename test_data/Markers.csv \\
        --output-filename test_data/metadata_care.csv

    # Include LJSpeech export alongside CARE metadata
    python scripts/export_metadata.py audacity --ljspeech
"""

import argparse
import os
import sys
from shutil import copyfile, rmtree

import pandas as pd

CARE_COLUMNS = [
    "file_id",
    "transcript",
    "speaker_id",
    "language",
    "consent_tier",
    "cultural_protocol",
    "knowledge_keeper_reviewed",
    "exclude_from_training",
    "exclude_reason",
    "recorded_by",
    "recording_date",
    "provenance_note",
]


def load_marker_file(file_type: str, input_filename: str) -> pd.DataFrame:
    if file_type == "audition":
        df = pd.read_csv(input_filename, sep="\t", encoding="utf-8")
        return df[["Name", "Description"]].rename(
            columns={"Name": "marker_name", "Description": "transcript"}
        )
    elif file_type == "audacity":
        df = pd.read_csv(
            input_filename,
            sep="\t",
            encoding="utf-8",
            header=None,
        )
        # Audacity label format: start_time, end_time, label
        # When STT output is appended it uses columns: start, end, name, description
        if df.shape[1] >= 4:
            return df.iloc[:, [2, 3]].rename(
                columns={df.columns[2]: "marker_name", df.columns[3]: "transcript"}
            )
        else:
            return df.iloc[:, [2]].rename(columns={df.columns[2]: "marker_name"}).assign(transcript="")
    else:
        raise ValueError(f"Unknown file_type: {file_type}")


def normalize_filename(name: str) -> str:
    return str(name).replace(" ", "_").replace("M", "m")


def build_care_row(file_id: str, transcript: str, template_row: pd.Series | None) -> dict:
    row = {col: "" for col in CARE_COLUMNS}
    row["file_id"] = file_id
    row["transcript"] = transcript

    if template_row is not None:
        for col in CARE_COLUMNS:
            if col in template_row.index and pd.notna(template_row[col]):
                row[col] = template_row[col]
        # transcript from marker file takes precedence over template
        row["file_id"] = file_id
        row["transcript"] = transcript

    return row


def run(
    file_type: str,
    wavs_export_path: str,
    wavs_final_path: str,
    input_filename: str,
    output_filename: str,
    metadata_template: str | None,
    ljspeech: bool,
) -> None:
    markers = load_marker_file(file_type, input_filename)

    template_df = None
    if metadata_template and os.path.exists(metadata_template):
        template_df = pd.read_csv(metadata_template, encoding="utf-8", dtype=str)
        if "file_id" in template_df.columns:
            template_df = template_df.set_index("file_id")

    if os.path.exists(wavs_final_path):
        rmtree(wavs_final_path)
    os.makedirs(wavs_final_path, exist_ok=True)

    care_rows = []
    ljspeech_lines = []

    for _, row in markers.iterrows():
        if pd.isnull(row.get("transcript", None)):
            continue

        wav_orig = str(row["marker_name"]) + ".wav"
        wav_norm = normalize_filename(wav_orig)
        file_id = wav_norm.replace(".wav", "")
        transcript = str(row["transcript"]).strip()

        src = os.path.join(wavs_export_path, wav_orig)
        dst = os.path.join(wavs_final_path, wav_norm)
        if os.path.exists(src):
            copyfile(src, dst)
        else:
            print(f"Warning: WAV not found: {src}", file=sys.stderr)

        template_row = None
        if template_df is not None and file_id in template_df.index:
            template_row = template_df.loc[file_id]

        care_rows.append(build_care_row(file_id, transcript, template_row))

        if ljspeech:
            exclude = False
            if template_row is not None:
                exclude = str(template_row.get("exclude_from_training", "false")).lower() == "true"
                consent = str(template_row.get("consent_tier", "open")).lower()
                if consent == "restricted":
                    exclude = True
            if not exclude:
                ljspeech_lines.append(f"{file_id}|{transcript}|{transcript}")

    out_df = pd.DataFrame(care_rows, columns=CARE_COLUMNS)
    out_df.to_csv(output_filename, index=False, encoding="utf-8")
    print(f"CARE metadata written to {output_filename} ({len(care_rows)} rows)")

    if ljspeech:
        ljspeech_path = output_filename.replace(".csv", "_ljspeech.csv")
        with open(ljspeech_path, "w", encoding="utf-8") as f:
            f.write("\n".join(ljspeech_lines) + "\n")
        print(f"LJSpeech metadata written to {ljspeech_path} ({len(ljspeech_lines)} rows)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Audition/Audacity markers to CARE-aligned metadata CSV.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    for cmd, defaults in [
        (
            "audition",
            {
                "wavs_export_path": "../test_data/wavs_export_audition/",
                "input_filename": "../test_data/Markers.csv",
            },
        ),
        (
            "audacity",
            {
                "wavs_export_path": "../test_data/wavs_export_audacity/",
                "input_filename": "../test_data/Label Track STT.txt",
            },
        ),
    ]:
        p = subparsers.add_parser(cmd)
        p.add_argument("--wavs-export-path", default=defaults["wavs_export_path"])
        p.add_argument("--wavs-final-path", default="../test_data/wavs/")
        p.add_argument("--input-filename", default=defaults["input_filename"])
        p.add_argument("--output-filename", default="../test_data/metadata_care.csv")
        p.add_argument(
            "--metadata-template",
            default=None,
            help="Path to pre-filled metadata_template.csv with CARE fields to merge",
        )
        p.add_argument(
            "--ljspeech",
            action="store_true",
            help="Also export an LJSpeech-format CSV (filtered by consent_tier and exclude_from_training)",
        )

    args = parser.parse_args()
    run(
        file_type=args.command,
        wavs_export_path=args.wavs_export_path,
        wavs_final_path=args.wavs_final_path,
        input_filename=args.input_filename,
        output_filename=args.output_filename,
        metadata_template=args.metadata_template,
        ljspeech=args.ljspeech,
    )


if __name__ == "__main__":
    main()
