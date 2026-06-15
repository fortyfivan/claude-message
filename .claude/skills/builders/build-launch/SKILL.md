---
name: build-launch
description: Orchestrates a product or feature launch from PRDs and release artifacts into coordinated internal-enablement and external-announcement waves with a mid-flow approval gate. Use when the user is launching a product, feature, integration, or major release.
---

# Launch Skill

Orchestrate a product or feature launch from artifacts to a coordinated bill of materials. Synthesize product inputs (PRDs, NPI docs, release notes, pricing) into launch messaging, plan an internal-then-external asset wave structure, get approval, then dispatch writer subagents per asset with precisely scoped context. Invoked via `/build launch [name]`.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona"). If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## Skill Composition

- **Loads at builder level:** the Context Loading pillar set (see below).
- **Loads after intake:** the product collection being launched, relevant persona collections, supporting stories and reports.
- **Loads once per launch (passed inline to writers):** the voice craft skill.
- **Loads once per asset (passed inline):** the asset envelope (and variant, when declared).
- **Dispatches:** the writer subagent per asset (parallel within waves). Internal waves precede external waves; a mid-flow approval gate sits between them.
- **Per-asset reader dispatch:** the reader subagent per asset; reader_mode chosen per asset (subagent for external high-stakes, inline for internal derivatives). Reader runs on Haiku and loads the review craft skill.

Two approval gates govern the build: one before production begins (brief), one between internal and external waves (so sales/support/CS are ready before anything ships externally).

---

## Context Loading

Load these pillars at the start of input synthesis; defer the rest until needed.

| Tier | Always at synthesis | Deferred until needed |
|---|---|---|
| **major** | profile, pitch, position, people, portfolio, proof | — (full house) |
| **minor** | profile, pitch, position, people, portfolio | proof (load at brief writing) |
| **feature** | profile, pitch, people, portfolio | position, proof (load at brief writing) |
| **integration** | profile, pitch, portfolio, people | position, proof (load if external assets need them) |

Brief writing always loads `proof.md` if not already loaded — proof matching is non-negotiable. Position loads if the launch has a competitive angle.

---

## Phase 1: Input Synthesis

Resolve the launch name first: use the argument if provided, otherwise ask for the kebab-case name (becomes the directory slug). Then synthesize the product inputs into a launch messaging foundation — the source of truth every downstream asset inherits.

### Check Input Materials

Scan `input/` subdirectories. Check `input/docs/` first (PRDs, release notes, NPI docs, pricing). Then `input/messaging/`, `input/research/`, `input/transcripts/`, `input/examples/`, and the `input/` root.

Match by `--launch-[name]` builder tag suffix or by prefix (`prd-`, `release-notes-`, `npi-`, `pricing-`). Note matches and produce a coverage map (what's well-covered, what's thin).

### Scenario Inference

Infer the launch's scenario across the 5 dimensions in MESSAGE.md `## Scenarios` before BOM planning. Launches almost always map to `Strategic shape: new-product-introduction`; the other dimensions vary by launch tier and market state.

| Dimension | Launch-specific signals | Default |
|---|---|---|
| Compelling event | GA date itself; analyst briefing window; competitor's recent launch | `none` (the launch IS the event) |
| Topic maturity | Product category state per MESSAGE.md Position | `established` (most launches extend mature categories) |
| Market moment | Competitive incursions in the category in past 90 days | `none` |
| Strategic shape | `new-product-introduction` (default); `category-creation` for truly novel; `competitive-takeout` for displacement-focused launches | `new-product-introduction` |
| Content lens | Launch tier mapped: major release → Awareness + Acquisition; minor/feature → Adoption; integration → Activation | `Acquisition` |

Surface the inferred scenario to the user before proceeding; allow adjustments.

### Launch Context Questions

Use AskUserQuestion to resolve what input materials and scenario inference don't cover:

| Question | Why it matters |
|---|---|
| Launch tier (major release, minor update, feature drop, integration)? | Determines BOM scope, wave structure, external noise level |
| Target GA date? | Drives sequencing and wave timing |
| GA / limited availability / beta? | Shapes external messaging and eligibility language |
| Which teams need to be ready at launch (sales, CS, support, partners, exec)? | Determines internal asset set |
| PR or analyst component? | Adds press release / analyst briefing prep |
| Competitive angle? | Adds competitive assets |

Do not ask for information already resolved by input materials.

### Launch Messaging Synthesis

Synthesize a launch messaging foundation from input materials + messaging house:

- **What's launching** — plain-language description (not marketing copy). Crisp factual statement the BOM derives from.
- **Why it matters** — customer problem solved + outcome enabled. Grounded in persona pain points.
- **What's different** — differentiated capability/approach. Must trace to `position.md` or the product profile.
- **Who it's for** — primary persona(s) and segment(s). Flag if launch targets a new audience not in the messaging house.
- **Key proof** — metrics, beta outcomes, validation available at launch. Flag "No proof available at launch" if none — common; note rather than paper over.
- **Messaging house gaps** — docs to create/update post-launch (new product profile needed, solution profile out of date, position.md competitive section behind). These ride along in the brief; resolution is a separate cycle.

Present the synthesis and ask the user to confirm before planning the BOM.

### Production Targets

After the BOM is final, ask which assets to produce as HTML. Skip the entire sub-flow if the user opts out: "Produce HTML for any launch assets? (yes/no)" — if no, set `production: null` for all and continue.

If yes, for each asset whose envelope declares a non-empty `production-targets` frontmatter array:

1. Ask: "Produce [asset-id] ([asset-slug]) as HTML? (yes/no)"
2. If yes and the asset has multiple targets: ask "Which target? Options: [list from production-targets]"
3. If yes and the asset has one target: use it (no question)
4. Result populates the asset's `production:` field in the brief manifest (e.g., `production: web`); omitted when the user declines

Assets with empty `production-targets` are skipped automatically.

---

## Phase 2: Launch Brief

The brief is the plan. Write to `output/launches/[launch-name]/brief.md`. **The user must approve before production begins.**

### Brief Length Discipline

Target **~200–250 lines total for a 10-asset launch**, scaling proportionally. Extra lines come from additional asset manifest entries, not from re-expanding narrative sections.

| Section | Target | Rule |
|---|---|---|
| Frontmatter | 30–35 lines | Essential contract fields only |
| Launch Summary | ~10 lines | One paragraph + headline facts |
| Launch Narrative | ~40 lines | 6 synthesis components at 5–7 lines each |
| What to Know | ~25 lines | 5 sub-sections at 2–3 sentences each |
| Asset Manifest | 7 lines × N assets | Tight spec per asset |
| Wave Structure | ~10 lines | Internal waves + mid-flow gate + external waves |
| Extracted Context | 60–80 lines | Selective verbatim; only what writers can't derive |
| Messaging Gaps | ~10 lines | Bullets flagging post-launch debt |
| Flagged Issues + Approval Gates | ~10 lines | Bullets |

### Brief Frontmatter

- `launch_name` — Kebab-case identifier
- `launch_folder` — Directory name
- `launch_tier` — major, minor, feature, integration
- `product` — Product or feature being launched
- `ga_date` — Target general availability date
- `availability` — ga, limited, beta
- `created` — Date string
- `status` — draft → approved → internal-in-progress → mid-gate → external-in-progress → complete
- `scenario` — 5-dimension scenario block from Phase 1 inference. Keys: `compelling-event`, `topic-maturity`, `market-moment`, `strategic-shape`, `content-lens`. `strategic-shape` is typically `new-product-introduction` for launches.
- `shared_context` — Personas, products, segments, `messaging_docs_loaded` list
- `messaging_gaps` — Docs flagged for post-launch creation/update
- `assets` — Array of entries: id, asset, variant, persona, altitude, audience (internal/external), wave, depends_on, reader_mode, status, production (optional — `web` | `email` | `print`; omitted when not producing HTML)

### Brief Body Sections

#### Launch Narrative

The messaging foundation derived from Phase 1 synthesis. Includes all six components (what's launching, why it matters, what's different, who it's for, key proof, messaging house gaps). This is the source of truth — some launch messaging is net-new and doesn't yet exist in the pillars.

#### What to Know

Internal primer (sales, field, exec, partners). 5 sub-sections at 2–3 sentences each: launch context, who we're talking to, what we're saying, how we're different, common objections.

#### Asset Manifest

Organized into **internal** and **external** tracks, then sequenced into waves. Internal always precedes external.

Tight 7-line spec per asset:

```yaml
- id: a01
  asset: sales-one-pager
  variant: thought-leadership
  audience: internal
  wave: 1
  persona: security-program-owners
  altitude: practitioner
  reader_mode: inline
  production: print
  depends_on: []
  notes: champion handoff doc; one printed page
  context_resolution: [asset-specific docs beyond shared launch context]
```

`reader_mode` heuristic: **subagent** for press release, announcement blog, customer email (external high-stakes); **inline** for internal enablement and external derivatives.

#### Wave Structure

```
Wave 1 (internal foundation): sales talking points, internal FAQ, support runbook
Wave 2 (internal readiness):   competitive battlecard, discovery guide, sales one-pager
       --- mid-flow approval gate: internal assets ready for review ---
Wave 3 (external announcement): press release, announcement blog, product page copy
Wave 4 (external follow-on):    customer email, social posts, nurture sequence
```

Adjust per BOM. Assets with no internal dependencies can land in Wave 1.

#### Extracted Context

Same shape as build-campaign — verbatim source material writers consume in lieu of re-reading shared pillars. Sections: Positioning, Key Messages with Verbatim Source Lines, Glossary Subset, Proof Library, Voice & Differentiation Anchors. Frozen at approval.

#### Messaging Gaps

Bullets surfaced during synthesis or production. Flagged for `/design` follow-up after the launch ships. Do not block on these during the launch; they're debt to resolve before the next campaign draws from the same content.

### Approval Flow

Present a summary (launch name, tier, GA date, asset count by track, wave count, flagged gaps) and accept Approve / Edit / Cancel. On Edit, modify through conversation or have the user edit the file directly. On Cancel, the brief is discarded.

---

## Phase 3: Production

After approval, update `status: internal-in-progress` and generate internal waves first.

### Pre-Wave Setup

Before dispatching Wave 1:

1. **Load voice gate once.** Read `.claude/skills/craft/voice/SKILL.md`; pass inline as `voice_gate` in every dispatch.
2. **Resolve assets per content-type.** For each unique asset, Read the asset envelope once; pass inline as `asset_inline`.
3. **Resolve variants per asset.** For each `(asset, variant)` pair, Read the variant once; pass inline as `variant_inline`. Use the asset's `default-variant` when the manifest doesn't specify. Omit for atomic assets.

### Per-Asset Slice

For each asset, build an `asset_slice` from the approved brief: asset manifest entry + launch narrative excerpt + matched proof + narrative header. Writers consume the slice as primary input; the full brief stays on disk.

### Writer Dispatch

Default mode: **subagent**, issued in parallel within a wave.

| Context | Source |
|---|---|
| `asset_slice` | Built per asset (above) |
| `scenario` | Brief frontmatter `scenario` block — passed verbatim |
| `extracted_context` | Brief body — verbatim |
| `voice_gate` (inline) | Loaded once pre-wave |
| `asset_inline` | Loaded once per asset |
| `variant_inline` | Loaded once per `(asset, variant)`; omitted for atomic assets |
| `asset_specific_docs` (paths) | Asset manifest `context_resolution` |
| `dependency_paths` | Previously generated assets in `output/launches/[name]/` |
| `reader_mode` | Asset manifest |

When `reader_mode: subagent`, the writer dispatches the reader on Haiku which loads `.claude/skills/craft/review/SKILL.md`. The writer surfaces only "Major rework" verdicts to the launch orchestrator.

### Producer Dispatch

After the writer (and reader, when `reader_mode: subagent`) complete for an asset, if the manifest declares a `production:` field, dispatch the producer subagent. Per-asset dispatches are independent — failures on one asset don't block others; surface warnings in the launch run summary.

Payload mirrors build-campaign's Producer Dispatch — see that builder for the full payload table and dispatch pattern. The only difference: `output_destination` uses the launch folder layout (`output/launches/[name]/[id]-[slug].html`).

If `brand/DESIGN.md` is missing or non-conformant, the producer refuses. Surface the specific failure in the launch run summary; the rest of the wave continues. To enable production, the user runs the one-time setup in `docs/brand-system.md`.

### Mid-Flow Approval Gate

After all internal waves complete, **stop**. Surface internal assets to the user:

> "Internal assets are ready. Review before I start external content?"

Update `status: mid-gate`. Wait for explicit approval before proceeding to external waves. This is the safety mechanism that prevents external content from shipping before sales/CS/support are aligned.

After user approval: `status: external-in-progress`. Proceed to Wave 3.

### Output Structure

```
output/launches/
  [launch-name]/
    brief.md
    internal/
      a01-[slug].md          ← markdown deliverable
      a01-[slug].json        ← JSON deliverable
      ...
    external/
      a07-[slug].md
      a07-[slug].json
      ...
    _meta/
      a01-[slug].md          ← audit trail
      a02-[slug].md
      ...
```

Internal and external tracks separate cleanly. Audit trails sit alongside in `_meta/`.

### Progress Tracking

Update each asset's `status` in `brief.md` as waves complete. Surface writer-flagged issues between waves. Pause at the mid-flow gate; pause at the end of external waves for final review.

After all external waves complete: update `status: complete`, present completion summary (per-asset status, flagged gaps still open, launch directory path), append journal entry to `output/journal.md`.

---

## Messaging House Gaps Tracking

Surfaced in the brief and again in the completion summary. Common: new product profile, solution profile update, position.md competitive section revision. Not blocking — launch ships first. Resolve via `/design [type] [slug]` after launch.

---

## Edge Cases

- **No input materials.** AskUserQuestion to collect the minimum for synthesis. Slower path — launch works best with product artifacts.
- **Launch conflicts with existing messaging.** Flag explicitly; do not resolve silently. Note in messaging gaps.
- **Beta / limited availability.** Adjust external messaging to reflect availability constraints. Soften GA language where required.
- **No proof at launch.** Common and expected. Writers use capability claims rather than outcome claims when proof is thin.
- **Asset not in messaging house.** Flag during brief generation; `/design asset [slug]` to define one, or map to closest.
- **Partial production failure.** Mark `needs-revision`, continue the wave. Downstream assets see a flagged dependency.
