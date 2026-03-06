# PRD: Campaign Agent

## Overview

The campaign agent is an orchestrator that builds a complete bill of materials for a marketing campaign. It doesn't write content — it plans what to write, gets human approval on the plan, then dispatches writer subagents to produce each asset with precisely scoped context.

The writer agent produces one asset against one resolved context graph. The campaign agent produces many assets that share a narrative thread but each resolve different context from the messaging house. A product launch campaign targeting CISOs about the vulnerability management product might produce an announcement blog, a press release, a customer email, a sales battlecard, a LinkedIn post series, and landing page copy. Each needs different depth, altitude, and proof points, but all share the same core positioning and narrative.

The coordination mechanism is a **messaging brief** — a structured plan document that defines the shared context, per-asset context resolution, narrative flow between assets, and generation sequence. The user approves the brief before any content is produced. The brief is the contract between the human and the system.

## What Ships

```
.claude/
  agents/
    campaign.md            → Campaign orchestrator agent definition
  commands/
    campaign.md            → /project:campaign slash command

campaigns/
[campaign-name]/
    brief.md             → Approved messaging brief (the plan)
    asset-01-*.md        → Generated assets
    asset-02-*.md
    ...
```

## How It Works

Three phases, with a hard gate between planning and production.

```
Intake (interactive) → Brief (human-in-the-loop) → Production (subagent orchestration)
                                    ↑
                              user approval gate
```

---

## Phase 1: Intake

Intake is a structured conversation that resolves three things: campaign type, profile selections, and asset selections. The agent gathers all three before writing the brief.

### Campaign Types

Each type carries a default bill of materials. Defaults are a starting point — the user customizes in asset selection.

| Type | Description | Default Assets |
|---|---|---|
| **launch** | Product or feature announcement | Announcement blog, press release, customer email, social post series (LinkedIn, X), sales talking points, landing page copy |
| **digital** | Inbound content engine | Anchor asset (whitepaper or ebook), blog series (2-3 posts), email nurture sequence (3-5 emails), social promotion posts, landing page copy |
| **event** | Conference, webinar, or field event | Pre-event email sequence, booth/session messaging, session abstract, post-event follow-up email, social posts (pre/during/post) |
| **outbound** | Sales-driven prospecting | Cold email sequence (3-5 emails), LinkedIn message sequence, sales one-pager, battlecard |
| **play** | Competitive or strategic play | Battlecard, competitive blog post, objection handling guide, sales email templates, internal cheat sheet |
| **abm** | Account-based targeting | Account brief, personalized email sequence, custom landing page copy, sales talking points, executive summary |

If the user doesn't specify a type, ask. If they provide a description that implies a type, confirm: "This sounds like a product launch campaign. I'd suggest these assets: [default list]. Want to adjust?"

### Profile Selection

Resolve the messaging context that applies to the campaign as a whole. These become the **shared context** that every asset inherits.

| Parameter | Question to resolve | Multi-select? |
|---|---|---|
| **Persona(s)** | Who is this campaign targeting? | Yes — different assets may target different personas |
| **Product/Solution** | What offering is being campaigned? | Usually one, sometimes multiple for portfolio campaigns |
| **Competitor** | Is this competitive? Against whom? | Yes — a play campaign might address multiple competitors |
| **Segment** | Is this segment-specific? | Usually one |
| **Motion** | What GTM motion does this support? | Often implied by campaign type |

The agent resolves each parameter against the messaging house. If the user says "target CISOs," scan `messaging/personas/` for a matching profile. If it exists, load and confirm. If it doesn't, flag it: "There's no CISO persona in the messaging house. Want me to create one first with `/project:persona ciso`, or proceed using the audience-level context from `audience.md`?"

Some campaigns target multiple personas across different assets. A launch campaign might have a CISO email, a DevOps blog post, and an executive press quote. Each asset gets its own persona assignment — this is resolved in the asset manifest, not at the campaign level. But the campaign-level persona list defines the universe of personas this campaign addresses.

### Asset Selection

Present the default BOM for the resolved campaign type. Walk through it with the user:

**Add** — Assets not in the default list. The user might want a webinar script added to a digital campaign.

**Remove** — Assets they don't need. Not every launch needs a press release.

**Modify** — Scope changes. "Make the blog series 4 posts instead of 2." "The email sequence should be 7 touches, not 3."

**Reassign** — Per-asset persona targeting. "The email sequence should target CISOs but the blog posts should target DevOps leads."

**Skill mapping** — For each asset, identify which skill category and type will be used. Check that the skill exists in `.claude/skills/`. If it doesn't, flag it: "There's no skill for 'session abstract.' I can generate it using the blog-copywriting skill adapted for event context, or you can create a custom skill first."

Confirm the final asset list before proceeding to the brief.

### Intake Output

By the end of intake, the agent has:

- Campaign type and name
- Campaign objective (one sentence)
- Shared profile selections (personas, products, competitors, segments)
- Final asset list with per-asset persona assignments and skill mappings
- Flagged gaps (missing personas, missing skills, thin messaging context)

---

## Phase 2: Messaging Brief

The brief is the plan. It's a structured markdown document written to `campaigns/[campaign-name]/brief.md`. The user must approve it before production begins.

### Brief Frontmatter

```yaml
---
campaign_name: "q1-vuln-mgmt-launch"
campaign_type: "launch"
objective: "Drive awareness and pipeline for the new vulnerability management module among enterprise security teams"
created: "2026-03-03"
status: "draft"

shared_context:
  personas:
    - enterprise-ciso
    - devops-lead
  products:
    - vuln-mgmt
  competitors:
    - acme-corp
  segments:
    - enterprise
  messaging_docs_loaded:
    - messaging/profile.md
    - messaging/space.md
    - messaging/portfolio.md
    - messaging/products/vuln-mgmt.md
    - messaging/audience.md
    - messaging/proof.md

assets:
  - id: "asset-01"
    type: "blog-post"
    skill: "blog-copywriting/product-announcement"
    title: "Announcement Blog: Introducing Vulnerability Management"
    persona: "devops-lead"
    altitude: "practitioner"
    depends_on: []
    status: "pending"
  - id: "asset-02"
    type: "press-release"
    skill: "pr-copywriting/product-launch"
    title: "Press Release: [Company] Launches Vulnerability Management Module"
    persona: "enterprise-ciso"
    altitude: "executive"
    depends_on: []
    status: "pending"
  - id: "asset-03"
    type: "email"
    skill: "email-copywriting/customer-announcement"
    title: "Customer Email: New Vulnerability Management Module"
    persona: "enterprise-ciso"
    altitude: "executive"
    depends_on: ["asset-01"]
    status: "pending"
  - id: "asset-04"
    type: "sales-enablement"
    skill: "sales-copywriting/talking-points"
    title: "Sales Talking Points: Vulnerability Management"
    persona: "enterprise-ciso"
    altitude: "consultative"
    depends_on: ["asset-01", "asset-02"]
    status: "pending"
  - id: "asset-05"
    type: "social-series"
    skill: "social-copywriting/linkedin-series"
    title: "LinkedIn Series: Vulnerability Management Launch (4 posts)"
    persona: "devops-lead"
    altitude: "practitioner"
    depends_on: ["asset-01"]
    status: "pending"
  - id: "asset-06"
    type: "landing-page"
    skill: "web-copywriting/landing-page"
    title: "Landing Page: Vulnerability Management"
    persona: "enterprise-ciso"
    altitude: "executive"
    depends_on: ["asset-01", "asset-03"]
    status: "pending"
---
```

### Brief Body

#### Campaign Narrative

The through-line that unifies every asset. This is the single strategic argument the campaign makes, expressed differently at different altitudes and for different audiences. Every asset should be traceable to this narrative.

The narrative has two parts:

**Positioning statement** — 2-3 sentences. The core argument. Derived from `profile.md` (identity), `space.md` (positioning and differentiation), and the relevant product doc.

**Key messages** — 3-5 specific claims the campaign makes. These are not taglines. They are grounded assertions, each citing the messaging doc it derives from. Key messages are the raw material that writers adapt to their asset's audience and altitude.

```markdown
## Campaign Narrative

**Positioning:**
[Company] is the only [category] platform that [primary differentiator],
enabling [primary persona] to [primary outcome] without [primary pain point].
The new vulnerability management module extends this advantage into [adjacent space],
giving security teams [specific new capability] that [competitive contrast].

**Key Messages:**

1. **[Capability claim]** — [Company]'s vulnerability management module [specific capability].
   _Source: messaging/products/vuln-mgmt.md (key_capabilities), messaging/portfolio.md_

2. **[Differentiation claim]** — Unlike [competitor approach], [Company] [unique method].
   _Source: messaging/space.md (key_differentiators), messaging/competitors/acme-corp.md (differentiators_against)_

3. **[Outcome claim]** — Customers using [Company] see [specific metric improvement].
   _Source: messaging/proof.md (case study: [customer name])_

4. **[Audience fit claim]** — For [persona], this means [translated benefit at their altitude].
   _Source: messaging/personas/enterprise-ciso.md (goals, pain_points)_
```

#### Asset Manifest

For each asset, the manifest specifies everything the writer subagent needs to produce it. This is where per-asset context resolution happens — the campaign agent's core planning work.

Each asset entry includes:

**Context resolution** — Which messaging docs this asset loads beyond the shared campaign context. The shared context gives every writer the baseline (profile, space, product). The asset-specific context adds what this particular asset needs. A CISO email loads the CISO persona and filters proof for executive-relevant metrics. A DevOps blog loads the DevOps persona and emphasizes technical depth.

**Narrative thread** — Which key messages this asset emphasizes and what angle it takes. Not every asset covers all key messages. The announcement blog might emphasize messages #1 and #3 (capability and outcome). The battlecard might emphasize #2 (differentiation). The narrative thread keeps assets coordinated without being repetitive.

**Dependencies** — Which assets must be generated first. Dependencies create narrative continuity: the customer email can reference the blog as a CTA. Sales talking points can reference the press release framing. Express as asset IDs.

**Altitude and tone** — Even when two assets target the same persona, altitude differs by format. A LinkedIn post is short and provocative. A whitepaper is authoritative and comprehensive. Specify the calibration.

**Notes** — Anything the writer needs to know that doesn't fit the above. "This is the anchor asset — blog posts #2 and #3 will reference arguments established here." "The customer email should assume the reader already uses the platform."

Example:

```markdown
### Asset 01: Announcement Blog Post

**Skill:** blog-copywriting / product-announcement
**Persona:** devops-lead
**Altitude:** Practitioner — technical detail, concrete use cases, workflow implications
**Dependencies:** None (anchor asset)

**Context Resolution:**
- Shared: profile.md, space.md, products/vuln-mgmt.md, portfolio.md
- Asset-specific: personas/devops-lead.md, proof.md (filter: devops-relevant metrics, deployment stats)
- Skip: competitors/ (not a competitive asset), motions.md (not motion-specific)

**Narrative Thread:**
Emphasizes key messages #1 (capability) and #3 (outcome).
Angle: "What this means for your daily workflow." Ground the announcement in practitioner
reality — specific technical capabilities, integration points, concrete before/after scenarios.
Avoid corporate messaging altitude.

**Notes:**
This is the anchor. The customer email (asset-03) will link to this post. The LinkedIn series
(asset-05) will pull arguments from here. Establish the technical narrative foundation that
other assets riff on.
```

```markdown
### Asset 04: Sales Talking Points

**Skill:** sales-copywriting / talking-points
**Persona:** enterprise-ciso (as the buyer the sales team is pitching)
**Altitude:** Consultative — business impact language, ROI framing, objection handling
**Dependencies:** asset-01 (blog framing), asset-02 (press release positioning)

**Context Resolution:**
- Shared: profile.md, space.md, products/vuln-mgmt.md, portfolio.md
- Asset-specific: personas/enterprise-ciso.md (pain_points, objections, decision_criteria),
  competitors/acme-corp.md (differentiators_against, key_weaknesses),
  proof.md (filter: enterprise case studies, ROI metrics),
  motions.md (sales motion context)

**Narrative Thread:**
Emphasizes key messages #2 (differentiation) and #3 (outcome).
Angle: Arm the sales team with the "why us, why now" argument. Include objection responses
derived from the CISO persona's objections field and the competitor's weaknesses.

**Notes:**
Reference the press release framing for consistency on external positioning claims.
Include a "what customers are saying" section drawn from proof.md quotes.
Format as scannable sections — sales reps need to find talking points fast, not read prose.
```

#### Generation Sequence

Order the assets by their dependency graph. Assets with no dependencies are grouped into the first wave and can be generated in parallel. Subsequent waves wait for their dependencies to complete.

```markdown
## Generation Sequence

### Wave 1 (parallel, no dependencies)
- asset-01: Announcement Blog Post
- asset-02: Press Release

### Wave 2 (depends on Wave 1)
- asset-03: Customer Email [depends: asset-01]
- asset-04: Sales Talking Points [depends: asset-01, asset-02]

### Wave 3 (depends on Waves 1-2)
- asset-05: LinkedIn Series [depends: asset-01]
- asset-06: Landing Page [depends: asset-01, asset-03]
```

### Approval Flow

After writing the brief, present a summary to the user:

```
Campaign: Q1 Vulnerability Management Launch
Type: launch
Objective: Drive awareness and pipeline for the new vuln-mgmt module

Shared Context:
  Personas: enterprise-ciso, devops-lead
  Products: vuln-mgmt
  Competitors: acme-corp
  Messaging docs: 6 pillar/collection docs loaded

Assets (6):
  1. Announcement blog (devops-lead, practitioner)
  2. Press release (enterprise-ciso, executive)
  3. Customer email (enterprise-ciso, executive) → depends on #1
  4. Sales talking points (enterprise-ciso, consultative) → depends on #1, #2
  5. LinkedIn series / 4 posts (devops-lead, practitioner) → depends on #1
  6. Landing page (enterprise-ciso, executive) → depends on #1, #3

Generation: 3 waves
Flagged issues: None

Ready to generate? You can also edit the brief directly at
campaigns/q1-vuln-mgmt-launch/brief.md and tell me when you're done.
```

The user can:

- **Approve** — Production begins.
- **Edit** — Modify the brief through conversation ("move the landing page to wave 2," "add a webinar script," "change the blog persona to CISO") or by editing the file directly and telling the agent to re-read it.
- **Cancel** — Brief stays as a draft for later. The user can resume with `/project:campaign --continue [name]`.

---

## Phase 3: Production

After approval, update the brief status to `in-progress` and generate assets by wave.

### Writer Subagent Dispatch

For each asset, the campaign agent spawns a writer subagent with five pieces of context:

| Context | Source | Purpose |
|---|---|---|
| Campaign narrative | Brief body, narrative section | Shared through-line every asset inherits |
| Asset spec | Brief body, asset manifest entry | Per-asset context resolution, narrative thread, altitude, notes |
| Shared messaging docs | Resolved from brief frontmatter `shared_context.messaging_docs_loaded` | Baseline messaging context |
| Asset-specific messaging docs | Resolved from asset manifest context resolution | Per-asset messaging additions |
| Dependency assets | File content from previously generated assets in `campaigns/[name]/` | Narrative continuity — reference without copying |

The subagent invocation:

```
/agents writer --campaign [campaign-name] --asset [asset-id]
```

The writer agent's existing seven-step process (parse → resolve → load skill → cross-reference → generate → evaluate → write) runs normally. The campaign brief pre-resolves most parameters, but the writer still:

- Loads and reads each messaging doc itself (the brief specifies which docs, the writer reads the content)
- Runs its own cross-reference checks (persona pain points vs. product use cases, proof relevance)
- Self-evaluates against the skill's criteria
- Flags thin context or missing proof back to the campaign agent

The campaign agent does not override the writer's quality checks. If a writer flags an issue, the campaign agent surfaces it to the user.

### Dependency Handling

When an asset has dependencies, the campaign agent passes the generated content from dependency assets as reference context. The writer uses this for narrative continuity:

- The customer email references the blog's framing and links to it as a CTA
- Sales talking points echo the press release's external positioning
- The LinkedIn series pulls specific arguments from the blog

The writer should maintain continuity without duplicating. If the blog establishes a technical argument, the email can reference it ("as we shared on the blog") rather than repeating it.

For large campaigns (10+ assets), pass dependency content as summaries rather than full files to manage context window constraints. The campaign agent extracts the key arguments, positioning statements, and CTAs from each dependency asset and passes those as structured reference.

### Output Structure

```
campaigns/
q1-vuln-mgmt-launch/
    brief.md
    asset-01-announcement-blog.md
    asset-02-press-release.md
    asset-03-customer-email.md
    asset-04-sales-talking-points.md
    asset-05-linkedin-series.md
    asset-06-landing-page.md
```

Each asset file includes metadata frontmatter linking back to the campaign:

```yaml
---
campaign: "q1-vuln-mgmt-launch"
asset_id: "asset-01"
type: "blog-post"
skill: "blog-copywriting/product-announcement"
persona: "devops-lead"
altitude: "practitioner"
key_messages: [1, 3]
messaging_docs_loaded:
  - messaging/profile.md
  - messaging/space.md
  - messaging/portfolio.md
  - messaging/products/vuln-mgmt.md
  - messaging/personas/devops-lead.md
  - messaging/proof.md
dependency_assets: []
generated: "2026-03-03"
status: "complete"
---
```

### Progress Tracking

As each wave completes, the campaign agent:

1. Updates each asset's status in the brief frontmatter (`pending` → `complete` or `needs-revision`).
2. Checks for writer-flagged issues. If any exist, surfaces them to the user between waves: "Asset 03 (customer email) generated but the writer flagged that proof.md has no enterprise-specific case study. The proof section uses general metrics instead. Continue with wave 3 or pause to address?"
3. Proceeds to the next wave.

After all waves complete:

1. Updates brief status to `complete`.
2. Presents a completion summary:

```
Campaign complete: Q1 Vulnerability Management Launch

Generated: 6/6 assets
  ✓ asset-01: Announcement Blog Post
  ✓ asset-02: Press Release
  ✓ asset-03: Customer Email
  ✓ asset-04: Sales Talking Points
  ⚠ asset-05: LinkedIn Series (flagged: proof.md thin on DevOps metrics)
  ✓ asset-06: Landing Page

Messaging docs loaded across campaign: 8 unique docs
Flagged issues: 1 (see asset-05)

Review assets in campaigns/q1-vuln-mgmt-launch/.
Regenerate individual assets with /project:generate if you want to iterate.
```

---

## Iteration

Campaigns are living documents. The directory structure supports incremental iteration without full regeneration.

### Single Asset Regeneration

The user can regenerate one asset without touching the rest:

```
/project:generate blog-copywriting/product-announcement "vuln-mgmt announcement blog"
```

Or have the campaign agent re-dispatch a specific asset:

```
/project:campaign --continue q1-vuln-mgmt-launch --asset asset-05
```

The campaign agent re-reads the brief, loads the asset spec, and spawns a fresh writer subagent with the same context.

### Adding Assets

Edit the brief to add new asset entries (either through conversation or by editing the file), then:

```
/project:campaign --continue q1-vuln-mgmt-launch
```

The campaign agent detects assets with `status: pending` and generates only those, treating existing complete assets as available dependencies.

### Brief Revision

If the campaign narrative shifts (new positioning, different competitor focus, persona change), the user edits the brief and re-runs production. The campaign agent re-generates all assets whose context was affected by the change. Assets unaffected by the change keep their `complete` status.

---

## Edge Cases

**Skill not found for an asset.** During brief generation, check that every asset's specified skill exists in `.claude/skills/`. If missing, flag it in the brief and suggest alternatives: "There's no skill for 'session abstract.' I can map it to blog-copywriting/thought-leadership adapted for event context, or you can create a custom skill first."

**Persona not in messaging house.** If the campaign targets a persona without a profile in `messaging/personas/`, flag during intake. Suggest running `/project:persona [role]` first. If the user wants to proceed, fall back to pillar-level audience context from `audience.md` and note the limitation in the brief.

**Context window pressure.** Large campaigns (10+ assets) may strain the context window during orchestration. The campaign agent tracks assets by file path rather than holding full content in memory. When dispatching a writer with dependencies, extract key arguments and CTAs from dependency assets rather than passing full content.

**Partial production failure.** If a writer subagent fails or produces poor output, the campaign agent marks that asset as `needs-revision` in the brief and continues with the next wave. Assets in later waves that depend on the failed asset receive a note that their dependency is flagged, so the writer can compensate or the user can choose to pause.

**Skill-to-asset mismatch.** Some assets don't map cleanly to a single skill type. A "social post series" is multiple outputs from one skill invocation. A "sales one-pager" might combine elements of sales-copywriting and brief-copywriting. The brief should specify how the writer should handle these: generate as a single file with multiple sections, or as multiple files under the same asset ID.

**Campaign type not listed.** If the user describes a campaign that doesn't match the six default types (e.g., "partner co-marketing campaign" or "analyst briefing prep"), the agent should propose a custom BOM from scratch rather than forcing a type. Ask: "What assets do you need for this campaign?" and build the manifest from the user's answer.

---

## Tool Scoping

- **Read** — `messaging/`, `research/`, `insights/`, `.claude/skills/`, `campaigns/`. Full access to the messaging house for context resolution and to previously generated campaign assets for dependency context.
- **Write** — `campaigns/` only. Creates the campaign directory, writes the brief, tracks progress. Individual asset files are written by writer subagents.
- **Subagent** — Spawns writer agents with scoped context per asset. The writer agent definition at `.claude/agents/writer.md` handles the actual content generation.
- **Glob, Grep** — Full access. Used during intake to discover available personas, products, competitors, segments, and skills.
- **WebSearch, WebFetch** — Not used directly. The campaign agent is a planner, not a researcher. Research needs should be addressed before campaign creation via `/project:research` or `/project:competitor`.

---

## Command

### /project:campaign [type] [topic]

```markdown
Build a full campaign bill of materials.

Campaign type: $1
Topic/description: $2

If no type specified, ask the user to choose from: launch, digital, event, outbound, play, abm.

Phase 1 (Intake): Resolve campaign type, present default asset BOM, resolve profile selections
(persona, product, competitor, segment) by scanning messaging/. Confirm final asset list with user.

Phase 2 (Brief): Write a messaging brief to campaigns/[name]/brief.md. Include campaign
narrative (through-line + key messages grounded in messaging docs), per-asset specs with context
resolution and dependencies, and generation sequence by wave. Present summary and get explicit
user approval before proceeding.

Phase 3 (Production): Spawn writer subagents for each asset by wave, passing campaign narrative +
asset-specific context + resolved messaging docs + skill. Track progress in brief frontmatter.
Surface issues between waves. Present completion summary.

/agents campaign $ARGUMENTS
```

### /project:campaign --continue [name]

```markdown
Resume or extend an existing campaign: $ARGUMENTS

Read the brief at campaigns/$1/brief.md. Check asset statuses.

If there are assets with status "pending" — generate them (new assets added to the brief).
If there are assets with status "needs-revision" — re-generate them with fresh writer subagents.
If a specific --asset flag is provided — re-generate only that asset.
If the brief status is "draft" — resume the approval flow from where it left off.

/agents campaign --continue $ARGUMENTS
```

---

## Deliverables

- Agent definition: `.claude/agents/campaign.md`
- Command templates: `.claude/commands/campaign.md`
- Output directory convention: `campaigns/[name]/`
- Brief schema (frontmatter + body structure) as documented above
- Updated CLAUDE.md with campaign agent description and `/project:campaign` command