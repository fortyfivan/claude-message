---
name: run-health
description: System health check — validates structural integrity of the messaging house, surfaces gaps and orphans, and detects calibration drift between the messaging system and the skills that generate against it. Invoked via /health.
---

# Health Skill

Single command for verifying the messaging system is structurally sound and well-calibrated. Adds structural validation that catches problems before they reach a campaign run.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

Two modes:

| Invocation | Scope |
|---|---|
| `/health` | Full check — structure, sync, drift |
| `/health --calibration` | Calibration drift only |

Output is a single report: green checks for what's healthy, warnings for what's drifting, errors for what's broken. The report includes specific remediation suggestions; this skill does not auto-fix anything.

## Boundary

Health is read-only. It reports. It does not write to the messaging house or to skill files. The user remediates with the appropriate workflow (`/design`, `/run investigation`, `/bootstrap`, or manual edit).

## Step 1: Load context

Walk the messaging house:

- All 6 pillar files (full body)
- All collection file frontmatter (frontmatter only; bodies on demand for spot checks)
- All asset envelopes (full body) and their variants
- MESSAGE.md (always-on; already loaded)
- `output/journal.md` if present (recent entries inform drift signals)

Skip the SKILL.md files of generation workflows in this step — they're scoped to the calibration check.

## Step 2: Structural validation

Validate the shapes the system expects.

### 2.1 Pillar section structure (warn-only per CI policy)

Each pillar must contain:
- `## Messaging Blocks`
- `## Collection Tables` (Position, People, Portfolio, Proof only — not Profile or Pitch)
- `## Writing Guidelines`
- `## Messaging Rules`

Report any missing sections. Per project policy, missing pillar sections produce **warnings**, not errors — they may be in-progress.

### 2.2 Pillar frontmatter

Each pillar frontmatter must include `title` and `updated`. Profile additionally must include `stage`, `type`, `market`.

### 2.3 Collection Tables sync

For each pillar with Collection Tables, cross-reference the table rows against the actual collection files in the corresponding collection directory.

- **Orphan files:** A collection file exists but no row in the parent pillar's table → warning (file present, not routed).
- **Broken rows:** A row in the table references a file that doesn't exist → error (route points nowhere).
- **Description drift:** A row's description doesn't match the collection file's `description` frontmatter → warning (they should agree).

### 2.4 Assets integrity

For each row in MESSAGE.md's `## Assets` table:
- The asset folder must exist
- The folder must contain an `asset.md` envelope
- The envelope must have valid frontmatter with `slug`, `content-keys`, `array-keys`
- The `default-variant` (if declared) must resolve to a file in `variants/`

Missing files or invalid frontmatter → error.

### 2.5 Glossary presence

MESSAGE.md must contain a populated `## Glossary` section. If missing or empty after bootstrap claims to have run → error.

## Step 3: Calibration drift

(Skip if invoked with no flag and the user only asks for structural; always run in default mode.)

Calibration lives in pillars (Profile Brand Voice, Pitch UVPs/Differentiators) and persona collections (Messaging Guidance). Drift is about *content gaps*, not *re-tune timing*.

### 3.1 Persona Messaging Guidance completeness

For each persona collection, verify the `### Messaging Guidance` section has populated values for:
- Altitude
- Lead with
- Avoid leading with
- Proof types
- Language cues
- CTA
- Format affinity

Missing or placeholder values → warning. Generation skills depend on these fields.

### 3.2 Coverage gaps

- **Personas without stories.** Any persona should have at least one story tagged to it. Zero stories → warning (proof gap for content targeting that persona).
- **Products without solutions.** Any product should have at least one related solution (or be a platform that doesn't need solutions). Neither → warning.
- **Categories without competitors.** Any category should have at least one competitor mapped to it. Zero competitors → warning.

### 3.3 Glossary divergence

Spot-check generated content in `output/` (last 30 days, if present). For each output file, scan for terms that appear in MESSAGE.md's `## Glossary` — any term used with a different capitalization, spelling, or definition → warning.

### 3.4 Recency signals

Check the `updated` frontmatter on each pillar and collection file:
- File `updated` more than 6 months old when active changes are happening (deduced from recent journal entries that touch the file's domain) → opportunity flag.
- File `updated` more than 12 months old with no recent reference → information only (not a warning).

## Step 4: Report

Produce a single structured report. Be concrete — every issue points to a specific file and section. Suggest the remediation workflow for each.

```
Health Check — [date]

## Structural ✓
- All 6 pillars present and well-formed.
- All collection types populated (categories: 4, competitors: 6, ...).
- Assets maps to existing format folders.
- Glossary populated.

## Warnings (3)
- Position pillar — Missing `## Collection Tables` section. (Remediate: /design pillar position)
- security-executives persona — Messaging Guidance "Format affinity" field is empty. (Remediate: /design persona security-executives)
- Orphan story file — Exists but no row in the proof pillar's Collection Tables. (Remediate: add row to the proof pillar or delete the orphan.)

## Errors (1)
- MESSAGE.md Assets references "whitepaper" but the asset folder does not exist. (Remediate: either /design asset whitepaper or remove the routing-table row.)

## Calibration opportunities (2)
- 2 personas have zero stories tagged: practitioners, developers. Proof for content targeting them is thin. (Remediate: /run investigation add-story or import existing customer wins.)
- Profile pillar was last updated 8 months ago; recent journal entries reference voice shifts. (Remediate: /design pillar profile to refresh voice attributes.)

## Suggested next actions
1. Fix the asset-routing error (10 min)
2. /design pillar position to add Collection Tables section (15 min)
3. Schedule a focused /run investigation on persona story gaps
```

## Tool Scoping

- **Read** — Full access to the messaging house, journal, and skill files.
- **Glob, Grep** — Used to inventory files and cross-reference table rows against directory contents.
- **Write** — Not used. Health is read-only by design.
