---
name: bootstrap
description: Build a complete messaging system through a consultative workshop session. Use on first repo use, or when the user says they want to set up their messaging house. Adapts depth based on input materials provided.
---

# Bootstrap Skill

Build a complete messaging system through a consultative workshop session. The result is a fully populated messaging house — six pillars, their collections, optional asset definitions — synthesized into a `MESSAGE.md` always-on foundation.

Treat this task as a strategist running a workshop, not a scribe filling in fields. Find the sharpest, most defensible position this company can own. If a claim could appear on a competitor's website, it doesn't belong here. Every synthesis should be identifiable as belonging to this company and no other.

The skill is consultative in three dimensions: it asks the right questions (not all questions), infers what can be inferred, and researches what needs researching. Each dimension reduces user burden while improving output quality.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, ICP, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

Note: this skill *creates* the messaging system when it doesn't exist yet. The blurb above describes runtime behavior; bootstrap itself is the genesis flow.

---

## What bootstrap produces

A complete messaging house: six pillars, their collection profiles, optional customized asset definitions, and a synthesized MESSAGE.md as the always-on foundation. Pillars and collections write first in dependency order; MESSAGE.md generates next as the distilled altitude-setter; optional assets follow last.

---

## Three phases

Bootstrap runs three phases:

1. **Discover** — read input materials, run the workshop, surgical web research for gaps
2. **Sharpen** — present strategic synthesis, surface tensions, resolve through user confirmations
3. **Generate** — write pillars and collections in dependency order, then MESSAGE.md as synthesis, then optional assets

The phases are sequential and gated. Phase 2 cannot start until Phase 1 produces complete discovery notes. Phase 3 cannot start until Phase 2 closes all open tensions.

---

## Setup

### Step 1: Check for prior session

Check for `messaging/.bootstrap-progress.md`. If it exists, offer to resume:

> "A previous bootstrap session exists. Resume from [last completed phase], or start fresh?"

If resuming, read previously written discovery notes and any committed messaging docs. If starting fresh, proceed.

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

Run the strategic workshop. Nine essential questions in four batches; agent skips covered questions per the coverage assessment. Produces `messaging/.bootstrap-discovery.md` as the private working document for Phase 2 and Phase 3.

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

9. **Asset types**: "What asset types does your team produce regularly?"

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

## Asset types
[Synthesis of Question 9]

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

This is the working document for Phase 2 (sharpening) and Phase 3 (generation). It gets deleted at completion.

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

After all tensions are resolved and inferences are confirmed, update `messaging/.bootstrap-discovery.md` with final answers. The discovery notes are now the source of truth for generation.

> "I have a clear picture. I'll generate your messaging house now — pillars and collections first, then MESSAGE.md as the always-on synthesis, then optional assets. About 5-10 minutes; I'll narrate as I go."

Then proceed to Phase 3.

---

## Phase 3: Generate

Write pillars and collections in dependency order. MESSAGE.md generates as the synthesis once the six pillars are written; optional assets follow last because `/design asset` updates MESSAGE.md's `## Assets` table row on every invocation. No user questions during generation. No web research during generation. The strategy is locked.

### Dependency order

1. **Profile** — voice attributes, boilerplate, brand pillars (anchors everything below)
2. **Position** — category, positioning statement, competitors collection, categories collection
3. **Pitch** — strategic narrative, UVPs, differentiators (references Position)
4. **People** — personas collection, segments collection, cross-functional dynamics (references audience discovery)
5. **Portfolio** — products collection, solutions collection (references offering + People)
6. **Proof** — stories collection, reports collection (references everything above)
7. **MESSAGE.md** — synthesized from the six pillars + identity facts as the always-on altitude-setter; Assets table written empty
8. **Assets** (optional) — asset definitions with variants; depends on Phase 1 Question 9 and runs *after* MESSAGE.md so `/design asset` can populate the `## Assets` row per asset

### Writing protocol per pillar

For each pillar:

1. Read the template from `templates/pillars/[pillar]-template.md` for section structure
2. Read relevant sections of discovery notes
3. Read previously-written pillars if referencing them (e.g., Pitch reads Position)
4. Write `messaging/pillars/[pillar].md` with company-specific content
5. Strip the bootstrap disclaimer block (`> **Not yet populated.**` blockquote) when populating
6. For each collection profile the pillar references, write `messaging/collections/[type]/[slug].md` from `templates/collections/[type]-template.md`
7. Sync the pillar's `## Collection Tables` H2 to reference each collection file
8. Confirm with one line per file written: `Created messaging/pillars/profile.md` etc.

No previews. No code blocks shown to user. The user approved the strategy in Phase 2; the agent writes.

After each pillar, bridge to the next: what this pillar established and how the next one builds on it.

### MESSAGE.md generation

After all six pillars and their collections are written, generate MESSAGE.md as the synthesis. Read the template from `templates/MESSAGE-template.md` and populate each section from existing content:

- **Attributes** — derived from Profile (voice attributes) + Position (market position) + identity facts
- **Facts** — from identity capture
- **ICP** — distilled from People (personas) to altitude-setting summary
- **Glossary** — extracted from all pillars (cross-cutting terms; product/competitor/persona names excluded by discipline)
- **Brand Guardrails** — derived from Profile voice attributes (extracted as testable rules)
- **Scenarios — Dimensions** — Compelling event and Market moment values calibrated from Position and Pitch context; other three dimensions are spec-fixed
- **Pillars table** — agent-authored from a filesystem walk of `messaging/pillars/`
- **Collections table** — agent-authored from a filesystem walk of `messaging/collections/`
- **Assets table** — written empty at this point; if the user opts in to the assets step (next), `/design asset` populates the rows during its normal interview flow

There is no script automating these tables — the agent reads each directory and authors the rows during generation.

Present MESSAGE.md to the user once written:

> "MESSAGE.md is generated. This is your always-on foundation — every workflow loads it first to set altitude. Want to review now or trust the synthesis?"

User can request adjustments to specific sections; otherwise proceed to assets (or completion if assets were declined).

### Assets phase (optional)

If the user listed asset types in Question 9, run the asset interview per asset *after* MESSAGE.md has been written. Delegate to `/design asset [slug]` — a two-phase interview (identity + envelope) plus optional third phase for the default variant when the asset has meaningful editorial variation. Cap at ~12 questions per asset. See `.claude/skills/workflows/design-asset/SKILL.md` for the canonical flow.

Each asset produces atomically:

1. `messaging/assets/[slug]/asset.md` (envelope)
2. `messaging/assets/[slug]/variants/[variant].md` (optional default variant)
3. MESSAGE.md `## Assets` table row — added by `/design asset` exactly as it does in normal post-bootstrap operation (no special bootstrap-only path)

Skip the assets step entirely if the user defers. `/design asset [slug]` is available anytime.

### Progress markers

After each pillar generation, update `messaging/.bootstrap-progress.md` with completed pillars, collection counts, and next step. Used for resume if session interrupts.

---

## Completion

After all phases:

### Consistency check

Read every file written during the session. Check:

- **MESSAGE.md ↔ pillars** — voice attributes in Profile align with MESSAGE.md Attributes; People aligns with MESSAGE.md ICP; no content duplicates across MESSAGE.md and pillars
- **Collection Tables sync** — every collection file has a row in its parent pillar's `## Collection Tables`, and every row has a matching file
- **Glossary discipline** — no product, competitor, customer, persona-title, or category names in MESSAGE.md Glossary
- **Cross-references** — products, personas, segments named in one doc exist as collection files
- **Contradictions** — claims in one doc that conflict with another
- **Gaps** — pillars that are thin or rely heavily on placeholders

Present a single summary:

```
Consistency Check:
  ✓ MESSAGE.md populated (10 sections); pillars and collections aligned
  ✓ [N] pillars, [N] collection profiles, [N] assets configured
  ✓ Collection Tables synced
  ⚠ [specific issue if any]

Recommended next steps:
  - Run /run health to validate the structure
  - (Optional) To enable HTML production: copy templates/DESIGN-template.md → brand/DESIGN.md, customize tokens, drop logo + font files into brand/logos/ and brand/fonts/. See docs/brand-system.md.
  - Test with /build campaign "test topic" to verify end-to-end
```

### Cleanup

Delete `messaging/.bootstrap-progress.md` and `messaging/.bootstrap-discovery.md`. They were working documents; the messaging house is the deliverable.

### Initial journal entry

Append the first entry to `output/journal.md`:

- **Source:** Bootstrap — initial build
- **Type:** process
- **Learning:** Assumptions made, conflicts surfaced, areas where information was thin, strategic choices that could go either way
- **Action:** Logged — initial messaging house populated

### Skipped assets message

If the user skipped the assets step, close with:

> "You skipped assets. You can add them anytime with `/design asset [slug]`."

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
| Phase 3 generation | Zero — strategy is locked |

If a session approaches budget, surface it: "I've done significant research; let me synthesize what we have."

### Tool scoping

- Read, Write, Edit: full access for messaging house files
- Glob, Grep: input materials, existing messaging house content
- AskUserQuestion: the 9 essential questions, sharpening exchanges, asset interview
- WebSearch: enabled with discipline (per budget; never during Phase 3)
- WebFetch: enabled for user-provided URLs and search result extraction (never during Phase 3)

### Writing conventions

- Write in the company's voice when you have enough signal; default to clear, direct prose when you don't
- Never default to marketing filler
- Sync the parent pillar's `## Collection Tables` after each phase
- Descriptions in Collection Tables are routing signals (~15 words, differentiating)
- Collection file frontmatter `description` matches its Collection Tables row exactly
- Messaging Blocks carry source material an agent draws from
- Collection Tables route to collection files
- Writing Guidelines: 3-5 bullets max per doc; interpretation rules only
- Messaging Rules: 3-5 bullets max per doc; company-specific constraints not derivable from content
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
