Create, update, or remove any messaging system artifact — MESSAGE.md sections, pillars, collection items, and assets. Template-driven; the skill detects file existence and the `--remove` flag to branch between create / update / remove.

Usage:
  /design message [section]                      — Update a section of MESSAGE.md (attributes, facts, icp, glossary, brand-guardrails, scenarios)
  /design pillar [name]                          — Update an existing pillar (update-only; pillars are structural)
  /design [collection-type] [name]               — Create, update, or remove a collection item (persona, competitor, segment, solution, story, category, product, report)
  /design asset [slug]                           — Create, update, or remove an asset definition (with paired writing type)

Flags:
  --remove                                       — Remove the artifact (cross-reference cleanup + forced approval; pillars and MESSAGE.md sections refuse)
  --research                                     — Drive composition from web research via `craft/research/` patterns

Subcommand → skill routing:
- `message` → `.claude/skills/messaging/design-message/SKILL.md` (update-only; MESSAGE.md sections are foundational)
- `pillar` → `.claude/skills/messaging/design-pillar/SKILL.md` (update only)
- `[collection-type]` → `.claude/skills/messaging/design-collection/SKILL.md`
- `asset` → `.claude/skills/messaging/design-asset/SKILL.md`

Examples:
  /design message glossary
  /design message brand-guardrails
  /design persona security-executives
  /design competitor acme-corp --research
  /design asset blog-post
  /design persona old-persona --remove
  /design pillar position

Read and follow the instructions in the matching skill. Pass all remaining arguments and flags.
