# What Should Not Be Digitized

*This framework is for communities to work through before a recording session or digitization project begins. It draws on the principle articulated by Diné scholar Delton Francis and others: some knowledge is not meant to circulate outside its proper context. The question "should we digitize this?" must be asked before "how do we digitize this?"*

*There is no universal answer. These questions are meant to surface the right conversations within your community.*

---

## The Core Question

Digitization makes things searchable, copyable, and distributable in ways that were not possible before. A recording that exists on a cassette tape in an elder's home has a specific, limited circulation. The same recording in a voice dataset can end up embedded in a model deployed anywhere in the world.

**Ask first:** Does this recording want to travel like that?

---

## Questions to Ask About a Recording

### 1. Who authorized this knowledge to be shared?

- Was this a deliberate teaching for outside audiences, or a private context that was recorded incidentally?
- Is the speaker still alive to give consent? If not, who holds custodial authority?
- Does the speaker's family, clan, or nation have a view on how this recording circulates?

### 2. Does this knowledge carry protocol?

Some knowledge is held under explicit cultural protocol and it may be:
- **Ceremonial** — belongs within a specific ritual context
- **Seasonal** — appropriate only at certain times of year
- **Gendered** — appropriate for one gender to hold or transmit
- **Initiatory** — held by those who have completed a specific process
- **Elder-restricted** — not for younger generations until a certain stage of life

If a recording carries any of these restrictions, it should at minimum be tagged `restricted` in the metadata. In many cases it should not be digitized at all.

### 3. What happens when this knowledge is separated from its context?

Oral knowledge often depends on context for its meaning and its safety. A healing plant song divorced from the protocols that govern its use can cause harm. A clan history told in the wrong sequence can misrepresent relationships.

Ask: Does the meaning of this recording survive without its context? Would digitizing it misrepresent or distort the knowledge?

### 4. What is the worst case?

If this recording ended up:
- In a publicly released voice model
- In a voice cloning tool
- In a search engine's training data
- In the hands of people who wish to appropriate or commercialize the culture

...would that cause harm? How serious would that harm be?

Some recordings carry low risk. Others carry irreversible risk. Be honest about which you are dealing with.

### 5. Has the community discussed this specific type of recording?

Many communities have governance structures such as elders' councils, language committees, cultural departments that have authority over these questions. This framework does not replace that authority. If your community has a process, use it.

---

## Categories That Typically Warrant Caution

This list is not exhaustive and is not prescriptive. It is a starting point for community deliberation.

| Category | Typical concern |
|---|---|
| Ceremonial songs or prayers | Context-dependent meaning; risk of appropriation or decontextualization |
| Healing knowledge | Separation from protocol may cause harm |
| Clan histories and genealogies | Contested authority; potential for misrepresentation |
| Prophecies and sacred narratives | Often held under specific custodial responsibility |
| Recordings of people who have passed | Complex consent questions; cultural protocols around the deceased vary widely |
| Children's voices | Additional consent and protection considerations |
| Knowledge from a specific region or family | May belong to that group, not the wider language community |

---

## How to Encode the Decision in Metadata

When a recording is reviewed, the decision should be recorded in `metadata_template.csv`:

| Situation | `consent_tier` | `exclude_from_training` | `exclude_reason` | `cultural_protocol` |
|---|---|---|---|---|
| Approved for public model | `open` | `false` | — | (any restrictions noted) |
| Approved for community model only | `community` | `false` | — | (any restrictions noted) |
| Archive only, no training | `restricted` | `true` | "archival only per community decision" | (context noted) |
| Do not include at all | — | Do not add to dataset | — | — |

The `cultural_protocol` field is free text. Use it to preserve context that no schema can fully capture:

> "Recorded during winter ceremony. Use restricted to November–February. Knowledge keeper review required before any use outside community."

---

## A Note on the `exclude_from_training` Field

This field exists specifically so that a collection can include recordings for archival and cultural preservation purposes and keep them accessible to community members without them ever entering a training pipeline. Preservation and training are separate decisions. A recording can serve one purpose without serving the other.

---

## Further Reading

- First Nations Information Governance Centre, OCAP Principles: https://fnigc.ca/ocap-training/
- CARE Principles for Indigenous Data Governance: https://www.gida-global.org/care
- Te Hiku Media on data sovereignty in language revitalization: https://tehiku.nz/te-hiku-tech/te-hiku-dev-korero/25141/data-sovereignty-and-the-kaitiakitanga-license
- Lorisia MacLeod, "More Than Personal Communication: Templates For Citing Indigenous Elders and Knowledge Keepers": https://kula.uvic.ca/index.php/kula/article/view/135
