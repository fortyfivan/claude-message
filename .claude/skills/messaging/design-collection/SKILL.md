---
name: design-collection
description: Full lifecycle (create, update, remove) for collection items — personas, competitors, segments, solutions, stories, categories, products, reports. Maintains parent pillar Collection Tables on every change. Remove operations enumerate cross-reference impact and require forced approval.
---

# Design Collection

Full lifecycle for collection items in the 8 collection types. Branches on file existence and the `--remove` flag.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

Invoked via `/design [collection-type] [name]` where `[collection-type]` is one of: `persona`, `competitor`, `segment`, `solution`, `story`, `category`, `product`, `report`.

## Modes

| Invocation | Behavior |
|---|---|
| `/design [type] [name]` (file doesn't exist) | **Create flow.** Read template → interview → generate → diff → approve → write. Updates parent pillar's `## Collection Tables`. |
| `/design [type] [name]` (file exists) | **Update flow.** Load current → focused interview → regenerate → diff → approve → write. |
| `/design [type] [name] --remove` (file exists) | **Remove flow.** Enumerate impact → preview → require "confirm" → atomic deletion + cross-reference cleanup → audit log. |
| `/design [type] [name] --research` | Dispatches the researcher subagent for web-search-driven calibration before the interview. |

## Collection type → parent pillar

| Collection type | Parent pillar |
|---|---|
| persona, segment | the people pillar |
| competitor, category | the position pillar |
| product, solution | the portfolio pillar |
| story, report | the proof pillar |

## Create flow

### Step 1: Detect

If the collection item doesn't exist for this `[type]` + `[name]`, proceed to create.

### Step 2: Load template

Read the template at `templates/collections/[type]-template.md`.

### Step 3: Interview

Run the calibration interview for this collection type. The template's `[Instructions: ...]` blocks describe what to populate; ask the user for each. If `--research` was passed, dispatch the researcher subagent first to pre-populate findings (task_type maps from collection type: `competitor` → `competitor`, `category` → `market`, `persona`/`segment`/`solution`/`story` → `generic`, `product` → `generic`, `report` → `market`), then narrow the interview to fill gaps.

Cap at 5-8 calibration questions to keep the interview tractable. Group related questions to minimize back-and-forth.

### Step 4: Generate

Replace `[Instructions: ...]` blocks with calibrated content. Populate frontmatter (`title`, `description`, `type`, `priority`/`status`, `updated`, type-specific fields). Description in frontmatter must match the row description that will go in the parent pillar's Collection Tables.

### Step 5: Update parent pillar's Collection Tables

Read the parent pillar (per the type → pillar map above). Add a row to the appropriate Collection Table referencing the new file with the same description.

### Step 6: Diff + approve

Show the diff: new collection file + parent pillar row addition. User approves, edits, or cancels.

### Step 7: Write

Write both files atomically. Set `updated` to today's date in the new collection file.

## Update flow

### Step 1: Detect

File `messaging/collections/[type]/[name].md` exists, no `--remove` → proceed to update.

### Step 2: Load current

Read the existing file. Show the user what's currently there.

### Step 3: Focused interview

"What do you want to change?" Probe for specific sections, frontmatter fields, or descriptions that need revision. Don't re-interview unchanged content. Accept `--research` for research-driven updates.

### Step 4: Regenerate

Apply changes; preserve structure. If the frontmatter `description` changed, the parent pillar's Collection Tables row description must also change to match.

### Step 5: Diff + approve

Show diff (file + parent pillar row if description changed). Approve or edit.

### Step 6: Write

Update collection file. Update parent pillar's Collection Tables row if description changed.

## Remove flow

### Step 1: Detect

File exists, `--remove` flag is present → proceed to remove.

### Step 2: Enumerate impact

Walk the messaging house and identify cross-references:

- **Parent pillar Collection Tables row** — will be removed
- **Other collection items** that reference this one in their frontmatter arrays (e.g., a story's `personas: [...]` array; a competitor's `category_overlap: [...]`)
- **Builder asset manifests in `output/`** that reference this item by name (historical references; flagged but NOT modified — those briefs are immutable history)
- **MESSAGE.md** routing or content references

### Step 3: Preview

Show the user the full impact: what will be removed, what will be modified (cross-reference cleanup), what will be flagged but unchanged (historical output).

```
Removing messaging/collections/[type]/[name].md

Cross-references to clean:
  - messaging/pillars/[parent].md: Collection Tables row will be removed
  - messaging/collections/stories/example.md: `personas` array will drop "[name]"

Historical references (flagged, not modified):
  - output/campaigns/example/01-blog.md: references [name] in metadata
  - output/launches/example/02-email.md: same

This deletes the source file. Git history is the recovery mechanism.
```

### Step 4: Forced approval

Require literal "confirm" text input. No `--yes` flag, no auto-confirm. If the user types anything else, abort.

### Step 5: Execute atomically

Delete the file. Clean up cross-references in identified files (Collection Tables row removal, frontmatter array entries). Write the audit log.

### Step 6: Audit log

Write to `.design/removals/YYYY-MM-DD-HHMMSS.md`:

```yaml
---
artifact: messaging/collections/[type]/[name].md
removed_at: 2026-05-22T15:30:00Z
removed_by: design-collection
---

# Removal of messaging/collections/[type]/[name].md

## Cross-references cleaned

- messaging/pillars/[parent].md — Collection Tables row removed
- messaging/collections/stories/example.md — `personas` array updated

## Historical references flagged (not modified)

- output/campaigns/example/01-blog.md
- output/launches/example/02-email.md
```

### Step 7: Confirmation

Report to the user: file deleted, cross-references cleaned, audit log path.

## Refused operations

If the file doesn't exist and `--remove` is passed, refuse:

> Cannot remove `messaging/collections/[type]/[name].md` — it doesn't exist. Run `/design [type] [name]` (without `--remove`) to create it.

## Tool Scoping

- **Read** — `MESSAGE.md`, `messaging/`, `templates/collections/`, `output/` (historical refs), `input/`, `output/research/`, `insights/`
- **Write, Edit** — `messaging/collections/[type]/` (user approval), `messaging/pillars/[parent].md` (Collection Tables row maintenance, user approval), `.design/removals/` (autonomous on remove)
- **Agent(researcher)** — Dispatched when `--research` flag is passed; isolates web-search/web-fetch context
- **Glob, Grep** — Full access (cross-reference enumeration)
- **AskUserQuestion** — Interactive interview + approval gates
