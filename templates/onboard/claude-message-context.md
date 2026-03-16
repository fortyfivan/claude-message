## Claude Message Plugin

Claude Message is a synamic messaging system that builds a single source of truth for your company's positioning, then generates on-strategy content from it using skills. Agents read the messaging house for context, write to it with your approval, and produce content grounded in what the company actually claims.

### Writing Profile

<!-- claude-message:profile:start -->
Run `/claude-message:bootstrap` to generate your writing profile from the messaging house.
<!-- claude-message:profile:end -->

### How It Works

**Messaging house** — Six pillar docs in `messaging/` that build on each other: Profile (who we are) -> Space (where we compete) -> Audience (who we sell to) -> Portfolio (what we sell) -> Proof (evidence it works) -> Motion (how we go to market). Collection profiles (personas, products, competitors, segments, etc.) add detail under each pillar.

**Skills** — Content generation instructions in `.claude/skills/`. Each skill defines an output format, guidelines, and evaluation criteria for a content type (blog post, email sequence, battlecard, etc.). Skills work out of the box; the tune command personalizes them to your messaging house.

**Workflows** — Bootstrap builds the messaging house from existing materials or Q&A. Compose creates and updates individual messaging docs. Generate produces content by resolving the right messaging docs + skill for the task. Investigate monitors for external changes that may affect your messaging.

### Commands

| Command | Purpose |
|---|---|
| `onboard` | Scaffold workspace |
| `bootstrap` | Build messaging system from scratch |
| `compose [type] [name]` | Create or update a messaging document |
| `generate [skill] [topic]` | Generate content from the messaging house |
| `produce [type] [file]` | Produce a finished deliverable |
| `produce --campaign [name]` | Produce all campaign deliverables |
| `investigate [focus]` | Run a messaging intelligence investigation |
| `campaign [type] [topic]` | Build a multi-asset content campaign |
| `tune` | Calibrate skills to the messaging house |
| `health` | Validate messaging system health |
| `feedback [input]` | Process feedback into messaging changes |
| `feedback --log [input]` | Log observation without proposing changes |

### Workspace

**Source of truth:** `messaging/` — the messaging house. Six pillar docs at the root, collection profiles in subdirectories.

**Content generation:** `.claude/skills/` — skill definitions for each content type. `output/` — where generated content lands. `output/production/` — finished deliverables (PDF, slides, designed documents).

**Production:** `messaging/brand.yml` — design tokens (colors, fonts, logos). `templates/content-schemas/` — structured contracts between writer and producer. `templates/assets/` — HTML asset templates for deliverables.

**Research & insights:** `input/` — source materials for bootstrap. `research/` — agent-generated research. `insights/` — investigation findings and scan digests.

**Reference:** `templates/` — messaging doc schemas, content schemas, and asset templates. Do not modify.

### Key Conventions

- The messaging house is the single source of truth. Read relevant docs before responding to any messaging or content request.
- Ask for confirmation before writing to `messaging/`.
- Always load `profile.md`, `space.md`, and `glossary.md` for context. Conditionally load other pillars and collection profiles based on the task.
- Ground every claim in generated content to a loaded messaging doc. If you can't ground it, don't write it.