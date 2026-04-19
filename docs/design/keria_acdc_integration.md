# KERIA / ACDC Voice Consent Integration — Design

**Status:** Draft, design only. Not implemented.
**Branch:** `design/keria-acdc-consent`
**Companion stack:** [matou-app](https://github.com/matou-dao/) (Go backend + signify-ts frontend + KERIA agent)

---

## 1. Motivation

Today, speaker consent is recorded as a row in `metadata/metadata_template.csv` with a `consent_tier` field (`open` / `community` / `restricted`) and an `exclude_from_training` boolean. The CSV is the single source of truth, edited by hand or by `scripts/export_metadata.py`. This works for small, single-organization datasets but has limits:

- **No cryptographic authority.** A row that says `consent_tier=open` is trusted because the operator wrote it — there is no signature tying that claim to the speaker or to a community-controlled identifier.
- **No revocation event log.** A speaker who withdraws consent leaves no auditable trace. The CSV row simply changes (or doesn't).
- **No portability.** A speaker contributing to two community projects has no way to carry their consent posture between them without re-signing on paper.

KERI ([Key Event Receipt Infrastructure](https://keri.one/)) and ACDC ([Authentic Chained Data Containers](https://trustoverip.github.io/tswg-acdc-specification/)) provide a community-controlled cryptographic substrate for these claims. Pairing this repository's CSV workflow with the [matou-app](https://github.com/matou-dao/) credential infrastructure means consent decisions become signed, registered, and revocable through the same mechanisms communities already use for organizational membership credentials.

This design is consistent with CARE Principle **A** (*Authority to Control*): the credential is issued by the community's AID, lives in a registry the community operates, and can be revoked by community action — none of which requires trusting this repository's CSV files or the operator who maintains them.

---

## 2. VoiceConsentCredential Schema

ACDC credentials carry a `s` (schema) field whose value is the SAID of a JSON-Schema document. The schema below is the source of truth for that document.

```json
{
  "$id": "",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Voice Consent Credential",
  "description": "Records a speaker's consent tier and cultural protocols for voice recordings. Issued per-speaker per-project. Revocation is performed via the ACDC registry, not by mutating fields on this credential.",
  "type": "object",
  "credentialType": "VoiceConsentCredential",
  "version": "1.0.0",
  "properties": {
    "v": { "description": "Version string", "type": "string" },
    "d": { "description": "Credential SAID", "type": "string" },
    "u": { "description": "Nonce for speaker privacy (REQUIRED — prevents cross-credential correlation by SAID alone)", "type": "string" },
    "i": { "description": "Issuer AID (community)", "type": "string" },
    "ri": { "description": "Registry ID — revocation events for this credential are written here", "type": "string" },
    "s": { "description": "Schema SAID", "type": "string" },
    "a": {
      "oneOf": [
        { "description": "Attributes SAID", "type": "string" },
        {
          "description": "Attributes block",
          "type": "object",
          "properties": {
            "d": { "description": "Attributes SAID", "type": "string" },
            "i": { "description": "Speaker AID — the cryptographic identity holding this credential. This is the authority. Not for joining to CSV metadata; use speakerId for that.", "type": "string" },
            "dt": { "description": "Issuance datetime", "type": "string", "format": "date-time" },
            "consentTier": {
              "description": "Default access tier for the speaker's recordings in this project. Per-recording metadata MAY tighten this (e.g. mark a single clip 'restricted') but MUST NOT loosen it.",
              "type": "string",
              "enum": ["open", "community", "restricted"]
            },
            "speakerId": {
              "description": "Pseudonymous join key to CSV metadata's speaker_id column. NOT an authority claim — the AID in 'i' is. This field exists only to bridge to the existing dataset metadata.",
              "type": "string"
            },
            "projectId": {
              "description": "Voice dataset project identifier (scopes the credential to one collection effort)",
              "type": "string"
            },
            "culturalProtocol": {
              "description": "Free text cultural restrictions (e.g. seasonal availability, ceremonial context, gender protocols). Mirrors the cultural_protocol metadata field.",
              "type": "string"
            },
            "augmentationPermitted": {
              "description": "Whether speed/pitch/noise augmentation is permitted on this speaker's recordings (per Pathway 3, notebook 04)",
              "type": "boolean"
            },
            "knowledgeKeeperReviewed": {
              "description": "Whether a knowledge keeper has reviewed this speaker's recordings",
              "type": "boolean"
            }
          },
          "additionalProperties": false,
          "required": ["d", "i", "dt", "consentTier", "speakerId", "projectId", "augmentationPermitted", "knowledgeKeeperReviewed"]
        }
      ]
    }
  },
  "additionalProperties": false,
  "required": ["v", "d", "i", "ri", "s", "a"]
}
```

### Schema design notes

Three deliberate departures from a generic ACDC template:

**`u` nonce is REQUIRED, not optional.** Voice recordings tie consent to a real human voice. If two VoiceConsentCredentials for the same speaker shared a deterministic SAID derivation, an outside observer could correlate them across projects without ever decrypting attribute blocks. The nonce blocks that.

**`sacred` is intentionally NOT in the `consentTier` enum.** The community-agreement template (`docs/community_agreement_template.md`) defines `sacred / do not digitize` to mean "this never becomes a recording." If a `VoiceConsentCredential` exists, the recording exists, so `sacred` would be a contradiction in terms. Anything sacred is filtered upstream by the `what_not_to_digitize.md` decision framework, before any audio reaches the consent layer.

**`speakerId` and `i` (speaker AID) play different roles.** `i` in the attributes block is the cryptographic authority — the AID controlling the keys that signed the credential. `speakerId` is the pseudonymous string that joins to `metadata_template.csv`'s `speaker_id` column. The schema description spells this out so downstream implementers don't conflate them.

### Revocation

**Withdrawal is a registry event, not a field mutation.** When a speaker withdraws consent, matou-app issues a revocation event into the registry referenced by `ri`. The credential itself is immutable. Verifiers MUST check the registry's current state before honoring a credential.

A `withdrawalDate` field in the CSV bridge (see §4) is a read-through convenience for human inspection — *not* a source of truth.

---

## 3. Per-recording override semantics

The credential carries a *default* `consentTier` for the speaker. The CSV `consent_tier` column on each row carries the *effective* tier for that recording.

**Tightening is allowed; loosening is not.** A speaker whose credential says `open` may mark an individual recording `restricted` in the CSV — perhaps a clip that turned out to contain personal information. A speaker whose credential says `restricted` may NOT have a row marked `open`, even if the operator types it.

`export_metadata.py` MUST enforce this: when a credential is present, the effective tier for each row is `min(credential_tier, csv_tier)` under the ordering `open > community > restricted`. Violations fail loudly.

This is the simplest workable model. The alternative — issuing a separate credential per recording — is more KERI-native but multiplies issuance burden and is left for a later iteration.

---

## 4. Integration architecture

Communities running matou-app already expose an HTTP API:

```
GET    /api/v1/credentials             — list (filter client-side by Schema SAID)
GET    /api/v1/credentials/{said}      — fetch one
POST   /api/v1/credentials             — store from frontend (issuance flow)
POST   /api/v1/credentials/validate    — verify structure
GET    /api/v1/org                     — fetch community AID and metadata
```

Backed by `anystore.LocalStore` and a `keri.Client` that talks to KERIA. The whole stack runs locally — no third-party service.

### `export_metadata.py` integration sketch

```python
# scripts/keri_consent.py — new module
from typing import Optional
import httpx

VOICE_CONSENT_SCHEMA_SAID = "..."  # populated when schema is registered

class VoiceConsent:
    def __init__(self, speaker_id: str, consent_tier: str,
                 augmentation_permitted: bool, knowledge_keeper_reviewed: bool,
                 cultural_protocol: str, revoked: bool):
        self.speaker_id = speaker_id
        self.consent_tier = consent_tier
        self.augmentation_permitted = augmentation_permitted
        self.knowledge_keeper_reviewed = knowledge_keeper_reviewed
        self.cultural_protocol = cultural_protocol
        self.revoked = revoked

class MatouClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self._client = httpx.Client(base_url=base_url, timeout=10.0)

    def fetch_voice_consents(self, project_id: str) -> dict[str, VoiceConsent]:
        """Return speaker_id -> VoiceConsent mapping for a project.

        Filters to Schema == VoiceConsentCredential and project matching.
        Drops credentials where the registry shows revocation.
        """
        ...

# scripts/export_metadata.py — integration point
def run(..., matou_url: Optional[str] = None, project_id: Optional[str] = None):
    consents: dict[str, VoiceConsent] = {}
    if matou_url and project_id:
        consents = MatouClient(matou_url).fetch_voice_consents(project_id)

    for _, row in markers.iterrows():
        ...
        speaker_id = template_row.get("speaker_id") if template_row else None
        consent = consents.get(speaker_id) if speaker_id else None

        if consent and consent.revoked:
            # Withdrawn — exclude from CARE export entirely, log it.
            print(f"Excluding {file_id}: speaker {speaker_id} withdrew consent", file=sys.stderr)
            continue

        if consent:
            effective_tier = _tighter(consent.consent_tier, csv_tier)
            if effective_tier != csv_tier:
                # CSV tried to loosen — that's a hard error, not a silent override.
                raise ConsentViolation(
                    f"{file_id}: csv_tier={csv_tier} loosens credential_tier={consent.consent_tier}"
                )
            row["consent_tier"] = effective_tier
            row["augmentation_permitted"] = str(consent.augmentation_permitted).lower()
            row["knowledge_keeper_reviewed"] = str(consent.knowledge_keeper_reviewed).lower()
        ...
```

CLI shape:
```bash
python scripts/export_metadata.py audacity \
    --matou-url http://localhost:8080 \
    --project-id voice-dataset-2026 \
    --ljspeech
```

When `--matou-url` is omitted the existing CSV-only behavior is preserved. The KERIA path is opt-in per invocation.

---

## 5. Open questions for Ben & Engie

**Q1 — Polymorphic CredentialData.** `keri.CredentialData` in matou-app is currently a fixed struct (`CommunityName`, `Role`, `JoinedAt`, `ExpiresAt`) — see `backend/internal/keri/client.go:25`. VoiceConsentCredential carries a different attribute shape. Three options:

1. Refactor `CredentialData` to `json.RawMessage` and decode per schema SAID at point of use. Cleanest long term, but touches the role-credential code paths.
2. Keep the existing struct; add a parallel `VoiceConsentData` struct and a discriminator switch on schema SAID at decode time. Less disruptive.
3. Skip matou-app for the voice path; have `export_metadata.py` talk to KERIA directly via signify-py. Loses the org-issuance check matou-app does for free.

**Recommendation:** Option 2 for the milestone, option 1 as a follow-up if voice-consent proves the polymorphic-Data pattern useful for other schemas.

**Q2 — Schema SAID registration.** Where does `VOICE_CONSENT_SCHEMA_SAID` get its value? Does matou-app have a flow for registering and SAIDing a new schema, or is that a manual signify-ts/keripy step? The integration depends on having a stable SAID before any credentials can be issued.

**Q3 — Revocation surfacing.** The matou-app HTTP API as it stands returns credentials from `anystore` — does the `Verified` field on `CachedCredential` (set at store time, see `credentials.go:116`) reflect ongoing registry state, or only the state at storage? The voice path needs *current* revocation status, not "was valid when first stored." If matou-app needs a `/api/v1/credentials/{said}/status` endpoint that re-checks the registry, that's a request to flag now.

**Q4 — Withdrawal UX.** When a speaker withdraws, the matou-app frontend (signify-ts) needs to issue a revocation event. Does that flow exist for role credentials today, and is it generalizable, or does VoiceConsentCredential need its own withdrawal UI?

**Q5 — Local development.** Can we point this repository's tests at a docker-compose'd matou-app + KERIA agent, or is the practical path to mock the HTTP client in tests and integration-test against a live local instance manually?

---

## 6. What's NOT in scope for this design

- Frontend issuance UI for VoiceConsentCredential (handled by matou-app + signify-ts)
- KERIA agent provisioning, key recovery, or witness selection (community-side concerns)
- Migration of existing CSV consent records into credentials (a one-shot job, separate design)
- Multi-community / federated consent (one credential per project for now)

---

## 7. Implementation milestones (when this design is approved)

1. **M1 — Schema registration.** Lock the schema, get a SAID, document it in `metadata/voice_consent_credential.schema.json`.
2. **M2 — `scripts/keri_consent.py`.** HTTP client, `VoiceConsent` dataclass, fetch + revocation filter. Unit tests against a recorded HTTP fixture.
3. **M3 — `export_metadata.py` integration.** `--matou-url` and `--project-id` flags, tightening enforcement, hard-error on loosening attempts. Tests cover credential-present, credential-absent, revoked, and loosen-attempt cases.
4. **M4 — Documentation.** Update `metadata_schema.md`, `community_agreement_template.md`, and the README workflow diagram to surface the optional credential path.
5. **M5 — End-to-end smoke test.** A full notebook walk-through against a local matou-app instance with a hand-issued VoiceConsentCredential.

Milestones are sequential except M4 may run in parallel with M3.
