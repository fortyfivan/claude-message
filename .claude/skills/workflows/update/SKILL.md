---
name: update
description: Manages the lifecycle of produced assets and artifacts. Invoked via command. Load if the user wants to edit, refresh, or update existing content — artifacts, campaign assets, launch assets, or standalone assets.
---

# Update Skill

Detect drift in produced assets, propose changes, get human approval, and refresh or version the result. This skill handles everything after an asset's initial production.

Covers four asset locations:
- **Artifacts** (`artifacts/[slug]/`) — Living, versioned assets with manifests, changelogs, and version archives.
- **Campaign assets** (`output/campaigns/[folder]/`) — Briefs and per-asset content files produced by the campaign workflow.
- **Launch assets** (`output/launches/[name]/`) — Briefs and per-asset content files produced by the launch workflow.
- **Standalone assets** (`output/assets/`) — Individually produced content files.

Invoked via `/update [target]`.

```
/update                                    — Unified drift discovery across all locations
/update [slug]                             — Update a living artifact (backward compatible)
/update campaign [folder]                  — Refresh drifted assets in a campaign
/update campaign [folder] [asset-id]       — Refresh a single campaign asset
/update launch [name]                      — Refresh drifted assets in a launch
/update launch [name] [asset-id]           — Refresh a single launch asset
/update asset [filename]                   — Refresh a standalone asset
```

## How You Work

Four phases with a hard approval gate between diff and refresh. Versioning (Phase 4) applies only to artifacts.

```
Pre-flight → Diff → Approval (human gate) → Refresh/Update
                                                    ↓
                                            [Artifacts only] Version & Log
```

---

## Step 0: Pre-flight

Resolve what to update, verify it exists, and determine the asset type.

### Routing

1. Parse arguments for a type keyword (`campaign`, `launch`, `asset`) and target identifier.
2. **No arguments** → unified discovery (scan all four locations).
3. **Bare slug** (no type keyword) → check `artifacts/[slug]/manifest.md`. If found, route to the artifact flow. If not, inform the user: "No artifact found at `artifacts/[slug]/`. Check the slug or use a type keyword (`campaign`, `launch`, `asset`)."
4. **`campaign [folder]`** → verify `output/campaigns/[folder]/brief.md` exists. If not, inform the user.
5. **`campaign [folder] [asset-id]`** → verify the brief exists and the asset file `output/campaigns/[folder]/[asset-id].md` exists.
6. **`launch [name]`** → verify `output/launches/[name]/brief.md` exists. If not, inform the user.
7. **`launch [name] [asset-id]`** → verify the brief exists and the asset file exists.
8. **`asset [filename]`** → verify the file exists in `output/assets/`. Check for frontmatter with `messaging_docs_loaded`.

### Unified Discovery (no arguments)

Scan all four locations and present a grouped drift overview.

**1. Artifacts.** Scan `artifacts/` for subdirectories containing `manifest.md`. For each, read manifest frontmatter (`title`, `slug`, `format`, `version`, `last_updated`). Run a lightweight drift check: compare each dependency's `updated` field against `last_updated`. Flag any where `updated > last_updated` or where `last_updated` is empty.

**2. Campaigns.** Scan `output/campaigns/` for subdirectories containing `brief.md`. For each, read brief frontmatter (`campaign_name`, `created`, `status`). Skip campaigns with `status: in-progress` — they're still being initially produced. Extract `messaging_docs_loaded` from `shared_context`. Compare each doc's `updated` field against the brief's `created` date. Count drifted docs and affected assets.

**3. Launches.** Same as campaigns but in `output/launches/`. Read brief frontmatter (`launch_name`, `created`, `status`). Skip `status: in-progress`.

**4. Standalone assets.** Scan `output/assets/` for `.md` files with `messaging_docs_loaded` in frontmatter. For each, compare doc `updated` fields against the asset's `generated` date.

Present the unified overview:

```
Produced Asset Drift Status

ARTIFACTS

| Artifact | Format | Version | Last Updated | Drift |
|---|---|---|---|---|
| [title] | [format] | [version] | [date or "Never"] | [N dependencies changed / No drift / Not yet authored] |

CAMPAIGNS

| Campaign | Created | Assets | Drift |
|---|---|---|---|
| [folder] | [date] | [count] | [N assets affected (M messaging docs changed) / No drift] |

LAUNCHES

| Launch | Created | Assets | Drift |
|---|---|---|---|
| [name] | [date] | [count] | [N assets affected (M messaging docs changed) / No drift] |

STANDALONE ASSETS

| Asset | Type | Generated | Drift |
|---|---|---|---|
| [filename] | [skill] | [date] | [N messaging docs changed / No drift] |
```

Omit any section where the directory doesn't exist or contains no assets. Use AskUserQuestion to ask which item to update.

### Artifact Pre-flight (after routing)

1. Read the manifest.
2. Check if `artifacts/[slug]/current.md` exists. If not, inform the user: "This artifact hasn't been authored yet — `current.md` doesn't exist. Use the campaign or writer workflow to author the initial version, then run `/update` to maintain it."

---

## Phase 1: Diff

Identify what has changed upstream since the asset was last produced or updated. The core operation is the same across types: compare the `updated` field of each referenced messaging doc against the asset's baseline date. The output format differs by type.

### Artifact Diff

Full dependency and insight analysis with section mapping.

#### Read Dependencies

1. Read the manifest's Dependencies section. Parse each dependency path and any filters.
2. For each dependency, read the file's YAML frontmatter and extract the `updated` field.
3. Compare each dependency's `updated` date against the manifest's `last_updated` date.
4. For dependencies that are directories (e.g., `messaging/competitors/`), check all files in the directory. Apply any filters declared in the manifest (e.g., `tier: primary`).

#### Check Insights

1. Read `insights/tracker.md`.
2. Find open or acknowledged insights where the Messaging Doc column matches any dependency path.
3. Note matching insights with their ID, severity, and description.

#### Map Changes to Sections

For each changed dependency or relevant insight, use the manifest's Structure table to identify which artifact sections are affected.

#### Read Current Artifact

Read `artifacts/[slug]/current.md` to understand existing content.

#### Produce Artifact Drift Report

```
## Drift Report — [Title] (v[VERSION])

Last updated: [manifest last_updated]
Checking against: [today's date]

### Changes found

**[dependency path]** (updated [date])
  [One-line description of what changed]
  Affects: [Section name(s) from Structure table]

**insights/tracker.md** — Insight [ID] ([severity], [status])
  [Insight description]
  Affects: [Section name(s)]

### No changes found

[dependency path] — unchanged

### Proposed updates

- [Section]: [Specific proposed change and rationale]

### Scope assessment

[Surgical patch — N sections affected / Full regeneration recommended — structural changes detected]
```

If no changes are found across any dependencies or insights, inform the user: "No drift detected — [title] is current as of [last_updated]." and exit.

### Campaign / Launch Diff

Two-layer drift check: brief-level (shared context) and asset-level (per-asset context).

#### Brief-Level Drift

1. Read the brief's full frontmatter. Extract `messaging_docs_loaded` from `shared_context` and `created` date.
2. For each messaging doc in the shared list, read its `updated` field.
3. Flag docs where `updated > created` (or `updated > generated` of the most recent asset, whichever is later).

#### Asset-Level Drift

1. For each asset file in the campaign/launch directory, read its frontmatter (`messaging_docs_loaded`, `generated`).
2. Compare each doc's `updated` against the asset's `generated` date.
3. Identify per-asset docs that drifted independently of the shared context.

If targeting a single asset (`/update campaign [folder] [asset-id]`), only check that asset's drift plus the brief-level context.

#### Produce Campaign/Launch Drift Report

```
## Drift Report — [Campaign/Launch Name]

Created: [date]
Checking against: [today's date]

### Brief-level drift (affects all assets)

**[messaging doc path]** (updated [date], was [original date])
  [One-line description of what changed]

### Asset-level drift

**[asset-id].md** — [N] additional doc(s) changed
  [messaging doc path] (updated [date]) — per-asset context

### Affected assets

| Asset | Brief Drift | Asset Drift | Total Changed Docs |
|---|---|---|---|
| [asset-id] | [N] | [N] | [N] |

### Proposed approach

[Brief-level drift detected — recommend refreshing the campaign narrative first, then regenerating affected assets with updated context.]
[or: Asset-level drift only — regenerate affected assets directly.]
```

If no changes are found, inform the user: "No drift detected — [name] is current as of [date]." and exit.

### Standalone Asset Diff

1. Read the asset's `messaging_docs_loaded` frontmatter and `generated` date.
2. For each messaging doc, read its `updated` field and compare against `generated`.

#### Produce Standalone Drift Report

```
## Drift Report — [Asset Title]

Generated: [date]
Checking against: [today's date]

### Changes found

**[messaging doc path]** (updated [date])
  [One-line description of what changed]

### No changes found

[messaging doc path] — unchanged

### Proposed refresh

[Description of what will change in the regenerated asset]
```

---

## Phase 2: Approval

Present the drift report to the user. Nothing is written until the user approves.

### Artifact Approval

Use AskUserQuestion with four options:

- **Approve** — Proceed with proposed updates as written.
- **Approve with edits** — User modifies the proposed changes before proceeding. Collect their edits and update the drift report accordingly.
- **Reject** — No update. Optionally log a note in the changelog: `## [next version] — [today] / **Trigger:** [trigger] / **Scope:** Rejected / **Changes:** Review triggered but changes rejected. [optional reason]`. Exit.
- **Defer** — No update now. Log a note in the changelog: `## [next version] — [today] / **Trigger:** [trigger] / **Scope:** Deferred / **Changes:** Review deferred. [optional reason]`. Exit.

### Campaign / Launch Approval

Use AskUserQuestion with five options:

- **Approve all** — Refresh brief narrative (if brief-level drift exists) and regenerate all affected assets.
- **Approve selective** — User picks which assets to regenerate. If brief-level drift exists, the brief narrative is always refreshed first.
- **Skip brief, update assets only** — Keep the brief narrative as-is, regenerate selected assets with current messaging context. Use when brief drift is minor and the user judges the narrative still holds.
- **Reject** — No updates.
- **Defer** — No updates now.

### Standalone Asset Approval

Use AskUserQuestion with three options:

- **Approve** — Regenerate the asset with updated messaging context.
- **Reject** — No refresh.
- **Defer** — No refresh now.

---

## Phase 3: Refresh / Update

Execute the approved changes. Branching by asset type.

### Artifact Update

Dispatch a **writer agent** with:

| Context | Source |
|---|---|
| Drift report | The approved drift report (what to change and how) |
| Current artifact | `artifacts/[slug]/current.md` as input |
| Changed messaging docs | Full content of each changed dependency |
| Structure table | From the manifest — scope the update to affected sections only |

Instruct the writer to make surgical edits — modify only the sections identified in the drift report. Unchanged sections must be preserved exactly.

The artifact's `format` field is informational only (target downstream rendering); the writer always produces markdown.

#### Writing the Updated File

Write the updated content to `artifacts/[slug]/current.md`, replacing the previous version. The previous version is archived in Phase 4 before this write occurs.

### Campaign / Launch Refresh

Two-stage process.

#### Stage 1: Brief Narrative Refresh (if approved)

Only runs when brief-level drift exists and the user approved it (not "Skip brief").

1. Read the full brief.
2. Read the changed messaging docs (those in `shared_context.messaging_docs_loaded` with `updated > created`).
3. Dispatch a **writer agent** to regenerate the Campaign Narrative / Launch Narrative section and the "What to Know" section with updated messaging context.
4. Preserve the Asset Manifest structure — do not change asset specs, skill mappings, wave ordering, or dependency graphs.
5. Update the `messaging_docs_loaded` list in the brief's `shared_context` to reflect current doc dates.
6. Write the updated brief.

#### Stage 2: Asset Regeneration

For each approved asset:

1. Dispatch a **writer agent** with:
   - The updated brief (if refreshed) or original brief
   - The asset spec from the brief's Asset Manifest
   - Full content of changed messaging docs
   - The original asset file as reference (for tone and structural continuity)
2. The writer generates a fresh draft following the same pipeline as initial production: context resolution from the brief, skill loading, voice gate, reader review.
3. Write the regenerated asset to the same path, replacing the original.
4. Update the asset's frontmatter:
   - Set `generated` to today's date.
   - Update `messaging_docs_loaded` to reflect current doc versions.
   - Append a `refresh_history` entry:
     ```yaml
     refresh_history:
       - date: "YYYY-MM-DD"
         trigger: "messaging drift: [changed doc paths]"
         docs_changed: [N]
     ```
5. If the asset has been rendered downstream (e.g., in Claude Design), note that the rendered version is now stale and should be refreshed externally.

### Standalone Asset Refresh

1. Dispatch a **writer agent** with:
   - The original asset file as reference
   - Full content of changed messaging docs
   - The same skill and persona from the original asset's frontmatter
2. Write the regenerated asset to the same path.
3. Update frontmatter: `generated` date, `messaging_docs_loaded`, and append `refresh_history` entry.

---

## Phase 4: Version & Log (Artifacts Only)

This phase runs only for artifacts. Campaigns, launches, and standalone assets skip this phase — their refresh is complete after Phase 3.

### Archive Previous Version

1. Copy `artifacts/[slug]/current.md` to `artifacts/[slug]/v[previous-version].md`.

### Determine Version Bump

Based on the scope assessment from the drift report:

| Scope | Bump |
|---|---|
| Typos, factual corrections, minor copy adjustments | Patch (x.x.+1) |
| Content updates — new sections, updated claims, refreshed proof | Minor (x.+1.0) |
| Structural changes — repositioned narrative, new format, significant scope | Major (+1.0.0) |

Present the recommended bump to the user via AskUserQuestion for confirmation. Allow override.

### Update Manifest

1. Set `version` to the new version number.
2. Set `last_updated` to today's date.

### Append Changelog Entry

Prepend an entry to `artifacts/[slug]/changelog.md`:

```markdown
## v[NEW-VERSION] — [TODAY]

**Trigger:** [What triggered the update — dependency changes, insight IDs, scheduled review]
**Scope:** [Surgical patch or full regeneration — which sections affected]
**Approved by:** [User name if known, otherwise "User"]
**Changes:**
- [Section]: [What changed and why]
```

### Resolve Linked Insights

If the drift report included insights from `insights/tracker.md`, and the update addresses them:

1. Read `insights/tracker.md`.
2. For each addressed insight, update: Status → `resolved`, Resolved Date → today's date, Resolution → `artifact update: [slug] v[version]`.
3. Write the updated tracker.

---

## Metadata Contract

The skill reads existing traceability metadata. No new required fields are introduced — only the optional `refresh_history` array is appended during campaign/launch/standalone refresh.

| Location | Date Field | Messaging Docs Field |
|---|---|---|
| `artifacts/[slug]/manifest.md` | `last_updated` | Dependencies section (file paths with optional filters) |
| `output/campaigns/[folder]/brief.md` | `created` | `shared_context.messaging_docs_loaded` |
| `output/campaigns/[folder]/asset-*.md` | `generated` | `messaging_docs_loaded` |
| `output/launches/[name]/brief.md` | `created` | `shared_context.messaging_docs_loaded` |
| `output/launches/[name]/asset-*.md` | `generated` | `messaging_docs_loaded` |
| `output/assets/*.md` | `generated` | `messaging_docs_loaded` |

---

## Edge Cases

- **In-progress campaigns/launches** (`status: in-progress`) — Skip during unified discovery. They're still being initially produced.
- **Asset not yet authored** — Report "Not yet authored" status in the overview. Do not attempt to update.
- **Missing messaging doc** — If a doc listed in `messaging_docs_loaded` no longer exists (deleted or renamed), flag it as a broken reference: "Warning: [path] is referenced but does not exist. This may indicate a renamed or removed doc."
- **Large campaigns (10+ assets)** — Present the full affected assets table but recommend selective refresh rather than regenerating all.
- **No drift detected** — Inform the user and exit cleanly, same as current artifact behavior.
- **Downstream rendered version stale after content refresh** — Flag for the user. Re-rendering happens externally (e.g., in Claude Design).

---

## Tool Scoping

- **Read** — `artifacts/` (manifests, current files, changelogs), `output/campaigns/` (briefs, asset files), `output/launches/` (briefs, asset files), `output/assets/` (content files), `messaging/` (dependency content), `insights/tracker.md` (drift detection), `templates/artifacts/` (manifest/changelog scaffolds)
- **Write, Edit** — `artifacts/` (manifests, changelogs, current files, version archives), `output/campaigns/` (briefs, asset files — refresh only), `output/launches/` (briefs, asset files — refresh only), `output/assets/` (content files — refresh only), `insights/tracker.md` (resolve insights)
- **Glob** — `artifacts/` (discover artifact directories), `output/campaigns/`, `output/launches/`, `output/assets/` (discover content files), `messaging/` (enumerate collection files for directory dependencies)
- **AskUserQuestion** — Target selection (unified discovery), approval flow, version bump confirmation (artifacts only)
- **Agent** — Writer agent (content updates and asset regeneration)
