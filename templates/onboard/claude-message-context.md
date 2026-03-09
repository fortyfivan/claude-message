## Claude Message Plugin

Messaging intelligence system — agents, commands, and skills for building and maintaining company messaging.

### Writing Profile

<!-- claude-message:profile:start -->
Run `/claude-message:bootstrap` to generate your writing profile from the messaging house.
<!-- claude-message:profile:end -->

### Commands

| Command | Purpose |
|---|---|
| `onboard` | Scaffold workspace |
| `bootstrap` | Build messaging system from scratch |
| `generate [skill] [topic]` | Generate content |
| `scan` | Run messaging intelligence scan |
| `investigate [topic]` | Deep-dive on an insight |
| `research [topic]` | Research a topic |
| `competitor [name]` | Profile a competitor |
| `persona [role]` | Draft or update a persona |
| `campaign [type] [topic]` | Build content campaign |
| `brief [topic]` | Generate a creative brief |
| `tune` | Calibrate skills to messaging house |
| `audit` | Audit messaging health |
| `glossary` | Update glossary from messaging house |

### Workspace

- `messaging/` — Source of truth. All messaging docs live here.
- `templates/` — Schemas and skill templates. Do not modify.
- `input/` — Drop existing materials here before running bootstrap.
- `research/` — Agent-generated research.
- `insights/` — Scan digests and investigations.
- `output/` — Generated content.
- `.claude/skills/` — Tuned skills calibrated to the messaging house.

### Key Conventions

- The messaging house (`messaging/`) is the single source of truth for all content generation.
- Ask for confirmation before writing to `messaging/`.
- Read relevant messaging docs before responding to any messaging or content request.
- Use progressive loading: always load profile.md, space.md, glossary.md; conditionally load others.
- See the plugin's CLAUDE.md for full instructions and agent details.
