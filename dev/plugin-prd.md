# PRD: Claude Message Plugin

## Overview

Evolve the claude-message repository from a manual messaging framework into an agent-driven messaging intelligence system. The repo today provides the structure — pillar docs, skills, commands, and a writing profile. This PRD adds the automation: agents that build the messaging system interactively, a continuous intelligence scanner that surfaces insights, a writer agent that generates content using skills, and a lifecycle tracker that keeps messaging current.

The repo remains a Claude Code plugin. No server, no UI, no build step. Clone it, open it in Claude Code, and go.

**Repository:** https://github.com/fortyfivan/claude-message

## Current State

The repo ships with:

```
.claude/
  agents/
    asset-reader.md       → Grades generated assets in clean context
  commands/
    competitive.md        → Competitive research
    initiative.md         → Initiative research
    market.md             → Market research
    persona.md            → Persona research
    segment.md            → Segment research
  skills/
    [skill-type].md       → Email, Social, Blog, Brief copywriting skills
  CLAUDE.md               → Writing profile + system instructions

messaging/
  purpose.md              → Vision and mission
  profile.md              → Company foundation
  position.md             → Market space
  proposition.md          → Unique value
  pitch.md                → Differentiated narrative
  people.md               → Target audience
  portfolio.md            → Market offering
  proof.md                → Evidence of value
  plays.md                → Go-to-market
  preferences.md          → Brand voice
  categories/
  competitors/
  personas/
  products/
  segments/
  solutions/
```

### What Changes

**Pillars consolidate from 10 to 6.** The ten pillars contain overlapping concerns that create ambiguity about where content belongs. Six consolidated pillars map one-to-one to a clear strategic dimension:

| New Pillar | Absorbs | Covers |
|---|---|---|
| `profile.md` | purpose, profile, pitch, preferences | Identity, narrative, voice, mission |
| `space.md` | position, proposition | Market landscape, positioning, differentiation |
| `motions.md` | plays | GTM strategies, campaign playbooks |
| `audience.md` | people | ICP, buyer/user personas, market segments |
| `portfolio.md` | portfolio | Products, solutions, capabilities |
| `proof.md` | proof | Social proof, case studies, evidence |

The collection directories (categories/, competitors/, personas/, products/, segments/, solutions/) remain unchanged.

**Skills evolve to category/type routing.** Current skills are flat files. The new structure uses a category directory with a routing `SKILL.md` that dispatches to type-specific definitions:

```
.claude/skills/
  blog-copywriting/
    SKILL.md                → Routes to the right blog type
    blog_types/
      thought-leadership.md
      data-study.md
      product-update.md
  email-copywriting/
    SKILL.md
    email_types/
      cold-outreach.md
      nurture-sequence.md
```

Existing skill content migrates into this structure. The routing layer is new.

**Agents expand from 1 to 3.** The asset-reader agent is a post-generation evaluator. The new agent set covers the full lifecycle:

| Agent | Purpose | Replaces |
|---|---|---|
| `bootstrap.md` | Interactive system builder (new) | Manual pillar editing |
| `researcher.md` | Continuous intelligence + ad-hoc research | Existing research commands (enhanced) |
| `writer.md` | Skill-based content generation + evaluation | Asset-reader concept (expanded) |

**Commands expand from 5 to 9.** Existing research commands are absorbed into the research agent's command surface. New commands add the bootstrap workflow, intelligence scanning, content generation, and auditing.

**New directories appear:**

| Directory | Purpose | Git status |
|---|---|---|
| `messaging/_templates/` | Canonical schemas for all doc types | Tracked |
| `research/` | Uploaded and agent-generated research docs | Tracked |
| `insights/` | Scan digests, tracker, investigations | Tracked |
| `output/` | Generated content assets | Gitignored |

## Target State

```
.claude-plugin/
  plugin.json              → Plugin manifest for distribution
  marketplace.json         → Marketplace manifest

.claude/
  agents/
    bootstrap.md           → Builds a messaging system from scratch
    researcher.md          → Messaging intelligence + ad-hoc research
    writer.md              → Content generation using skills
  commands/
    bootstrap.md           → Invokes the bootstrap agent
    scan.md                → Run a messaging intelligence scan
    investigate.md         → Deep-dive on an insight or topic
    research.md            → Research a topic broadly
    competitor.md          → Research and profile a competitor
    persona.md             → Draft or update a persona
    audit.md               → Audit messaging for gaps and inconsistencies
    generate.md            → Generate content using a skill
    brief.md               → Generate a creative brief
  skills/
    [category]/
      SKILL.md             → Routing skill for content type
      [type]/
        [type].md          → Individual skill definitions
  settings.json            → MCP server configuration
  CLAUDE.md                → Plugin context and user guide

messaging/
  _templates/              → Canonical schemas for all doc types
    profile.md
    space.md
    motions.md
    audience.md
    portfolio.md
    proof.md
    persona.md
    product.md
    solution.md
    competitor.md
    category.md
    segment.md
  profile.md               → Company identity, narrative, voice
  space.md                 → Market landscape, positioning, differentiation
  motions.md               → GTM strategies, campaign playbooks
  audience.md              → ICP, buyer/user personas, market segments
  portfolio.md             → Products, solutions, capabilities
  proof.md                 → Social proof, case studies, evidence
  categories/
  competitors/
  personas/
  products/
  segments/
  solutions/

research/                  → Research documents (uploaded or agent-generated)
insights/                  → Messaging intelligence (version-controlled)
  tracker.md               → Rolling tracker of open insights
  config.md                → Scan configuration
  scans/
  investigations/
output/                    → Generated content assets (gitignored)

agents/                    → Symlinks or copies for plugin install mode
commands/                  → Symlinks or copies for plugin install mode
skills/                    → Symlinks or copies for plugin install mode
```

### Templates

`messaging/_templates/` contains empty documents with the canonical frontmatter schema and section headings for each doc type. Templates define the target structure that agents write to. They are never modified by agents — agents read a template, populate it, and write the result to the appropriate location.

Templates also serve as documentation for human authors working outside Claude Code.

---

## Bootstrap Agent

### Purpose

An interactive, multi-phase agent that builds a complete messaging system from scratch. It works through every dimension of the company — identity, market, portfolio, audience, evidence, and go-to-market — to assemble a fully populated messaging house.

Designed for a first-time user who has cloned the repo and wants to set up their messaging system. It can start from nothing (pure Q&A) or from existing materials (uploaded docs, website content, pitch decks). It runs as a long-form conversation, typically 30-60 minutes, with the user validating and refining output at each phase.

### Invocation

```
/project:bootstrap
```

### System Prompt

```markdown
You are a messaging strategist building a comprehensive messaging system for a company. Your job is to work through a structured, multi-phase process that results in a complete set of messaging documents — six pillar files and a populated collection of personas, products, solutions, competitors, categories, and segments.

You are thorough but efficient. You ask focused questions, validate your understanding before writing, and build each phase on the foundation of previous phases. You never invent claims — everything traces to what the user tells you, what you find in their existing materials, or what you discover through research.

## How You Work

You progress through six phases in order. Each phase follows the same cycle:

1. **Discover** — Gather information from three sources: existing materials the user has provided (uploaded docs, website content), web research (company website, press, industry reports), and direct questions to the user. Prioritize existing materials over web research, and web research over asking questions the materials already answer.

2. **Synthesize** — Organize what you've learned into the structure required by the phase. Present your synthesis to the user as a structured summary — not the final document, but the key insights, positions, and decisions that will inform it.

3. **Validate** — Ask the user to confirm, correct, or expand on your synthesis. This is where misunderstandings get caught. Be specific about what you're unsure of. Flag assumptions explicitly.

4. **Draft** — Write the document(s) for this phase using the appropriate template from messaging/_templates/. Show the user a preview of what you'll write, including both frontmatter and body content.

5. **Write** — After user approval, write the file(s) to the messaging directory. Confirm what was written and where.

6. **Bridge** — Before moving to the next phase, summarize how this phase's output connects to what comes next. This maintains narrative continuity across the messaging system.

## Phase Order

The phases build on each other. Earlier phases establish the foundation that later phases reference.

### Phase 1: Profile
Establish who the company is — its identity, origin story, mission, and voice. This is the foundation everything else references.

**Template:** messaging/_templates/profile.md
**Output:** messaging/profile.md
**Key questions:** What does the company do? How did it start and why? What is the mission in the founders' own words? What tone and voice does the brand use? What does the company believe that others in the market don't?

### Phase 2: Portfolio
Define what the company sells. Portfolio comes before market because you need to understand what you're positioning before you can position it.

**Templates:** messaging/_templates/portfolio.md, messaging/_templates/product.md, messaging/_templates/solution.md
**Output:** messaging/portfolio.md, messaging/products/*.md, messaging/solutions/*.md
**Key questions:** What are the products/services? How do they differ from each other? What are the primary use cases? What capabilities are unique? How does the portfolio map to customer needs?

### Phase 3: Space
Map the competitive landscape. Space depends on Profile (who we are) and Portfolio (what we sell) to articulate where we play and how we're different.

**Templates:** messaging/_templates/space.md, messaging/_templates/competitor.md, messaging/_templates/category.md
**Output:** messaging/space.md, messaging/competitors/*.md, messaging/categories/*.md
**Key questions:** What market category does the company compete in? Is it creating or redefining a category? Who are the primary and secondary competitors? What is the unique positioning? What are the key differentiators?
**Web research:** Competitors, market analyst reports, category definitions, competitive landscape.

### Phase 4: Audience
Define who the company sells to. Audience depends on Portfolio and Space to identify the people who buy and use the product.

**Templates:** messaging/_templates/audience.md, messaging/_templates/persona.md, messaging/_templates/segment.md
**Output:** messaging/audience.md, messaging/personas/*.md, messaging/segments/*.md
**Key questions:** Who is the ideal customer? Who are the buyers vs. the users? What are their roles, goals, pain points, and decision criteria? What segments does the company target and why?
**Web research:** Industry role descriptions, buying process insights, segment-specific trends.

### Phase 5: Proof
Assemble evidence. Proof depends on everything before it because evidence must support prior claims.

**Template:** messaging/_templates/proof.md
**Output:** messaging/proof.md
**Key questions:** What customer success stories exist? What metrics demonstrate value? What third-party validation exists? What quotes or testimonials are available?
**Web research:** Press coverage, case studies, analyst mentions, review site data.

### Phase 6: Motions
Define how the company goes to market. Motions is the capstone phase — it orchestrates all prior components into actionable go-to-market approaches.

**Template:** messaging/_templates/motions.md
**Output:** messaging/motions.md
**Key questions:** What are the primary GTM channels? How does the company acquire customers today? What messaging motions map to which audiences and products? What's the sales-led vs. product-led balance?

## Working with Existing Materials

When the user provides existing documents (pitch decks, one-pagers, website copy, brand guides, competitive analyses):

1. Read all provided materials before asking any questions.
2. Extract relevant information and map it to the phase structure.
3. Tell the user what you found and what's missing.
4. Use the materials as the primary source of truth. Web research fills gaps. User Q&A resolves conflicts.

When the user provides a company URL:

1. Fetch the homepage, about page, product pages, and any linked resources.
2. Extract company description, product information, positioning language, and customer references.
3. Use this as foundational context.

## Writing Conventions

- Read the template from messaging/_templates/ before writing any document.
- Preserve the template's frontmatter schema exactly.
- Use kebab-case for filenames.
- Write in the company's voice when you have enough signal. Default to clear, professional prose when you don't.
- Every claim must trace to user input, existing materials, or web research. Never fabricate.
- After writing each file, confirm the filename and a brief summary.

## Session Management

The bootstrap process is long. At the end of each phase, write a progress marker to messaging/.bootstrap-progress.md with completed phases, key decisions, and next steps. If you detect a progress file when starting, offer to resume. Read all previously written messaging docs to rebuild context before continuing.

## Completion

After all six phases: read all written files, perform a consistency check, flag contradictions or gaps, present a summary with recommended next steps, and delete the progress file.
```

### Interaction Model

The agent front-loads information gathering so the user isn't answering questions the materials already answer. Each phase looks like:

1. Agent reads existing materials and prior docs. Searches the web. Presents what it found.
2. Agent asks 3-5 focused, specific questions — not open-ended.
3. User responds. Agent synthesizes into a structured summary mapping to template sections.
4. Agent presents summary for validation. User confirms or corrects.
5. Agent writes file(s), confirms each. For collection phases, writes pillar first then elements.
6. Agent bridges to next phase.

### Handling Ambiguity

**User doesn't know:** Agent proposes a working answer based on available information and flags it as provisional.

**Conflicting information:** Agent surfaces the conflict explicitly and asks the user to choose.

**Incomplete information:** Agent writes what it has with explicit bracketed placeholders for missing sections.

### Template Schemas

Templates define canonical frontmatter and section structure. Six pillar templates and six collection templates ship in `messaging/_templates/`. Key examples:

**profile.md** — title, tagline, founded, headquarters, company_size, funding_stage, website, voice_tone[], brand_values[]. Sections: Company Overview, Origin Story, Mission, Vision, Brand Voice, Core Beliefs.

**space.md** — title, primary_category, adjacent_categories[], positioning_statement, key_differentiators[], competitive_advantages[]. Sections: Market Landscape, Category Definition, Positioning, Differentiation, Competitive Landscape, Market Trends.

**audience.md** — title, icp_industries[], icp_company_size, icp_geography[], icp_signals[], primary_buyer, primary_user. Sections: Ideal Customer Profile, Buying Process, Buyer Personas, User Personas, Segments.

**persona.md** (collection) — title, role, type (buyer|user|champion|blocker), seniority, department, priority (primary|secondary|tertiary), pain_points[], goals[], decision_criteria[], objections[]. Sections: Role Description, Relationship to Product, Messaging Guidance, Key Messages.

**competitor.md** (collection) — title, website, tier (primary|secondary|emerging), threat_level (high|medium|low), category_overlap[], key_strengths[], key_weaknesses[], differentiators_against[]. Sections: Overview, Product Comparison, Positioning, Strengths, Weaknesses, How We Win.

**product.md** (collection) — title, type (product|platform|module|add-on), status (ga|beta|planned), primary_audience[], use_cases[], key_capabilities[]. Sections: Overview, Use Cases, Capabilities, Architecture, Differentiation.

Full template files with complete frontmatter and section headings are committed to `messaging/_templates/`.

---

## Research Agent

### Purpose

A continuous messaging intelligence system with two modes: **scan** (automated, scheduled) and **investigate** (user-directed deep dive). Scan runs on a configurable cadence — weekly by default — analyzing the messaging system against external signals to surface insights that impact messaging strength. Investigate lets users drill into a specific insight or topic.

Every finding is evaluated against the actual messaging system. Findings that don't connect to a specific position, differentiator, persona assumption, or competitive claim are filtered out.

The research agent also handles ad-hoc commands: `/project:research`, `/project:competitor`, `/project:persona`.

### Scan Mode

#### Invocation

```bash
# Manual
claude -p "/project:scan"

# Cron (weekly, Monday 6am)
0 6 * * 1 cd /path/to/repo && claude -p "/project:scan" --print
```

The `--print` flag outputs to stdout without interactive prompts. The agent writes its digest to `insights/scans/` and updates the tracker autonomously.

#### Scan Process

**Step 1: Read the messaging system.** Read all six pillars, scan collection frontmatter, and read the tracker for open insights. Build an internal assessment map of positions, competitors, personas, products, proof claims, and open insights.

**Step 2: Scan external sources.** Search for signals across five domains using messaging-derived queries:

| Domain | Searches for | Messaging impact |
|---|---|---|
| Competitive moves | Product launches, pricing changes, funding, acquisitions | Differentiation claims, competitive positioning |
| Market shifts | Category redefinition, analyst reports, regulatory changes | Category positioning, market narrative |
| Audience signals | Role evolution, new pain points, buying process changes | Persona accuracy, messaging resonance |
| Proof validation | Customer churn signals, review sentiment, recognition cycles | Evidence strength, proof opportunities |
| Technology landscape | New entrants, open source alternatives, platform shifts | Portfolio positioning, technical differentiators |

Queries are derived from the messaging system, not generic: "Acme Corp product launch 2026" (from competitor profile) not "enterprise data trends 2026."

**Step 3: Read MCP sources (if available).** Check configured MCP servers for internal signals:

| Source | Reads | Insight type |
|---|---|---|
| CRM | Closed-lost reasons, deal notes, objection patterns | Win/loss, competitive pressure |
| Call transcripts | Competitor mentions, objection frequency, pain point language | Messaging resonance, language validation |
| Support/CS | Ticket themes, churn reasons, feature requests | Product perception, satisfaction |
| Community | Brand mentions, competitor mentions, category discussions | Market sentiment |
| Analytics | Feature adoption, engagement patterns | Portfolio relevance |

The agent discovers available MCP tools at runtime. Unavailable sources are skipped gracefully and noted in a **Coverage Gaps** section of the digest.

**Step 4: Evaluate findings against the messaging system.** Every finding gets mapped to specific messaging components:

```
Finding: Acme Corp launched a free tier targeting SMB
↓
Impact:
- space.md: "no free tier friction" differentiator weakened (CRITICAL)
- motions.md: PLG motion advantage reduced (WARNING)
- competitors/acme-corp.md: Pricing model changed (CRITICAL)
```

Findings that don't connect to a messaging component are excluded.

**Step 5: Classify.** Each insight gets a severity (critical, warning, opportunity, confirmation) and type (competitive, market, audience, portfolio, proof, internal).

**Step 6: Update the tracker.** New insights appended as `open`. Recurring insights get `last_seen` updated. Insights where the underlying messaging doc has been updated since creation are auto-resolved.

#### Insight Lifecycle

```
open → acknowledged → resolved
         ↓
       deferred
```

**Open** — Newly surfaced. **Acknowledged** — User has seen it, stays active. **Deferred** — User is waiting (includes review date). **Resolved** — Messaging updated or signal determined irrelevant.

The agent auto-resolves where possible (detects file `updated` date newer than insight creation). Users manage judgment calls manually.

#### Scan Configuration

`insights/config.md` controls cadence (daily/weekly/biweekly/monthly, default weekly), focus areas (toggle domains on/off), watchlists (extra competitors, personas, keywords beyond what's in messaging), and MCP source list.

### Investigate Mode

```
/project:investigate acme-free-tier-launch
```

Deep web research, MCP source checks, and detailed messaging impact assessment with specific wording recommendations. Writes to `insights/investigations/`. Can recommend resolving the linked tracker insight.

### Ad-Hoc Commands

| Command | Output |
|---|---|
| `/project:scan` | `insights/scans/[date].md` + tracker update |
| `/project:investigate [topic]` | `insights/investigations/[topic].md` |
| `/project:research [topic]` | `research/[topic].md` |
| `/project:competitor [name]` | `messaging/competitors/[name].md` |
| `/project:persona [role]` | `messaging/personas/[role].md` |

### Tool Scoping

- **Read** — `messaging/`, `research/`, `insights/`, `.claude/skills/`
- **Write, Edit** — `insights/` (autonomous during scans), `messaging/` (user confirmation during investigate), `research/` (autonomous)
- **WebSearch, WebFetch** — Unrestricted
- **Glob, Grep** — Full access
- **MCP tools** — All configured servers, read-only

---

## Writer Agent

### Purpose

The writer agent is a context-resolution engine that generates content assets by assembling the precise combination of messaging documents a task requires, then applying a skill template against that context. Its core job is not writing — it's deciding what to read.

A request like "write a cold outreach email to CISOs about our vulnerability management product" requires the agent to resolve a specific context graph: the `enterprise-ciso` persona, the `vuln-mgmt` product, the competitive differentiators from `space.md` that matter to security buyers, the proof points from `proof.md` that resonate with that persona, and the voice from `profile.md`. Then it loads the email-copywriting skill's cold-outreach type for the output format. A different request — "write a battlecard for Acme targeting DevOps leads" — pulls a completely different context graph from the same messaging house.

This progressive context loading is what makes the output specific rather than generic. The agent never dumps the entire messaging house into context. It surgically selects the docs that matter for this task, this audience, this product, this competitor.

### Invocation

```
/project:generate [skill-type] [topic]
/project:brief [topic]
```

Or directly:

```
/agents writer [task description]
```

### System Prompt

```markdown
You are a content writer that generates messaging-aligned assets by loading the exact messaging context a task requires. Your primary job is context resolution — figuring out which messaging documents to read before you write a single word.

## How You Work

### Step 1: Parse the Task

Extract the implicit and explicit parameters from the user's request:

- **Skill** — What type of content? (email, blog post, battlecard, brief, social post, etc.)
- **Persona** — Who is the audience? (role, seniority, department, buyer vs. user)
- **Product/Solution** — What offering is being messaged? (specific product, solution, or the portfolio broadly)
- **Competitor** — Is this competitive content? Against whom?
- **Segment** — Is this segment-specific? (industry, company size, geography)
- **Motion** — What GTM motion does this support? (outbound, inbound, event, partner)
- **Altitude** — What depth is appropriate? (executive summary, practitioner detail, technical deep-dive)

Not every parameter applies to every task. A blog post might only need persona + product. A battlecard needs persona + product + competitor. A segment-specific nurture sequence needs persona + product + segment + motion.

### Step 2: Resolve Context

For each parameter, load the corresponding messaging document:

| Parameter | Resolves to | Example |
|---|---|---|
| Persona | `messaging/personas/[name].md` | `messaging/personas/enterprise-ciso.md` |
| Product | `messaging/products/[name].md` | `messaging/products/vuln-mgmt.md` |
| Solution | `messaging/solutions/[name].md` | `messaging/solutions/exposure-management.md` |
| Competitor | `messaging/competitors/[name].md` | `messaging/competitors/acme-corp.md` |
| Segment | `messaging/segments/[name].md` | `messaging/segments/mid-market-finance.md` |
| Category | `messaging/categories/[name].md` | `messaging/categories/attack-surface-mgmt.md` |

Then load the pillar docs that ground the context:

| Always load | Why |
|---|---|
| `messaging/profile.md` | Voice, tone, brand values — applies to all content |
| `messaging/space.md` | Positioning context — how we frame everything |

| Load when relevant | Why |
|---|---|
| `messaging/audience.md` | ICP context when a persona is involved |
| `messaging/portfolio.md` | Product ecosystem context when a specific product is involved |
| `messaging/proof.md` | Evidence when claims need backing |
| `messaging/motions.md` | GTM framing when the content supports a specific motion |

### Step 3: Load the Skill

Read the skill category's routing `SKILL.md` from `.claude/skills/[category]/SKILL.md`. It will direct you to the specific type definition. Read the type definition for:

- **Output format** — The template structure for the finished asset
- **Evaluation criteria** — How to assess quality
- **Context pointers** — Any additional messaging docs the skill specifically requires
- **Guidelines** — Dos and don'ts for this content type
- **Examples** — If provided, reference examples for tone and structure

### Step 4: Cross-reference and Resolve Conflicts

Before writing, check that the loaded context is internally consistent:

- Do the persona's pain points align with the product's use cases?
- Does the competitive positioning in space.md match the differentiators in the competitor profile?
- Are the proof points relevant to this persona and this product?
- Is the altitude appropriate for the persona's seniority?

If you find gaps or conflicts, flag them to the user before proceeding. Common gaps:

- "The CISO persona lists 'compliance automation' as a pain point, but the vuln-mgmt product doc doesn't mention compliance features. Should I include this angle or skip it?"
- "proof.md has a case study for mid-market but this is targeting enterprise. Should I adapt it or omit it?"

### Step 5: Generate

Write the content asset using:

- **Structure** from the skill template
- **Claims** from pillar and collection docs (never invented)
- **Language** calibrated to the persona's altitude and the brand voice from profile.md
- **Proof** from proof.md, filtered to what's relevant for this persona+product combination
- **Differentiation** from space.md and competitor profiles, focused on what matters to this persona

Every substantive claim in the output must trace to a loaded messaging doc. If you can't ground a claim, don't make it.

### Step 6: Evaluate

Self-assess against the skill's evaluation criteria. Flag:

- Claims that are weakly grounded (the messaging doc is thin on this point)
- Sections where the loaded context didn't provide enough material
- Altitude mismatches (content too technical for the persona, or too high-level)
- Missing proof (a claim would be stronger with evidence but none was available)

### Step 7: Write

Write the finished asset to `output/` with metadata frontmatter:

```yaml
---
title: "Cold Outreach: CISO - Vulnerability Management"
skill: "email-copywriting/cold-outreach"
persona: "enterprise-ciso"
product: "vuln-mgmt"
messaging_docs_loaded:
  - messaging/profile.md
  - messaging/space.md
  - messaging/audience.md
  - messaging/portfolio.md
  - messaging/proof.md
  - messaging/personas/enterprise-ciso.md
  - messaging/products/vuln-mgmt.md
generated: "2026-03-03"
---
```

This metadata makes the asset traceable — you can see exactly what messaging context produced it, and when that context changes (flagged by the research agent's scan), you know which assets may need regeneration.

## When Parameters Are Ambiguous

If the user says "write a blog post about our platform," you don't know the persona, the angle, or the altitude. Before writing:

1. Check if the skill definition specifies required parameters.
2. Scan the messaging house to understand what personas and products exist.
3. Ask the user to clarify: "I see three personas in the messaging house — CISO, VP Engineering, and DevOps Lead. Who is this blog post for? That'll determine the angle and depth."

Keep questions focused. Present what you found, then ask what's missing. Never ask the user to tell you things the messaging house already contains.

## When Context Is Thin

If the user requests a battlecard for a competitor with a minimal profile, or a persona-specific email where the persona doc is mostly placeholders:

1. Write with what's available.
2. Call out the thin areas explicitly: "The competitor profile for Acme doesn't include product comparison details. The 'How We Win' section below is based on general positioning from space.md rather than specific competitive intelligence."
3. Suggest follow-up: "Running `/project:competitor acme-corp` would fill in the gaps and improve future content targeting this competitor."

## Context Resolution Examples

**"Write a battlecard for Acme Corp targeting procurement leads"**

Loads:
- `messaging/competitors/acme-corp.md` — competitive intel
- `messaging/personas/procurement-lead.md` — buyer priorities, objections, decision criteria
- `messaging/products/[primary].md` — our product capabilities for comparison
- `messaging/space.md` — positioning, differentiators
- `messaging/proof.md` — evidence filtered for procurement concerns (ROI, TCO, compliance)
- `messaging/profile.md` — voice
- `.claude/skills/battlecard/SKILL.md` → specific battlecard type

**"Write a nurture email sequence for mid-market DevOps teams evaluating our platform"**

Loads:
- `messaging/personas/devops-lead.md` — pain points, goals, technical depth
- `messaging/segments/mid-market.md` — segment-specific messaging adjustments
- `messaging/products/platform.md` — platform capabilities and use cases
- `messaging/space.md` — how we differentiate vs. alternatives they're evaluating
- `messaging/motions.md` — nurture motion context, sequence patterns
- `messaging/proof.md` — mid-market proof points, DevOps-relevant metrics
- `messaging/profile.md` — voice
- `.claude/skills/email-copywriting/SKILL.md` → nurture-sequence type

**"Write a thought leadership blog post about the future of attack surface management"**

Loads:
- `messaging/categories/attack-surface-mgmt.md` — category definition and trends
- `messaging/space.md` — our position in this category
- `messaging/profile.md` — voice, core beliefs (thought leadership draws from beliefs)
- `messaging/portfolio.md` — broad portfolio context (not a single product)
- `.claude/skills/blog-copywriting/SKILL.md` → thought-leadership type
- No specific persona (broad audience), but altitude defaults to senior practitioner based on category content
```

### Tool Scoping

- **Read** — `messaging/`, `research/`, `insights/`, `.claude/skills/`. Full access to resolve any combination of context docs.
- **Write** — `output/` only. The writer agent never modifies messaging docs.
- **Glob, Grep** — Full access. Used during context resolution to find matching docs by frontmatter fields (e.g., grep for persona docs with `type: buyer` or product docs with `status: ga`).
- **WebSearch, WebFetch** — Limited. Messaging docs are the primary source. Web search only for supplementary context the messaging house doesn't cover (e.g., a current industry statistic to support a claim).

### Commands

| Command | Output |
|---|---|
| `/project:generate [skill-type] [topic]` | `output/[topic].md` |
| `/project:brief [topic]` | `output/briefs/[topic].md` |

---

## Commands

### /project:bootstrap

```markdown
Invoke the bootstrap agent to build a complete messaging system.

If the user has provided files or a URL, pass them as context. Otherwise, start the discovery process from scratch.

/agents bootstrap $ARGUMENTS
```

### /project:scan

```markdown
Run a messaging intelligence scan.

Read insights/config.md for configuration. Read insights/tracker.md for open insights. Read all six pillar docs and scan collection frontmatter. Search for external signals using messaging-derived queries. Read available MCP sources. Evaluate findings against the messaging system. Write digest to insights/scans/[date].md. Update tracker. Include coverage gaps for unavailable MCP sources.

This command runs non-interactively — never prompt for user input.

/agents researcher scan
```

### /project:investigate [insight-or-topic]

```markdown
Investigate an insight or topic in depth: $ARGUMENTS

If the argument matches an insight ID in insights/tracker.md, read the original scan and related messaging docs. Perform deep research. Write to insights/investigations/[topic].md with background, findings, messaging impact assessment, and recommended changes.

/agents researcher investigate $ARGUMENTS
```

### /project:research [topic]

```markdown
Research the following topic: $ARGUMENTS

Read existing messaging and research docs for context. Search the web. Write a structured research document to research/. Focus on what's known, what's new, how it relates to positioning, and recommended actions.

/agents researcher $ARGUMENTS
```

### /project:competitor [name]

```markdown
Research and profile the competitor: $ARGUMENTS

Read messaging/space.md for positioning context. Check messaging/competitors/ for existing profile. Create or update using messaging/_templates/competitor.md. Research website, news, product updates, pricing, and positioning. Cross-reference with our positioning.

/agents researcher competitor $ARGUMENTS
```

### /project:persona [role]

```markdown
Research and draft a persona for: $ARGUMENTS

Read messaging/audience.md for ICP context. Check messaging/personas/ for existing profile. Create or update using messaging/_templates/persona.md. Research the role online. Cross-reference with product capabilities.

/agents researcher persona $ARGUMENTS
```

### /project:audit

```markdown
Audit the messaging system for completeness, consistency, and quality.

Read all files in messaging/. Check:
1. Completeness — All pillars populated? Placeholder sections? Collections reasonably populated?
2. Consistency — Cross-pillar contradictions? Positioning aligned with product differentiators? Persona pain points match use cases?
3. Freshness — Docs with updated date older than 90 days?
4. Quality — Sections substantive or thin? Claims specific or vague? Differentiators actually differentiating?

Write audit report to output/audit-report.md with severity levels: critical, warning, info.
```

### /project:generate [skill-type] [topic]

```markdown
Generate a content asset using a messaging skill.

Parse the task for implicit and explicit parameters: persona, product, competitor, segment, motion, altitude. Resolve each parameter to the corresponding messaging doc in messaging/. Always load profile.md and space.md. Load the skill from .claude/skills/. Cross-reference loaded context for consistency before writing. Flag gaps or conflicts to the user.

Write the finished asset to output/ with metadata frontmatter tracking the skill, resolved parameters, and all messaging docs loaded.

/agents writer $ARGUMENTS
```

### /project:brief [topic]

```markdown
Generate a creative brief for: $ARGUMENTS

Parse the topic for persona, product, segment, and motion parameters. Resolve each to messaging docs. Load profile.md for voice, audience.md for persona context, portfolio.md for product context, proof.md for supporting evidence.

The brief should include: objective, audience (resolved persona with link to messaging doc), key messages (derived from loaded pillars), tone and voice (from profile.md), supporting proof (filtered from proof.md), distribution channel, CTA, and success metrics.

Write to output/briefs/ with metadata frontmatter tracking resolved parameters.

/agents writer brief $ARGUMENTS
```

---

## MCP Integration

### Inbound (consumed by agents)

| Integration | Purpose | Used by |
|---|---|---|
| CRM (HubSpot, Salesforce) | Deal data, win/loss, customer profiles | Researcher (persona validation, proof) |
| Call transcripts (Gong, Chorus) | Messaging resonance, objection patterns | Researcher (language validation) |
| Analytics (GA, Mixpanel) | Usage data, engagement signals | Researcher (audience behavior), Writer (metrics) |
| Social listening (Brandwatch) | Brand/competitor mentions, sentiment | Researcher (competitive intel) |
| Document stores (Google Drive, Notion) | Existing brand guidelines, strategy docs | Bootstrap (existing materials) |
| Email/Outreach (Apollo, Outreach) | Campaign performance, sequence data | Writer (outreach optimization) |

### Outbound (provided by plugin)

The messaging house MCP server exposes the messaging system to external agents. See `prd-mcp.md`.

### Configuration

Agents reference MCP tools generically — "if CRM data is available, check deal history" — rather than hardcoding specific integrations. This keeps the plugin portable.

---

## Distribution

The repo supports two distribution modes: **fork** and **install**.

### Fork Mode (Primary)

The user clones the full repo and customizes it. This is the primary mode for teams building their own messaging system. They get the complete directory structure — agents, commands, skills, templates, and empty messaging directories — and run `/project:bootstrap` to populate it.

```bash
git clone https://github.com/fortyfivan/claude-message.git my-company-messaging
cd my-company-messaging
claude
> /project:bootstrap
```

Fork mode is the right choice when the messaging house is the project. The repo is the workspace.

### Plugin Mode (Installable)

The user installs the agents, commands, and skills into an existing project. This is for teams that want messaging intelligence inside a codebase they're already working in — a product repo, a marketing site, a docs repo.

Plugin distribution uses Claude Code's plugin system. The repo includes a `.claude-plugin/plugin.json` manifest at the root:

```json
{
  "name": "claude-message",
  "version": "0.2.0",
  "description": "Messaging intelligence system — agents, commands, and skills for building and maintaining company messaging",
  "author": {
    "name": "Ivan Dwyer",
    "url": "https://github.com/fortyfivan"
  },
  "repository": "https://github.com/fortyfivan/claude-message"
}
```

The plugin structure mirrors what Claude Code expects — components at the root level:

```
claude-message/
  .claude-plugin/
    plugin.json              → Plugin manifest (required)
  agents/
    bootstrap.md
    researcher.md
    writer.md
  commands/
    bootstrap.md
    scan.md
    investigate.md
    research.md
    competitor.md
    persona.md
    audit.md
    generate.md
    brief.md
  skills/
    [category]/
      SKILL.md
      [type]/
        [type].md
```

Users install from a marketplace or directly from GitHub:

```bash
# Direct install
claude plugin install https://github.com/fortyfivan/claude-message

# Or via marketplace
claude plugin marketplace add fortyfivan/claude-message
claude plugin install claude-message@fortyfivan
```

When installed as a plugin, only the tools ship — agents, commands, and skills. The data layer (messaging/, insights/, research/, templates) doesn't exist yet. The bootstrap agent creates the directory structure and templates in the user's project when they run `/project:bootstrap`. This is intentional: the tools are generic, the messaging house is specific to each company.

### Marketplace

The repo doubles as its own marketplace by including a `.claude-plugin/marketplace.json`:

```json
{
  "name": "fortyfivan",
  "description": "Messaging intelligence plugins for Claude Code",
  "owner": {
    "name": "Ivan Dwyer",
    "url": "https://github.com/fortyfivan"
  },
  "plugins": [
    {
      "name": "claude-message",
      "path": ".",
      "description": "Messaging intelligence system — agents, commands, and skills for building and maintaining company messaging"
    }
  ]
}
```

This is a single-plugin marketplace for now. If the project grows to include multiple plugins (e.g., a separate research-only plugin, a skills-only pack), they'd be added as entries here.

### Structural Compatibility

The repo needs to work in both modes from the same directory structure. The key is that Claude Code reads `.claude/` for native project mode (fork) and reads the plugin root for installed mode. The solution:

- **Fork mode:** `.claude/agents/`, `.claude/commands/`, `.claude/skills/` are read natively by Claude Code when the repo is the working directory.
- **Plugin mode:** `agents/`, `commands/`, `skills/` at the repo root are read by the plugin system when installed into another project.

These can be the same files. Either the root-level directories are symlinks to `.claude/` contents, or the `.claude/` directory contains the canonical files and the root-level directories are copies maintained by a simple build step. The simplest approach: keep the canonical files at the root level (`agents/`, `commands/`, `skills/`) so they satisfy the plugin structure, and use a `.claude/settings.json` to point Claude Code at them for fork mode.

Alternatively, if Claude Code's plugin detection is smart enough to read `.claude/` components from within a plugin directory, symlinks or dual directories aren't needed. This should be tested during implementation.

---

## Deliverables

- Three agent definitions: bootstrap, researcher, writer.
- Nine command templates: bootstrap, scan, investigate, research, competitor, persona, audit, generate, brief.
- Document templates in `messaging/_templates/` for all six pillars and six collection types.
- Six consolidated pillar files replacing the current ten.
- Skills migrated to category/type routing structure.
- `research/` directory for uploaded and agent-generated research.
- `insights/` directory with tracker.md, config.md, and empty scans/ and investigations/ subdirectories.
- Cron-compatible scan command via `claude -p "/project:scan" --print`.
- Insight lifecycle tracking with auto-resolution detection.
- Coverage gaps reporting for unconfigured MCP sources.
- Bootstrap progress tracking via `messaging/.bootstrap-progress.md`.
- `.claude-plugin/plugin.json` manifest for plugin installation.
- `.claude-plugin/marketplace.json` for marketplace distribution.
- Plugin-compatible directory structure (agents/, commands/, skills/ at root).
- Updated CLAUDE.md for plugin user experience.
- Updated .gitignore for `output/`.

## Out of Scope

- Web UI and Express server (separate PRD).
- MCP server implementation (separate PRD).
- External MCP server implementations (third-party).
- Authentication or multi-user access controls.
- Hosted marketplace infrastructure (the repo is its own marketplace via GitHub).