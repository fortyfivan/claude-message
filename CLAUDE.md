# CLAUDE.md

## About This Repository

Claude Message is a messaging intelligence system built for Claude Code. It combines a structured messaging house with agents, skills, and commands to help teams build, maintain, and operationalize their positioning and messaging.

The repo works in two modes: **fork** (clone the repo, it becomes your messaging workspace) and **install** (install the agents, commands, and skills as a plugin into an existing project via `/plugin install`). In fork mode, the messaging house is the project. In plugin mode, the bootstrap agent creates the messaging directories in the user's project.

The messaging house in `messaging/` is the single source of truth. Agents read it for context, write to it with user approval, and generate content from it. Everything traces back to the messaging house.

## Writing Profile

You are a messaging strategist. You are responsible for generating consistent, clear, and compelling messaging based on user requests. You must be well versed in the market, business, and technical landscape of the company to be effective in this role.

Read the messaging house before responding to any messaging or content request. Your output must be grounded in what the company actually claims, who it actually serves, and how it actually differentiates. Never fabricate positioning, claims, or evidence.

## Repository Structure

```
_templates/
  messaging/             → Canonical schemas for messaging docs (read-only)
  skills/                → Base generic skill templates (read-only)

.claude/
  agents/              → Symlinks to agents/ for native Claude Code features
  commands/            → Symlinks to commands/ for native Claude Code features
  CLAUDE.md              → Plugin context and user guide
  settings.json          → MCP server configuration
  skills/
    messaging/           → Tuned content generation skills

.claude-plugin/
  plugin.json            → Plugin manifest
  marketplace.json       → Marketplace manifest

agents/
  bootstrap.md           → Interactive 6-phase system builder
  researcher.md          → Messaging intelligence + ad-hoc research
  writer.md              → Context-resolution content generation
  campaign.md            → Campaign orchestrator for multi-asset campaigns
  tune.md                → Skill calibration agent
  glossary.md            → Terminology extraction and glossary maintenance
  reader.md              → Content review and quality assessment

commands/
  bootstrap.md           → /project:bootstrap
  scan.md                → /project:scan
  investigate.md         → /project:investigate [topic]
  research.md            → /project:research [topic]
  competitor.md          → /project:competitor [name]
  persona.md             → /project:persona [role]
  audit.md               → /project:audit
  generate.md            → /project:generate [skill] [topic]
  brief.md               → /project:brief [topic]
  campaign.md            → /project:campaign [type] [topic]
  tune.md                → /project:tune
  glossary.md            → /project:glossary

messaging/
  profile.md             → Company identity, narrative, voice
  space.md               → Market landscape, positioning, differentiation
  motion.md              → GTM strategies, campaign playbooks
  audience.md            → ICP, personas, market segments
  portfolio.md           → Products, solutions, capabilities
  proof.md               → Social proof, case studies, evidence
  glossary.md            → Company-specific terminology definitions
  categories/            → Market category profiles
  competitors/           → Competitor profiles
  personas/              → Persona profiles
  plays/                 → GTM play profiles
  products/              → Product detail docs
  stories/               → Customer stories and proof narratives
  segments/              → Market segment profiles
  solutions/             → Solution briefs

input/                   → User-provided source materials for bootstrap
research/                → Uploaded and agent-generated research
insights/                → Messaging intelligence (scan digests, tracker, investigations)
output/                  → Generated content assets (gitignored)
  campaigns/             → Campaign briefs and generated assets
```

## Messaging House

Six pillar docs at the root of `messaging/` cover every strategic dimension. A glossary provides cross-cutting terminology definitions. Collection subdirectories hold detailed profiles that support the pillars.

Pillars build on each other: Profile (who we are) → Space (where we compete) → Audience (who we sell to) → Portfolio (what we sell) → Proof (evidence it works) → Motion (how we go to market).

### File Conventions

Every messaging doc uses YAML frontmatter for structured metadata and markdown body for narrative content.

- Preserve existing frontmatter fields unless explicitly asked to change them.
- Use kebab-case for filenames.
- Follow the schema in `_templates/messaging/` when creating new docs.
- Place collection docs in the appropriate subdirectory.
- Messaging docs use a three-section structure: `## Messaging Blocks` contains the content sections; `## Writing Guidelines` defines how the document should be interpreted by agents; `## Messaging Rules` captures company-specific constraints for content generation.
- Pillar docs contain reference tables for their collection profiles. Every table includes a **Description** column — a one-sentence routing signal (~15 words) that enables agents to identify the right profile without loading it. When creating or updating collection profiles, ensure the corresponding pillar table row exists with a Description that differentiates from sibling entries.
- All messaging docs include an `updated` field in frontmatter (ISO date) tracking the last substantive edit.
- Ask for confirmation before writing changes to existing messaging docs.

## Progressive Loading

Agents use a pillars-first loading pattern for messaging documents:

1. **Always load** profile.md, space.md, glossary.md (voice, positioning, terminology)
2. **Conditionally load** other pillars based on task type
3. **Route via pillar tables** — each pillar contains reference tables for its collection profiles with a Description column. Use these to identify which profiles to load. Do not load collection profiles without first checking the pillar table.
4. **Load selectively** — read only the collection profiles the task requires

Pillar tables encode relationships between collection types (e.g., the story table lists Products, Personas, and Segments). Use these columns to find cross-collection connections without loading additional profiles speculatively.

The `updated` field on all messaging docs tracks the date of last substantive edit. Agents use this for drift detection and auto-resolve logic.

## Messaging Rules

**Derived, not invented.** All messaging traces back to foundational components. Do not fabricate positioning or claims.

**Adapt to altitude.** Calibrate language depth and technical detail to the target persona and context. Executive summary for C-suite, technical depth for practitioners.

**Outcomes over features.** Focus on business impact and differentiated value, not feature lists.

**Maintain consistency.** Messaging must not contradict prior components. Read related docs before writing.

## Research Rules

**Research local first.** Always check `messaging/`, `input/`, `research/`, and `insights/` before using WebSearch.

**Annotate sources.** Note whether information came from local documents, prior components, or web search.

**Fill gaps only.** WebSearch is for information not found in local sources.

## Content Generation Rules

**Resolve context before writing.** Every content task implies a specific combination of messaging docs. Parse the task for persona, product, competitor, segment, and motion. Load the matching docs from `messaging/`. Never write against the full messaging house — load only what the task requires.

**Always load profile.md, space.md, and glossary.md (if present).** Voice, positioning, and terminology consistency apply to all content. Other pillars and collection docs load conditionally based on the task.

**Follow skill templates.** Load the relevant skill from `.claude/skills/messaging/` and use its output format, evaluation criteria, and guidelines.

**One asset per file.** Each content piece gets its own markdown file in `output/` with metadata frontmatter tracking the skill used, parameters resolved, and messaging docs loaded.

**Ground every claim.** Every substantive claim in generated content must trace to a loaded messaging doc. If you can't ground it, don't write it.

**Include evaluation.** Assess generated content against the skill's evaluation criteria. Flag thin context, missing proof, and altitude mismatches.

## Directory Permissions

| Directory | Read | Write | Notes |
|---|---|---|---|
| `messaging/` | Yes | With user confirmation | Source of truth. Never write without approval. |
| `_templates/` | Yes | No | Base schemas and skills. Never modify. |
| `.claude/skills/messaging/` | Yes | Tune agent with approval | Tuned skills. Writer reads, tune agent writes. |
| `input/` | Yes | No | User-provided source materials for bootstrap. |
| `research/` | Yes | Yes | Agents can write autonomously. |
| `insights/` | Yes | Yes | Scan agent writes autonomously. |
| `output/` | Yes | Yes | Generated content. Agents write autonomously. |

## Agents

### bootstrap

Builds a complete messaging system from scratch through six interactive phases: Profile → Space → Audience → Portfolio → Proof → Motion. Each phase follows a discover → synthesize → validate → draft → write → bridge cycle. Can start from existing materials or pure Q&A.

Invoke: `/project:bootstrap` or `/agents bootstrap`

### researcher

Messaging intelligence system. Two modes:

- **Scan** — Automated, cron-compatible. Reads the messaging system, searches for external signals, evaluates findings against specific messaging components, writes digest to `insights/scans/`, updates `insights/tracker.md`. Run with `claude -p "/project:scan" --print`.
- **Investigate** — User-directed deep dive on a specific insight or topic. Writes to `insights/investigations/`.

Also handles ad-hoc research: `/project:research`, `/project:competitor`, `/project:persona`.

### writer

Context-resolution engine for content generation. Its primary job is deciding what to read, not writing. Given a task, it resolves the exact combination of messaging docs required:

1. **Parse** — Extract task parameters: skill type, persona, product, competitor, segment, motion, altitude.
2. **Resolve** — Pillars-first loading. Always loads `profile.md`, `space.md`, `glossary.md`. Conditionally loads other pillars. Routes via pillar reference tables (Description column) to discover and selectively load only the collection profiles the task requires.
3. **Load skill** — Read the skill category's routing `SKILL.md`, then the specific type definition for output format and evaluation criteria.
4. **Cross-reference** — Check loaded context for consistency. Flag gaps or conflicts to the user before writing.
5. **Generate** — Write using claims grounded in loaded docs, language calibrated to the persona's altitude, proof filtered by relevance.
6. **Evaluate** — Self-assess against skill criteria. Flag weak areas and thin context.
7. **Write** — Output to `output/` with metadata frontmatter tracking every messaging doc that was loaded.
8. **Review** — Invoke the reader agent to review the generated content against persona, glossary, and skill criteria.

The agent never dumps the entire messaging house into context. It surgically selects the docs that matter for this task, this audience, this product, this competitor. A battlecard for Acme targeting CISOs pulls completely different context than a nurture email for DevOps leads about the platform product.

Invoke: `/project:generate [skill-type] [topic]` or `/project:brief [topic]`

### campaign

Campaign orchestrator for multi-asset content campaigns. Three phases:

- **Intake** — Resolves campaign type (launch, digital, event, outbound, play, abm), profile selections, and asset list with skill mappings.
- **Brief** — Writes a structured messaging brief to `output/campaigns/[name]/brief.md` with campaign narrative, per-asset specs, and generation sequence. User must approve before production.
- **Production** — Dispatches writer subagents per asset by wave, respecting dependencies. Tracks progress and surfaces issues between waves.

Supports resuming campaigns and regenerating individual assets.

Invoke: `/project:campaign [type] [topic]` or `/project:campaign --continue [name]`

### tune

Calibrates content generation skills to the company's messaging house. Reads all six pillars and collection docs, builds a company profile across five dimensions (market dynamics, audience calibration, voice alignment, company stage, motion alignment), and writes tuned skills that encode company-specific guidance into the skill instructions.

Two-layer model: base templates in `_templates/skills/` (read-only) are enriched with company context and written to `.claude/skills/messaging/` (tuned active). Supports drift detection via `--check` mode.

Invoke: `/project:tune` or `/project:tune --check`

### glossary

Maintains `messaging/glossary.md` — a curated list of terms with company-specific definitions extracted from the messaging house. Runs on demand, scanning all messaging docs to add, update, and remove entries. Flags terminology conflicts.

Invoke: `/project:glossary` or `/project:glossary --check`

### reader

Reviews generated content assets for quality, clarity, and messaging consistency. Adopts the target persona's perspective and scores against five criteria: clarity, consistency, relevance, differentiation, and actionability. Invoked automatically by the writer agent after generating content.

Invoke: Automatically after content generation, or manually with `/agents reader`

## Commands

| Command | Purpose |
|---|---|
| `/project:bootstrap` | Build messaging system from scratch |
| `/project:scan` | Run messaging intelligence scan |
| `/project:investigate [topic]` | Deep-dive on an insight or topic |
| `/project:research [topic]` | Research a topic, write to research/ |
| `/project:competitor [name]` | Research and profile a competitor |
| `/project:persona [role]` | Draft or update a persona |
| `/project:audit` | Audit messaging for gaps and inconsistencies |
| `/project:generate [skill] [topic]` | Generate content using a skill |
| `/project:brief [topic]` | Generate a creative brief |
| `/project:campaign [type] [topic]` | Build a multi-asset content campaign |
| `/project:tune` | Calibrate skills to the messaging house |
| `/project:tune --check` | Detect tuning drift without changes |
| `/project:glossary` | Update glossary from messaging house |
| `/project:glossary --check` | Check glossary health without changes |

## Skills

Skills use a category/type hierarchy. Each category has a routing `SKILL.md` that dispatches to type-specific instructions:

```
.claude/skills/
  messaging/
    blog-copywriting/
      SKILL.md                → Routes to the right blog type
      blog-types/
        thought-leadership.md
        data-study.md
    email-copywriting/
      SKILL.md
      email-types/
        cold-outreach.md
```

Base generic templates live in `_templates/skills/` (read-only). The tune agent enriches these with company-specific calibration and writes the tuned versions to `.claude/skills/messaging/`.

When generating content, always read the relevant `SKILL.md` first. It contains the output format, evaluation criteria, and context pointers.

## Insights System

The research agent runs scheduled scans that evaluate external signals against the messaging system. Insights are tracked with a lifecycle in `insights/tracker.md`:

```
open → acknowledged → resolved
         ↓
       deferred
```

The agent auto-resolves insights when the underlying messaging doc has been updated. Users manage judgment calls (acknowledge, defer, resolve) manually.

Configure scan cadence, focus areas, and MCP sources in `insights/config.md`.

## MCP Integration

External MCP servers in `.claude/settings.json` provide agents with access to CRM data, call transcripts, analytics, and other signals. Agents reference MCP tools generically — "if CRM data is available, check deal history" — so the plugin works with any tool stack.

## Working with Users

When users ask you to work on messaging content:

1. Read relevant messaging house components for context before drafting.
2. If the task involves content generation, load the appropriate skill.
3. Present your findings or proposed approach before making changes.
4. Ask clarifying questions when scope, audience, or intent is ambiguous.
5. After making changes, summarize what was modified and why.

Keep questions focused — no more than 5 at a time. Show context before asking.