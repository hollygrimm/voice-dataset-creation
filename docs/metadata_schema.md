# Metadata Schema

Every recording in this project is described by a row in `metadata/metadata_template.csv`. This document explains each field: what it means, what values it accepts, and why it exists.

The schema is designed around the CARE Principles — it captures not just what was recorded, but who authorized it, under what conditions, and what it can be used for.

---

## Fields

### `file_id`

**Type:** string
**Required:** yes

The WAV filename without the `.wav` extension. Must match the actual filename exactly.

Examples: `001`, `elder_mary_01`, `marker_19`

Avoid spaces — use underscores. Avoid names that identify speakers beyond their preference (see `speaker_id`).

---

### `transcript`

**Type:** string
**Required:** yes (unless `exclude_from_training` is true)

The verified text of what is spoken in the recording. This is the text that will appear in the LJSpeech export paired with the audio.

This field should reflect what was *actually spoken*, not a normalized or corrected version. If a speaker uses a dialect form, preserve it.

---

### `speaker_id`

**Type:** string
**Required:** yes

An identifier for the speaker. This can be:
- An anonymized code (e.g., `SPK_001`) if the speaker prefers privacy
- A name, if the speaker has explicitly consented to attribution
- A role (e.g., `knowledge_keeper_01`) if that is the speaker's preference

Set per the speaker's choice documented in the [Community Data Agreement](community_agreement_template.md).

---

### `language`

**Type:** string
**Required:** yes

The language spoken in the recording. Use [ISO 639-3](https://iso639-3.sil.org/) codes where available, followed by a dialect or variety note if relevant.

Examples:
- `miq` (Mi'kmaq)
- `mri-ngapuhi` (Maori, Ngapuhi dialect)
- `en-nova-scotia` (English, Nova Scotia variety)

If the recording is code-switching between languages, list both: `miq+en`

---

### `consent_tier`

**Type:** enum
**Required:** yes
**Values:** `open` | `community` | `restricted`

Controls what the recording can be used for:

| Value | Meaning |
|---|---|
| `open` | Can be included in a publicly released dataset or model |
| `community` | Can be used to train a community-held model; not for public release |
| `restricted` | For archival/preservation only; must not enter any training pipeline |

The LJSpeech export notebook (05) only includes `open` and `community` recordings by default. Override this only with explicit community approval.

---

### `cultural_protocol`

**Type:** string (free text)
**Required:** no, but strongly encouraged for any non-open recording

Free text field for cultural obligations that exist outside the technical schema. Use this to preserve context that would otherwise be lost.

Examples:
- `"seasonal restriction: winter ceremony context, November-February only"`
- `"elder knowledge: knowledge keeper review required before any external use"`
- `"women's teaching: appropriate for women's language programs only"`
- `"no restrictions noted"`

This field travels with the recording. Future users of the dataset should read it before making any decisions.

---

### `knowledge_keeper_reviewed`

**Type:** boolean (`true` / `false`)
**Required:** yes

Indicates whether a community knowledge keeper (elder, language custodian, or cultural authority) has reviewed this recording and its transcript.

For `restricted` recordings, this should always be `true` before the recording is considered finalized. For `open` recordings in a community language, this is strongly recommended.

---

### `augmentation_permitted`

**Type:** boolean (`true` / `false`)
**Required:** yes
**Default:** `false` (opt-in, not opt-out)

Whether the speaker (or community, per the ownership model) has consented to data augmentation — speed perturbation, pitch shifting, or additive noise — being applied to this recording.

Set from the speaker's choice documented in the [Community Data Agreement](community_agreement_template.md) ("Augmentation permitted: Yes / No").

The augmentation notebook ([notebooks/04_augmentation.ipynb](../notebooks/04_augmentation.ipynb)) filters on this field: recordings with `augmentation_permitted=false` or a missing value are not augmented. Augmented derivative rows inherit `true` from their source (they would not exist otherwise).

This field has no effect on LJSpeech export — the original recording is still eligible for training based on `consent_tier` and `exclude_from_training`. `augmentation_permitted` only governs whether *derivative copies* are created.

---

### `exclude_from_training`

**Type:** boolean (`true` / `false`)
**Required:** yes

If `true`, this recording will never be included in a training dataset export, regardless of `consent_tier`. It may still be archived and accessible to community members.

This is the mechanism that separates *preservation* from *training*. A recording can be in the archive without being in the model.

See [what_not_to_digitize.md](what_not_to_digitize.md) for guidance on when to set this to `true`.

---

### `exclude_reason`

**Type:** string
**Required:** only when `exclude_from_training` is `true`

A plain-language explanation of why this recording is excluded from training.

Examples:
- `"ceremonial content — archival only per elder council decision"`
- `"low SNR quality — background noise"`
- `"speaker withdrew consent"`
- `"duplicate of file_id 045"`

---

### `recorded_by`

**Type:** string
**Required:** yes

The name or identifier of the person or organization who made the recording.

---

### `recording_date`

**Type:** ISO 8601 date (`YYYY-MM-DD`)
**Required:** yes

The date the recording was made. For historical recordings being digitized, use the best available date and add a note in `provenance_note`.

---

### `provenance_note`

**Type:** string (free text)
**Required:** no, but required for augmented files

Free text for any additional context about the recording's origin or history.

Required values for augmented files: `"augmented from {source_file_id}"` — this ensures no downstream user mistakes a speed-perturbed or pitch-shifted recording for original speech.

Other examples:
- `"digitized from cassette tape, original recorded circa 1987"`
- `"segment 3 of 12 from session 2024-03-15"`
- `"background noise from outdoor recording session"`

---

## Minimal Valid Row

A recording ready for training export must have:

```
file_id, transcript, speaker_id, language, consent_tier, knowledge_keeper_reviewed=true, exclude_from_training=false, recorded_by, recording_date
```

All other fields are recommended but not blocking.

---

## Example Rows

See `metadata/metadata_template.csv` for example rows covering open, community, and excluded recordings.
