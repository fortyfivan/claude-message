# CLAUDE.md

## About Claude Message

Claude Message is a dynamic messaging system for Claude Code. It provides the harness that help product marketers build, maintain, and operationalize their positioning and messaging.

Bootstrap guides users through an interactive seven-phase build of the messaging system. The workspace ships complete — all directories, seed files, skills, and templates are in the repo. Run `/bootstrap` and start building.

The messaging house in `messaging/` is the single source of truth. Agents read it for context, write to it with user approval, and generate content from it. Everything traces back to the messaging house.

## Writing Profile

Generate consistent, clear, and compelling messaging grounded in the company's market position, audience, and differentiation.

<!-- claude-message:profile:start -->
Run `/bootstrap` to generate your writing profile from the messaging house.
<!-- claude-message:profile:end -->

When a writing profile exists between the markers above, use it as the primary context for all messaging work. The profile specifies the company identity, stage, and market — use these to calibrate tone, proof expectations, and positioning decisions.

Read the messaging house before responding to any messaging or content request. Output must be grounded in what the company actually claims, who it actually serves, and how it actually differentiates. Never fabricate positioning, claims, or evidence.

## Project Structure

```
claude-message/
├── .claude/
│   ├── agents/                    <- 4 subagents (writer, researcher, reader, producer)
│   ├── commands/                  <- slash command entrypoints
│   └── skills/
│       ├── workflows/             <- multi-step interactive workflows
│       │   ├── bootstrap/         <- messaging system build
│       │   ├── campaign/          <- multi-asset campaign planning
│       │   ├── launch/            <- product launch orchestration
│       │   ├── compose/           <- messaging doc composition
│       │   └── insights/          <- intelligence, feedback, and health
│       ├── tasks/
│       │   ├── copywriting/       <- assessment, blog, brief, email, enablement, paper, social, story, web
│       │   └── production/        <- datasheets, one-pagers, slides, briefs
│       ├── craft/
│       │   └── voice/             <- universal writing quality gate
│       └── system/
│           └── tune/              <- skill calibration
├── templates/
│   ├── messaging/                 <- doc schemas (read-only)
│   ├── schemas/                   <- content contracts (writer-to-producer)
│   └── assets/                    <- HTML asset templates
├── messaging/                     <- the messaging house (populated by bootstrap)
│   ├── brand.yml                  <- design tokens (colors, fonts, logos)
│   ├── brand/                     <- logo files and brand assets
│   ├── [pillars]                  <- core messaging documents
│   ├── [profiles]                 <- distinct messaging elements
├── input/                         <- user-provided source materials (flat, tagged filenames)
├── research/                      <- agent-generated research
├── insights/                      <- insight tracker, config, findings
│   ├── config.md
│   ├── tracker.md
│   └── findings/
├── output/                        <- generated content
│   ├── assets/                    <- finished deliverables (PDF, slides, etc.)
│   ├── campaigns/                 <- multi-asset campaign outputs
│   ├── plans/                     <- campaign plans
│   ├── research/                  <- agent research reports
│   └── trainings/                 <- enablement outputs
├── .mcp.json                      <- MCP server config
├── CLAUDE.md                      <- project context + writing profile
└── README.md
```

## Messaging House

Six pillar docs at the root of `messaging/` cover every strategic dimension. A glossary provides controlled vocabulary and cross-cutting terminology definitions. Collection subdirectories hold detailed profiles that support the pillars.

Pillars build on each other: Profile (who we are) -> Space (where we compete) -> Audience (who we sell to) -> Portfolio (what we sell) -> Proof (evidence it works) -> Motion (how we go to market).

### File Conventions

Every messaging doc uses YAML frontmatter for structured metadata and markdown body for narrative content.

- Preserve existing frontmatter fields unless explicitly asked to change them.
- Use kebab-case for filenames.
- Follow the schema in `templates/messaging/` when creating new docs.
- Place collection docs in the appropriate subdirectory.
- Messaging docs use a three-section structure: `## Messaging Blocks` contains the content sections; `## Writing Guidelines` defines how the document should be interpreted by agents; `## Messaging Rules` captures company-specific constraints for content generation.
- Follow bracketed guidance in templates (`[Instructions:]`, `[Tips:]`, `[Format:]`) during drafting — these are instructions for populating each section. Do not copy brackets into generated files.
- Pillar docs contain reference tables for their collection profiles. Every table includes a **Description** column — a one-sentence routing signal (~15 words) that enables agents to identify the right profile without loading it. When creating or updating collection profiles, ensure the corresponding pillar table row exists with a Description that differentiates from sibling entries.
- Collection profiles include a `description` field in frontmatter — the same routing signal (~15 words) that appears in the parent pillar's reference table Description column. The frontmatter `description` is canonical; the pillar table Description is a copy. Keep them in sync when creating or updating profiles.
- All messaging docs include an `updated` field in frontmatter (ISO date) tracking the last substantive edit.
- Ask for confirmation before writing changes to existing messaging docs.

## Progressive Loading

Agents use a three-layer loading pattern to minimize unnecessary document reads:

**Foundation pillars.** Always load `profile.md`, `space.md`, `glossary.md`. Conditionally load other pillars based on task type.

**Layer 1 — Pillar tables (discovery).** Scan pillar reference tables. Each row includes a Description column (~15 words) as the primary routing signal. Match task parameters against table columns to build a candidate set.

**Layer 2 — Frontmatter scan (confirmation).** For candidates from Layer 1, read only YAML frontmatter. Use `description`, `type`, `tier`, `status`, `priority`, and relationship fields (`products`, `personas`, `segments`) to confirm relevance before loading full documents. Skip this layer when the task names a specific entity by exact name — go directly to Layer 3.

**Layer 3 — Full body (content).** Load complete documents for confirmed matches. `## Messaging Blocks` contains claims and context. `## Writing Guidelines` contains interpretation rules. `## Messaging Rules` contains constraints.

Pillar tables encode cross-collection relationships (e.g., the story table lists Products, Personas, and Segments). Use these columns to find connections without loading profiles speculatively.

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

**Scan the journal for recent learnings.** Before generating content, check `messaging/journal.md` (if it exists) for entries from the last 30 days related to the target persona, product, or competitor. Recent learnings may affect messaging guidance that hasn't been fully propagated.

**Follow skill definitions.** Load the relevant skill from `.claude/skills/` and use its output format, quality signals, and guidelines.

**One asset per file.** Each content piece gets its own markdown file in `output/` with metadata frontmatter tracking the skill used, parameters resolved, and messaging docs loaded.

**Ground every claim.** Every substantive claim in generated content must trace to a loaded messaging doc. If you can't ground it, don't write it.

**Include self-assessment.** Note grounding confidence, thin context, missing proof, and altitude mismatches. The reader agent handles formal evaluation.

## Directory Permissions

| Directory | Read | Write | Notes |
|---|---|---|---|
| `messaging/` | Yes | With user confirmation | Source of truth. Never write without approval. `messaging/journal.md` can be appended autonomously after approved changes. |
| `messaging/brand.yml` | Yes | With approval | Design tokens for the production system. |
| `templates/` | Yes | No | Messaging doc schemas. Never modify. |
| `templates/schemas/` | Yes | No | Content schemas. Never modify. |
| `templates/assets/` | Yes | No | HTML asset templates. Never modify. |
| `.claude/skills/` | Yes | Tune skill with approval | Content generation skills. Tuned in place by `/tune`. |
| `input/` | Yes | No | User-provided source materials for bootstrap. |
| `research/` | Yes | Yes | Agents can write autonomously. |
| `insights/` | Yes | Yes | Insights skill writes autonomously. |
| `output/` | Yes | Yes | Generated content. Agents write autonomously. |
| `output/assets/` | Yes | Yes | Finished deliverables. Agents write autonomously. |

## Agents

Four subagents handle execution. They are dispatched by workflow skills and the user — they don't own workflows themselves.

### writer

Context-resolution engine for content generation. Its primary job is deciding what to read, not writing. Given a task, it resolves the exact combination of messaging docs required:

1. **Parse** — Extract task parameters: skill type, persona, product, competitor, segment, motion, altitude.
2. **Resolve** — Three-layer loading. Always loads `profile.md`, `space.md`, `glossary.md`. Conditionally loads other pillars. Routes via pillar tables (Layer 1), scans frontmatter to confirm relevance (Layer 2), then loads full profiles for confirmed matches (Layer 3).
3. **Load skill** — Read skill from `.claude/skills/tasks/`. Read the routing `SKILL.md`, then the specific type definition for output format and quality signals.
4. **Cross-reference** — Check loaded context for consistency. Flag gaps or conflicts to the user before writing.
5. **Present brief** — Show resolved context, key messages, proof, and flags for user approval before generating.
6. **Generate** — Draft in memory using claims grounded in loaded docs, language calibrated to the persona's altitude, proof filtered by relevance.
7. **Voice validate** — Scan the draft against the voice gate (banned phrases, structural patterns, diagnostic checklist). PASS/FAIL verdict with max 2 passes.
8. **Self-assess** — Note grounding confidence, thin context, and voice compliance summary.
9. **Write** — Output to `output/` with metadata frontmatter tracking messaging docs loaded and revision history.
10. **Review** — Mandatory reader dispatch with explicit context. Handle verdict: "Ready" → finalize; "Needs revision" → revise and finalize; "Major rework" → escalate to user/orchestrator.
11. **Finalize** — Update revision history, present results (standalone) or return status (campaign).

The agent never dumps the entire messaging house into context. It surgically selects the docs that matter for this task, this audience, this product, this competitor.

### researcher

Research execution agent that searches external sources and evaluates findings against the messaging system. Two modes:

- **Standalone** — Invoked directly for ad-hoc research questions. Writes a research report to `research/`. No tracker, no journal, no insights system.
- **Sub-agent** — Dispatched by the insights workflow skill with scope parameters. Returns structured findings without writing output.

Searches across six domains (competitive, market, audience, proof, technology, GTM & channel signals). Classifies findings by severity and type. Never writes to `messaging/` or `insights/`.

### reader

The single formal evaluation gate for generated content. Reviews assets for quality, clarity, and messaging consistency. Adopts the target persona's perspective and scores against six dimensions: clarity, consistency, relevance, differentiation, actionability, and authenticity. Invoked automatically by the writer agent after generating content.

### producer

Creates finished deliverables from approved content. Reads brand tokens, loads asset templates, discovers available platform skills (PDF, PPTX, frontend-slides, revealjs), and produces the file. Falls back to self-contained HTML when no platform skill is available. Never modifies content — formats and designs only.

## Commands

Commands in `.claude/commands/` are the stable invocation layer. Each command routes to a skill or agent.

| Command | Purpose |
|---|---|
| `/bootstrap` | Build messaging system from scratch |
| `/build campaign [type] [topic]` | Build a multi-asset content campaign |
| `/build launch [name]` | Orchestrate a product launch |
| `/compose [type] [name]` | Compose or update a messaging document |
| `/investigate` | Broad scan across all domains |
| `/investigate [type] [name]` | Targeted investigation of a specific entity |
| `/investigate feedback [input]` | Process feedback into messaging changes |
| `/investigate health` | Validate messaging system health |
| `/investigate health --fix [check]` | Health check + propose and apply fixes |
| `/investigate review` | Tracker dashboard + health summary |
| `/generate [skill] [topic]` | Generate content using a skill |
| `/produce [type] [file]` | Produce a finished deliverable |
| `/review [file]` | Review a content asset |
| `/tune` | Calibrate skills to the messaging house |

## Skills

Skills are organized into four tiers — `workflows`, `tasks`, `craft`, `system` — each serving a distinct role in the system:

```
.claude/skills/
  workflows/                     <- multi-step interactive workflows
    bootstrap/SKILL.md
    campaign/SKILL.md
    launch/SKILL.md
    compose/SKILL.md
    insights/SKILL.md
  tasks/
    copywriting/                 <- content generation by category
      assessment/SKILL.md + types/
      blog/SKILL.md + types/
      brief/SKILL.md + types/
      email/SKILL.md + types/
      enablement/SKILL.md + types/
      paper/SKILL.md + types/
      social/SKILL.md + types/
      story/SKILL.md + types/
      web/SKILL.md + types/
    production/SKILL.md + types/ <- deliverable production
  craft/
    voice/SKILL.md               <- universal writing quality gate
  system/
    tune/SKILL.md                <- skill calibration
```

Skills live in `.claude/skills/` and are auto-loaded by Claude Code. They work without tuning. The `/tune` skill personalizes them in place with company-specific calibration derived from the messaging house. Git preserves the original untuned versions — use `git checkout .claude/skills/` for a full reset.

When generating content, always read the relevant `SKILL.md` first. It contains the output format, quality signals, and context pointers.

**Workflows** are multi-step interactive skills with approval gates. Bootstrap builds the messaging system. Campaign and Launch plan multi-asset content sets. Compose handles on-demand messaging doc creation/updates. Insights consolidates intelligence, feedback, and health into a single workflow.

**Tasks** are content generation skills organized by category, each with a routing `SKILL.md` that dispatches to type-specific definitions in `types/`. The production skill routes to deliverable-specific guides.

**Craft** contains the voice gate (`.claude/skills/craft/voice/SKILL.md`) — writing rules loaded by the writer agent for every content task. It eliminates AI writing patterns (banned phrases, structural anti-patterns, cadence tropes) and enforces clean prose rules. The gate governs writing mechanics — brand voice and terminology remain in the messaging house (`profile.md`, `glossary.md`).

**System** contains the tune skill for calibrating task and craft skills to the messaging house.

## Insights System

The insights workflow skill (`/investigate`) unifies three signal sources into a single tracker:

- **Scan/Target** — External signals from research scans and targeted investigations. Dispatches the researcher agent, processes findings, writes to `insights/findings/`, and manages the tracker lifecycle. Source: `insights:scan`, `insights:targeted`.
- **Health** — Internal system integrity findings across 7 checks (gaps, relationships, schemas, freshness, glossary, profile, journal). Only `critical` and `warning` findings that require human judgment or composition work are tracked. Source: `insights:health`, `insights:fix`.
- **Feedback** — Real-world field signals. Only deferred and log-only signals are tracked (approved changes don't need tracking — docs are already updated). Source: `insights:feedback`.

The tracker in `insights/tracker.md` is the single surface for all actionable findings. Each row includes a Source column (`insights:[mode]`) and a Severity column (`critical | warning | opportunity | info`) to identify origin and priority. Insights are tracked with a lifecycle:

```
open -> acknowledged -> resolved
         |
       deferred
```

Auto-resolution works generically across all sources — when the referenced messaging doc's `updated` date is newer than the insight date, the insight resolves automatically. Users manage judgment calls (acknowledge, defer, resolve) via `/investigate`. The review dashboard groups open insight counts by source mode.

Configure investigation cadence, focus areas, insight source toggles, and MCP sources in `insights/config.md`.

## MCP Integration

External MCP servers provide agents with access to CRM data, call transcripts, analytics, and other signals. Agents reference MCP tools generically — "if CRM data is available, check deal history" — so the system works with any tool stack.

## Input Directory

`input/` is a flat folder for user-provided source materials. Drop files directly — no subdirectories. Use a prefix tag in the filename to signal what the file is and which workflow it supports.

**Common tags:** `prd-`, `deck-`, `brief-`, `battlecard-`, `research-`, `pricing-`, `release-notes-`, `brand-guide-`, `case-study-`, `npi-`

**Examples:** `prd-payments-api.pdf`, `deck-series-b-pitch.pptx`, `brief-q2-campaign.md`

Any format works — PDF, PPTX, MD, DOCX, TXT. Agents read `input/` but never write to it.

## Working with Users

When users ask you to work on messaging content:

1. Read relevant messaging house components for context before drafting.
2. If the task involves content generation, load the appropriate skill.
3. Present your findings or proposed approach before making changes.
4. Ask clarifying questions when scope, audience, or intent is ambiguous.
5. After making changes, summarize what was modified and why.

Keep questions focused — no more than 5 at a time. Show context before asking.
