---
name: build-play
description: Generates a scenario-specific GTM play (competitive displacement, expansion, win-back, signal, partner) with the assets needed to run it. Use when the user wants to build a targeted play around a competitive, account, or moment trigger.
---

# Play Skill

Generate a complete GTM play for a specific buying scenario — competitive displacement, signal-driven outreach, expansion, win-back, partner motion, or custom. Synthesize the messaging house into a play strategy, plan the field assets that operationalize it, get approval, then dispatch writer subagents per asset. Invoked via `/build play [type] [name]`.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, ICP, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## Skill Composition

- **Loads at workflow level:** the Context Loading pillar set (see below).
- **Loads after intake:** the selected persona, named competitor (for competitive plays), products in scope, supporting stories/reports.
- **Loads once per play (passed inline to writers):** the voice craft skill.
- **Loads once per asset (passed inline):** the asset envelope and variant (when declared).
- **Dispatches:** the writer subagent per asset (parallel within waves).
- **Per-asset reader dispatch:** the reader subagent; reader_mode per asset. Reader runs on Haiku and loads the review craft skill.

## Context Loading

Load these pillars at intake; defer the rest until needed.

| Play type | Always at intake | Deferred until needed |
|---|---|---|
| **competitive** | profile, pitch, position, people, portfolio | proof (load at brief writing) |
| **signal** | profile, pitch, position, people | portfolio, proof (load only if assets require) |
| **expansion** | profile, pitch, portfolio, people, proof | position (load if competitive angle surfaces) |
| **win-back** | profile, pitch, position, people, proof | portfolio (load if reactivation references products) |
| **partner** | profile, pitch, portfolio, people | position, proof (load only if needed) |
| **custom** | Full pillar set | — |

For all types, route through pillar Collection Tables to surface the relevant collection profiles: persona(s), named competitor (competitive), products in scope (expansion/partner), supporting stories/reports (proof-heavy plays).

---

## Phase 1: Intake

Resolve play type first: use the argument if provided, otherwise ask the user to pick from competitive, signal, expansion, win-back, partner, custom. Then run a structured conversation resolving scenario, profile selections, and asset selections.

### Check Input Materials

Scan `input/` subdirectories. Match by `--play-[slug]` suffix or by topic. Priority: `input/messaging/`, `input/research/` (competitive intel, signal data), `input/transcripts/` (win-back), `input/docs/`, `input/examples/`, root.

### Play Types

| Type | Description | Default Assets |
|---|---|---|
| **competitive** | Displace or defend against a named alternative | Competitive battlecard, comparison page, displacement email sequence, objection handling guide, internal cheat sheet |
| **signal** | Compelling-event triggered outreach | Signal map, outbound email sequence, LinkedIn message sequence, sales talking points |
| **expansion** | Existing-customer cross-sell or upsell | Expansion email sequence, account brief, internal cheat sheet, customer-facing one-pager |
| **win-back** | Re-engage churned or stalled accounts | Re-engagement email sequence, win-back talking points, updated value summary, decision-maker brief |
| **partner** | Co-sell or joint-solution motion | Partner better-together brief, joint-solution guide, partner outreach sequence |
| **custom** | Anything else | User-defined |

### Scenario Inference

Infer the play's scenario across the 5 dimensions in MESSAGE.md `## Scenarios` before profile selection. Plays map most strongly to `Strategic shape` (the play type usually IS the strategic shape) and `Content lens` (plays are usually Activation or Acquisition stage).

| Dimension | Play-specific signals | Default |
|---|---|---|
| Compelling event | Trigger that activated the play (intent signal, breach, leadership change, renewal window) | `none` (the trigger IS the event) |
| Topic maturity | Category state per MESSAGE.md Position | `established` |
| Market moment | Recent competitor activity or market shift relevant to this play | `none` |
| Strategic shape | Play type maps directly: competitive → `competitive-takeout`; expansion → `customer-expansion`; signal/win-back → `demand-generation`; partner → `brand-campaign` (joint) | derived from play type |
| Content lens | Play-type-driven: competitive → Acquisition; signal → Acquisition; expansion → Adoption / Advocacy; win-back → Acquisition; partner → Awareness + Acquisition | `Acquisition` |

**Play-type-specific gap questions:**

| Type | Attributes |
|---|---|
| **competitive** | Which competitor? Greenfield or displacement? Specific weakness or moment we're targeting? Which persona owns the decision? |
| **signal** | What signal triggers the play? How is it detected (intent data, news, hiring, funding, breach disclosure)? Window the signal stays hot? |
| **expansion** | Which segment of customers? Which product is the expansion vector? Catalyst (usage maturity, renewal window, org change)? |
| **win-back** | Why did the deal stall or churn? What's changed on our side or theirs? Right re-entry persona? |
| **partner** | Which partner? Joint use case? Who pitches first — us, partner, or both? |
| **custom** | Free-form — scenario, trigger, win condition. |

Surface the inferred scenario back to the user before profile selection; allow adjustments.

### Profile Selection

Resolve shared messaging context for the play:

| Parameter | Question |
|---|---|
| **Persona(s)** | Who does this play target? Required. |
| **Competitor** | For competitive plays — against whom? |
| **Product/Solution** | What's in scope? |
| **Segment** | Is this segment-specific? |

If the user names an entity not in the messaging house, flag and offer `/design [type] [slug]`.

### Asset Selection

Present the default asset set as a numbered checklist via AskUserQuestion. User can Add, Remove, Modify, Reassign per-asset persona, or define Custom. Verify each asset exists in MESSAGE.md `## Assets`; flag missing.

Confirm the final list before the brief.

### Production Targets

After the asset list is final, ask which assets to produce as HTML. Skip the entire sub-flow if the user opts out: "Produce HTML for any play assets? (yes/no)" — if no, set `production: null` for all and continue.

If yes, for each asset whose envelope declares a non-empty `production-targets` frontmatter array:

1. Ask: "Produce [asset-id] ([asset-slug]) as HTML? (yes/no)"
2. If yes and the asset has multiple targets: ask "Which target? Options: [list from production-targets]"
3. If yes and the asset has one target: use it (no question)
4. Result populates the asset's `production:` field in the brief manifest (e.g., `production: web`); omitted when the user declines

Assets with empty `production-targets` are skipped automatically.

---

## Phase 2: Play Brief

Generate folder name: play type + kebab-case scenario slug + current date (e.g., `competitive-acme-displacement-05-22-26`). Write to `output/plays/[folder]/brief.md`. **The user must approve before production begins.**

### Brief Length Discipline

Target **~150–200 lines total for a 4–6 asset play**, scaling proportionally.

| Section | Target | Rule |
|---|---|---|
| Frontmatter | 25–30 lines | Essential contract fields only |
| Play Summary | ~10 lines | One paragraph + headline facts |
| Play Strategy | ~30 lines | Trigger, win condition, positioning, key messages, counter-moves |
| Field Playbook | ~20 lines | Sequence, timing, persona handoffs, fixed vs. flex |
| Asset Manifest | 7 lines × N assets | Tight spec per asset |
| Generation Sequence | ~5 lines | One line per wave |
| Extracted Context | 40–60 lines | Selective verbatim |
| Flagged Issues + Approval Gate | ~10 lines | Bullets |

### Brief Frontmatter

- `play_name` — Semantic kebab-case identifier
- `play_folder` — Directory name
- `play_type` — competitive, signal, expansion, win-back, partner, custom
- `scenario_summary` — One-sentence scenario summary (free-form)
- `scenario` — 5-dimension scenario block from Phase 1 inference. Keys: `compelling-event`, `topic-maturity`, `market-moment`, `strategic-shape`, `content-lens`. `strategic-shape` is typically derived from play type.
- `created` — Date string
- `status` — draft → approved → in-progress → complete
- `shared_context` — Personas, products, competitors, segments, `messaging_docs_loaded` list
- `assets` — Array of entries: id, asset, variant, persona, altitude, depends_on, reader_mode, status, production (optional — `web` | `email` | `print`; omitted when not producing HTML)

### Brief Body Sections

#### Play Strategy

The strategic argument for the play. Derived from the messaging house.

- **Trigger** — The event, signal, or moment that activates the play. For signal plays, list the specific signals. For competitive plays, the displacement window. For expansion, the maturity threshold.
- **Win condition** — Concrete outcome. Not a feeling.
- **Positioning** — 2–3 sentence argument. From `pitch.md` (UVPs, differentiators) + `position.md` + relevant collection profiles.
- **Key messages** — 3–5 grounded claims, each citing source and supporting proof from `proof.md`.
- **Counter-moves** — For competitive and win-back plays: predicted objections / competitor responses and how the messaging holds up.

#### Field Playbook

Operational guidance for the team running the play.

- **Sequence** — Order of touches and channels.
- **Timing** — How long the play runs; when to pivot; when to abandon.
- **Persona handoffs** — When the conversation expands beyond the entry persona. Reference Buying Considerations from `people.md`.
- **What stays consistent vs. what flexes** — Fixed message + room for personalization.

#### Asset Manifest

Tight 7-line spec per asset:

```yaml
- id: a01
  asset: competitive-battlecard
  variant: thought-leadership
  persona: security-program-owners
  altitude: practitioner
  reader_mode: subagent
  production: print
  depends_on: []
  notes: anchor — front of the playbook
  context_resolution: [asset-specific docs beyond shared play context]
```

`reader_mode` heuristic: **subagent** for battlecard, comparison page, partner-facing assets (external-quality required); **inline** for internal cheat sheets and derivative sequences.

#### Extracted Context

Same shape as build-campaign. Sections: Positioning, Key Messages with Verbatim Source Lines, Glossary Subset, Proof Library, Voice & Differentiation Anchors.

#### Generation Sequence

Order assets by dependency graph into waves. Independent assets generate in parallel.

### Approval Flow

Present a summary (play name, type, scenario, asset count, wave count, flagged gaps). User can Approve, Edit, or Cancel.

---

## Phase 3: Composition

After approval, update `status: in-progress` and generate by wave.

### Pre-Wave Setup

Before dispatching the first wave:

1. **Load voice gate once.** Read `.claude/skills/craft/voice/SKILL.md`; pass inline as `voice_gate` in every dispatch.
2. **Resolve assets per content-type.** For each unique asset, Read the asset envelope once; pass inline as `asset_inline`.
3. **Resolve variants per asset.** For each `(asset, variant)` pair, Read the variant once; pass inline as `variant_inline`. Use the asset's `default-variant` when the manifest doesn't specify. Omit for atomic assets.

### Per-Asset Slice

For each asset, build an `asset_slice` from the approved brief: asset manifest entry + play strategy excerpt + matched proof + counter-moves (when relevant). Writers consume the slice as primary input.

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
| `dependency_paths` | Previously generated assets in `output/plays/[folder]/` |
| `reader_mode` | Asset manifest |

When `reader_mode: subagent`, the writer dispatches the reader on Haiku which loads `.claude/skills/craft/review/SKILL.md`. Writer surfaces "Major rework" verdicts to the play orchestrator.

### Producer Dispatch

After the writer (and reader, when `reader_mode: subagent`) complete for an asset, if the manifest declares a `production:` field, dispatch the producer subagent. Per-asset dispatches are independent — failures on one asset don't block others; surface warnings in the play run summary.

Payload mirrors build-campaign's Producer Dispatch — see that workflow for the full payload table and dispatch pattern. The only difference: `output_destination` uses the play folder layout (`output/plays/[folder]/[id]-[slug].html`).

If `brand/DESIGN.md` is missing or non-conformant, the producer refuses. Surface the specific failure in the play run summary; the rest of the wave continues. To enable production, the user runs the one-time setup in `docs/brand-system.md`.

### Dependency Handling

Pass dependency content as reference for narrative continuity. For competitive plays, the battlecard usually anchors — later assets reference it for consistent positioning.

### Output Structure

```
output/plays/
  [type-scenario-mm-dd-yy]/
    brief.md
    a01-[slug].md          ← markdown deliverable
    a01-[slug].json        ← JSON deliverable
    a02-[slug].md
    a02-[slug].json
    ...
    _meta/
      a01-[slug].md        ← audit trail
      a02-[slug].md
```

### Progress Tracking

Update each asset's `status` as waves complete. Surface writer-flagged issues between waves.

After all waves complete: update `status: complete`, present a completion summary, append a "process" journal entry to `output/journal.md`.

---

## Edge Cases

- **Competitor not in messaging house.** Critical for competitive plays — flag and recommend `/design competitor [slug]` before proceeding.
- **Signal not yet documented.** For signal plays, capture the signal definition in the brief itself (under Trigger). Plays don't require a separate signal collection.
- **Persona not in messaging house.** Flag during intake. Suggest `/design persona [slug]`.
- **Asset not in messaging house.** Flag during brief generation; `/design asset [slug]` to define one, or map to closest existing asset with adaptation notes.
- **Custom asset.** Identify the closest skill mapping and add to the manifest with adaptation notes.
- **Partial production failure.** Mark `needs-revision`, continue the wave.
