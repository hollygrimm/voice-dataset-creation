# What Should Not Be Used for Training

*This framework extends [what_not_to_digitize.md](./what_not_to_digitize.md) beyond voice recordings to cover images, text, cultural artifacts, and other materials that communities may encounter when building AI datasets. The same core principle applies: the question "should we train on this?" must be asked before "how do we train on this?"*

*There is no universal answer. These questions are meant to surface the right conversations within your community.*

---

## The Core Question

Training a model on a piece of data means embedding it — its patterns, its style, its content — into a system that can reproduce and recombine it in unpredictable ways. A photograph in a community archive has a known audience. The same photograph in a training dataset can influence what a model generates for anyone, anywhere, forever.

**Ask first:** Should this material's patterns be reproducible by a machine? Who benefits? Who is harmed?

---

## Questions to Ask About Any Training Material

### 1. Who authorized this material to be used this way?

- Was this created for public circulation, or for a specific context?
- Does the creator or their community retain authority over how it is used?
- Is there a difference between consenting to *display* and consenting to *training*? (There almost always is.)
- For historical materials: who holds custodial authority now?

### 2. Does this material carry cultural protocol?

Some materials are governed by cultural protocols that exist outside intellectual property law:

- **Sacred or ceremonial** — images of ceremonies, ritual objects, sacred sites
- **Seasonal or contextual** — knowledge appropriate only at certain times or places
- **Lineage-restricted** — designs, patterns, or stories belonging to specific families, clans, or societies
- **Gender-specific** — knowledge held by one gender
- **Mortuary** — images or recordings of people who have passed (protocols vary widely)
- **Place-based** — knowledge tied to a specific geographic location that should not travel beyond it

If any of these apply, the material should not enter a training dataset without explicit community authorization — and in many cases should not enter one at all.

### 3. What does the model learn from this?

Different modalities teach models different things:

| Material | What the model learns | Risk |
|---|---|---|
| **Images of art/craft** | Visual patterns, styles, compositions | Model can generate imitations of culturally specific art styles |
| **Photographs of people** | Faces, body types, cultural dress | Can generate synthetic images of Indigenous people without consent |
| **Photographs of places** | Landscapes, sacred sites, architecture | Can expose or trivialize restricted locations |
| **Text (stories, oral histories)** | Narrative patterns, vocabulary, cultural knowledge | Can reproduce sacred narratives or restricted knowledge out of context |
| **Text (language data)** | Grammar, vocabulary, usage patterns | Can enable language tools without community control |
| **Songs and music** | Melodic patterns, rhythmic structures, vocal styles | Can generate imitations of ceremonially restricted music |
| **Designs and patterns** | Visual motifs, symbolic systems | Can reproduce clan-specific or sacred designs |
| **Metadata** | Relationships between people, places, events | Can reveal community structure or sensitive associations |

### 4. What is the worst case?

If this material were used to train a model, and that model were deployed publicly:

- Could it generate imitations of culturally restricted art or ceremony?
- Could it produce synthetic images of real community members?
- Could it reproduce sacred or restricted knowledge on demand?
- Could it enable outsiders to produce culturally specific work without authorization?
- Could it reveal the location of sacred or protected sites?
- Could it create a tool that competes with community-controlled language resources?

### 5. Is the training reversible?

Once material enters a training dataset and a model is trained on it:

- The material's influence cannot be fully removed from the model
- Retraining without the material is expensive and may not fully eliminate learned patterns
- If the model or dataset is shared, copies may exist beyond your control

This asymmetry — easy to include, nearly impossible to remove — means the default should be caution.

---

## Categories That Typically Warrant Caution

This list is not exhaustive. It is a starting point for community deliberation.

### Images and Visual Materials

| Category | Typical concern |
|---|---|
| Ceremonial regalia, ritual objects | Style replication; decontextualization |
| Sacred site photographs | Location exposure; trivialization |
| Portraits of elders or knowledge keepers | Synthetic image generation without consent |
| Clan-specific designs or patterns | Unauthorized reproduction of lineage-restricted art |
| Photographs of people who have passed | Mortuary protocols; synthetic resurrection |
| Children's images | Heightened consent and protection requirements |
| Archival photographs with unclear provenance | Original consent may not have included AI training |

### Text and Language Materials

| Category | Typical concern |
|---|---|
| Sacred narratives or origin stories | Reproduction out of context; loss of custodial control |
| Ceremonial language or prayer texts | Decontextualization; inappropriately casual access |
| Unpublished oral histories | Speaker consent may not extend to AI training |
| Language documentation from academic archives | Community may not have authorized the original collection |
| Traditional ecological knowledge | Commercial extraction; biopiracy via AI intermediary |
| Clan or family histories | Contested authority; misrepresentation |

### Audio and Music

| Category | Typical concern |
|---|---|
| Ceremonial songs | Context-dependent meaning; sacred restriction |
| Healing songs or chants | Separation from protocol may cause harm |
| Lullabies and children's songs | May carry clan-specific or family-specific ownership |
| Recordings from academic or missionary archives | Consent for the original recording may not have included AI use |

---

## How to Encode the Decision

When reviewing materials for potential inclusion in a training dataset, record the decision using the same consent tier system from the voice dataset:

| Decision | `consent_tier` | `exclude_from_training` | Notes |
|---|---|---|---|
| Approved for public model | `open` | `false` | Material can appear in a publicly released dataset |
| Approved for community model only | `community` | `false` | Training limited to community-controlled models |
| Archive only, no training | `restricted` | `true` | Preserved for community access; never enters a training pipeline |
| Do not include | — | Do not add to dataset | Material should not be part of this project |

For visual and text materials, add a `modality` field to your metadata:

| Field | Values |
|---|---|
| `modality` | `audio`, `image`, `text`, `video`, `design`, `other` |
| `source_context` | Where the material came from and under what circumstances |
| `cultural_protocol` | Free text — preserve context that no schema can capture |

---

## The Relationship Between Display and Training

A common assumption: if something is publicly visible (in a museum, on a website, in a published book), it is available for training. This assumption is wrong for Indigenous materials.

- **Display** is contextual. A museum exhibit has a physical location, a curatorial frame, and (ideally) a community agreement governing how materials are shown.
- **Training** is extractive. It strips context, embeds patterns, and makes them reproducible without attribution or control.

A community may consent to a photograph appearing in a museum catalog while absolutely prohibiting that photograph from entering a training dataset. These are different decisions with different consequences.

---

## Provenance Questions for Existing Datasets

If you are evaluating whether to use an existing dataset (e.g., a scraped image dataset, a digitized text collection, a speech corpus):

1. **How was the data collected?** Was it scraped from the internet? Digitized from archives? Donated by communities?
2. **Was consent obtained for AI training specifically?** Consent for one use does not transfer to another.
3. **Does the dataset contain Indigenous materials?** Many large scraped datasets contain Indigenous art, language, and cultural materials without community knowledge or consent.
4. **Who benefits from models trained on this data?** If the answer is "not the communities whose materials are in the dataset," proceed with extreme caution.

---

## Further Reading

- First Nations Information Governance Centre, OCAP Principles: https://fnigc.ca/ocap-training/
- CARE Principles for Indigenous Data Governance: https://www.gida-global.org/care
- Te Hiku Media on data sovereignty: https://tehiku.nz/te-hiku-tech/te-hiku-dev-korero/25141/data-sovereignty-and-the-kaitiakitanga-license
- Local Contexts TK Labels: https://localcontexts.org/labels/traditional-knowledge-labels/
- Abeba Birhane & Vinay Uday Prabhu, "Large image datasets: A pyrrhic win for computer vision?" (2021): https://arxiv.org/abs/2006.16923
- Timnit Gebru et al., "Datasheets for Datasets" (2021): https://arxiv.org/abs/1803.09010
- Jason Edward Lewis et al., "Indigenous Protocol and Artificial Intelligence Position Paper" (2020): https://doi.org/10.11573/spectrum.library.concordia.ca.00986506
- WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (2024) — the first international treaty addressing biopiracy of traditional knowledge: https://www.wipo.int/pressroom/en/articles/2024/article_0007.html
