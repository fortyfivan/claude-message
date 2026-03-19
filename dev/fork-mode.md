# Convert from Plugin Mode to Fork Mode

## Context

Claude Message is currently distributed as a Claude Code plugin — users install it via marketplace, and a scaffold script (`onboard.sh`) copies templates, skills, agents, and context into their project. This adds indirection, namespace conflicts (`.claude/` owned by both plugin and user), and setup friction.

The workspace IS the product. The messaging house, skills, agents, and templates aren't add-ons to another project — they're the project itself. Fork mode makes this relationship legible: clone the repo, run `/bootstrap`, start building. No plugin layer to discover, no cross-project copying, no namespace conflicts.

Skills live in `.claude/skills/` — one location, no duplication. The tune agent modifies skills in place, replacing the `## Company Calibration` section and its inline enrichments on each run. Git preserves the original base if a full reset is ever needed.

---

## Structural Changes

### Current (Plugin Mode)
```
claude-message/                    ← plugin root (installed via marketplace)
├── .claude-plugin/                ← plugin manifest
├── agents/                        ← discovered by plugin system
├── commands/                      ← discovered by plugin system
├── skills/                        ← base templates, copied to user project
├── templates/
│   ├── messaging/
│   ├── content-schemas/
│   ├── assets/
│   ├── insights/
│   └── onboard/                   ← CLAUDE.md injection template
├── settings.json
├── .mcp.json
├── CLAUDE.md                      ← developer docs
└── README.md
```

User runs onboard.sh → creates messaging workspace in a SEPARATE project.

### Target (Fork Mode)
```
claude-message/                    ← the project (user forks/clones this)
├── .claude/
│   ├── agents/                    ← auto-discovered by Claude Code
│   ├── commands/                  ← auto-discovered by Claude Code
│   └── skills/                    ← auto-loaded by Claude Code, tuned by tune agent
│       ├── messaging/bootstrap/   ← bootstrap SKILL.md (no scripts/)
│       ├── copywriting/
│       ├── enablement/
│       └── production/
├── templates/
│   ├── messaging/                 ← doc schemas
│   ├── content-schemas/           ← writer-to-producer contracts
│   └── assets/                    ← HTML asset templates
├── messaging/                     ← the messaging house (populated by bootstrap)
│   ├── brand.yml                  ← design tokens seed
│   ├── categories/
│   ├── competitors/
│   ├── personas/
│   ├── plays/
│   ├── products/
│   ├── stories/
│   ├── segments/
│   └── solutions/
├── input/                         ← user source materials
├── research/                      ← agent research
├── insights/                      ← insight tracker + findings
│   ├── config.md                  ← scan config seed
│   ├── tracker.md                 ← tracker seed
│   └── findings/
├── output/                        ← generated content
│   ├── assets/                    ← finished deliverables (PDF, slides, etc.)
│   ├── campaigns/                 ← multi-asset campaign outputs
│   ├── plans/                     ← tune plans, campaign plans, etc.
│   ├── research/                  ← agent research reports
│   └── trainings/                 ← future: enablement outputs
├── .mcp.json
├── CLAUDE.md                      ← project context + writing profile markers
└── README.md
```

Everything ships in the repo. No scaffold step. Clone → open → `/bootstrap` → build.

---

## File Operations

### Move (git mv)

| From | To |
|------|-----|
| `agents/*.md` (10 files) | `.claude/agents/*.md` |
| `commands/*.md` (10 files) | `.claude/commands/*.md` |
| `skills/copywriting/` | `.claude/skills/copywriting/` |
| `skills/enablement/` | `.claude/skills/enablement/` |
| `skills/production/` | `.claude/skills/production/` |
| `skills/messaging/bootstrap/` | `.claude/skills/messaging/bootstrap/` |

### Delete

| File/Directory | Reason |
|---------------|--------|
| `.claude-plugin/plugin.json` | Plugin manifest — not needed |
| `.claude-plugin/marketplace.json` | Marketplace catalog — not needed |
| `.claude-plugin/` | Empty directory |
| `settings.json` | Plugin settings placeholder (empty) |
| `templates/onboard/claude-message-context.md` | CLAUDE.md injection template — content lives in CLAUDE.md directly |
| `templates/onboard/` | Empty directory |
| `templates/insights/` | Seed files move to `insights/` directly |
| `templates/brand.yml` | Seed file moves to `messaging/brand.yml` directly |
| `skills/` | Entire directory — all skills move to `.claude/skills/` |
| `skills/messaging/bootstrap/scripts/` | onboard.sh deleted — no scaffold needed |

### Create

Ship the complete workspace directory structure in the repo. Each empty directory gets a `.gitkeep` so git tracks it:

| Path | Contents |
|------|----------|
| `messaging/` | `brand.yml` (moved from `templates/brand.yml`) |
| `messaging/categories/` | `.gitkeep` |
| `messaging/competitors/` | `.gitkeep` |
| `messaging/personas/` | `.gitkeep` |
| `messaging/plays/` | `.gitkeep` |
| `messaging/products/` | `.gitkeep` |
| `messaging/stories/` | `.gitkeep` |
| `messaging/segments/` | `.gitkeep` |
| `messaging/solutions/` | `.gitkeep` |
| `input/` | `.gitkeep` |
| `research/` | `.gitkeep` |
| `insights/` | `config.md`, `tracker.md` (moved from `templates/insights/`) |
| `insights/findings/` | `.gitkeep` |
| `output/` | `.gitkeep` |
| `output/assets/` | `.gitkeep` |
| `output/campaigns/` | `.gitkeep` |
| `output/plans/` | `.gitkeep` |
| `output/research/` | `.gitkeep` |
| `output/trainings/` | `.gitkeep` |

---

## File Modifications

### `CLAUDE.md`

Major rewrite. Key changes:

1. **"About This Plugin" → "About Claude Message"** — Remove all "plugin" language. Frame as a project you fork/clone.

2. **Add Writing Profile markers** — The profile section currently describes how to use a profile. Add the actual `<!-- claude-message:profile:start -->` and `<!-- claude-message:profile:end -->` markers here so bootstrap writes the profile directly into this file.

3. **Update structure diagram** — Show single unified structure:
   - `.claude/agents/`, `.claude/commands/`, `.claude/skills/`
   - `templates/` (doc schemas, content schemas, asset templates)
   - `messaging/` and workspace directories (shipped empty, populated by bootstrap)
   - No "plugin root" vs "user project" separation

4. **Remove plugin references throughout:**
   - "plugin root" → not needed
   - "auto-discovered by plugin system" → "auto-discovered by Claude Code"
   - "copied from plugin" → reference where things actually are
   - "The plugin provides the tools" → adjust language
   - Remove `.plugin-root` references

5. **Update Skills section** — Single location: `.claude/skills/`. Auto-loaded by Claude Code, tuned in place by the tune agent. Git preserves the original base.

6. **Update Directory Permissions** — Remove `.claude/skills/` tune agent note about "auto-loaded from plugin". Update `output/production/` → `output/assets/`.

7. **Merge useful content from onboard context template** — The command table and workspace description from `templates/onboard/claude-message-context.md` are useful for users. Integrate where appropriate.

8. **Update bootstrap command description** — No plugin namespace prefix.

9. **Remove `messaging/brand/` from structure** — `brand.yml` is sufficient, no separate brand directory.

10. **Update output directory structure** — Replace `output/production/` and `output/tune/` with `output/assets/`, `output/campaigns/`, `output/plans/`, `output/research/`, `output/trainings/`.

### `.claude/skills/messaging/bootstrap/SKILL.md`

1. **Remove Scaffold Workspace section entirely** — No onboard script, no plugin root resolution, no directory creation. The workspace ships complete.

2. **Simplify Setup** — With no scaffold step, Setup becomes:
   - Input Materials
   - Profile Context
   - Company Basics

   The opening message should note: "The workspace is ready. We'll start by reading any input materials, then I'll ask a few questions before we begin."

3. **Remove `[skill-dir]` and `[plugin-root]` resolution** — No script to call, no paths to resolve.

4. **Remove `scripts/` directory reference** — The `scripts/onboard.sh` file is deleted. Remove the `scripts/` subdirectory from the bootstrap skill.

5. **Completion → Write Profile Block** — Keep as-is but simplify: write between the `<!-- claude-message:profile -->` markers in the project root's CLAUDE.md.

### `.claude/agents/tune.md`

Adapt to in-place tuning with no separate base directory:

1. **Opening paragraph and "How You Work"** — Remove references to "base templates from the plugin" and "original base templates from the plugin's `skills/` directory." Replace with: skills live in `.claude/skills/`, tune modifies them in place. The `## Company Calibration` section is always replaced wholesale. Inline enrichments are re-derived from the current messaging house on each run. Git preserves the original untuned versions.

2. **Step 2** — Remove plugin root discovery entirely:
   - Remove: "Read `.claude/.plugin-root` to locate the plugin directory. Read base templates from `$PLUGIN_ROOT/skills/`."
   - Remove fallback logic about missing `.plugin-root`
   - Replace with: "Read current skills from `.claude/skills/`." For each skill, assess tuning state via `tuned: true` in frontmatter.
   - Remove manual edit detection by comparing against a separate base (no base exists). Instead, note if `tuned: true` is present from a previous run.

3. **Step 7** — Update write flow:
   - Remove: "Read the base template from `$PLUGIN_ROOT/skills/`"
   - Replace with: "Read the current skill file from `.claude/skills/`. Strip the existing `## Company Calibration` section if present. Apply approved inline enrichments. Append the new `## Company Calibration` section."

4. **Step 8** — Remove `$PLUGIN_ROOT` references for recommended skills. New skills are written directly to `.claude/skills/`.

5. **Manual Edit Detection section** — Remove comparison against plugin base. Instead, detect manual edits by checking if the file has been modified since `tuned_date` (via git or file metadata). Simplify: warn the user that re-tuning will overwrite any manual changes to tuned sections.

6. **Tool Scoping** — Remove `$PLUGIN_ROOT/skills/` and `.claude/.plugin-root` from read paths. Read scope is `messaging/`, `.claude/skills/`, `output/plans/`.

7. **Output paths** — `output/tune/tune-plan-YYYY-MM-DD.md` → `output/plans/tune-plan-YYYY-MM-DD.md`.

### `.claude/agents/producer.md`

Update output paths: `output/production/` → `output/assets/`. Also update campaign production path: `output/campaigns/[name]/production/` → `output/campaigns/[name]/assets/`.

### `.claude/commands/tune.md`

Update path: `output/tune/tune-plan-YYYY-MM-DD.md` → `output/plans/tune-plan-YYYY-MM-DD.md`.

### `.claude/skills/production/SKILL.md`

Update output path: `output/production/` → `output/assets/`.

### `README.md`

Rewrite Getting Started:

```markdown
## Getting Started

Fork or clone the repository:

```bash
git clone https://github.com/fortyfivan/claude-message.git my-company-messaging
cd my-company-messaging
```

Open in Claude Code and build your messaging system:

```
> /bootstrap
```
```

- Remove plugin install commands
- Remove `/claude-message:` namespace prefix from commands
- Update command references throughout
- Add a section on pulling upstream updates
- Update version history

### `.gitignore`

Keep minimal — just OS artifacts and dev scratch:

```
.DS_Store
dev/*
```

Workspace directories ship in the repo and are tracked. Users manage their own versioning strategy.

---

## Files NOT Changed

These files need no modifications — they already reference project-relative paths:

- Agent files: `composer.md`, `investigate.md`, `researcher.md`, `writer.md`, `campaign.md`, `feedback.md`, `health.md`, `reader.md`
- Command files: `bootstrap.md`, `compose.md`, `generate.md`, `investigate.md`, `insights.md`, `health.md`, `feedback.md`, `campaign.md`, `produce.md`
- All template files in `templates/messaging/`, `templates/content-schemas/`, `templates/assets/`
- `.mcp.json` — empty config, stays at root

---

## Key Design Decisions

### Single skills directory

All skills live in `.claude/skills/`. No duplication. The tune agent modifies skills in place — it strips the existing `## Company Calibration` section and inline enrichments, re-derives them from the current messaging house, and writes them back. Git preserves the original untuned versions for reverting if needed (`git checkout .claude/skills/`).

### No onboard script

The workspace ships complete. Every directory and seed file is in the repo. Bootstrap just starts the 6-phase build. No scaffold, no script, no copying.

### Versioning user content

The repo ships with empty workspace directories (messaging/, input/, research/, insights/, output/) tracked via `.gitkeep`. Users decide whether to version their messaging house. The `.gitignore` does NOT exclude these directories — they're part of the project. If users fork and want to keep the upstream clean, they manage that via their own branching strategy.

### No CLAUDE.md injection

In plugin mode, onboard.sh injected context into the user's separate project CLAUDE.md. In fork mode, the CLAUDE.md IS the project context — no injection needed. The writing profile markers live directly in CLAUDE.md.

### Output directory restructure

`output/` subdirectories organized by content type rather than agent:
- `assets/` — finished deliverables (replaces `production/`)
- `campaigns/` — multi-asset campaign outputs
- `plans/` — tune plans, campaign plans, and other planning docs (replaces `tune/`)
- `research/` — agent research reports
- `trainings/` — future: enablement and training outputs

---

## Verification

1. Run `ls .claude/agents/` — confirm 10 agent files
2. Run `ls .claude/commands/` — confirm 10 command files
3. Run `ls .claude/skills/` — confirm copywriting/, enablement/, production/, messaging/ directories
4. Confirm no `skills/` directory at root (moved to `.claude/skills/`)
5. Confirm no `.claude-plugin/` directory exists
6. Confirm no `settings.json` at root
7. Confirm no `templates/onboard/` directory
8. Confirm no `templates/insights/` directory (seeds moved to `insights/`)
9. Confirm no `agents/` or `commands/` at root (moved to `.claude/`)
10. Confirm no `onboard.sh` anywhere in the repo
11. Confirm `messaging/`, `input/`, `research/`, `insights/`, `output/` directories exist with `.gitkeep` files
12. Confirm `insights/config.md` and `insights/tracker.md` exist
13. Confirm `messaging/brand.yml` exists
14. Grep for "plugin-root" — should return zero results
15. Grep for "PLUGIN_ROOT" — should return zero results
16. Grep for "onboard" — should return zero results (except possibly git history or README context)
17. Read `CLAUDE.md` — confirm `<!-- claude-message:profile:start -->` markers present, no "plugin" language
18. Read `.claude/skills/messaging/bootstrap/SKILL.md` — confirm no scaffold/onboard step
19. Read `.claude/agents/tune.md` — confirm no `$PLUGIN_ROOT` or `.plugin-root` references
