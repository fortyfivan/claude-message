# CLAUDE.md

## About Claude Message

Claude Message is a dynamic messaging system for Claude Code. It provides the harness that helps product marketers build, maintain, and operationalize their positioning and messaging across the entire GTM lifecycle. The messaging house in `messaging/` is the single source of truth — agents read it for context, write to it with user approval, and generate content from it. Users run `/bootstrap` to build the messaging system from scratch.

Messaging architecture, frontmatter contracts, glossary, progressive loading guidance, and the writing profile block live in `/MESSAGE.md`. Visual identity (brand tokens, colors, typography, logos) lives in `/DESIGN.md`. Read both before any messaging or content work.

## Project Layout

| Directory | Purpose |
|---|---|
| `MESSAGE.md` | The messaging design system — architecture, contracts, loading rules, writing profile |
| `DESIGN.md` | The visual identity — brand tokens, colors, typography, logo rules |
| `messaging/` | The messaging house — pillar files, collection profiles, schemas, journal |
| `templates/` | Deliverable schemas and artifact templates (read-only) |
| `.claude/agents/` | Subagent definitions (writer, researcher, reader) |
| `.claude/skills/` | Workflow, task, craft, and system skills |
| `.claude/commands/` | Slash command entrypoints |
| `input/` | User-provided source materials organized by type (see below) |
| `insights/` | Insight tracker, config, and findings |
| `artifacts/` | Living artifacts — versioned, maintained markdown content with manifests and changelogs |
| `output/` | Generated content for downstream rendering |

### Input Directory

The `input/` directory has five subdirectories scanned in priority order:

| Subdirectory | Content | Priority |
|---|---|---|
| `input/messaging/` | Brand guides, positioning decks, messaging frameworks | Highest |
| `input/docs/` | PRDs, release notes, specs, pricing sheets | High |
| `input/research/` | Market research, analyst reports, competitive intel | Medium |
| `input/transcripts/` | Sales calls, customer interviews, feedback logs | Medium |
| `input/examples/` | Content references, competitor samples | Lowest |

Files in the `input/` root still work for backward compatibility. Use a workflow tag suffix (`--launch-[name]` or `--campaign-[slug]`) to associate files with specific workflows. See `input/README.md` for the full naming and tagging guide.

**Note:** `input/research/` (user-provided) is distinct from `output/research/` (agent-generated).

## Artifacts

Living artifacts are versioned, continuously maintained content sources (decks, collateral, roadmaps) that must stay current with the messaging house. Each artifact lives in `artifacts/[slug]/` with three files: `manifest.md` (dependencies, structure, triggers), `current.md` (the canonical content), and `changelog.md` (version history). Versioned archives (`v1.0.0.md`, etc.) accumulate as the artifact is updated.

Artifacts hold markdown content only — rendering happens externally (e.g., Claude Design, Claude Artifacts). The `format` field in the manifest is informational metadata about the intended downstream rendering target. Initial content is authored via the campaign or writer workflows. Run `/update [slug]` to detect drift, review proposed changes, and version the result. Run `/update` with no arguments to see all artifacts and their drift status.

## Rules

1. **Ground in the messaging house.** For any messaging or content work, read `/MESSAGE.md` first — it defines the 8P architecture, frontmatter contracts, and progressive loading guidance. The glossary lives in `messaging/glossary.md`; brand tokens in `/DESIGN.md`. Never fabricate positioning, claims, or evidence.
2. **Protect the source of truth.** Never write to `messaging/`, `MESSAGE.md`, or `DESIGN.md` without user approval. Never modify `templates/`.
3. **Load the skill before generating.** Read the relevant `SKILL.md` from `.claude/skills/` for output format, quality signals, and guidelines.
4. **Read before writing.** Check related messaging docs before drafting to maintain consistency. Adapt language depth to the target persona's altitude.
5. **Skills work without tuning.** `/tune` personalizes skills in place with company-specific calibration. Git preserves originals — use `git checkout .claude/skills/` to reset.

## Agents

Three subagents handle execution. Each carries its own detailed instructions in `.claude/agents/`.

- **writer** — Context-resolution engine that determines which messaging docs to load, generates content grounded in them, and dispatches the reader for review.
- **researcher** — Searches external sources and evaluates findings against the messaging system. Works standalone or as a sub-agent of the investigate workflow.
- **reader** — Formal evaluation gate for generated content. Scores against clarity, consistency, relevance, differentiation, actionability, and authenticity.

## Working with Users

When users ask you to work on messaging content:

1. Read `/MESSAGE.md` first, then relevant pillar/collection files based on task context.
2. If the task involves content generation, load the appropriate skill.
3. Present your findings or proposed approach before making changes.
4. Ask clarifying questions when scope, audience, or intent is ambiguous.
5. After making changes, summarize what was modified and why.

Keep questions focused — no more than 5 at a time. Show context before asking.
