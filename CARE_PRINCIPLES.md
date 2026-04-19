# CARE Principles in Practice

The [CARE Principles for Indigenous Data Governance](https://www.gida-global.org/care) provide the ethical framework for this repository. This document explains how each principle shapes concrete decisions in the workflow.

---

## Collective Benefit

**The principle:** Data ecosystems should be designed and function in ways that enable Indigenous Peoples to derive benefit from the data.

**How this repo enacts it:**

- The three pathways (record, transcribe, augment) are designed to produce assets that communities own and control (not to feed external platforms).
- The LJSpeech export is a means for communities to train their own models, not an endpoint that transfers data to a third party.
- The `consent_tier` field (`open` / `community` / `restricted`) allows communities to decide granularly who benefits from each recording. A recording can be in the archive and benefit the community without ever being exported to a training dataset.
- The augmentation pathway (Pathway 3) prioritizes real speaker voices over synthetic ones. Community members' voices remain at the center of any model trained on this data.

---

## Authority to Control

**The principle:** Indigenous Peoples' rights and interests in Indigenous data must be recognised and their authority to control such data be empowered.

**How this repo enacts it:**

- **No audio leaves the community's infrastructure.** Transcription runs locally via [Whisper](https://github.com/openai/whisper), Meta's [MMS](https://ai.meta.com/blog/multilingual-model-speech-recognition/) for Indigenous languages Whisper does not cover, or manual transcription for languages neither model supports. The original repository used Google Cloud Speech-to-Text, which required audio to be uploaded to a third-party server. This dependency has been removed entirely.
- The `exclude_from_training` boolean gives communities a clear mechanism to include recordings in an archive for cultural preservation while preventing them from ever entering a training pipeline.
- The [Community Data Agreement template](docs/community_agreement_template.md) establishes speaker ownership explicitly before any recording session begins.
- The `knowledge_keeper_reviewed` field creates a formal checkpoint: community experts, not just technical operators, have authority over what is finalized.

---

## Responsibility

**The principle:** Those working with Indigenous data have a responsibility to share how those data are used to support Indigenous Peoples' self-determination and collective benefit.

**How this repo enacts it:**

- The `recorded_by` and `provenance_note` fields create an auditable chain of custody for every file. This is a responsibility to future users of the dataset, not just the current operator.
- Augmented files are always flagged in metadata (`provenance_note: "augmented from {source_id}"`), so no one downstream can mistake a synthetically extended recording for an original.
- The [docs/what_not_to_digitize.md](docs/what_not_to_digitize.md) decision framework asks communities to actively consider which knowledge should never be digitized. Thus exercising responsibility at the point of collection, before harm is possible.
- The `cultural_protocol` field carries forward obligations that exist outside any technical system (seasonal restrictions, ceremonial context, gender protocols) so that downstream users cannot claim ignorance.

---

## Ethics

**The principle:** Indigenous Peoples' rights and wellbeing should be the primary concern at all stages of the data life cycle and across the data ecosystem.

**How this repo enacts it:**

- The [Community Data Agreement template](docs/community_agreement_template.md) is written in plain language, not legal boilerplate, so speakers can give informed consent rather than procedural consent.
- The `what_not_to_digitize.md` framework centers the question: *should* this be digitized at all, before asking *how* to digitize it. This reflects the principle articulated by Delton Francis (Diné) that some knowledge is not meant to circulate outside its proper context.
- The `access_tier` structure (`open` / `community` / `restricted` / `sacred-do-not-digitize`) provides a vocabulary for communities to express gradations of sensitivity without requiring legal or technical expertise.
- The repository avoids the synthetic data shortcut (using a corporate TTS model to generate training data) precisely because doing so would introduce a voice that the community did not provide. Ethics here means keeping the dataset grounded in real, consented human speech.
