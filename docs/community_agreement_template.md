# Community Voice Recording Agreement

*This is a template. Communities should adapt it to their own protocols, governance structures, and languages before use. It is written in plain language, not legal language, as the goal is genuine understanding, not procedural compliance.*

---

## What We Are Doing

We are recording voices for the purpose of:

- [ ] Creating a voice dataset to train a speech recognition or text-to-speech model
- [ ] Archiving language for cultural preservation
- [ ] Research (describe: ___________________________________)
- [ ] Other: _______________________________________________

The recordings will be in the format of: spoken words / sentences / stories / songs / other: _______________

---

## Who Owns the Recordings

The recordings made during this project belong to:

**[ ] The speaker** — each person retains full ownership of their own recordings.

**[ ] The community** — [Community/Tribe/Nation name]: _______________________

**[ ] A shared arrangement** — describe: ___________________________________

*If ownership is shared or community-held, the decision-making body for questions about the recordings is:* ________________________________

---

## What the Recordings Can Be Used For

Each recording will be assigned an access tier. The tier can be changed later at the speaker's or community's request.

| Tier | Meaning |
|---|---|
| **open** | Can be included in a publicly released dataset or model |
| **community** | Can be used to train a community model; not for public release |
| **restricted** | For archival/preservation only; not for any training dataset |
| **sacred / do not digitize** | Should not be part of this project |

Default tier for this project: _____________________

Speakers may assign a different tier to individual recordings.

---

## Data Augmentation

To increase dataset size without adding synthetic voices, recordings may be processed to create modified copies — speed perturbation, pitch shifting, or added background noise. These copies are flagged in the metadata with a `provenance_note` and inherit the same access tier as the original recording.

- [ ] Augmentation is permitted for my recordings
- [ ] Augmentation is not permitted for my recordings

*(See [notebooks/04_augmentation.ipynb](../notebooks/04_augmentation.ipynb) for the specific techniques used.)*

---

## Cultural Protocols

Some recordings may have cultural restrictions that exist outside this document — seasonal availability, ceremonial context, gender-specific knowledge, or other protocols. These should be noted in the metadata field `cultural_protocol` for each recording.

Examples of what to note:
- "Winter ceremony context — not for use outside November–February"
- "Elder knowledge — requires knowledge keeper review before any use"
- "Women's teaching — appropriate for women's programs only"

Knowledge keeper review: **[ ] Required [ ] Not required** for this project

If required, the reviewing knowledge keeper is: _______________________________

---

## How to Withdraw

A speaker may withdraw their recordings at any time by contacting:

Name: ___________________________________
Role: ___________________________________
Contact: ___________________________________

When a withdrawal request is made:
- Recordings will be removed from the active dataset within: _____ days
- Recordings already included in a released model: *[describe what can and cannot be reversed — be honest about technical limitations]*
- Archival copies: *[describe retention/deletion policy]*

---

## What Happens to the Data

The recordings will be stored at: _______________________________

Backups: _______________________________

Access is limited to: _______________________________

The recordings will **not** be:
- [ ] Shared with commercial companies without explicit community approval
- [ ] Used to train models for purposes other than those listed above
- [ ] Processed by services that require audio to be uploaded to external servers

*(This project transcribes audio locally using [Whisper](https://github.com/openai/whisper), Meta's [MMS](https://ai.meta.com/blog/multilingual-model-speech-recognition/), or manual transcription — depending on the language. No audio is sent to any third-party service.)*

---

## Speaker Acknowledgment

I have read and understood this agreement. I am participating voluntarily. I know I can withdraw at any time.

Speaker name (or pseudonym, if preferred): _______________________________

Speaker ID (for metadata — can be anonymous): _______________________________

Preferred language/dialect for recordings: _______________________________

Access tier for my recordings: _______________________________

Augmentation permitted: **[ ] Yes [ ] No**

Cultural protocol notes: _______________________________

Signature or mark: _______________________________

Date: _______________________________

---

## Project Acknowledgment

On behalf of this project:

Name: _______________________________

Role: _______________________________

Signature: _______________________________

Date: _______________________________

---

*For institutional-level dataset governance documentation (funding, ownership, access policies, legal commitments), see [adapted_datasheet_for_indigenous_datasets.md](adapted_datasheet_for_indigenous_datasets.md). This agreement and that datasheet operate at different levels — this one is for individual speakers, the datasheet is for the dataset as a whole.*
