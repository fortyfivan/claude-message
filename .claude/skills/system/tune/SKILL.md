---
name: tune
description: Define the company's asset types and variants from its go-to-market motions. Use after bootstrap to populate the asset layer — interviews on the campaigns, launches, plays, and events the team runs, calibrates altitude and format from existing examples, then generates every asset envelope + variant in parallel. Resolves the MESSAGE.md `## Assets` catalog.
---

# Tune Skill

Define the asset layer of the messaging house — the `asset.md` envelopes and their variants — from the company's go-to-market motions. Bootstrap builds the *house* (pillars, collections, MESSAGE.md); tune builds the *production layer* on top of it.

Treat this as a strategist mapping content operations, not a scribe cataloguing file types. The right asset catalog falls out of the motions the company actually runs: a team that runs ABM campaigns and hosts a customer summit needs different assets — and different variants of each — than one running inbound digital campaigns and sponsoring conferences. Infer the catalog from the motions and the examples; ask only what you can't infer.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the people pillar," "the CISO persona"). If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## Precondition

Tune requires a populated, conformant house — it grounds every variant's voice and altitude in existing personas, the voice profile, and the customer journey. Before starting, confirm MESSAGE.md exists and the pillars are populated. If the house is empty or non-conformant, refuse:

> "Tune defines your asset types from a populated messaging house — it needs your personas, voice, and journey to calibrate each asset. The house isn't ready yet. Run `/bootstrap` to build it, or `/run health` if you think it's already there."

---

## Three phases

1. **Discover** — runs in two tiers. *Tier A (Catalog):* ground in the house, scan `input/`, map the company's GTM motions to a candidate asset+variant list. *Tier B (Shape):* drill each asset and variant into a concrete **anatomy** — grounded in a real specimen, not inferred from motion type.
2. **Plan** — compose the **asset plan** (`messaging/.tune-plan.md`): the resolved catalog, each variant carrying its full structure anatomy. Run an integrity check; get explicit approval.
3. **Generate** — fan out `designer` subagents in two waves (envelopes, then variants) from the approved plan, passing each variant's specimen inline. Reconcile the MESSAGE.md `## Assets` table and each envelope's `## Variants` table, then clean up.

The phases are gated. Phase 3 cannot start until the plan is approved. The plan is the consistency contract: one agent resolves the whole catalog — every asset, every variant, every convention — so the parallel writers in Phase 3 transcribe their slice instead of re-deriving format and voice from each other.

---

## Phase 1: Discover

Two tiers. **Tier A** builds the catalog (which assets + variants exist). **Tier B** drills each into a concrete shape. Tier A is fast and breadth-first; Tier B is the heart of this skill — it's what keeps the output from going generic.

### Tier A — Catalog (breadth)

**Ground in the house.** Load the pillars that calibrate asset content: **people** (personas + ICP + journey — sets altitude and CTA per variant), **profile** (voice attributes), **pitch** and **position** (what each asset argues). Read the MESSAGE.md `## Assets` table — if rows already exist, tune *extends* the catalog (merge, don't duplicate). Note existing `messaging/assets/` slugs.

**Map motions to the asset universe.** The asset types a company needs are implied by the motions it runs. The four builders already encode the motion → default-asset mapping; read their default-Bill-of-Materials tables as the candidate universe:

| Builder | Source | Motion types → default assets |
|---|---|---|
| `builders/build-campaign/SKILL.md` | Campaign Types table (~lines 49–54) | digital, outbound, abm |
| `builders/build-launch/SKILL.md` | Context Loading by tier (~lines 29–37) + internal/external asset split | major, minor, feature, integration |
| `builders/build-play/SKILL.md` | Play Types table (~lines 50–57) | competitive, signal, expansion, win-back, partner, custom |
| `builders/build-event/SKILL.md` | Asset Plans by Phase (~lines 94–100) | industry-conference, hosted-conference, partner-event, regional-event, hospitality-event |

Take the **union of the default assets for the motions the company runs** as the candidate catalog. Resolve variants per asset from three signals: the motions that use it (each motion implies an editorial flavor — an outbound campaign's email is a different variant than a nurture campaign's), the personas/altitudes it targets, and any examples on hand.

**Motion interview** (light — infer what you can, ask only what you can't; a few grouped AskUserQuestion exchanges):

- **Which motions do you run?** Campaigns (digital / outbound / ABM), launches (cadence/tier mix), competitive or expansion plays, events (which types). The load-bearing question — it sets the catalog.
- **Channels** — where assets ship (email, web, print/PDF, social). Sets each asset's `production-targets`.
- **Cadence / priority** — which motions are frequent vs. occasional.

**Output of Tier A:** the asset+variant **list**, each item marked **priority** — `primary` (tied to a high-cadence motion, plus every asset's default/lead variant) or `long-tail` (occasional motion or secondary variant). Priority drives how hard Tier B drills each one.

### Tier B — Shape (depth, per asset + variant)

Catalog rows are not shapes. A "nurture email" or "product landing page" row tells you nothing about the *ordered sections, their lengths, the opening move, the CTA pattern* — and inferring those from the motion type is exactly what produces generic output. Tier B fixes that by grounding each shape in a real specimen.

**1. Find a specimen.** For each asset type, locate a real artifact — first from `input/examples/`, then the other `input/` dirs. A real sent email, a published landing page, a shipped one-pager is the truest signal for altitude, structure, and format. If none is staged, **actively solicit one** (batch the asks across assets):

> "To shape your [outbound email] accurately, paste a representative one — or point me to a file. One real send beats me guessing its structure."

Accept pasted text or a local file path (tune has no web access — it can't fetch a URL; ask the user to paste or save the file into `input/examples/`).

**2. Extract the anatomy.** Deconstruct each specimen into the variant template's sections (`templates/assets/[type]-template/variants/variant-template.md`):

- **Structure** — the ordered sections, each with its purpose and a length / word-count band (e.g., *Subject ≤6 words → Opening: 1 sentence on the trigger → Hook: 1–2 sentences naming the pain → Bridge: 1 sentence → CTA: single low-friction ask*).
- **CTA pattern** — placement, form (question vs. imperative), destination, policy (e.g., no calendar link on first touch).
- **Voice tells** — the register shift specific to this variant, on top of the house voice baseline.
- **Writing checks** — observable tells to enforce or avoid, including notable *absences* in the specimen (what good ones never do).
- **Envelope facts** — the `content-keys` / frontmatter the specimen actually uses, and overall length bands.

Synthesize across multiple specimens for the same variant. When one specimen covers an asset with several variants, map it to its matching variant and note which variants still lack one.

**3. Tier the depth.** Drill **primary assets + their default/lead variants to full anatomy** — a specimen is required; solicit if missing. **Long-tail variants** get a lighter spec: they inherit the envelope conventions plus a short structure adapted from the closest drilled sibling or the motion's content lens, and are marked `shape: inferred` so the gap is visible.

**4. Gap fallback.** If a *primary* item has no specimen and the user can't supply one, run a tight shape-interview for that item only — reuse the `design-asset` Phase C question set (`messaging/design-asset/SKILL.md`: structure sequence → CTA conventions → writing checks → voice notes). Don't duplicate those questions here; load that skill's flow. Mark the result `shape: interviewed`.

**Output of Tier B:** a concrete anatomy per variant, ready to drop into the plan.

---

## Phase 2: Plan

Compose the asset plan — the resolved catalog every envelope and variant generates from. Write it to `messaging/.tune-plan.md`. No web research; the catalog is what discovery surfaced.

### Plan fidelity: decisions, not prose

The plan carries the **irreducible decisions and raw material** a designer cannot derive — not pre-rendered envelope/variant copy. If a section reads like a finished variant file, it's too detailed (no time saved). If it reads like a production spec, it's right.

| In the plan (resolved decisions + material) | NOT in the plan (the designer renders these in voice) |
|---|---|
| Which asset types; each one's `content-keys` schema, `production-targets`, `publishing`, `default-variant` | The envelope's `## Conventions` prose paragraphs |
| Per-variant: when-to-use *trigger*, the voice-shift *note*, the **full structure anatomy** (ordered sections, each with purpose + length band), the CTA *pattern*, the writing-check *bullets* | The variant's `## When to use` / `## Voice notes` / `## Structure` written out in the company's voice |
| The **specimen excerpt** per variant — passed inline to the designer as the format-fidelity reference | Connective tissue and worked examples |
| Motion trace + priority + `shape:` grounding (grounded / inferred / interviewed) per item | — |

The structure anatomy is a **decision/material**, not prose: it comes from the specimen or the user, and the designer cannot derive it — so it belongs in the plan in full. Only the *rendering* of each section in voice is the designer's job. (Carrying the ordered sections + lengths is not "writing the file early"; omitting them is what produced generic files.)

### Plan structure

`messaging/.tune-plan.md`:

```markdown
---
company: [name]
status: draft        # → approved
motions: [the declared motions — campaign types, launch tiers, play types, event types]
channels: [email, web, print, social]
extends: [existing MESSAGE.md ## Assets rows being added to, if any]
---

# Asset Plan — [Company]

## Asset Catalog
One mini-brief per asset type. Each variant carries its full structure anatomy — enough for a designer to render the file without re-deriving the shape.

### [asset-slug]  (content-type: [brief verb] · template: [closest template-type] · motions: [trace] · priority: [primary | long-tail])
- **Envelope:** content-keys [list]; array-keys [list]; production-targets [list]; publishing [platform|—]; default-variant [slug]
- **Conventions (decisions):** [cross-variant standards — length norms, sender identity, deliverability/format rules — as bullets]
- **Specimen(s):** [`input/examples/<file>` | pasted | none]
- **Atomic?** [yes → the anatomy below lives in the envelope, no variants; no → one block per variant]

#### Variant: [slug]  (default: [✓|—] · priority: [primary | long-tail] · shape: [grounded | interviewed | inferred])
- **When-to-use trigger:** [one line — what makes a writer reach for this vs. siblings]
- **Voice-shift note:** [one line — register shift on top of the house voice]
- **Structure anatomy (decisions):**
  1. [Section] — [purpose] — [length / word-count band]
  2. [Section] — [purpose] — [length band]
  3. …
- **CTA pattern:** [placement / form (question|imperative) / destination / policy]
- **Writing checks:** [testable bullets — tells to enforce or avoid]
- **Specimen excerpt:** [the real artifact excerpt to pass inline; `—` if shape is inferred]

## Cross-Asset Conventions
[Standards that hold across all assets — naming, UTM/tracking discipline, shared CTA destinations, brand-voice anchors pulled from the profile pillar. Feeds the designers as shared context.]

## Plan Integrity Check
[pass/flag per check — see below]
```

### Plan integrity check

Before presenting, audit the plan and resolve flags — rigor moves upfront so the parallel writers don't re-litigate it:

- **Every primary variant is shape-grounded** — each `primary` variant's anatomy comes from a specimen (`grounded`) or an interview (`interviewed`), not inference. Any `primary` variant marked `shape: inferred` is the core failure mode this skill exists to prevent — flag it.
- **Every asset traces to a motion** — each asset serves ≥1 declared motion. An asset with no motion behind it is speculative; cut it or confirm with the user.
- **Variants are distinct** — each variant of an asset has a non-overlapping when-to-use trigger *and* a distinguishable structure anatomy. Two variants a writer couldn't tell apart should be one variant.
- **Default set** — every multi-variant asset names exactly one `default-variant`; atomic assets set it to `—`.
- **Production-targets trace to channels** — no `print` target if the company never prints; no asset targeting a channel they didn't declare.
- **Schema present** — every envelope has a `content-keys` list (and `array-keys` for any list-valued field).
- **No duplication** — no asset duplicates an existing `messaging/assets/` slug; if it overlaps, merge into the existing one instead of creating a parallel.

Resolve flags via AskUserQuestion (bundle them; Option A current / Option B sharper / Option C custom).

**Thin-input guard.** The dominant gap is an **inferred primary variant** — a high-use variant whose shape was guessed, not grounded. For each, push to AskUserQuestion: offer to (a) take a pasted/staged specimen now, or (b) run the `design-asset` Phase C shape-interview, or (c) explicitly accept the inferred shape. Resolve it in the plan, not in the writers — parallel designers inventing structure in isolation is exactly what produces generic files. (Long-tail inferred variants are acceptable; just surface them.)

### Approval gate

Present a readable summary — the asset count, and **per asset, its variants with their `shape:` grounding** (grounded / interviewed / inferred) so fidelity is visible at a glance — plus any remaining flags, then the gate:

> "Here's the asset plan — the catalog I'll generate from. Approve to start generation, or tell me what to change."

User approves, edits, or cancels. **If the user edits the plan, re-run the integrity check** — an edit can reintroduce overlapping variants or an orphaned asset. On approval, set `status: approved` and proceed to Phase 3.

---

## Phase 3: Generate

Generation transcribes the approved plan into `messaging/assets/`. No user questions, no web research, no new strategy — the plan is locked. The main agent slices the plan and dispatches `designer` subagents (`.claude/agents/designer.md`) in two parallel waves, then reconciles.

### Pre-wave setup

1. **Load the voice gate once.** Read `.claude/skills/craft/voice/SKILL.md`; pass its content inline as `voice_gate` in every dispatch.
2. **Seed the progress manifest** — see Progress markers below; mark every target `pending`.

### Wave 1 — envelopes (parallel)

Dispatch one `designer` per asset type in a single message. Build each envelope's `plan_slice` from its Asset Catalog mini-brief (envelope schema + conventions decisions; for atomic assets, also the structure/CTA/checks). No envelope reads another — the Cross-Asset Conventions block is the shared contract.

```
Agent(
  subagent_type: "designer",
  prompt: "Apply the protocol in .claude/agents/designer.md.

  target_type: asset
  target_path: messaging/assets/[slug]/asset.md
  template_path: templates/assets/[type]-template/asset.md   # closest-fit (e.g. blog-post-template) if no exact match

  plan_slice (resolved envelope decisions + cross-asset conventions, verbatim; content-keys/conventions
  are specimen-derived. For an ATOMIC asset, also include the full structure anatomy + CTA pattern + checks):
  [paste the asset's envelope decisions + the Cross-Asset Conventions block; for atomic assets, the anatomy block]

  example_inline (atomic assets only — the specimen excerpt; omit for variant-bearing envelopes and inferred shapes):
  [paste the specimen excerpt]

  voice_gate (inline):
  [paste full voice gate content]

  Write the single envelope file to target_path. Populate frontmatter from the slice (slug, status, content-keys, array-keys, publishing, default-variant, production-targets). Author Conventions + Frontmatter requirements (and, for atomic assets, transcribe the Structure / CTA conventions / Writing checks from the anatomy, matching example_inline). LEAVE the ## Variants table for orchestrator reconciliation. Strip instruction scaffolding, run the voice gate. Return the path and a one-line status (complete | needs-revision)."
)
```

### Wave 2 — variants (parallel)

After Wave 1 returns, dispatch one `designer` per variant from the plan, in a single message (the harness queues if the count exceeds the concurrency cap). Order default and primary variants first so an interrupt leaves the most-used files done. Each variant gets its `parent_asset_path` for read-only grounding and — when its shape is `grounded` — its specimen excerpt inline as `example_inline` (the builders' `variant_inline` pattern: read the artifact once, pass it inline so the designer matches a real shape, not a generic one). Skip variants for atomic assets.

```
Agent(
  subagent_type: "designer",
  prompt: "Apply the protocol in .claude/agents/designer.md.

  target_type: variant
  target_path: messaging/assets/[slug]/variants/[name].md
  template_path: templates/assets/[type]-template/variants/variant-template.md   # blog-post-template/variants fallback

  plan_slice (this variant's block — when-to-use trigger, voice-shift note, FULL structure anatomy
  (ordered sections w/ purpose + length band), CTA pattern, writing checks):
  [paste the variant block + the asset's relevant conventions]

  example_inline (the real specimen excerpt — the format-fidelity reference; omit if shape is inferred):
  [paste the specimen excerpt]

  voice_gate (inline):
  [paste full voice gate content]

  parent_asset_path: messaging/assets/[slug]/asset.md   # read-only grounding for shared conventions + content-keys

  Write the single variant file to target_path. Transcribe the structure anatomy into `## Structure`; match section
  order, length bands, and the CTA pattern to example_inline; render only the prose in the company's voice — do not
  generalize the shape. Strip instruction scaffolding, run the voice gate. Return the path and a one-line status
  (complete | needs-revision)."
)
```

**Partial failure.** A designer returning `needs-revision` or erroring does not block its wave. Mark the target non-complete, let the wave finish, and re-dispatch failed targets before reconciliation.

### Reconciliation

After Wave 2, the main agent — which holds the plan — reconciles the two tables that must stay in sync with the files on disk. This removes parallel-drift by construction; don't rely on independent designers having matched.

1. **Each envelope's `## Variants` table** — write one row per variant file actually written: variant, file, ✓ for the `default-variant`, and a description matching the variant's when-to-use trigger.
2. **MESSAGE.md `## Assets` table** — write/overwrite one row per asset: `content-type → asset slug → default-variant → available-variants`, so it matches `messaging/assets/` exactly. Append to existing rows when extending a populated catalog; never duplicate a content-type row.

Confirm generation with one line per file written, grouped by wave.

### Progress markers

Track generation as a per-target wave manifest in `messaging/.tune-progress.md`, not a phase log. Seed every target `pending`, flip to `dispatched` when its `Agent` call is issued, and to `complete` when its payload returns:

```
phase: generate
wave_1_envelopes:
  email: complete
  landing-page: dispatched
  one-pager: pending
wave_2_variants:
  email/outbound: pending
  email/nurture: pending
  landing-page/campaign-destination: pending
reconcile: pending
```

On resume, re-dispatch any target not `complete`. Designer writes are idempotent (it overwrites its target from the plan), so re-running a half-written file is safe. The plan (`messaging/.tune-plan.md`) is the durable contract; resume needs only the plan plus this manifest.

---

## Completion

### Consistency check

Read every asset and variant written. Check:

- **Voice fidelity** — each variant's `## Voice notes` trace to the profile pillar's voice attributes; the catalog reads as one company (the parallel-drift backstop)
- **No orphan variants** — every variant has a parent envelope, and every multi-variant envelope's `## Variants` table matches its `variants/` directory
- **Catalog sync** — every `messaging/assets/` slug has a MESSAGE.md `## Assets` row, and every row resolves to a file
- **Distinct variants** — no two variants of an asset have overlapping when-to-use
- **Schema** — every envelope's `content-keys` is populated; `array-keys` ⊆ `content-keys`

Present a single summary:

```
Asset Catalog:
  ✓ [N] asset types, [N] variants configured
  ✓ MESSAGE.md ## Assets synced to messaging/assets/
  ⚠ [specific issue if any]

Recommended next steps:
  - Run /run health to validate the asset layer
  - Test with /build campaign "test topic" to exercise an asset end-to-end
  - Add a one-off asset anytime with /design asset [slug]
```

### Cleanup

Delete `messaging/.tune-plan.md` and `messaging/.tune-progress.md`. They were working documents — the generation contract and the resume manifest; the asset catalog is the deliverable.

### Journal entry

Append an entry to `output/journal.md`:

- **Source:** Tune — asset layer build
- **Type:** process
- **Learning:** Which motions drove the catalog, where examples were thin, variants that could go either way — the approved asset plan was the generation contract
- **Action:** Logged — asset catalog populated

---

## Reference

### Tune vs. /design asset

Tune is the **bulk, motion-driven** setup — it resolves the whole catalog coherently and reconciles the `## Assets` table once. `/design asset [slug]` is the **surgical follow-up** — add, update, or remove one asset or variant at a time. After tune, point one-off changes at `/design asset`.

### Tool scoping

- **Read** — `MESSAGE.md`, `messaging/`, `templates/assets/`, `input/` (incl. user-supplied specimens), `.claude/skills/builders/build-*/` (motion → asset mapping), `.claude/skills/messaging/design-asset/SKILL.md` (Phase C question set for the shape-interview fallback)
- **Write, Edit** — `messaging/assets/` (via designer dispatch, user-approved), MESSAGE.md `## Assets` table + envelope `## Variants` tables (reconciliation, user-approved), `messaging/.tune-plan.md` + `messaging/.tune-progress.md` (working docs)
- **Agent(designer)** — dispatched in Phase 3 to author envelopes and variants in parallel from the approved plan, with the specimen passed inline
- **Glob, Grep** — input materials, existing asset/messaging content
- **AskUserQuestion** — the motion interview, specimen solicitation + shape-gap resolution (Tier B), plan integrity flags, the approval gate
- No web access — the catalog and shapes come from the house, the specimens (staged or pasted), and the interview; tune can't fetch a URL.
