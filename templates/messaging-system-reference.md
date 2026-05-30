# Messaging System Reference (canonical blurb)

This file is the single source of truth for the **Messaging System Reference** blurb that every skill operating against the messaging system carries. Paste the blurb verbatim — paraphrasing breaks CI's grep-based presence check and weakens the conformance signal.

## Placement

Insert the blurb in a `SKILL.md` (or agent file) directly after the frontmatter and the skill's brief one-paragraph description, before any behavior documentation. The exact heading is `## Messaging System Reference` — keep it consistent across files.

## Canonical text (verbatim)

```markdown
## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.
```

## When to omit

A skill that genuinely operates independently of the messaging system can omit the blurb. Mark such skills with `system-independent: true` in frontmatter so CI's blurb-presence check skips them. This is rare — most skills in `.claude/skills/` (including all baseline skills) reference messaging content and should carry the blurb.
