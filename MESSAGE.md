# MESSAGE.md — The Messaging Design System

The single source of truth for company messaging. Every agent doing messaging or content work in this repository reads this file before resolving messaging context.

## Writing Profile

The block below applies to every messaging or content task in this repository. If unfilled, recommend the user run `/bootstrap`.

<!-- claude-message:profile:start -->
Run `/bootstrap` to generate your writing profile from the messaging house.
<!-- claude-message:profile:end -->

## Purpose

The messaging system is the company's positioning, narrative, audience, products, propositions, proof, and go-to-market motion expressed as structured markdown documents. Every piece of generated content traces back to it — no fabricated positioning, no claims without evidence, no voice drift between assets.

## The 8P Messaging System

### Messaging Pillars

| Pillar          | Purpose                                   | File                       | Collections             |
|-----------------|-------------------------------------------|----------------------------|-------------------------|
| **Profile**     | Identity, voice, marketplace statement    | `messaging/profile.md`     | —                       |
| **Proposition** | UVPs, differentiators, value claims       | `messaging/proposition.md` | —                       |
| **Pitch**       | Strategic narrative                       | `messaging/pitch.md`       | —                       |
| **Position**    | Category & competitive landscape          | `messaging/position.md`    | categories, competitors |
| **People**      | ICP, buying process                       | `messaging/people.md`      | personas, segments      |
| **Portfolio**   | Product ecosystem                         | `messaging/portfolio.md`   | products, solutions     |
| **Proof**       | Customer evidence and external validation | `messaging/proof.md`       | stories, reports        |
| **Play**        | GTM motion, plays & signals               | `messaging/play.md`        | plays, signals          |

Each pillar contains substantive messaging content for its domain *and* a reference table routing to its collections. Collections are deeper profiles agents load on demand.

### Messaging Profiles

| Profile        | Purpose                                                                | File                              | Pillar    |
|----------------|------------------------------------------------------------------------|-----------------------------------|-----------|
| **Category**   | Market category the company aligns with or competes in                 | `messaging/categories/[name].md`  | Position  |
| **Competitor** | An alternative buyers evaluate (vendor, DIY, status quo)               | `messaging/competitors/[name].md` | Position  |
| **Persona**    | Buyer or user role with altitude, pain points, and messaging guidance  | `messaging/personas/[name].md`    | People    |
| **Segment**    | Industry, size, region, or maturity slice with adjusted messaging      | `messaging/segments/[name].md`    | People    |
| **Product**    | A product, module, platform, or add-on in the portfolio                | `messaging/products/[name].md`    | Portfolio |
| **Solution**   | A use-case bundle composed of one or more products                     | `messaging/solutions/[name].md`   | Portfolio |
| **Story**      | Customer evidence — outcome, quote, and proof                          | `messaging/stories/[name].md`     | Proof     |
| **Report**     | Third-party research — analyst report, market study, survey, benchmark | `messaging/reports/[name].md`     | Proof     |
| **Play**       | GTM motion narrative for a buyer situation or competitive scenario     | `messaging/plays/[name].md`       | Play      |
| **Signal**     | Compelling event that triggers one or more plays                       | `messaging/signals/[name].md`     | Play      |

### Glossary

Custom terminology lives in `messaging/glossary.md`. Every messaging doc body should be checked against the glossary for consistency. A glossary term, once defined, overrides all other word-choice guidance. Bootstrap seeds initial entries; `/investigate fix glossary` adds and prunes.

### Journal

The operational log for longitudinal learnings that lives in `messaging/journal.md`. Entries grow over time based on insights and investigations.

## File Conventions

- YAML frontmatter for metadata; markdown body for narrative.
- `## Messaging Blocks` — source content an agent **draws from**.
- `## Writing Guidelines` — interpretation rules an agent **follows**.
- `## Messaging Rules` — company-specific constraints (3-5 max). Encoded during bootstrap.
- Bracketed scaffolding (`[Instructions:]`, `[Tips:]`, `[Format:]`) guides drafting only — never copied into final files.
- Schemas live in `messaging/_schemas/pillars/[name].md` (pillar instructions) and `messaging/_schemas/collections/[name].md` (collection schemas). 

## Progressive Loading

Three layers, each with a distinct responsibility:

- **Spec layer (always loaded)** — MESSAGE.md. Architecture, contracts, patterns. Brand tokens live in `/DESIGN.md`; the glossary lives in `messaging/glossary.md`.
- **Domain layer (loaded selectively)** — the 8 pillar files. Load a pillar only when its domain is relevant to the task. Profile is "near-always" (identity + voice touch every generation), but even Profile is skipped for system audits that only need frontmatter and section headers.
- **Profile layer (loaded with filtering)** — the collection profiles. Discovered via parent-pillar reference tables; narrowed via frontmatter; loaded full-body only on confirmed match.

## Reference Patterns

| Pattern | Domain pillars typically loaded | Collections via routing |
|---|---|---|
| Persona-targeted content (email, LP, persona-specific messaging) | Profile + Pitch + People | persona profile; matching Stories filtered on persona+product |
| Competitive content (battlecard, comparison, displacement) | Profile + Position + Proposition | competitor profile; relevant Products; supporting Reports |
| Compelling-event driven (signal trigger, news-jacking, reactive outreach) | Profile + Play + People | signal profile + matching plays; affected personas |
| Product launch (release announcement, GTM material) | Profile + Pitch + Portfolio + Position + Proposition + Proof | product profile; positioning category; supporting Stories and Reports |
| Campaign orchestration (multi-asset campaign brief) | Full pillar set | personas/products/competitor/plays from intake parameters |
| Composing a new collection profile | Profile + the parent pillar | schema from `messaging/_schemas/collections/[type].md`; existing file if updating |
| System audit / health check | All 8 pillars (frontmatter + Messaging Rules sections) + journal | frontmatter-only of every collection |
| Skill tuning / voice calibration | All 8 pillars + journal | full bodies of personas, competitors, categories; frontmatter for the rest |

## Guardrails

Cross-cutting craft rules. Per-pillar and per-profile guidance lives in each schema's Writing Guidelines section.

### Do's and Don'ts

**Grounding**
- Do trace every claim to a specific messaging doc before publishing.
- Don't write a UVP, differentiator, or proof point that isn't already in `proposition.md` or `proof.md`.

**Persona discipline**
- Do match content depth to the persona's altitude — executives get the headline, practitioners get the detail, developers get the specifics.
- Don't merge two personas in one asset. Pick one. If both must be addressed, separate sections or separate assets.

**Stage discipline**
- Do calibrate proof aggressiveness to `profile.md` stage. Emerging companies cite design partners; established companies cite analyst leadership.
- Don't claim "industry-leading" or "best-in-class" without a Report in `messaging/reports/` to back it.

**Voice discipline**
- Do use glossary terms exactly as defined in `messaging/glossary.md`.
- Don't paraphrase the strategic narrative from Pitch verbatim across assets — preserve the logic, never duplicate the language.

**Competitive discipline**
- Do load only the named competitor's profile. One competitor per asset unless the asset is explicitly a multi-vendor comparison.
- Don't introduce a differentiator in competitive content that isn't already in `proposition.md`.

**Citation discipline**
- Do attribute every Report-derived claim — source name and date, on the same line as the claim.
- Don't strip attribution when porting a finding from one asset to another.

### Litmus tests

- **Load Pitch?** Narrative-led asset = yes. Feature page, datasheet, technical brief = no.
- **Cite a Story or a Report?** Awareness/credibility framing = Report. Realized customer value = Story. Eval stage = both.
- **Is the claim grounded?** If you can't point to a messaging doc, don't write it.
- **Is the altitude right?** Read the persona's altitude. Read your draft. Mismatch = altitude wrong.

### Common failure modes

- **Generic positioning** — "leading platform for X" without specific differentiation. If a competitor could write the same sentence, cut it. Cure: ground in a UVP from `proposition.md`.
- **Stage drift** — claims that exceed `proof.md`. Watch for unhedged superlatives. Cure: re-check `profile.md` stage and the evidence basis before publishing.
- **Persona blur** — content addressed to "security professionals" generally instead of a named persona. Cure: pick a persona file, load it, write to that one human.
- **Voice mixing** — pulling Pitch's narrative cadence into a battlecard. Cure: each asset type has its register; load the asset's skill, not the closest-to-hand pillar.
- **Citation evaporation** — a stat appears mid-asset without attribution. Cure: cite on the same line as the claim, every time.

