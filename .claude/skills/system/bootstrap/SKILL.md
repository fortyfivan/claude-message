---
name: bootstrap
description: Build a complete messaging system through a consultative workshop session. Use on first repo use, or when the user says they want to set up their messaging house. Adapts depth based on input materials provided.
---

# Bootstrap Skill

Build a complete messaging system through a consultative workshop session. The result is a fully populated messaging house — six pillars and their collections — synthesized into a `MESSAGE.md` always-on foundation. The asset layer (asset envelopes + variants) is defined separately by `/tune` once the house is built.

Treat this task as a strategist running a workshop, not a scribe filling in fields. Find the sharpest, most defensible position this company can own. If a claim could appear on a competitor's website, it doesn't belong here. Every synthesis should be identifiable as belonging to this company and no other.

The skill is consultative in three dimensions: it asks the right questions (not all questions), infers what can be inferred, and researches what needs researching. Each dimension reduces user burden while improving output quality.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

Note: this skill *creates* the messaging system when it doesn't exist yet. The blurb above describes runtime behavior; bootstrap itself is the genesis flow.

---

## What bootstrap produces

A complete messaging house: six pillars, their collection profiles, and a synthesized MESSAGE.md as the always-on foundation. The discovery and sharpening converge on an approved **messaging plan** — the resolved blueprint for every pillar and collection. Generation then fans out from that plan: pillars and collections write in parallel waves, then MESSAGE.md generates as the distilled altitude-setter. The asset catalog is built afterward by `/tune`, which defines asset envelopes and variants from the company's go-to-market motions.

---

## Four phases

Bootstrap runs four phases:

1. **Discover** — read input materials, run the workshop, surgical web research for gaps
2. **Sharpen** — present strategic synthesis, surface tensions, resolve through user confirmations
3. **Plan** — compose the messaging plan (resolved per-pillar decisions + a collection manifest + cross-cutting blocks), run an integrity check, get explicit approval
4. **Generate** — fan out parallel `designer` subagents (pillars, then collections) from the approved plan, reconcile Collection Tables, synthesize MESSAGE.md, then hand off the asset layer to `/tune`

The phases are sequential and gated. Phase 2 cannot start until Phase 1 produces complete discovery notes. Phase 3 cannot start until Phase 2 closes all open tensions. Phase 4 cannot start until the plan is approved.

The plan is the consistency contract. Because one agent resolves the whole strategic picture in the plan — every claim, differentiator, and cross-reference — the parallel writers in Phase 4 transcribe their slice rather than re-deriving coherence from each other. Coherence is resolved once, upfront, instead of reconstructed five times during sequential writing.

---

## Setup

### Step 1: Check for prior session

Check for `messaging/.bootstrap-progress.md`. If it exists, offer to resume:

> "A previous bootstrap session exists. Resume from [last completed phase], or start fresh?"

If resuming, read the discovery notes, the plan (`messaging/.bootstrap-plan.md`) if it exists, the progress manifest, and any committed messaging docs. If a plan exists and generation was interrupted, resume from Phase 4 and re-dispatch any target not marked `complete` (see Progress markers). If starting fresh, proceed.

### Step 2: Read input materials

Scan all `input/` subdirectories in priority order. Do not ask whether materials exist — read what's there and report.

**Priority order:**
1. `input/messaging/` — brand guides, positioning decks, messaging frameworks (highest weight; treat as authoritative)
2. `input/docs/` — PRDs, release notes, specs, pricing
3. `input/research/` — market research, analyst reports, competitive intel
4. `input/transcripts/` — sales calls, customer interviews, feedback
5. `input/examples/` — content references, competitor samples (lowest weight)
6. `input/` root — backward compat

For any external URLs referenced in input materials, web_fetch them opportunistically to deepen the foundation before the workshop.

### Step 3: Coverage assessment and mode selection

Map input coverage against the nine essential strategic questions (see Phase 1). Produce a coverage assessment:

```
Coverage assessment:
✓ Offering — clear from product overview deck
✓ Unique value — positioning deck Q4 page strong
✓ Competitive frame — analyst report has competitor matrix
~ POV — implicit in positioning deck; needs explicit articulation
✗ Audience — no buyer profile in inputs
~ Customer journey — case studies show outcomes; journey detail thin
✓ Proof — 12 case studies, 3 analyst reports
✗ Voice — no brand guide
✓ Asset types — content audit lists types
```

Coverage determines mode:

| Mode | Inputs | Workshop questions | Web research budget |
|---|---|---|---|
| Rich | Most areas covered (≥7 of 9 ✓) | 2-4 (gaps + sharpening) | 2-3 searches |
| Standard | Mixed coverage (4-6 of 9 ✓) | 5-7 questions | 5-10 searches |
| Empty | Sparse or no coverage (<4 of 9 ✓) | All 9 questions | 10-15 searches |

Tell the user which mode and what questions remain. Example for Rich mode:

> "I have strong material on most areas. I need to ask about audience (no buyer profile in inputs) and voice (no brand guide), plus sharpen your POV. About 3 questions plus pressure-testing. Ready?"

Then proceed to Phase 1.

### Identity check

If basic identity isn't in input materials, ask once before Phase 1:

> "Quick basics — company name, website URL, year founded, rough employee count, where you're based, funding stage if applicable?"

This populates the eventual MESSAGE.md Facts section and gives the workshop opening context.

---

## Phase 1: Discover

Run the strategic workshop. Nine essential questions in four batches; agent skips covered questions per the coverage assessment. Produces `messaging/.bootstrap-discovery.md` as the private working document for the sharpening and planning phases.

### The nine essential questions

Each feeds multiple pillars; none redundant.

**Batch 1: Offering and market** (4 questions, ~12 min)

1. **Offering**: "What do you sell? Walk me through the portfolio quickly."
2. **Unique value**: "What does your company do that no one else can do as well?"
3. **POV**: "What do you believe about your market that most people don't?"
4. **Competitive frame**: "Who are your main competitors, and how do they frame the space differently than you?"

**Batch 2: Audience and customer** (2 questions, ~8 min)

5. **Audience**: "Who actually buys this? Walk me through champion vs. economic buyer, and how deals typically come together."
6. **Customer journey**: "What does success look like for a customer 90 days in? A year in?"

**Batch 3: Evidence and voice** (2 questions, ~6 min)

7. **Proof**: "What customer stories, analyst reports, or market data do you reference most often?"
8. **Voice**: "How do you want to sound? What words ARE you, what words AREN'T you?"

**Batch 4: Operations** (1 question, ~2 min)

9. **Asset types**: "What asset types does your team produce regularly?" — a light seed only; bootstrap doesn't build assets. Capture the answer to pass to `/tune`, which defines the asset catalog after the house is built.

Each batch goes through one AskUserQuestion call with the batch's questions presented together. Don't interrupt between questions in a batch; let the user answer the set.

### Adaptive questioning

For questions marked ✓ in coverage assessment, skip the full question and present the extracted answer for confirmation:

> "Your positioning deck says your unique value is [extracted]. Is that still current, or do you want to refine?"

For questions marked ~ (partial coverage), ask a sharpening question rather than the full open question:

> "Your deck implies a POV about [topic]. Can you state it as a single sentence — 'we believe X, others believe Y'?"

For questions marked ✗, ask the full question.

### Surgical web research

Use web_search and web_fetch during the workshop to compensate for thin inputs or extend user answers. Discipline:

- Maximum 5-15 searches per session (per mode budget); budget burns down across all phases
- Search only for: competitive positioning details, analyst coverage, category research, persona patterns, customer story extraction from URLs
- Every search anchored to the company name, a competitor name, or a specific product
- Fetch only when: user provides a URL, or a search result needs extraction
- Stop when you have enough to synthesize; don't search to confirm what you know

After a competitor or proof URL is mentioned, the agent may search once to deepen its understanding. Surface findings during sharpening: "I looked at Competitor X's positioning — they're emphasizing [Y]. Your differentiation of [Z] holds; want to add anything?"

### Inferring beyond the nine

Beyond the nine questions, infer everything else from the answers plus input materials. Do not ask the user to author:

- Mission and vision (synthesize from POV + customer outcome + offering)
- Boilerplate (synthesize from identity + offering + position)
- Brand pillars (extract from voice + POV + unique value)
- Category name (derive from competitive frame + position)
- Specific use cases / solutions (derive from offering + audience pain points)
- Persona altitude / lead-with / proof / CTA conventions (derive from audience + customer journey + voice)
- Scenarios dimensions (compelling event values, market moment values) (derive from position + pitch context)
- Glossary entries (extract cross-cutting terms from all answers + inputs)
- Brand guardrails as testable rules (extract from voice answer + experience patterns)

Inferences get presented in Phase 2 for confirmation. The user doesn't author; they refine and approve.

### Discovery notes output

After the workshop completes, write `messaging/.bootstrap-discovery.md`:

```markdown
# Discovery Notes — [Company]

## Identity
[Name, founded, HQ, size, funding, customers]

## Offering
[Synthesis of Question 1]

## Unique value
[Synthesis of Question 2]

## POV / Market argument
[Synthesis of Question 3 + Question 4 competitive frame]

## Competitive landscape
[Synthesis of Question 4 + web research findings]

## Audience
[Synthesis of Question 5: personas, buying motion, champion/economic dynamics]

## Customer journey
[Synthesis of Question 6: 90-day, year-one outcomes]

## Evidence inventory
[Synthesis of Question 7 + URLs fetched]

## Voice and brand
[Synthesis of Question 8 + extracted guardrails]

## Asset types (seed for /tune)
[Synthesis of Question 9 — not acted on in bootstrap; handed to /tune]

## Inferences (to confirm in Phase 2)
- Mission: [synthesized]
- Boilerplate: [synthesized]
- Brand pillars: [3-4 extracted themes]
- Category name: [derived]
- [Other inferences]

## Open tensions
- [Specific tension to resolve in Phase 2]
- [...]

## Gaps
- [What we still don't know that may need user input or research]
```

This is the working document for Phase 2 (sharpening) and Phase 3 (planning) — the plan is composed from it. It gets deleted at completion.

---

## Phase 2: Sharpen

Walk the strategic argument back to the user. Surface tensions. Present inferences for confirmation. Resolve generic claims by offering sharper alternatives.

### The sharpening conversation

Open by summarizing what was heard:

> "Here's what I'm hearing: [3-4 sentence synthesis of the strategic argument]. Three things I want to pressure-test before we write."

Then walk through tensions and inferences. Group related items into single AskUserQuestion calls to minimize back-and-forth.

### Trope filter

Before presenting any synthesis, scan for AI tells and rewrite if found:

- Setup-payoff cliches: "the brutal truth," "here's the thing," "the result?"
- Inverted definitions: "it's not X, it's Y," "X isn't about Y, it's about Z"
- Importance-signaling adjectives: "load-bearing," "table-stakes," "non-negotiable"
- Empty intensifiers: "fundamentally," "ultimately," "at its core"
- Rhetorical hand-waves: "and that's the point," "and that changes everything"

If the synthesis reads like a LinkedIn post, rewrite it to read like a strategist's memo.

### Challenges as choices

For each weak or generic claim, present as a decision via AskUserQuestion:

- **Option A:** Current framing — "[original]"
- **Option B:** Sharper alternative — "[proposed]" *(Recommended — [reason])*
- **Option C:** Custom input

Bundle multiple challenges into single AskUserQuestion calls. Resolve all challenges before proceeding to Phase 3.

### Light web research

If sharpening requires evidence (a claim feels strong but unsupported, a competitor description feels stale), one to three additional searches are acceptable. Stay within the session's total budget.

### Inference confirmation

Present each inference as a confirmation, not an authoring task:

> "Based on what you said, I drafted these:
>
> **Mission:** [synthesized]
> **Boilerplate:** [synthesized]
> **Brand pillars:** [3-4 themes]
>
> Want me to use these as drafted, or refine?"

User confirms, refines, or replaces. Either way, the burden is on the agent to draft first.

### Closing Phase 2

After all tensions are resolved and inferences are confirmed, update `messaging/.bootstrap-discovery.md` with final answers. The discovery notes are now complete enough to compose the plan.

> "I have a clear picture. I'll compose the messaging plan now — the resolved blueprint we'll generate from. You'll review it before I write any files."

Then proceed to Phase 3.

---

## Phase 3: Plan

Compose the messaging plan — the resolved blueprint every pillar and collection generates from. One agent holding the whole strategic picture resolves coherence here, once, so the parallel writers in Phase 4 transcribe their slice instead of re-deriving consistency from each other.

Write the plan to `messaging/.bootstrap-plan.md`. No web research during planning — the budget is spent; the strategy is what Phase 2 confirmed.

### Plan fidelity: decisions, not prose

The plan carries the **irreducible decisions and raw material** a writer cannot derive — not pre-rendered pillar copy. If a section reads like finished pillar copy, it's too detailed and you've moved the serial authoring upstream (no time saved). If it reads like a strategist's spec, it's right.

| In the plan (resolved decisions + material) | NOT in the plan (the designer renders these in voice) |
|---|---|
| Positioning statement components filled (For / Who / We are / Unlike / Only us …) | The narrative arc's prose; the boilerplate paragraph |
| UVP statements with brand-pillar / differentiator / proof / portfolio pointers | Differentiator write-ups expanded into paragraphs |
| Differentiators with evidence tags (→ which UVP / story / report) | Per-persona objection reframes phrased in voice |
| Per-persona load-bearing spec: altitude, lead-with, avoid-leading-with, proof types, CTA, format affinity | Journey-stage prose; relationship-to-product narrative |
| Collection routing descriptions (~15 words) + cross-tags (story → personas/products/segments) | Section connective tissue and examples |
| Glossary term list, testable guardrails, attributes/facts, scenario dimension values | — |

Target ~350–550 lines for a Standard-mode house.

### Plan structure

`messaging/.bootstrap-plan.md`:

```markdown
---
company: [name]
mode: [rich | standard | empty]
status: draft        # → approved
facts: [founded, HQ, employees, funding, customers]
scenario_seed: [the 5 scenario dimensions — compelling-event, topic-maturity, market-moment, strategic-shape, content-lens]
---

# Messaging Plan — [Company]

## Strategic Spine
[The verbatim through-line every designer anchors to, ~15 lines: category, the core argument,
the one-sentence "why us," the POV, the proof posture, the voice in two adjectives. Frozen text —
writers transcribe it, they don't paraphrase it.]

## Pillar Plans
### Profile
[Resolved decisions: mission, vision, boilerplate inputs, voice attributes, brand pillars (themes UVPs map to)]
### Position
[Positioning statement components, market landscape points, trends w/ direction]
### Pitch
[Strategic narrative beats (as bullets), elevator pitch inputs, UVPs w/ pointers (brand pillar / differentiators / proof / portfolio), differentiators w/ evidence tags]
### People
[ICP decisions, buying considerations, journey stages, persona list pointer]
### Portfolio
[Portfolio overview/structure, product list pointer, solution list pointer]
### Proof
[Value-evidence metrics w/ proven|projected basis, community-evidence patterns, story + report list pointers]

## Collection Manifest
One mini-brief per collection. Each is enough to author the full file.

| Type | Slug | Parent pillar | Routing description (~15 words) | Load-bearing spec / cross-tags |
|---|---|---|---|---|
| persona | ciso | people | [differentiating one-liner] | altitude / lead-with / avoid / proof / CTA / format |
| competitor | acme | position | [their positioning approach] | tier; how-we-win → differentiator refs |
| story | acme-corp | proof | [outcome one-liner] | personas:[…] products:[…] segments:[…] |
| … | | | | |

## Cross-Cutting (feeds MESSAGE.md)
- **Glossary:** [cross-cutting terms — no product/competitor/persona/category names]
- **Brand Guardrails:** [4–8 testable rules]
- **Attributes:** [stage, type, market, position, business model]
- **Scenarios — Dimensions:** [compelling-event + market-moment values; other three spec-fixed]

## Plan Integrity Check
[pass/flag per check — see below]
```

### Plan integrity check

Before presenting, audit the composed plan and resolve flags — this is where rigor moves upfront:

- **Claims trace to proof** — every quantitative claim maps to a metric in the evidence inventory or a story/report in the manifest. Flag unsupported claims.
- **Differentiators trace to UVPs** — every differentiator references a UVP or a proof point. A differentiator without backing is an aspiration; cut or downgrade it.
- **Personas have behavioral specificity** — each persona's spec is more than a job title (signals, challenges, success metrics). Flag generic personas.
- **No cross-pillar contradictions** — positioning, pitch, and proof tell one story. Flag conflicts.
- **Routing descriptions present** — every manifest entry has a ~15-word description.

Resolve flags via AskUserQuestion (bundle them), using the Phase 2 challenge format (Option A current / Option B sharper-recommended / Option C custom).

**Empty / thin-input guard.** In Empty mode, flag every plan block backed *only* by inference (no input or research behind it) and force those through AskUserQuestion before approval. Resolve placeholder debt in the plan, not in the writers — six designers inventing in isolation is worse than one agent inventing where you'd notice the drift.

### Approval gate

Present a readable summary of the plan (spine + the pillar headlines + the collection manifest count + any remaining flags) and the approval gate:

> "Here's the messaging plan — the blueprint I'll generate from. Approve to start generation, or tell me what to change."

User approves, edits, or cancels. **If the user edits the plan (directly or in conversation), re-run the integrity check** — an edit can reintroduce a contradiction the check previously cleared. On approval, set the plan's `status: approved` and proceed to Phase 4.

---

## Phase 4: Generate

Generation transcribes the approved plan into the messaging house. No user questions, no web research, no authoring of new strategy — the plan is locked. The main agent slices the plan and dispatches `designer` subagents (`.claude/agents/designer.md`) in two parallel waves, then reconciles and synthesizes.

### Pre-wave setup

1. **Load the voice gate once.** Read `.claude/skills/craft/voice/SKILL.md`; pass its content inline as `voice_gate` in every dispatch.
2. **Extract the spine.** Take the `## Strategic Spine` block verbatim; pass as `spine` in every dispatch.
3. **Seed the progress manifest** — see Progress markers below; mark every target `pending`.

### Wave A — pillars (parallel)

Dispatch all six pillars in a single message (six `Agent` calls). No pillar reads another pillar — the spine is the shared contract. Build each pillar's `plan_slice` from its `## Pillar Plans` block; for pillars with collections, build `manifest_rows` by filtering the Collection Manifest to that parent pillar.

```
Agent(
  subagent_type: "designer",
  prompt: "Apply the protocol in .claude/agents/designer.md.

  target_type: [profile | position | pitch | people | portfolio | proof]
  target_path: messaging/pillars/[slug].md
  template_path: templates/pillars/[slug]-template.md

  plan_slice (resolved decisions + material for this pillar, verbatim):
  [paste the pillar's Pillar Plans block]

  spine (verbatim, anchor — do not paraphrase):
  [paste Strategic Spine]

  voice_gate (inline):
  [paste full voice gate content]

  manifest_rows (this pillar's Collection Tables — author rows from these; omit for Profile/Pitch):
  [paste filtered manifest rows: file + ~15-word description per collection]

  Write the single file to target_path, strip the disclaimer, run the voice gate. Return the path and a one-line status (complete | needs-revision)."
)
```

### Wave B — collections (parallel)

After Wave A returns, dispatch one `designer` per collection from the manifest, in a single message (or batched if the count exceeds the concurrency cap — the harness queues transparently). Order high-value collections first (primary personas, flagship products, hero stories) so an interrupt leaves the most important files done. Each collection gets its `parent_pillar_path` for read-only grounding.

```
Agent(
  subagent_type: "designer",
  prompt: "Apply the protocol in .claude/agents/designer.md.

  target_type: [persona | competitor | segment | category | product | solution | story | report]
  target_path: messaging/collections/[type]/[slug].md
  template_path: templates/collections/[type]-template.md

  plan_slice (this collection's manifest entry — routing description, load-bearing spec, cross-tags):
  [paste the manifest row + any pillar-plan detail relevant to this collection]

  spine (verbatim):
  [paste Strategic Spine]

  voice_gate (inline):
  [paste full voice gate content]

  parent_pillar_path: messaging/pillars/[parent].md   # read-only grounding (e.g., persona reads People's ICP)

  Write the single file to target_path, strip the disclaimer, run the voice gate. The frontmatter description must match the manifest routing description exactly. Return the path and a one-line status (complete | needs-revision)."
)
```

**Partial failure.** A designer returning `needs-revision` or erroring does not block its wave. Mark that target non-complete, let the wave finish, and re-dispatch failed targets before MESSAGE.md.

### Collection Tables reconciliation

After Wave B completes, the main agent — which holds the manifest — writes each pillar's `## Collection Tables` rows from the manifest, so the rows and the collection-file frontmatter `description` are sourced from one place and match exactly. This removes the parallel-drift hazard by construction; do not rely on two independent designers having matched.

(Profile and Pitch have no Collection Tables; skip them.)

Confirm generation with one line per file written, grouped by wave.

### MESSAGE.md generation

After both waves and reconciliation complete, the main agent — not a subagent — authors MESSAGE.md as the synthesis. It must run after the waves so the catalog tables reflect what was actually written. Read the template from `templates/MESSAGE-template.md` and populate each section:

- **Attributes** — from the plan's Cross-Cutting `Attributes` block + identity facts
- **Facts** — from the plan frontmatter / identity capture
- **Glossary** — from the plan's Cross-Cutting `Glossary` block (cross-cutting terms; product/competitor/persona names excluded by discipline)
- **Brand Guardrails** — from the plan's Cross-Cutting `Brand Guardrails` block (testable rules)
- **Scenarios — Dimensions** — Compelling event and Market moment values from the plan's Cross-Cutting `Scenarios` block; other three dimensions are spec-fixed
- **Pillars table** — agent-authored from a filesystem walk of `messaging/pillars/`
- **Collections table** — agent-authored from a filesystem walk of `messaging/collections/`
- **Assets table** — written empty (leave its `[Instructions: ]` row intact); `/tune` populates the rows when it builds the asset catalog

There is no script automating these tables — the agent reads each directory and authors the rows during generation. The cross-cutting content was resolved in the plan; the tables are derived from the written files.

Present MESSAGE.md to the user once written:

> "MESSAGE.md is generated. This is your always-on foundation — every skill loads it first to set altitude. Want to review now or trust the synthesis?"

User can request adjustments to specific sections; otherwise proceed to the assets hand-off, then completion.

### Assets — hand off to `/tune`

Bootstrap stops at the messaging house; it does not interview per-asset. The asset layer (asset envelopes + variants) is defined separately by `/tune`, which is purpose-built for it: it infers the asset catalog from the company's go-to-market motions (the campaigns, launches, plays, and events they run), calibrates altitude and format from `input/examples/`, and generates every envelope + variant in one coherent pass. Keeping it separate keeps bootstrap fast and lets each flow stay focused.

Leave the MESSAGE.md `## Assets` table empty (its `[Instructions: ]` row intact). If the user named asset types in Question 9, pass that as a seed to tune rather than acting on it here. Recommend the next step in Completion. For a single one-off asset, `/design asset [slug]` is also available anytime.

### Progress markers

Track generation as a per-target wave manifest in `messaging/.bootstrap-progress.md`, not a phase log. Seed every target `pending` before the waves, flip each to `dispatched` when its `Agent` call is issued, and to `complete` when its return payload arrives:

```
phase: generate
wave_a:
  profile: complete
  position: complete
  pitch: dispatched        # interrupted mid-wave
  people: complete
  portfolio: pending
  proof: pending
wave_b:
  personas/ciso: pending
  competitors/acme: pending
  ...
message_md: pending
```

On resume, re-dispatch any target not `complete`. Writes are idempotent — a designer overwrites its target file from the plan — so re-running a half-written file is safe. The plan (`messaging/.bootstrap-plan.md`) is the durable contract; resume needs only the plan plus this manifest. Don't track sub-file progress; the target is the atom, partial files are discarded on re-dispatch.

---

## Completion

After all phases:

### Consistency check

Read every file written during the session. Check:

- **Spine fidelity** — each pillar's core claim traces to the Strategic Spine; the six files read as one company's voice (the parallel-drift backstop — should be a near-pass since the spine was passed verbatim)
- **MESSAGE.md ↔ pillars** — voice attributes in Profile align with MESSAGE.md Attributes; the People pillar carries the ICP; no content duplicates across MESSAGE.md and pillars
- **Collection Tables sync** — every collection file has a row in its parent pillar's `## Collection Tables`, and every row has a matching file (reconciliation should guarantee this; verify)
- **Glossary discipline** — no product, competitor, customer, persona-title, or category names in MESSAGE.md Glossary
- **Cross-references** — products, personas, segments named in one doc exist as collection files
- **Contradictions** — claims in one doc that conflict with another
- **Gaps** — pillars that are thin or rely heavily on placeholders

Present a single summary:

```
Consistency Check:
  ✓ MESSAGE.md populated (10 sections); pillars and collections aligned
  ✓ [N] pillars, [N] collection profiles configured
  ✓ Collection Tables synced
  ⚠ [specific issue if any]

Recommended next steps:
  - Run /run health to validate the structure
  - Run /tune to define your asset types and variants from the campaigns, launches, plays, and events you run
  - (Optional) To enable HTML production: copy templates/DESIGN-template.md → brand/DESIGN.md, customize tokens, drop logo + font files into brand/logos/ and brand/fonts/. See docs/brand-system.md.
  - Test with /build campaign "test topic" to verify end-to-end
```

### Cleanup

Delete `messaging/.bootstrap-progress.md`, `messaging/.bootstrap-discovery.md`, and `messaging/.bootstrap-plan.md`. They were working documents — the discovery notes, the generation contract, and the resume manifest; the messaging house is the deliverable.

### Initial journal entry

Append the first entry to `output/journal.md`:

- **Source:** Bootstrap — initial build
- **Type:** process
- **Learning:** Assumptions made, conflicts surfaced, areas where information was thin, strategic choices that could go either way — the approved plan was the generation contract
- **Action:** Logged — initial messaging house populated

### Assets next step

Bootstrap doesn't build assets. Close by pointing the user to the dedicated flow:

> "Your messaging house is built. Next, run `/tune` to define your asset types and variants — it infers the catalog from the campaigns, launches, plays, and events you run. (Or add a single asset anytime with `/design asset [slug]`.)"

---

## Reference

### Handling ambiguity

**User doesn't know.** Propose a working answer based on available evidence. Flag it as provisional. Move on.

**Conflicting information.** Surface the conflict during Phase 2. Resolve before generation.

**Incomplete information.** Write what you have. Use bracketed placeholders only when truly necessary. Bracketed content is a debt the user pays later.

### Web research budget

Total session budget: 5-15 searches across all phases (per mode).

| Activity | Search use |
|---|---|
| Input material URL fetches (Step 2) | Free — not counted |
| Phase 1 workshop | Surgical — typically 0-5 |
| Phase 2 sharpening | Light — typically 0-3 |
| Phase 3 planning | Zero — strategy is locked |
| Phase 4 generation | Zero — strategy is locked |

If a session approaches budget, surface it: "I've done significant research; let me synthesize what we have."

### Tool scoping

- Read, Write, Edit: full access for messaging house files
- Glob, Grep: input materials, existing messaging house content
- AskUserQuestion: the 9 essential questions, sharpening exchanges, plan integrity flags
- Agent(designer): dispatched in Phase 4 to author pillars and collections in parallel from the approved plan
- WebSearch: enabled with discipline (per budget; never during Phase 3 or 4)
- WebFetch: enabled for user-provided URLs and search result extraction (never during Phase 3 or 4)

### Writing conventions

- Write in the company's voice when you have enough signal; default to clear, direct prose when you don't
- Never default to marketing filler
- Sync the parent pillar's `## Collection Tables` after each phase
- Descriptions in Collection Tables are routing signals (~15 words, differentiating)
- Collection file frontmatter `description` matches its Collection Tables row exactly
- Messaging Blocks carry source material an agent draws from
- Collection Tables route to collection files
- Writing Guidelines: 3-5 bullets max per doc; company-specific application rules and constraints, not generic interpretation
- Persona Messaging Guidance is load-bearing — populate altitude, lead-with, avoid-leading-with, proof types, language cues, CTA, format affinity for every persona

### When to push back

Bootstrap is consultative. The agent has standing to push back when:

- A claim is generic enough that a competitor could make it
- A POV isn't actually contrarian — it's conventional wisdom dressed up
- A unique value isn't differentiated — it's a feature most vendors offer
- A persona description is a job title without behavioral specificity
- Voice attributes are abstract ("be human") without concrete contrasts
- Brand guardrails aren't testable ("be authentic")

Push back constructively. Offer the sharper alternative. Get to a defensible position.
