---
name: design-message
description: Update a section of MESSAGE.md (the always-on foundation). MESSAGE.md is structural; sections cannot be removed — they can only be edited. Update-only behavior with downstream-impact awareness.
---

# Design MESSAGE.md

Update behavior only. MESSAGE.md is the always-on foundation; sections are required structural elements and cannot be removed. Bootstrap populates MESSAGE.md end-to-end; this skill is for incremental section edits afterward.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

Invoked via `/design message [section]`. The skill loads the existing section, runs a focused update interview, generates the revised content, shows a diff, and writes after approval.

## Editable sections

| Section | Slug | What it holds |
|---|---|---|
| Attributes | `attributes` | Company type, stage, market, position, regions, business model |
| Facts | `facts` | Founded, HQ, employees, funding, customers |
| Glossary | `glossary` | Cross-cutting terminology with usage rules |
| Brand Guardrails | `brand-guardrails` | 4–8 testable absolute output rules |
| Scenarios | `scenarios` | Dimensions table (customizable rows: compelling-event, market-moment) |

Other catalog sections (Pillars, Collections, Assets) are maintained by their respective `/design` skills or are spec-fixed. Company name + intro live at the top of MESSAGE.md and are edited there directly.

**ICP is not a MESSAGE.md section.** ICP (Characteristics, Behaviors, Environmental) lives in the People pillar — route ICP edits to `/design pillar people`.

## Modes

| Invocation | Behavior |
|---|---|
| `/design message [section]` | Update flow. Loads existing section → interview → generate → diff → approve → write. |
| `/design message [section] --remove` | **Refused.** "MESSAGE.md sections are structural and cannot be removed. Edit the section to change content." |
| `/design message icp` | **Redirected.** "ICP now lives in the People pillar. Use `/design pillar people` to edit it." |
| `/design message [section]` for unknown section | **Refused with section list.** "Section `[section]` doesn't exist. Editable: attributes, facts, glossary, brand-guardrails, scenarios." |

## Update flow

### Step 1: Detect

Validate `[section]` against the editable list. If invalid, refuse with the section list.

Confirm `MESSAGE.md` exists at repo root and contains the named section. If MESSAGE.md is unpopulated (still has bracketed `[Instructions:]` placeholders throughout), redirect to `/bootstrap`.

### Step 2: Load current section

Read MESSAGE.md and extract the named section's current content. Present it to the user verbatim so they see what's there before deciding what to change.

For Glossary: enumerate current entries (term + usage rule) with index numbers so the user can reference specific rows.

For Brand Guardrails: enumerate current rules with index numbers.

### Step 3: Update interview

Focused — "What do you want to change?" Not a full re-interview of every field.

Probe for:
- Which field/row needs revision
- What specifically (replace, add, remove)
- Whether the change is driven by recent feedback, market shift, or new evidence — if yes, accept `--research` for research-backed updates

Use AskUserQuestion when scope is ambiguous. Do not re-interview on content that isn't changing.

**Glossary discipline.** When the user proposes adding a term, check whether it belongs elsewhere:
- Product name → "That looks like a product name. It should live in `messaging/collections/products/[slug].md`. Add it there with `/design product [slug]` instead?"
- Competitor name → redirect to `/design competitor [slug]`.
- Customer name → redirect to `/design story [slug]`.
- Persona role title → redirect to `/design persona [slug]`.
- Category name → redirect to `/design category [slug]`.

Soft redirect — let the user override and proceed if they have a reason.

**Brand Guardrails discipline.** Each rule must be testable. Reject rules that aren't:
- "Be authentic" — not testable. Push back: "What's the observable signal? Rephrase as a testable constraint."
- "Never use the word 'leverage' as a verb" — testable. Accept.

### Step 4: Generate updated section

Preserve the section's structural shape. Regenerate only the changed fields/rows. Follow MESSAGE.md conventions (bullet style, table format, subsection headers).

For Glossary and Brand Guardrails: append-only by default; explicit `replace [N]` or `remove [N]` operations for existing rows.

### Step 5: Show diff

Unified diff of the section before/after. Annotate clearly which rows/fields changed.

### Step 6: Approve and write

Present the diff + approval gate. User approves, edits, or cancels.

On approve: write the updated MESSAGE.md (atomic write — read full file, replace section content, write back). Update the `version` field in frontmatter to today's ISO date.

### Step 7: Post-write summary

```
Updated MESSAGE.md [section].

Sections like Glossary and Brand Guardrails affect every generation. Consider running:
  - /run health    — validate the messaging house
  - /review [recent asset]    — spot-check that voice still passes
```

## Refused operations

### Create

MESSAGE.md sections aren't created individually — bootstrap establishes the full file as the synthesis of the populated pillars. If a section is unpopulated, the user should run `/bootstrap` or edit MESSAGE.md directly.

### Remove

If `--remove` is passed:

> MESSAGE.md sections are structural and cannot be removed. Edit the section to change content. For Glossary or Brand Guardrails entries specifically, you can remove individual rows during the update interview.

## Tool Scoping

- **Read** — `MESSAGE.md`, `messaging/` (impact analysis), `templates/` (section structure reference)
- **Edit** — `MESSAGE.md` (user approval required)
- **Glob, Grep** — Full access (used to enumerate downstream references when relevant)
- **AskUserQuestion** — Interactive update interview
