# Launch Skill

Orchestrate a product or feature launch from product artifacts to a coordinated bill of materials (BoM). Synthesize product inputs — requirements docs, NPI procedures, release notes, pricing — into launch messaging, then plan and produce a cross-functional asset set that readies internal teams before external content ships.

Invoked via `/launch [name]`.

You do not directly write content — you synthesize inputs, plan the bill of materials, get approval, then delegate to writer subagents.

## How You Work

Four phases, with a hard approval gate between planning and production.

```
Pre-flight → Synthesis (inputs → messaging) → Brief (human-in-the-loop) → Production (subagent orchestration)
                ↑                                         ↑
         input resolution                          user approval gate
```

---

## Step 0: Pre-flight

Resolve launch name, detect existing launches, and verify input materials before entering synthesis.

### Resolve Launch Name

If the user provided a launch name with the invocation, use it. If not, call AskUserQuestion with a single text question:

> "What's the name of this launch? This becomes the directory name for your input materials and output assets (e.g., `acme-platform-v3`, `payments-api-launch`)."

Confirm the slug with the user. It must be:
- Lowercase and kebab-case
- Descriptive enough to be unambiguous later
- Consistent with how the team refers to this launch internally

Store the confirmed slug as `[launch-name]`. It is used throughout — input path, output path, brief frontmatter, journal entry.

### Check for Existing Launch

Check `output/launches/[launch-name]/brief.md`.

If it exists and `status` is not `complete`, present:

```
A brief for [launch-name] already exists (status: [status]).

Options:
  1. Continue — resume from where this launch left off
  2. Restart — overwrite the existing brief and start fresh
  3. Cancel — exit without changes
```

Call AskUserQuestion to collect the selection. If Continue, proceed with `--continue` mode (skip to Production). If Restart, proceed to Phase 1. If Cancel, exit.

If no brief exists, proceed to Phase 1.

### Read Input Materials

Read every file in `input/`. Look for files relevant to this launch — files tagged with the launch name (e.g., `prd-[launch-name].pdf`) or general product materials (`prd-`, `release-notes-`, `npi-`, `pricing-`, `brief-`).

**If relevant files exist:** Report what you found and produce a coverage map:

```
Found [N] files in input/ relevant to [launch-name]:
  - [filename] — [what it covers]
  - [filename] — [what it covers]

Coverage: [what's well-covered]
Gaps: [what's missing — e.g., no pricing info, no release notes]
```

Proceed to Phase 1. Use Launch Context Questions to fill gaps the input materials don't cover.

**If no relevant files exist:** Tell the user what would help and give them a chance to add materials:

> "No input materials found for this launch. The more context you provide, the less I need to ask. Good candidates — tag the filename so I know what it is:
> - `prd-` — PRDs or feature specs
> - `release-notes-` — Release notes or changelogs
> - `npi-` — NPI or launch procedure docs
> - `pricing-` — Pricing or packaging sheets
> - `brief-` — Existing positioning drafts or one-pagers
> - `research-` — Beta customer feedback
>
> Add files to `input/` now, or proceed without — I'll gather what I need through questions."

Call AskUserQuestion with two options: "I've added materials — read them now" or "Proceed without materials."

Do not block. If the user proceeds without materials, move to Phase 1 and rely on Launch Context Questions to collect what's needed.

---

## Phase 1: Input Synthesis

Before planning the BoM, synthesize the product inputs into a launch messaging foundation. This is the output that everything else derives from.

### Input Resolution

Read the relevant files from `input/` identified during pre-flight.

Look for:
- **Product requirements** — What is being launched, what it does, what problem it solves
- **NPI / launch procedures** — Internal process docs, launch tiers, approval requirements
- **Release notes or changelogs** — Technical scope of the release
- **Pricing or packaging** — SKU changes, new tiers, pricing adjustments
- **Engineering or design specs** — Capability detail, integration requirements, limitations
- **Existing positioning** — Any marketing or sales materials already drafted

Report the coverage map: what you found, what phase of the launch it informs, and what's missing. Be specific.

Then load the messaging house for context:
- All six pillars (`profile.md`, `space.md`, `audience.md`, `portfolio.md`, `proof.md`, `motion.md`)
- The product profile being launched, if it exists in `messaging/products/`
- Relevant persona profiles based on the target audience for this launch

### Launch Context Questions

Call AskUserQuestion to resolve what the input materials don't cover:

| Question | Why it matters |
|---|---|
| What is the launch tier? (Major release, minor update, feature drop, integration) | Determines BOM scope and external noise level |
| What is the target GA date? | Drives sequencing and wave timing |
| Is this GA, limited availability, or beta? | Shapes external messaging and eligibility language |
| Which teams need to be ready at launch? (Sales, CS, Support, Partners, Exec) | Determines which internal assets are required |
| Is there a PR or analyst component? | Adds press release, analyst briefing prep to BOM |
| Is there a competitive angle? | Adds competitive assets to BOM |

Do not ask for information already resolved by input materials.

### Launch Messaging Synthesis

From the input materials and messaging house context, synthesize a launch messaging foundation:

**What's launching** — A clear, plain-language description of the product or feature. What it is, what it does, what's new. Not marketing copy — a crisp factual statement the rest of the BOM derives from.

**Why it matters** — The customer problem it solves and the outcome it enables. Grounded in persona pain points from the messaging house.

**What's different** — The differentiated capability or approach. Must trace to `space.md` or product messaging — not invented.

**Who it's for** — Primary persona(s) and segment(s). If this launch targets a new audience not in the messaging house, flag it.

**Key proof** — Any metrics, beta customer outcomes, or validation available at launch. Flag "No proof available at launch" if none exists — this is common and should be noted rather than papered over.

**Messaging house gaps** — Which docs need to be created or updated as a result of this launch. Common gaps: new product profile needed, solution profile needs updating, space.md competitive section needs revision. These are flagged for the user to address after launch assets are produced.

Present the synthesis and call AskUserQuestion:

> "Does this capture the launch correctly? Any corrections before I plan the BOM?"

Do not proceed until the user confirms.

---

## Phase 2: Launch Brief

Write the brief to `output/launches/[launch-name]/brief.md`. The user must approve it before production begins.

### Brief Frontmatter

Write YAML frontmatter with:

- `launch_name` — Kebab-case identifier (e.g., `acme-platform-v3-launch`)
- `launch_tier` — major, minor, feature, integration
- `product` — Product or feature being launched
- `ga_date` — Target general availability date
- `availability` — ga, limited, beta
- `created` — Date string
- `status` — "draft" → "approved" → "in-progress" → "complete"
- `shared_context` — Personas, products, segments, and `messaging_docs_loaded` list
- `messaging_gaps` — Docs flagged for creation or update post-launch
- `assets` — Array of asset entries, each with: id, type, skill, title, audience (internal/external), wave, depends_on, status

### Brief Body

#### Launch Narrative

The messaging foundation derived from Phase 1 synthesis. This is the source of truth every asset inherits from — not the messaging house directly, since some launch messaging may be net-new.

Include all six synthesis components: what's launching, why it matters, what's different, who it's for, key proof, and messaging house gaps.

#### Asset Manifest

Organized into **internal** and **external** tracks, then sequenced into waves. Internal assets always precede external.

For each asset, specify:
- **Skill** — Category/type mapping from the asset catalog below
- **Audience** — Internal (sales, CS, support, exec) or external (prospects, customers, press, analysts)
- **Wave** — Which production wave this asset belongs to
- **Dependencies** — Asset IDs that must be complete before this one is dispatched
- **Context Resolution** — Which launch narrative sections and messaging docs this asset draws from
- **Notes** — Format guidance, length, tone calibration, adaptation instructions

#### Generation Sequence

Wave structure enforces internal-before-external ordering:

```
Wave 1 (internal foundation):
  Sales talking points, internal FAQ, support runbook

Wave 2 (internal readiness):
  Competitive battlecard, discovery guide, sales one-pager

Wave 3 (external — gated on internal completion):
  Press release, announcement blog, product page copy

Wave 4 (external — follow-on):
  Email to customers, social post series, nurture sequence
```

Adjust waves based on which assets are in the BOM. Assets with no internal dependencies can move to Wave 1.

### Approval Flow

After writing the brief, present a summary:

```
Launch: [Name]
Product: [product]
GA Date: [date] ([tier], [availability])

Assets ([count]):
  Internal ([count]):
    Wave 1: [asset titles]
    Wave 2: [asset titles]
  External ([count]):
    Wave 3: [asset titles]
    Wave 4: [asset titles]

Messaging house gaps flagged: [count or "None"]
Flagged issues: [count or "None"]

Ready to generate? You can also edit the brief directly at
output/launches/[name]/brief.md and tell me when you're done.
```

The user can:
- **Approve** — Production begins.
- **Edit** — Modify through conversation or by editing the file directly and telling you to re-read it.
- **Cancel** — Brief stays as a draft. Resume later using `--continue [name]`.

---

## Phase 3: Production

After approval, update brief status to `in-progress` and generate assets wave by wave.

Internal waves must complete before external waves begin. After Wave 2 completes, surface internal assets to the user for review before proceeding to Wave 3: "Internal assets are ready. Review before I start external content?"

### Writer Subagent Dispatch

For each asset, spawn a writer subagent with:

| Context | Source | Purpose |
|---|---|---|
| Launch narrative | Brief body, launch narrative section | Shared foundation every asset inherits |
| Asset spec | Brief body, asset manifest entry | Per-asset context, wave, audience, notes |
| Shared messaging docs | Resolved from brief frontmatter | Baseline messaging context |
| Input materials | Relevant files from `input/` | Product detail, specs, pricing |
| Dependency assets | Previously generated assets in `output/launches/[name]/` | Narrative continuity |

The writer skips its own brief approval step — the launch brief was already approved. The writer generates the draft, validates against the voice gate (max 2 voice passes), writes to disk, dispatches the reader for formal review, and iterates on reader feedback autonomously (max 1 post-reader revision). Only "Major rework" verdicts are surfaced to the launch orchestrator. If the writer flags critical gaps or conflicts, it surfaces them rather than blocking.

### Progress Tracking

As each wave completes:

1. Update each asset's status in the brief frontmatter (`pending` → `complete` or `needs-revision`). An asset arrives as `complete` when the writer resolved the reader's feedback internally (including "Needs revision" verdicts handled via post-reader revision). An asset arrives as `needs-revision` only when the reader returned "Major rework" and the writer escalated.
2. Surface writer-flagged issues to the user.
3. For the internal/external boundary: pause and present internal assets before proceeding to external waves.
4. Proceed to the next wave after user confirmation at the internal/external boundary.

After all waves complete:

1. Update brief status to `complete`.
2. Present a completion summary: per-asset status, flagged issues, messaging house gaps still open, and the launch directory path.
3. Append a journal entry to `messaging/journal.md` with type "process" — launch execution notes, gaps surfaced, decisions made.

---

## Asset Catalog

Assets available for launch BOMs, organized by track.

### Internal Track

| Asset | Skill Category | Skill Type | Notes |
|---|---|---|---|
| Sales talking points | copywriting/enablement | discovery-guide | Situation trigger, core message, proof point, pivot |
| Internal FAQ | copywriting/enablement | playbook-walkthrough | Q&A format — what is it, who is it for, how do we sell it |
| Competitive battlecard | copywriting/enablement | competitive-battlecard | If competitive angle exists |
| Discovery guide | copywriting/enablement | discovery-guide | Full persona-aligned discovery framework |
| Sales one-pager | copywriting/brief | product-datasheet | Leave-behind for sales conversations |
| Objection handling guide | copywriting/enablement | competitive-battlecard | Launch-specific objection set |
| Support runbook | copywriting/enablement | playbook-walkthrough | Support team reference for common issues |
| Executive summary | copywriting/brief | company-overview | For exec alignment and board-level communication |
| Partner brief | copywriting/brief | solution-brief | If partner motion exists |
| Pricing one-pager | copywriting/brief | product-datasheet | Packaging and pricing reference |

### External Track

| Asset | Skill Category | Skill Type | Notes |
|---|---|---|---|
| Press release | copywriting/blog | press-release | Dateline, quotes, boilerplate, media contact |
| Announcement blog | copywriting/blog | product-announcement | Primary external launch post |
| Product page copy | copywriting/web | product-page | Updated or new product page |
| Solution page copy | copywriting/web | solution-page | If launch introduces or updates a solution |
| Customer announcement email | copywriting/email | product-newsletter | Existing customer communication |
| Prospect nurture email | copywriting/email | inbound-sequence | For pipeline in motion |
| LinkedIn post | copywriting/social | linkedin-post | |
| X post | copywriting/social | x-post | |
| Social post series | copywriting/social | linkedin-post, x-post | Multi-platform bundle |
| Use case blog | copywriting/blog | use-case-deep-dive | Follow-on content post-launch |
| Data sheet | copywriting/brief | product-datasheet | Formal product specification document |
| Event session abstract | copywriting/brief | session-abstract | If launch coincides with an event |

---

## Messaging House Gaps

When Launch introduces new products, capabilities, or positioning not yet reflected in the messaging house, flag the specific docs that need attention:

```
Messaging House Gaps:
- messaging/products/[product-slug].md — does not exist, needs to be created
- messaging/solutions/[solution-slug].md — needs updating to include new capability
- messaging/space.md — competitive section may need revision given new differentiation
```

Present this list in the brief and again in the completion summary. These are not blocking — launch assets can be produced without them — but they represent debt that should be resolved before the next campaign draws from the messaging house.

---

## Edge Cases

**No input materials.** If no relevant files exist in `input/`, AskUserQuestion to collect the minimum needed for synthesis: what is launching, what problem it solves, what's differentiated, who it's for. This is a slower path — launch works best when product artifacts are available.

**Launch conflicts with existing messaging.** If the launch introduces positioning that contradicts `space.md` or an existing product profile, flag the conflict explicitly. Do not resolve it silently. Surface it to the user and note it in the messaging house gaps section.

**Beta or limited availability.** Adjust external messaging to reflect availability constraints. Flag any assets where GA language needs to be softened (e.g., "coming soon," "available to select customers").

**No proof at launch.** Common and expected. Note it in the launch narrative and flag it in the brief. Do not fabricate proof. Writer subagents producing external assets should use capability claims rather than outcome claims when proof is unavailable.

**Skill not found for an asset.** Flag during brief generation and suggest the closest alternative.

**Partial production failure.** If a writer subagent fails, produces poor output, or the reader flags it as "Major rework," mark the asset as `needs-revision` and continue. Assets in later waves that depend on it receive a note that their dependency is flagged.