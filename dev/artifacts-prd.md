# PRD: Living Artifacts

## Overview

Living artifacts are versioned, continuously maintained assets that must stay current with the messaging system. They differ from campaign assets in one essential way: they don't expire. A First Call Deck produced today is expected to be accurate six months from now. That expectation creates a maintenance obligation — detect drift, propose updates, get approval, version the change.

This PRD introduces three things: a directory structure for artifact storage and version history, a manifest format that declares each artifact's dependencies and ownership, and an Update skill that governs the maintenance loop with human approval at every change.

Living artifacts are not produced by the Update skill. Initial production uses the campaign or writer workflows. The Update skill handles everything that happens after first publication.

---

## Directory Structure

```
artifacts/
  [artifact-slug]/
    manifest.md
    current.[ext]
    changelog.md
    v1.0.0.[ext]
    v1.1.0.[ext]
    v2.0.0.[ext]
```

Each artifact lives in its own subdirectory under the top-level `artifacts/` directory. `current` is always the canonical version — the one distributed, linked, or referenced. Versioned files are the audit trail. `changelog.md` is the human-readable history of every change: what changed, why, who approved, when.

### Versioning semantics

| Bump | When |
|---|---|
| Patch (1.0.x) | Typos, factual corrections, minor copy adjustments |
| Minor (1.x.0) | Content updates — new sections, updated competitive claims, refreshed proof points |
| Major (x.0.0) | Structural changes — repositioned narrative, new format, significant scope change |

### Supported artifact types

Any file format the writer or producer agents can generate. Common types:

| Artifact | Format |
|---|---|
| First Call Deck | `.pptx` |
| Product Roadmap | `.md` |
| Product Collateral | `.pdf` or `.md` |
| Battlecard | `.md` |
| One-Pager | `.pdf` or `.md` |

The manifest declares the format. The Update skill handles regeneration for any declared type.

---

## Manifest

The manifest lives inside the artifact's subdirectory. It is the contract between the artifact and the messaging system — what the artifact depends on, who owns it, and what conditions trigger a review.

```markdown
---
title: First Call Deck
slug: first-call-deck
format: pptx
owner: Ivan
version: 1.2.0
last_updated: 2026-03-27
---

## Dependencies

Messaging components this artifact draws from. Changes to any of these
should trigger a drift review.

- messaging/profile.md
- messaging/space.md
- messaging/audience.md — personas: ciso, vp-engineering
- messaging/portfolio.md — products: core-platform
- messaging/proof.md
- messaging/competitors/ — tier: primary

## Trigger Conditions

What warrants a review:

- Any primary competitor changes pricing, positioning, or product
- Any pillar file updated with a version bump
- Insight severity: critical (immediate), warning (next scheduled review)
- Scheduled: quarterly

## Structure

Sections and what each draws from. Used by the Update skill to scope
surgical patches vs. full regeneration.

| Section | Source |
|---|---|
| Company overview | profile.md |
| Market problem | space.md |
| Audience + pain points | audience.md (personas) |
| Product overview | portfolio.md |
| Differentiation | space.md, competitors/ |
| Proof points | proof.md |
| Pricing | portfolio.md |
| Next steps | motion.md |

## Notes

Context the Update skill should carry across versions — decisions made,
sections intentionally excluded, format constraints.
```

---

## Update Skill

The Update skill is a workflow Skill — it runs in the main session, not as a subagent. Human approval is required before any file is written or versioned.

### Invocation

```
/update [artifact-slug]
```

If no slug is provided, list all artifacts in `artifacts/` with their last updated date and any open drift flags, and ask the user which to update.

### Phase 1: Diff

Read the artifact manifest. Read `current.[ext]` to understand existing content. Identify what has changed upstream since `last_updated` in the manifest:

- Read each dependency listed in the manifest. Check file modification dates against `last_updated`.
- Read `insights/tracker.md`. Flag any open insights that reference messaging components listed as dependencies.
- For each change found, map it to the artifact sections declared in the manifest's Structure table.

Produce a plain-language drift report:

```
## Drift Report — First Call Deck (v1.2.0)

Last updated: 2026-01-15
Checking against: 2026-03-27

### Changes found

**messaging/space.md** (updated 2026-02-03)
  Differentiators section revised — "no free tier friction" removed.
  Affects: Differentiation slide

**insights/tracker.md** — Insight #047 (critical, open)
  Acme Corp launched SMB free tier. Competitive claim on slide 8 no longer accurate.
  Affects: Differentiation slide, Pricing comparison slide

**messaging/proof.md** (updated 2026-03-10)
  Two new customer proof points added (Acme Health, Riverdale Financial).
  Affects: Proof points slide

### No changes found

messaging/profile.md — unchanged
messaging/audience.md — unchanged
messaging/portfolio.md — unchanged

### Proposed updates

- Slide 7 (Differentiation): Remove "no free tier" claim. Reframe around
  enterprise-grade onboarding and dedicated support tier.
- Slide 8 (Pricing comparison): Update Acme column to reflect new SMB tier.
  Add footnote: "Acme free tier limited to 10 users, no enterprise SLA."
- Slide 12 (Proof points): Add Acme Health and Riverdale Financial logos
  and result metrics.

### Scope assessment

Surgical patch — 3 slides affected. Full regeneration not required.
```

### Phase 2: Human approval

Present the drift report to the user. Four options:

- **Approve** — proceed with proposed updates as written
- **Approve with edits** — user modifies the proposed changes before proceeding
- **Reject** — no update; optionally log a deferred review note in the changelog
- **Defer** — no update now; set a reminder date in the manifest

Nothing is written until the user approves. This is the governance gate.

### Phase 3: Update

After approval, dispatch the writer or producer agent with the approved diff as explicit instructions. The agent receives:

- The approved drift report (what to change and how)
- The current artifact as input
- The relevant messaging sections as context
- The manifest's Structure table to scope the update

For `.md` artifacts: surgical edits using the approved diff.
For `.pptx` and `.pdf` artifacts: full regeneration using the approved diff as the writer's brief, with unchanged sections explicitly preserved.

### Phase 4: Version and log

1. Copy `current.[ext]` to `v[previous-version].[ext]` in the artifact directory
2. Write the updated file as `current.[ext]`
3. Bump the version in `manifest.md` and update `last_updated`
4. Append a changelog entry to `changelog.md`
5. Resolve any linked insights in `insights/tracker.md` if the update addresses them

### Changelog entry format

```markdown
## v1.3.0 — 2026-03-27

**Trigger:** Insight #047 (Acme Corp SMB tier launch) + proof.md update
**Scope:** Surgical patch — slides 7, 8, 12
**Approved by:** Ivan
**Changes:**
- Slide 7: Removed "no free tier friction" differentiator. Reframed around
  enterprise onboarding and dedicated support.
- Slide 8: Updated Acme pricing comparison to reflect new SMB tier. Added
  10-user cap footnote.
- Slide 12: Added Acme Health and Riverdale Financial proof points.
```

---

## Drift Detection Integration

The researcher agent already writes to `insights/tracker.md` with severity classifications. The Update skill reads this tracker during Phase 1. No changes to the researcher are required — the integration is read-only.

Artifacts are not automatically updated when an insight is filed. The insight surfaces the drift. The Update skill, triggered by the user, acts on it. The governance model is always human-initiated.

For teams running the researcher as a scheduled program: the Slack notification at the end of each scan should include a summary of artifacts with open drift flags. This prompts the user to run `/update [artifact-slug]` at their discretion.

---

## Deliverables

- `artifacts/` top-level directory with per-artifact subdirectory structure
- `manifest.md` template in `_templates/artifacts/manifest.md`
- `changelog.md` seed file template
- Update skill at `.claude/skills/workflows/update.md`
- `/update` command at `.claude/commands/update.md`
- Three seed artifact directories with manifests: `artifacts/first-call-deck/`, `artifacts/product-roadmap/`, `artifacts/product-collateral/`
- Updated `CLAUDE.md` to document `artifacts/` structure and the Update skill
- Updated `onboard.sh` to scaffold `artifacts/` on install
- Updated researcher Slack notification template to include artifact drift summary

## Out of Scope

- Automatic artifact updates without human approval
- Multi-owner approval workflows
- Artifact distribution or publishing (sharing, uploading to Drive, etc.)
- Initial artifact production (handled by campaign or writer workflows)
- Diff rendering for binary formats (`.pptx`, `.pdf`) — drift report is text-based regardless of artifact format