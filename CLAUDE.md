# CLAUDE.md

The operating guide for AI tools working in this repository.

## About claude-message

`claude-message` is a Claude-native messaging system for marketing teams. The messaging house in `messaging/` is the single source of truth — agents read it for context, write to it with explicit user approval, and generate every asset from it. 

## Always-On Foundation

`MESSAGE.md` loads automatically at session start as foundational context. It provides:

- Company attributes (altitude-setters)
- ICP definition (characteristics, behaviors, environmental)
- Glossary (cross-cutting terminology)
- Brand Guardrails (absolute constraints)
- Scenarios vocabulary (dimensions for runtime assembly)
- The catalog of pillars, collections, and assets

If MESSAGE.md is missing, malformed, or non-conformant to the format spec, prompt the user to run `/bootstrap` (for empty repos) or `/run health` (to diagnose). Do not proceed with content production tasks until MESSAGE.md is present and valid.

## Progressive Loading

After MESSAGE.md, the agent loads additional content based on task context. The catalog tables in MESSAGE.md declare what's available and the load conditions for each.

**Two steps before any task-specific load:**

1. **Infer the scenario** from the Scenarios dimensions in MESSAGE.md, the task, and current context (insights, recent messaging house activity, explicit signals in the request).
2. **Assemble the context** by loading pillars, collections, and assets per the rules below. Apply the inferred content lens to set posture; let the Strategic shape guide which collections and pillars to emphasize.

**Default loading behavior:**

- **Pillars** load per the catalog's `Load When` column. Profile and Pitch load always. Position, People, and Proof load by default for marketing content. Portfolio loads when content references products.
- **Collections** load per the catalog's `Load When` column. Each collection loads when content references its specific entity type (personas when a named role/tier appears, competitors when a named competitor appears, etc.).
- **Assets** load when a specific asset is referenced by content type. Variants under the asset's `variants/` directory load when a specific variant is named.

Skills may override these defaults with their own context-loading rules (build-campaign / build-launch / build-play / build-event each carry a Context Loading table). Skill-specific overrides take precedence.

**Reference patterns** (typical task footprints):

| Pattern | Pillars typically loaded | Collections via routing |
|---|---|---|
| Persona-targeted content (email, LP, persona-specific messaging) | Profile + Pitch + People | persona; matching Stories filtered on persona+product |
| Competitive content (battlecard, comparison, displacement) | Profile + Position + Pitch | competitor; relevant Products; supporting Reports |
| Build orchestration (campaign / launch / play multi-asset brief) | Per the workflow's Context Loading table | personas / products / competitors from intake; assets from MESSAGE.md `## Assets` |
| Composing a new collection | Profile + parent pillar | template from `templates/collections/`; existing file if updating |
| System audit / health check | All 6 pillars (frontmatter + Messaging Rules) | frontmatter-only of every collection |

A typical content production task loads MESSAGE.md plus 3–7 additional files. Avoid "load everything to be thorough" patterns.

## File Path Conventions

Resources resolve to predictable paths. Skills reference content by name ("the position pillar," "the CISO persona," "the blog-post asset"); the agent resolves the path from these conventions.

| Resource | Path |
|---|---|
| Always-on foundation | `MESSAGE.md` |
| Pillars | `messaging/pillars/[slug].md` |
| Collection items | `messaging/collections/[type]/[slug].md` |
| Assets | `messaging/assets/[slug]/asset.md` |
| Skills | `.claude/skills/[category]/[name]/SKILL.md` |
| Subagents | `.claude/agents/[name].md` |
| Commands | `.claude/commands/[name].md` |
| Generated output | `output/[workflow]/[name]/` |
| Investigation state | `insights/` |
| Brand foundation | `brand/DESIGN.md` |

Brand foundation loads inside the producer subagent at dispatch time; never in the main session.

### Input directory priority

The `input/` directory has five subdirectories scanned in priority order:

| Subdirectory | Content | Priority |
|---|---|---|
| `input/messaging/` | Brand guides, positioning decks, messaging frameworks | Highest |
| `input/docs/` | PRDs, release notes, specs, pricing sheets | High |
| `input/research/` | Market research, analyst reports, competitive intel | Medium |
| `input/transcripts/` | Sales calls, customer interviews, feedback logs | Medium |
| `input/examples/` | Content references, competitor samples | Lowest |

## Workflow Recognition

When a user describes intent that matches an available workflow, invoke the workflow directly rather than waiting for an explicit slash command. Each workflow's frontmatter `description` field documents when to use it; match user intent to the most fitting workflow. Slash commands (`/build`, `/design`, `/run`, `/search`, `/generate`, `/review`) remain available for users who prefer explicit invocation.

### Intent Table

When the user's request matches one of these intents, read the named skill and follow its protocol.

| Intent (trigger phrasings) | Skill |
|---|---|
| "bootstrap the messaging system," "start from scratch," "set up messaging" | `.claude/skills/system/bootstrap/SKILL.md` |
| "clone a brand from a website," "build brand/ from our site," "extract design tokens from [url]," "set up the brand folder from our homepage" | `.claude/skills/system/clone/SKILL.md` |
| "build a campaign," "plan an outbound campaign," "ABM campaign for..." | `.claude/skills/workflows/build-campaign/SKILL.md` |
| "launch our product," "orchestrate a launch," "prep the launch BoM" | `.claude/skills/workflows/build-launch/SKILL.md` |
| "build a play," "competitive displacement play," "expansion play for..." | `.claude/skills/workflows/build-play/SKILL.md` |
| "build an event," "plan our conference program," "plan an event around...," "RSA program," "user summit content" | `.claude/skills/workflows/build-event/SKILL.md` |
| "update the glossary," "edit MESSAGE.md," "add a brand guardrail," "update the ICP" | `.claude/skills/workflows/design-message/SKILL.md` |
| "create a persona," "design a competitor profile," "update the position pillar" | `.claude/skills/workflows/design-collection/SKILL.md` (collection types) or `.claude/skills/workflows/design-pillar/SKILL.md` (pillars) |
| "create a new asset," "define a thought-leadership blog asset," "add a webinar asset" | `.claude/skills/workflows/design-asset/SKILL.md` |
| "remove a persona," "delete this asset," "retire the X competitor" | `.claude/skills/workflows/design-collection/` (with `--remove`) or `.claude/skills/workflows/design-asset/` (with `--remove`) |
| "investigate X," "what's changing in the market," "process this feedback," "research [competitor]" | `.claude/skills/system/run-investigation/SKILL.md` |
| "find content about X," "what do we have on Y," "search the messaging house" | `.claude/skills/system/search/SKILL.md` |
| "generate a blog post," "write me an outbound email," "produce a one-pager" | `.claude/agents/writer.md` (standalone mode via the writer subagent) |
| "review this draft," "evaluate this asset," "check this against our messaging" | `.claude/skills/craft/review/SKILL.md` |
| "check system health," "audit the messaging house," "what's drifted" | `.claude/skills/system/run-health/SKILL.md` |
| "produce HTML from this asset," "render the campaign for web," "make this print-ready" | `.claude/agents/producer.md` |

If multiple workflows could apply, ask one clarifying question. If no workflow fits, proceed conversationally.

### Direct queries

Some natural-language patterns don't need a workflow — answer them directly from the messaging house. No skill invocation required.

| Pattern | Source |
|---|---|
| "What's our position on [topic]?" | the position pillar, relevant category profiles |
| "Show me our personas" | the people pillar Collection Tables + persona files |
| "Pull up the [customer] story" | the matching story collection |
| "What's our canonical term for [concept]?" | `MESSAGE.md` `## Glossary` |
| "What stage / market / position is the company?" | `MESSAGE.md` `## Attributes` |
| "Who is the ICP?" | `MESSAGE.md` `## ICP` |
| "What are the brand guardrails?" | `MESSAGE.md` `## Brand Guardrails` |
| "What products do we sell?" | the portfolio pillar Collection Tables + product files |
| "How do we win against [competitor]?" | the matching competitor collection |
| "What's our blog post asset definition?" | the blog-post asset envelope |
| "What proof do we have for [claim]?" | the proof pillar + matching stories/reports |

## Search Pattern

When the agent needs to find content in the messaging house matching a natural-language query, invoke the `search` skill (via `/search` or skill dispatch). The skill knows the messaging house structure and navigates intelligently.

Do not implement ad-hoc search logic in other skills. Do not load all pillars and collections to "find" something — let `search` handle navigation. The search skill is the canonical query layer for both human users and workflow consumers.

Examples:

- `/search "what's our position on AI surveillance?"`
- `/search "proof points relevant to CISO conversations" --scope collections`
- Workflow dispatch: `search query="proof for enterprise security buyers" scope=["collections"]`

## Custom Skills

Users may add custom skills beyond the baseline shipped with claude-message. Custom skills live in the same directory structure as baseline skills:

- Custom system skills: `.claude/skills/system/[name]/SKILL.md`
- Custom workflow skills: `.claude/skills/workflows/[name]/SKILL.md`
- Custom task skills: `.claude/skills/tasks/[name]/SKILL.md`
- Custom craft skills: `.claude/skills/craft/[name]/SKILL.md`

Custom skills that operate against the messaging system include the Messaging System Reference blurb (see below). Skills that omit the blurb (or set `system-independent: true` in frontmatter) signal independence from the messaging architecture. The agent discovers all available skills through filesystem walk at session start — no manifest required.

## Rules

Two hard rules that bind every action.

1. **Protect the source of truth.** Never write to `messaging/` or `MESSAGE.md` without explicit user approval. The `/design` skills (message, pillar, collection, asset) and bootstrap have user-approval gates built in; honor them.
2. **Read before writing.** Check related messaging docs before drafting to maintain consistency. Adapt language depth to the target persona's altitude.

## Agents

Three subagents live at `.claude/agents/`. Each carries its own protocol — read the file before dispatching.
