---
name: build-campaign
description: Plans multi-asset content campaigns from a topic or theme — synthesizes inputs, assembles a bill of materials, writes a messaging brief for approval, then dispatches writer subagents per asset. Use when the user wants to build a digital, outbound, or ABM campaign around a topic.
---

# Campaign Skill

Plan multi-asset content campaigns. Synthesize inputs, assemble a bill of materials, write a structured messaging brief for human approval, then dispatch the writer subagent per asset with precisely scoped context. Invoked via `/build campaign [type] [topic]`.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## Skill Composition

- **Loads at workflow level:** the campaign-type's Context Loading pillar set (see below).
- **Loads after user selection:** selected persona, product, competitor, category, segment collections.
- **Loads once per campaign (passed inline to writers):** the voice craft skill.
- **Loads once per asset (passed inline to writers):** the asset envelope and, when declared, the variant.
- **Dispatches:** the writer subagent per asset (parallel within waves) with a pre-built **asset slice** instead of the full brief.
- **Per-asset reader dispatch:** the reader subagent per asset; mode chosen per asset in the manifest (inline for derivatives, subagent for high-stakes). Reader runs on Haiku and loads the review craft skill; writers run on the parent's model.

## Context Loading

Load these pillars at intake; defer the rest until needed.

| Type | Always at intake | Deferred until needed |
|---|---|---|
| **digital** | profile, pitch, position, people, proof | portfolio (load when an asset references a product/solution) |
| **outbound** | profile, pitch, position, people, proof | portfolio (load only if asset list includes product-page or product-newsletter) |
| **abm** | profile, pitch, position, people, proof | portfolio (load only if the account context references specific products) |

Brief writing always loads `proof.md` if not already loaded — proof matching is non-negotiable. Portfolio loads when the asset manifest first references a product/solution.

During intake, route through pillar Collection Tables before loading any collection profile. Read frontmatter of candidates first to enrich AskUserQuestion options (`type`, `status`, `priority`, `description`); load full bodies only after user confirms selection.

---

## Phase 1: Intake

Resolve campaign type first: use the argument if provided, otherwise ask the user to pick from digital, outbound, abm. Then run a structured conversation resolving profile selections and asset selections. Use AskUserQuestion to present options from pillar Collection Tables and the `## Assets` table.

### Check Input Materials

Scan `input/` subdirectories in priority order — `input/messaging/`, `input/docs/`, `input/research/`, `input/transcripts/`, `input/examples/`, root. Match by `--campaign-[slug]` suffix or topic-relevant prefix. Note matches; they supplement (don't replace) the intake conversation.

### Campaign Types

| Type | Description | Default Assets |
|---|---|---|
| **digital** | Inbound content engine | Thought leadership blog (anchor), white paper or research report (alternative anchor), use case blog series (2–3 posts), nurture email sequence (3–5 emails), social post series, product page copy |
| **outbound** | Sales-driven prospecting | Cold email sequence (3–5 emails), LinkedIn message sequence, sales one-pager, competitive battlecard |
| **abm** | Account-based targeting | Account brief, personalized email sequence, solution page copy, sales talking points, executive summary |

If type is implied but not stated, confirm: "This sounds like a [type] campaign. I'd suggest these assets: [default list]. Want to adjust?"

### Scenario Inference

Infer the campaign's scenario across the 5 dimensions in MESSAGE.md `## Scenarios` before profile selection. Combine signals from the user's request, recent messaging house activity (stories/reports/competitors/categories modified in the last 30 days), `insights/findings/`, and campaign-type defaults. Surface the inferred scenario for user confirmation.

| Dimension | Campaign signals | Default |
|---|---|---|
| Compelling event | Named events, customer wins, analyst reports, executive moves | `none` |
| Topic maturity | Category state per Position; product lifecycle | `established` |
| Market moment | Competitive incursions, regulatory shifts in past 90 days | `none` |
| Strategic shape | Objective intent: launching → new-product-introduction; competitive → competitive-takeout; awareness-led → thought-leadership; demand-led → demand-generation; expansion → customer-expansion | `thought-leadership` |
| Content lens | Funnel stage: top → Awareness; mid → Acquisition; trial → Activation; onboarding → Adoption; existing-customer → Advocacy; reach → Amplification | `Awareness` |

**Campaign-type-specific gap questions** (only ask what signals don't answer):

| Type | Additional questions |
|---|---|
| **digital** | Content theme or angle? Anchor asset preference? |
| **outbound** | Prospecting trigger (why now)? Target account profile? Value hypothesis? Channel preference (email, LinkedIn, multi-channel)? |
| **abm** | Target account(s)? Known stakeholders? Deal stage? Account intelligence (recent news, initiatives, tech stack)? |

The user can adjust any inferred dimension; locked-in values flow into the brief frontmatter.

### Profile Selection

Resolve campaign-wide messaging context. These become the **shared context** every asset inherits.

| Parameter | Multi-select? | Required |
|---|---|---|
| **Persona(s)** | Yes — different assets may target different personas | **Yes** |
| **Product/Solution** | Usually one (multiple for portfolio campaigns) | No |
| **Category** | Usually one | No |
| **Competitor** | Yes if competitive | No |
| **Segment** | Usually one | No |

For each parameter, present the relevant pillar's Collection Tables with Descriptions via AskUserQuestion. If the user names an entity not in the messaging house, flag it and offer `/design [type] [slug]` to compose it first or fall back to pillar-level context. Per-asset persona targeting is resolved in the asset manifest, not at the campaign level.

### Asset Selection

Present the default BOM for the resolved campaign type as a numbered checklist with skill mappings visible. Walk through interactively via AskUserQuestion.

Options:
- **Add** — From MESSAGE.md `## Assets` or a custom asset (work with the user to identify the closest existing asset; if none fits, suggest `/design asset [slug]` to create one before continuing).
- **Remove** — Drop assets they don't need.
- **Modify** — Scope changes ("Make the blog series 4 posts instead of 2").
- **Reassign** — Per-asset persona targeting.

For each asset, verify the asset envelope exists. If the manifest entry specifies a variant, verify that variant file exists. If either is missing, flag with alternatives (closest asset, asset's default-variant, or atomic if no variants directory). Confirm the final asset list before proceeding to the brief.

### Production Targets

After the asset list is final, ask which assets to produce as HTML. Skip the entire sub-flow if the user opts out: "Produce HTML for any of these assets? (yes/no)" — if no, set `production: null` for all and continue.

If yes, for each asset whose envelope declares a non-empty `production-targets` frontmatter array:

1. Ask: "Produce [asset-id] ([asset-slug]) as HTML? (yes/no)"
2. If yes and the asset has multiple targets: ask "Which target? Options: [list from production-targets]"
3. If yes and the asset has one target: use it (no question)
4. Result populates the asset's `production:` field in the brief manifest (e.g., `production: web`); omitted when the user declines for that asset

Assets with empty `production-targets` (e.g., social-post, internal Slack messages) are skipped automatically — no question asked.

### Intake Output

By the end of intake, you have: campaign type and name, one-sentence objective, shared profile selections, final asset list with per-asset persona assignments and asset/variant mappings, flagged gaps (missing personas, missing skills, thin context).

---

## Phase 2: Messaging Brief

The brief is the plan. Write to `output/campaigns/[topic-mm-dd-yy]/brief.md`. **The user must approve it before production begins.**

### Brief Length Discipline

A brief is a planning artifact — not a content asset. Tight is correct. Target **~180–220 lines total for a 5–7 asset campaign**, scaling proportionally for larger campaigns (extra lines come only from additional asset manifest entries, not from re-expanding the narrative sections).

| Section | Target | Rule |
|---|---|---|
| Frontmatter | 25–30 lines | Essential contract fields only — no narrative duplication |
| Campaign Summary | ~10 lines | One short paragraph + headline frontmatter facts |
| Campaign Narrative | ~30 lines | Positioning (3 sentences), 3–5 key messages at ~3 lines each |
| What to Know | ~25 lines | 5 sub-sections at 2–3 sentences each |
| Asset Manifest | 7 lines × N assets | Tight spec per asset; no prose |
| Generation Sequence | ~6 lines | One line per wave with comma-separated asset IDs |
| Extracted Context | 60–80 lines | Selective verbatim — only passages writers can't derive from the asset slice |
| Flagged Issues + Approval Gate | ~10 lines | Bullets, not prose |

**Selectivity rule for Extracted Context:** quote only what writers can't derive. If a key message in the manifest already carries the positioning, don't re-quote `pitch.md` in Extracted Context. Quote when the asset slice references back to it.

### Brief Frontmatter

- `campaign_name` — Semantic kebab-case identifier
- `campaign_folder` — Directory name: kebab-case topic + date (mm-dd-yy)
- `campaign_type` — digital, outbound, abm, or "custom"
- `objective` — One-sentence campaign goal
- `created` — Date string
- `status` — draft → approved → in-progress → complete
- `scenario` — 5-dimension scenario block from Phase 1 inference. Keys: `compelling-event`, `topic-maturity`, `market-moment`, `strategic-shape`, `content-lens`. Values may be null where no signal applied.
- `shared_context` — Personas, products, competitors, segments, `messaging_docs_loaded` list
- `assets` — Array of entries: id, asset, variant, persona, altitude, depends_on, reader_mode, status, production (optional — `web` | `email` | `print`; omitted when not producing HTML)

### Brief Body Sections

#### Campaign Narrative

- **Positioning** — 2–3 sentences derived from `profile.md` + `position.md` + `pitch.md` + product/solution doc. Assembled, not invented.
- **Key Messages** — 3–5 specific defensible claims. Each: claim, source citation, matching proof from `proof.md` (or "No proof available"), asset emphasis (which manifest IDs).
- **Glossary terms in play** — One-line definitions for the campaign-relevant subset from MESSAGE.md's Glossary. Flag any net-new terms for `/run investigation fix glossary`.

#### What to Know

Internal primer for sales, field, executives, partners. 5 sub-sections at 2–3 sentences each:
- **Campaign context** — Why now. The trigger, signal, or business event.
- **Who we're talking to** — Persona(s) in plain language, drawn from selected persona profiles.
- **What we're saying** — Key messages in conversational language.
- **How we're different** — Competitive angle from `position.md`, `pitch.md`, competitor profiles if loaded.
- **Proof we can point to** — Matched stories and metrics from `proof.md` and loaded stories.
- **Common objections** — 2–4 likely pushbacks and how to address them.

#### Asset Manifest

Tight 7-line spec per asset (no prose paragraphs):

```yaml
- id: a01
  asset: blog-post
  variant: thought-leadership
  persona: security-executives
  altitude: executive
  reader_mode: subagent
  production: web
  depends_on: []
  narrative_thread: KM1, KM3 — leads on AI-readiness inflection
  notes: anchor asset; ~1500 words
  context_resolution: [asset-specific docs beyond shared campaign context]
```

`reader_mode` heuristic: **subagent** for anchor blogs, press releases, executive content, customer-facing announcements, anything surfacing direct quotes. **inline** for derivatives — social, nurture emails, supporting use-case blogs.

#### Extracted Context

Verbatim source material writers consume in lieu of re-reading shared pillars. Built during brief writing while the full pillar set is loaded; frozen at approval.

```markdown
## Extracted Context

### Positioning (verbatim from pitch.md + position.md)
[Direct copy of the positioning paragraphs. Cite source line ranges.]

### Key Messages with Verbatim Source Lines
[Each key message paired with the verbatim source passage(s), with file path and line range.]

### Glossary Subset
[Only the glossary terms this campaign exercises, verbatim from MESSAGE.md.]

### Proof Library
[Full text of matched customer stories and analyst evidence — the exact quotes writers can use.]

### Voice & Differentiation Anchors
[Brand voice + differentiation guardrails that apply across all assets in this campaign.]
```

#### Generation Sequence

Order assets by dependency graph into waves. Independent assets go in Wave 1 (parallel dispatch). Subsequent waves wait for their dependencies.

### Approval Flow

After writing the brief, present a summary (campaign name, type, objective, shared context, asset count, wave count, flagged issues) and accept Approve / Edit / Cancel. On Edit, modify through conversation or have the user edit the file directly and tell you to re-read. On Cancel, the brief is discarded.

---

## Phase 3: Composition

After approval, update `status: in-progress` and generate by wave.

### Pre-Wave Setup

Before dispatching the first wave:

1. **Load voice gate once.** Read `.claude/skills/craft/voice/SKILL.md`; pass content inline as `voice_gate` in every dispatch.
2. **Resolve assets per content-type.** For each unique asset in the wave, Read the asset envelope once; pass inline as `asset_inline`. Lookup via MESSAGE.md's `## Assets` table or per-asset manifest override.
3. **Resolve variants per asset.** For each `(asset, variant)` pair in the wave, Read the variant once; pass inline as `variant_inline`. If the manifest doesn't specify a variant, use the asset's `default-variant` frontmatter field. For atomic assets (no variants/ directory), omit `variant_inline`.

### Per-Asset Slice

For each asset, build an `asset_slice` from the approved brief:

- **Asset manifest entry** — Full entry from Phase 2.
- **Tagged key messages** — Only key messages whose `Assets:` field includes this asset's id. Verbatim text plus source citations.
- **Matched proof** — Only proof entries tagged to those key messages.
- **Narrative header** — Positioning paragraph + "What we're saying" / "How we're different" framing.

Writers consume the asset slice as primary input. The full brief stays on disk for resume/audit; writer subagents don't Read it.

### Writer Dispatch

Default mode: **subagent**, issued in parallel within a wave.

| Context | Source |
|---|---|
| `asset_slice` | Built per asset (above) |
| `scenario` | Brief frontmatter `scenario` block — passed verbatim to every asset in the campaign |
| `extracted_context` | Brief body — verbatim |
| `voice_gate` (inline) | Loaded once pre-wave |
| `asset_inline` | Loaded once per asset; resolved via MESSAGE.md `## Assets` |
| `variant_inline` | Loaded once per `(asset, variant)`; omitted for atomic assets |
| `asset_specific_docs` (paths) | Asset manifest `context_resolution` |
| `dependency_paths` | Previously generated assets in `output/campaigns/[folder]/` |
| `reader_mode` | Asset manifest |

**Dispatch pattern:**

```
Agent(
  subagent_type: "writer",
  prompt: "Apply the protocol in .claude/agents/writer.md (Campaign mode) to asset [asset-id] in campaign [folder].

  Asset slice:
  [paste asset_slice]

  Extracted Context (shared, verbatim):
  [paste Extracted Context block]

  Voice gate (inline):
  [paste full voice gate content]

  Asset (inline):
  [paste resolved asset envelope content — content-keys, array-keys, Conventions, Frontmatter requirements]

  Variant (inline, when present):
  [paste resolved variant content — When to use, Voice notes, Structure, CTA conventions, Examples]

  Asset-specific messaging docs (paths — re-read these fresh):
  [list]

  Dependency asset paths:
  [list]

  Reader dispatch mode: [inline | subagent]

  Produce both .md and .json deliverables plus a _meta/ audit file. Return file paths and a one-line status (complete | needs-revision)."
)
```

When `reader_mode: subagent`, the writer dispatches the reader on Haiku (`model: "claude-haiku-4-5-20251001"`) which loads `.claude/skills/craft/review/SKILL.md` for the evaluation framework. The writer surfaces only "Major rework" verdicts and critical gaps to the orchestrator.

### Producer Dispatch

After the writer (and reader, when `reader_mode: subagent`) complete for an asset, if the manifest declares a `production:` field, dispatch the producer subagent. Per-asset dispatches are independent — failures on one asset don't block others; surface warnings in the run summary.

Payload:

| Key | Source |
|---|---|
| `target` | Asset manifest `production` field |
| `asset_slug` | Asset manifest `asset` field |
| `variant_slug` | Asset manifest `variant` field (omitted when atomic) |
| `writer_output_md` | Path the writer returned (`output/campaigns/[folder]/[id]-[slug].md`) |
| `writer_output_json` | Sibling `.json` path |
| `output_destination` | `output/campaigns/[folder]/[id]-[slug].html` (web), `.email.html` (email), `.print.html` (print) |
| `asset_metadata` | Title, excerpt, publishing — extracted from the writer `.json` |

Dispatch:

```
Agent(
  subagent_type: "producer",
  prompt: "Apply the protocol in .claude/agents/producer.md. Produce HTML for asset [asset-id] in campaign [folder].

  target: [web | email | print]
  asset_slug: [slug]
  variant_slug: [variant or null]
  writer_output_md: [path]
  writer_output_json: [path]
  output_destination: [path]
  asset_metadata: { title, excerpt, publishing }"
)
```

If `brand/DESIGN.md` is missing or non-conformant, the producer refuses. Surface the specific failure in the campaign run summary; the rest of the wave continues. To enable production, the user runs the one-time setup in `docs/brand-system.md`.

### Dependency Handling

Pass dependency content as reference context for narrative continuity. For 10+ asset campaigns, pass summaries (key arguments, positioning, CTAs) rather than full files.

### Output Structure

```
output/campaigns/
  [topic-mm-dd-yy]/
    brief.md
    a01-[slug].md          ← clean markdown deliverable
    a01-[slug].json        ← structured JSON deliverable (CMS-ready)
    a02-[slug].md
    a02-[slug].json
    ...
    _meta/
      a01-[slug].md        ← audit trail (brief spec excerpt, outline, design notes,
                              messaging references, self-assessment, reader scores)
      a02-[slug].md
```

The writer protocol writes all three artifacts per asset together (see `.claude/agents/writer.md` Step 9). Resume flows read both `.md` deliverables and `_meta/` audit files.

### Progress Tracking

Spot-check the brief between waves; update each asset's `status` in `brief.md` frontmatter as waves complete (`pending` → `complete` or `needs-revision`). Surface writer-flagged issues from return payloads between waves.

After all waves complete: update `status: complete`, present a completion summary (per-asset status, flagged issues, messaging docs loaded, campaign directory path), and append a "process" journal entry to `output/journal.md`.

---

## Edge Cases

- **Asset not in messaging house.** Flag during brief generation; suggest `/design asset [slug]` to define one, or map to the closest existing asset with adaptation notes.
- **Writing-type variant not in `types/`.** Flag during brief generation; suggest `/design asset [slug]` to generate a paired variant, or pick a sibling variant.
- **Persona not in messaging house.** Flag during intake; offer `/design persona [slug]` to compose or pillar-level fallback from `people.md` (noted in the brief).
- **Context window pressure on large campaigns (10+ assets).** Track assets by file path; pass dependency content as summaries.
- **Partial production failure.** Mark the asset `needs-revision`, continue the wave. Downstream assets see a flagged dependency.
- **Campaign type not listed.** Propose a custom BOM built from MESSAGE.md `## Assets`.
- **User invokes `/build campaign event`.** Events are now their own workflow. Redirect: "Events have phase-distinct audiences (pre/on-site/post) and an asset mix that outgrew the campaign-as-single-wave model — run `/build event [event-name]` instead."
