# Changelog

## 2026 — Major reframe: community sovereignty edition

Prepared as the digital companion to "AI Techniques for Indigenous Cultural Expression" in *Envisioning Indigenous Methods in Digital Media and Ecologies*.

### Philosophy shift

The original repository (2020) was output-centric: produce an LJSpeech-format dataset for TTS training. This version reframes the entire workflow around community control and Indigenous data sovereignty. The question is no longer "how do we get training data?" but "how does a community maintain authority over its own voices?"

### Governance and documentation added

- `CARE_PRINCIPLES.md` — how the CARE Principles for Indigenous Data Governance (Collective Benefit, Authority to Control, Responsibility, Ethics) are enacted in this repo
- `docs/community_agreement_template.md` — plain-language (not legal) speaker consent template covering ownership tiers, cultural protocols, and withdrawal rights
- `docs/what_not_to_digitize.md` — decision framework for identifying recordings that should not become training data
- `docs/adapted_datasheet_for_indigenous_datasets.md` — OCAP®-based institutional governance template for dataset-level documentation
- `docs/metadata_schema.md` — field-by-field documentation for the CARE-aligned metadata schema
- `metadata/metadata_template.csv` — structured provenance template with consent tiers, cultural protocol notes, and exclusion flags

### Transcription pathways restructured

The original repository used a single Google Cloud Speech-to-Text script (`wav_to_text.py`). This has been replaced with three local pathways, routed by language:

| Old | New |
|---|---|
| `scripts/wav_to_text.py` (Google Cloud STT) | `notebooks/02a_transcribe_whisper.ipynb` (local Whisper) |
| — | `notebooks/02b_transcribe_mms.ipynb` (local Meta MMS, for Cree syllabics, Ojibwe, Mi'kmaq, and others) |
| — | `notebooks/02c_transcribe_manual.ipynb` (manual transcription workflow for languages not covered by either tool) |

No audio leaves community infrastructure. No cloud credentials required.

### Synthetic voice generation removed

`scripts/text_to_wav.py` (Google Cloud TTS) has been removed. Generating synthetic training data from a corporate voice model contradicts the goal of building community voice models. Pathway 3 now uses speaker augmentation (speed perturbation, pitch shifting, additive noise) on real consented recordings instead.

### Scripts updated

| Old | New | Change |
|---|---|---|
| `scripts/markersfile_to_metadata.py` | `scripts/export_metadata.py` | Outputs CARE-aligned metadata CSV; adds `--ljspeech` flag and `--metadata-template` merge |
| `scripts/wav_to_text.py` | removed | Replaced by notebook pathways above |
| `scripts/text_to_wav.py` | removed | Synthetic generation removed |

### Notebooks added

- `notebooks/01_record_and_segment.ipynb` — Audacity recording workflow with routing table to 02a/02b/02c
- `notebooks/03_snr_quality_analysis.ipynb` — migrated from Google Colab; runs locally; adds community framing around SNR as a quality gate, not the only gate
- `notebooks/04_augmentation.ipynb` — speaker augmentation replacing synthetic voice generation
- `notebooks/05_export_ljspeech.ipynb` — filters by `exclude_from_training` and `consent_tier` before export

### Dependencies

- Removed: `google-cloud-speech`, `google-cloud-texttospeech`, `torchaudio`
- Added: `openai-whisper`, `transformers` (for MMS), `pydub`, `librosa`, `audiomentations`, `protobuf`
- Dependency management: `uv` with `uv.lock` (hash verification, no `pip install` in notebooks)

---

## 2020 — Initial release

Original repository for transcribing English and Spanish voice recordings using Google Cloud Speech-to-Text and generating synthetic training data with Google Cloud Text-to-Speech. LJSpeech format output for TTS model training.
