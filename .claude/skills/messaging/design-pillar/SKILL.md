---
name: design-pillar
description: Update an existing pillar (Profile, Pitch, Position, People, Portfolio, Proof). Pillars are structural — they can't be created (bootstrap scaffolds them) or removed (they're foundational). Update-only behavior with downstream impact analysis.
---

# Design Pillar

Update behavior only. Pillars are required structural elements; create and remove operations are refused with clear redirects.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona"). If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

Invoked via `/design pillar [name]`. The skill loads the existing pillar, runs a focused update interview, generates the revised content, shows a diff, enumerates downstream impact, and writes after approval.

## Modes

| Invocation | Behavior |
|---|---|
| `/design pillar [name]` | Update flow. Loads existing → interview → generate → diff → impact → approve → write. |
| `/design pillar [name] --remove` | **Refused.** "Pillars are structural and cannot be removed. Edit the pillar to change content, or remove the value of specific sections within the file." |
| `/design pillar [name]` for missing pillar | **Refused.** "Pillar `[name]` doesn't exist. The six pillars (profile, pitch, position, people, portfolio, proof) are pre-scaffolded by bootstrap. Run `/bootstrap` if the messaging house is empty." |

## Update flow

### Step 1: Detect

Check the pillar exists. If not, refuse (see above). The valid `[name]` values are: `profile`, `pitch`, `position`, `people`, `portfolio`, `proof`. Any other value is refused.

### Step 2: Load current content

Read the existing pillar file. Present the three required sections (Messaging Blocks, Collection Tables where applicable, Writing Guidelines) so the user can see what's currently there before deciding what to change.

### Step 3: Update interview

Focused — "What do you want to change?" Not the full bootstrap-style interview. Probe for:
- Which section(s) need revision (Messaging Blocks, Writing Guidelines; Collection Tables generally update via `/design [collection-type]`, not here)
- What specifically (a paragraph, a rule, a sub-section)
- Whether the change is additive (adding a new claim, voice attribute, rule) or replacement (rewording, retiring)
- Whether the change is driven by recent feedback or research — if yes, accept `--research` to dispatch the researcher subagent before regeneration

Use AskUserQuestion when the change scope is ambiguous. Do not re-interview the user on content that isn't changing.

#### Boundary soft-prompt

If the user describes content that belongs in `MESSAGE.md` rather than a pillar, surface a soft prompt before proceeding. The boundaries:

| Content the user describes | Belongs in | Soft prompt |
|---|---|---|
| Cross-cutting glossary terms (capitalization, abbreviations, prohibited terms, replacements) | MESSAGE.md Glossary | "That looks like glossary content. The canonical Glossary lives in `MESSAGE.md`. Want to add it there with `/design message glossary` instead?" |
| Absolute, testable output rules ("never use X," "always capitalize Y") | MESSAGE.md Brand Guardrails | "That sounds like a brand guardrail — an absolute output constraint. Those live in `MESSAGE.md`. Want to add it with `/design message brand-guardrails` instead?" |
| Company-level attributes (stage, market position, business model) | MESSAGE.md Attributes | "That's a company-level attribute. Update with `/design message attributes`." |
| Stable identity facts (founded, HQ, employees, funding) | MESSAGE.md Facts | "That's stable identity. Update with `/design message facts`." |
| Scenarios dimensions (compelling event values, market moment values) | MESSAGE.md Scenarios | "That's runtime scenario vocabulary — `/design message scenarios` is the path." |

This is a soft prompt, not a hard refusal. The user can override by saying "no, put it in the pillar" and you proceed with the pillar edit. Soft-prompt once per session per category — don't repeat for every entry.

### Step 4: Generate updated content

Preserve the structural shape of the pillar; regenerate only the changed sections. Follow the existing voice and conventions. If `--research` was passed, ground the changes in the research findings.

### Step 5: Show diff

Before/after of the pillar file, focused on the sections that changed. Use unified diff or clear annotation; the user should see exactly what's different.

### Step 6: Enumerate downstream impact

Walk the messaging house and identify downstream artifacts that reference content in the changed sections:

- **Builder skills** that reference this pillar in their Context Loading tables (build-campaign, build-launch, build-play, build-event). List by skill name.
- **Collection items** in this pillar's `## Collection Tables` (if the pillar has them). Categories, competitors, personas, segments, products, solutions, stories, reports — whichever apply.
- **Assets** that reference categories or competitors transitively (only if the change affects positioning content).

Report by name only (per A.6 plan decision point #6 — name-only listing). Don't load and re-validate downstream docs.

### Step 7: Approve and write

Present the diff + impact list + approval gate. User approves, edits, or cancels.

On approve: write the updated pillar file. Set `updated` to today's date in frontmatter.

### Step 8: Post-write summary

```
Updated messaging/pillars/[name].md.

The following docs reference content you changed and may need review:
  - builders/build-campaign/SKILL.md
  - messaging/collections/competitors/acme.md
  - messaging/collections/categories/xdr.md
  
Consider running `/run health` to validate.
```

## Refused operations

### Create

If the pillar doesn't exist, refuse:

> Pillar `[name]` doesn't exist. The six pillars (profile, pitch, position, people, portfolio, proof) are pre-scaffolded by bootstrap. Run `/bootstrap` if the messaging house is empty.

### Remove

If `--remove` is passed:

> Pillars are structural and cannot be removed. Edit `[name].md` to change content, or remove the value of specific sections within the file.

## Tool Scoping

- **Read** — `MESSAGE.md`, `messaging/pillars/`, `messaging/collections/` (impact analysis), `.claude/skills/builders/build-*/` (Context Loading checks), `templates/pillars/`
- **Edit** — `messaging/pillars/[name].md` (user approval required)
- **Glob, Grep** — Full access (used to enumerate downstream references)
- **AskUserQuestion** — Interactive update interview
