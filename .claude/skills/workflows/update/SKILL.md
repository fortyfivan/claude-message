# Update Skill

Detect drift in living artifacts, propose changes, get human approval, and version the result. This is a maintenance workflow — it handles everything after an artifact's initial production.

Invoked via `/update [artifact-slug]`.

## How You Work

Four phases with a hard approval gate between diff and update.

```
Pre-flight → Diff → Approval (human gate) → Update → Version & Log
```

---

## Step 0: Pre-flight

Resolve which artifact to update and verify it's ready for maintenance.

**If a slug is provided:**

1. Verify `artifacts/[slug]/manifest.md` exists. If not, inform the user: "No artifact found at `artifacts/[slug]/`. Check the slug or create the artifact directory with a manifest first."
2. Read the manifest.
3. Check if `artifacts/[slug]/current.[format]` exists. If not, inform the user: "This artifact hasn't been produced yet — `current.[format]` doesn't exist. Use the campaign or writer workflow to produce the initial version, then run `/update` to maintain it."

**If no slug is provided:**

1. Scan `artifacts/` for subdirectories containing `manifest.md`.
2. For each artifact, read the manifest frontmatter (`title`, `slug`, `format`, `version`, `last_updated`).
3. Run a lightweight drift check: compare each dependency's `updated` frontmatter field against the manifest's `last_updated`. Flag any where `updated > last_updated` or where `last_updated` is empty.
4. Present an artifact overview table:

```
Living Artifacts

| Artifact | Format | Version | Last Updated | Drift Status |
|---|---|---|---|---|
| [title] | [format] | [version] | [date or "Never"] | [N changes detected / No drift / Not yet produced] |
```

5. Use AskUserQuestion to ask which artifact to update.
6. After selection, check for `current.[format]` as above.

---

## Phase 1: Diff

Identify what has changed upstream since the artifact was last updated.

### Read Dependencies

1. Read the manifest's Dependencies section. Parse each dependency path and any filters.
2. For each dependency, read the file's YAML frontmatter and extract the `updated` field.
3. Compare each dependency's `updated` date against the manifest's `last_updated` date.
4. For dependencies that are directories (e.g., `messaging/competitors/`), check all files in the directory. Apply any filters declared in the manifest (e.g., `tier: primary`).

### Check Insights

1. Read `insights/tracker.md`.
2. Find open or acknowledged insights where the Messaging Doc column matches any dependency path.
3. Note matching insights with their ID, severity, and description.

### Map Changes to Sections

For each changed dependency or relevant insight, use the manifest's Structure table to identify which artifact sections are affected.

### Read Current Artifact

Read `artifacts/[slug]/current.[format]` to understand existing content. For binary formats (pptx, pdf), note that the current file exists but content comparison will be text-based via the drift report.

### Produce Drift Report

Generate a plain-language drift report:

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

---

## Phase 2: Approval

Present the drift report to the user. Use AskUserQuestion with four options:

- **Approve** — Proceed with proposed updates as written.
- **Approve with edits** — User modifies the proposed changes before proceeding. Collect their edits and update the drift report accordingly.
- **Reject** — No update. Optionally log a note in the changelog: `## [next version] — [today] / **Trigger:** [trigger] / **Scope:** Rejected / **Changes:** Review triggered but changes rejected. [optional reason]`. Exit.
- **Defer** — No update now. Log a note in the changelog: `## [next version] — [today] / **Trigger:** [trigger] / **Scope:** Deferred / **Changes:** Review deferred. [optional reason]`. Exit.

Nothing is written until the user approves.

---

## Phase 3: Update

After approval, dispatch agents based on the artifact's `format` field.

### Markdown artifacts (`format: md`)

Dispatch a **writer agent** with:

| Context | Source |
|---|---|
| Drift report | The approved drift report (what to change and how) |
| Current artifact | `artifacts/[slug]/current.md` as input |
| Changed messaging docs | Full content of each changed dependency |
| Structure table | From the manifest — scope the update to affected sections only |

Instruct the writer to make surgical edits — modify only the sections identified in the drift report. Unchanged sections must be preserved exactly.

### Binary artifacts (`format: pptx` or `pdf`)

Two-stage dispatch:

1. **Writer agent** — Produces an updated content draft in markdown. Receives the same context as markdown artifacts. The draft follows the Structure table layout, marking which sections changed and which are preserved verbatim.
2. **Producer agent** — Renders the approved markdown draft to the target binary format using brand tokens and asset templates. The producer never modifies content.

This matches the campaign workflow's two-stage pattern for non-markdown deliverables.

### Writing the Updated File

Write the updated content to `artifacts/[slug]/current.[format]`, replacing the previous version. The previous version is archived in Phase 4 before this write occurs.

---

## Phase 4: Version & Log

### Archive Previous Version

1. Copy `artifacts/[slug]/current.[format]` to `artifacts/[slug]/v[previous-version].[format]`.

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

## Tool Scoping

- **Read** — `artifacts/` (manifests, current files, changelogs), `messaging/` (dependency content), `insights/tracker.md` (drift detection), `templates/artifacts/` (reference)
- **Write, Edit** — `artifacts/` (manifests, changelogs, current files, version archives), `insights/tracker.md` (resolve insights)
- **Glob** — `artifacts/` (discover artifact directories), `messaging/` (enumerate collection files for directory dependencies)
- **AskUserQuestion** — Artifact selection (no-slug mode), approval flow, version bump confirmation
- **Agent** — Writer agent (content updates), producer agent (binary format rendering)
