"""
Smoke tests for scripts/export_metadata.py using test_data/ fixtures.
"""

import csv
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest

# Allow importing from scripts/
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from export_metadata import load_marker_file, run


REPO_ROOT = Path(__file__).parent.parent
TEST_DATA = REPO_ROOT / "test_data"


class TestLoadMarkerFile:
    def test_audacity_label_track(self):
        """Audacity Label Track.txt loads with marker_name and transcript columns."""
        # Create a minimal STT-style label file (4 columns: start, end, name, description)
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("0.0\t1.5\t1\tHello world\n")
            f.write("2.0\t5.0\t2\tLanguage preservation\n")
            tmp_path = f.name

        try:
            df = load_marker_file("audacity", tmp_path)
            assert list(df.columns) == ["marker_name", "transcript"]
            assert len(df) == 2
            assert df.iloc[0]["transcript"] == "Hello world"
        finally:
            os.unlink(tmp_path)

    def test_audition_markers_csv(self):
        """Audition Markers.csv loads with marker_name and transcript columns."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write("Name\tDescription\tExtra\n")
            f.write("Marker 19\tFirst sentence\t0:01.000\n")
            f.write("Marker 20\tSecond sentence\t0:05.000\n")
            tmp_path = f.name

        try:
            df = load_marker_file("audition", tmp_path)
            assert list(df.columns) == ["marker_name", "transcript"]
            assert df.iloc[0]["marker_name"] == "Marker 19"
            assert df.iloc[1]["transcript"] == "Second sentence"
        finally:
            os.unlink(tmp_path)


class TestRunAudacity:
    def test_produces_care_metadata_csv(self):
        """run() with audacity format produces a CSV with all CARE columns."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as label_f:
            label_f.write("0.0\t1.5\t1\tFirst clip\n")
            label_f.write("2.0\t5.0\t2\tSecond clip\n")
            label_path = label_f.name

        with tempfile.TemporaryDirectory() as wavs_export, \
             tempfile.TemporaryDirectory() as wavs_final, \
             tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as out_f:
            output_path = out_f.name

        try:
            run(
                file_type="audacity",
                wavs_export_path=wavs_export + "/",
                wavs_final_path=wavs_final + "/",
                input_filename=label_path,
                output_filename=output_path,
                metadata_template=None,
                ljspeech=False,
            )

            df = pd.read_csv(output_path)
            assert "file_id" in df.columns
            assert "transcript" in df.columns
            assert "consent_tier" in df.columns
            assert "exclude_from_training" in df.columns
            assert len(df) == 2
            assert df.iloc[0]["transcript"] == "First clip"
        finally:
            os.unlink(label_path)
            os.unlink(output_path)

    def test_ljspeech_export_filters_excluded(self):
        """--ljspeech flag excludes rows where exclude_from_training=true."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as label_f:
            label_f.write("0.0\t1.5\t1\tKeep this\n")
            label_f.write("2.0\t5.0\t2\tAlso keep\n")
            label_f.write("6.0\t8.0\t3\tExclude this\n")
            label_path = label_f.name

        # Create a template with the third file excluded
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmpl_f:
            writer = csv.DictWriter(tmpl_f, fieldnames=[
                "file_id", "transcript", "speaker_id", "language", "consent_tier",
                "cultural_protocol", "knowledge_keeper_reviewed",
                "augmentation_permitted",
                "exclude_from_training", "exclude_reason",
                "recorded_by", "recording_date", "provenance_note",
            ])
            writer.writeheader()
            writer.writerow({"file_id": "1", "consent_tier": "open",
                             "exclude_from_training": "false"})
            writer.writerow({"file_id": "2", "consent_tier": "open",
                             "exclude_from_training": "false"})
            writer.writerow({"file_id": "3", "consent_tier": "open",
                             "exclude_from_training": "true",
                             "exclude_reason": "test exclusion"})
            tmpl_path = tmpl_f.name

        with tempfile.TemporaryDirectory() as wavs_export, \
             tempfile.TemporaryDirectory() as wavs_final, \
             tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as out_f:
            output_path = out_f.name

        try:
            run(
                file_type="audacity",
                wavs_export_path=wavs_export + "/",
                wavs_final_path=wavs_final + "/",
                input_filename=label_path,
                output_filename=output_path,
                metadata_template=tmpl_path,
                ljspeech=True,
            )

            ljspeech_path = output_path.replace(".csv", "_ljspeech.csv")
            assert os.path.exists(ljspeech_path), "LJSpeech file not created"

            with open(ljspeech_path, encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]

            file_ids = [line.split("|")[0] for line in lines]
            assert "3" not in file_ids, "Excluded file should not be in LJSpeech export"
            assert "1" in file_ids
            assert "2" in file_ids
        finally:
            os.unlink(label_path)
            os.unlink(tmpl_path)
            os.unlink(output_path)
            ljspeech_path = output_path.replace(".csv", "_ljspeech.csv")
            if os.path.exists(ljspeech_path):
                os.unlink(ljspeech_path)
