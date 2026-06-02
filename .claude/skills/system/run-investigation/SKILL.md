---
name: run-investigation
description: Unified messaging-system intelligence engine. Performs external research, processes field feedback, inspects and validates the system, and manages the lifecycle of messaging insights. Invoked via `/run investigation [mode]`. Load if the user is looking for insights, processing signals, or asking questions about the messaging system.
---

# Run Investigation Skill

Unified intelligence and system-health skill. Consolidates external research, field feedback processing, system health validation, and insight lifecycle management into a single skill.

Invoked via `/run investigation [mode] [args]`.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## Modes

| Mode | Invocation | Purpose |
|---|---|---|
| Scan | `/run investigation scan` | Broad investigation across all enabled domains |
| Target | `/run investigation target [type] [name]` | Focused investigation of a specific entity |
| Feedback | `/run investigation feedback [input]` or `--log` | Process field signals into messaging changes |
| Review | `/run investigation review` or `/run investigation` | Tracker dashboard + health check summary |
| Fix | `/run investigation fix [check]` | Health check remediation |
| Report | `/run investigation report` | Full health report to `output/health-report.md` |
| State mgmt | `/run investigation acknowledge/defer/resolve [ID]` | Direct insight state transitions |

All modes share the **Methods** and **Tracker Management** sections below.

---

## Methods

### Reading the messaging house

Walk the messaging house using the System Audit pattern. Used by health checks, tracer steps, and impact analysis:

- Read all 6 pillar files.
- Enumerate every collection directory; for each file, read frontmatter (most checks don't need full bodies — frontmatter + section headers suffice).
- Build an index: pillar `updated` dates; collection frontmatter + `updated` dates; pillar `## Collection Tables` rows (Name, Description); cross-reference fields from collection frontmatter.

### Reading templates

Load templates for schema reference (required frontmatter fields, valid enum values, expected sections within `## Messaging Blocks`, three-section structure requirements). The frontmatter contracts are also defined canonically in `MESSAGE.md` — templates are the operational form; MESSAGE.md is the spec.

### Dispatching the researcher subagent

For external scanning (Scan + Target modes), dispatch the researcher subagent (`agents/researcher.md`) rather than performing inline web search. The researcher isolates research context (search results, fetched pages) from the orchestrator's window and returns a structured synthesis.

Dispatch pattern:

```
Agent(
  subagent_type: "researcher",
  prompt: "Apply the protocol in .claude/agents/researcher.md.

  task_type: [market | competitor | company]
  entity: [name or category]
  depth: [quick | standard | deep]
  time_bounds: [past N months, or 'any']
  output_path: output/research/[topic]-[YYYY-MM-DD].md

  Domains to emphasize (from insights/config.md): [filtered list]
  Open insights context (avoid duplicates): [list of INS-IDs + summaries]
  Messaging house context (claims to validate or contradict): [extracted passages]"
)
```

After the researcher returns:

1. Map each finding to specific messaging components (pillars, collections affected). The researcher's synthesis identifies findings; the orchestrator decides what they mean for the messaging house.
2. Classify findings by severity (critical / warning / opportunity / confirmation) and type (competitive / market / audience / portfolio / proof / internal) per the Severity & Type table below.
3. Write trackable findings to `insights/tracker.md` per Tracker Management.

### Severity classification

| Severity | When | Action implied |
|---|---|---|
| **Critical** | A claim, positioning, or competitive contrast in the messaging house is now wrong or fragile | Messaging update required before next campaign |
| **Warning** | A messaging element is weakening but not broken | Monitor; revisit at next quarterly review |
| **Opportunity** | A new angle, proof point, or competitive opening surfaces that strengthens the messaging house | Add to next design/update cycle |
| **Confirmation** | The finding validates existing messaging | Increases confidence; record for future tuning |

| Type | Maps to |
|---|---|
| Competitive | Position, competitors, pitch differentiators |
| Market | Position, categories, pitch narrative |
| Audience | People, personas |
| Portfolio | Portfolio, products, solutions |
| Proof | Proof, stories, reports |
| Internal | MCP-sourced signals; team or product changes |

---

## Tracker Management

Single source of truth for tracker behavior. All modes that touch the tracker use these conventions.

### ID generation

Sequential: `INS-001`, `INS-002`, etc. Read `insights/tracker.md` to find the highest existing ID before appending. If no insights exist, start at `INS-001`.

### Row format

```
| INS-[NNN] | [YYYY-MM-DD] | [source] | [severity] | [one-line finding] | [messaging doc path] | open | | |
```

`[source]` is one of: `investigate:scan`, `investigate:targeted`, `investigate:health`, `investigate:fix`, `investigate:feedback`, `investigate:feedback:log`.

### Auto-resolution

For each `open` or `acknowledged` insight, compare the referenced messaging doc's `updated` field against the insight's Date. If `updated > Date`, mark resolved:
- Status → `resolved`
- Resolved Date → today's date
- Resolution → "auto-resolved: [doc] updated [date]"

### Recurring detection

When a new finding matches an existing open insight (same Messaging Doc + similar signal type), update the existing insight rather than creating a duplicate. Add `last_seen: [date]` to the Resolution column.

### Stale deferral detection

`deferred` insights older than 30 days with no messaging doc update since deferral are flagged in findings under a **Stale Deferrals** heading.

### Writing health insights to tracker

After any health-check run, write trackable insights for findings that require human judgment or composition work:

1. **Filter.** Only `critical` and `warning` findings qualify. Exclude `info` findings and auto-fixable items (missing `updated` field, filename casing, missing table rows for existing files).
2. **Read tracker.** Find the highest existing ID.
3. **Detect recurring.** Update existing rows instead of creating duplicates.
4. **Append rows.** One per qualifying finding using the row format above.
5. **Write findings file.** `insights/findings/health-YYYY-MM-DD.md` with the Findings frontmatter (see Findings Output Format).

Skip entirely if no findings meet the tracker threshold.

### Direct state actions

| Command | Action |
|---|---|
| `/run investigation acknowledge [ID]` | open → acknowledged |
| `/run investigation defer [ID]` | → deferred |
| `/run investigation resolve [ID]` | → resolved |

Read the tracker, find the insight by ID, update Status / Resolved Date (if resolving) / Resolution. Write back.

---

## Scan Mode

Broad investigation across all enabled domains.

1. Read `insights/config.md` for enabled domains, thresholds, watchlists.
2. Read `insights/tracker.md`. Run auto-resolution (Tracker Management).
3. Dispatch the researcher subagent per Methods (one dispatch per enabled domain, or one dispatch with task_type `generic` for broad scans). Pass enabled domains + open-insights context.
4. Process returned findings: assign IDs, detect recurring, check auto-resolution.
5. Write consolidated findings to `insights/findings/scan-YYYY-MM-DD.md`.
6. Update tracker: append new as `open`, update recurring with `last_seen`, auto-resolve stale.
7. Log to journal if findings include messaging effectiveness learnings (see Journal Logging).
8. Present summary: key findings, tracker updates, recommended actions.
9. **Produced asset drift summary.** Scan `output/{campaigns,launches,plays,assets}/` for assets whose `messaging_docs_loaded` references docs with `updated` dates newer than the asset's `created` / `generated` date. Skip in-progress items.

```
## Produced Asset Drift

CAMPAIGNS / LAUNCHES / PLAYS
| Folder | Created | Assets | Status |
|---|---|---|---|
| [folder] | [date] | [count] | [N assets affected / Current] |

STANDALONE ASSETS
| Asset | Generated | Status |
|---|---|---|
| [filename] | [date] | [N docs changed / Current] |
```

Omit sections where the directory doesn't exist or has no assets. Read-only. For drifted output, regenerate via `/build [campaign|launch|play] --continue [folder]`.

---

## Target Mode

Focused investigation of a specific entity.

1. Read `insights/config.md` and `insights/tracker.md`.
2. Load the specific collection profile(s) matching the focus entity. Use pillar Collection Tables to identify the right profile(s).
3. Dispatch the researcher subagent. Select task_type by entity: competitor → `competitor` (loads `tasks/research-competitor/`); company → `company` (loads `tasks/research-company/`); category or market topic → `market` (loads `tasks/research-market/`); persona or other → `generic`. Pass entity name, depth (default `standard`), time bounds (default past 12 months for competitor/company; longer for market), and open-insights context.
4. Process findings: assign IDs, detect recurring.
5. Write findings to `insights/findings/[topic].md`.
6. Update tracker; log to journal.
7. Present findings with specific wording recommendations and `/design` command suggestions:
   - "Competitor Acme has shifted positioning — run `/design competitor acme-corp` to update the profile."
   - "The CISO persona's pain points may have shifted — run `/design persona ciso` to review and update."

---

## Feedback Mode

Process real-world signals (sales conversations, campaign performance, customer interactions, market observations) and translate them into proposed messaging changes. The skill doesn't assume feedback is correct — it analyzes the signal, traces impact, proposes changes, and waits for user approval.

**Full feedback** (default): Parse input → Read messaging house → Trace impact → Propose changes → User approval → Execute changes + journal entry.

**Log-only** (`--log`): Parse input → Append journal entry "Logged — no changes proposed" → Write tracker entry (source `feedback:log`, status `open`) + findings file. Skip propose/approve/execute.

### Step 1: Parse the input

Extract the signal: what changed, source (sales / campaign data / customer conversation / analyst briefing / observation), confidence (pattern vs. anecdote). If ambiguous, ask focused clarifying questions — "Is this multiple reps or one deal?" matters; "Tell me more about the competitive landscape" doesn't.

**Log-only mode:** skip Steps 2-4. Go directly to Step 5.

### Step 2: Trace the impact

Read the messaging house (Methods). Use each pillar's `## Collection Tables` to identify every collection file the feedback touches. Load full collection files for confirmed matches. The impact trace is exhaustive — the user needs the full blast radius before approving.

### Step 3: Propose changes

For each impacted doc:

```
## Proposed Changes

### 1. [doc path] ([HIGH | MEDIUM | LOW] impact)

**Section:** [exact section path]
**Current:** [current text]
**Proposed:** [proposed text]
**Reasoning:** [why this change follows from the feedback]
```

Include a **Downstream Effects** section noting:
- Whether calibration in pillar Brand Voice or persona Messaging Guidance sections needs refresh (run `/design pillar profile` or `/design persona [slug]`)
- Whether active campaigns / launches / plays may be affected (check `output/` for in-progress work)
- Whether the canonical glossary in MESSAGE.md needs updating

### Step 4: User approval

Present the full proposal with a summary (affected docs by impact tier, downstream effects). User can: Approve all / Approve selectively / Edit / Reject / Defer.

### Step 5: Execute

After approval:

1. Make approved changes to each messaging doc. Set `updated` to today's date.
2. Append a journal entry to `output/journal.md` documenting the feedback, learning, and actions taken.
3. Note downstream effects that need follow-up.

For rejected feedback: journal entry "Rejected — [reason]." For deferred: journal entry "Deferred — [reason]," append a tracker row (source `feedback:signal`, severity from impact, status `deferred`), write findings file.

### Feedback principles

- Feedback is a signal, not a directive. One rep's anecdote ≠ a pattern across five deals.
- Trace the full impact before proposing changes. A persona's Lead With affects every skill targeting that persona.
- Propose specific text changes, not vague directions. "Update CISO messaging" is not actionable; "Change Lead With from X to Y" is.
- When feedback contradicts established messaging, surface the tension explicitly.
- Log everything. Even rejected feedback gets a journal entry — it may matter later.
- Never modify messaging docs without explicit user approval.

---

## Review Mode

Tracker dashboard + health check summary + insight state transitions.

1. Read `insights/tracker.md`. Run auto-resolution (Tracker Management).
2. Run all 7 health checks. Collect findings.
3. Present dashboard:
   - Source breakdown by source prefix
   - Counts by status (open, acknowledged, deferred, resolved)
   - Recent open insights (last 30 days)
   - Stale deferrals
   - Health check summary: `[N] checks run | [N] critical | [N] warning | [N] info | [N] passed`
4. For open insights, present each with messaging impact; ask user to acknowledge / defer / resolve.
5. Update tracker with state transitions.

---

## Health Checks

Seven checks validate messaging-system integrity. Run automatically during Review Mode, or standalone via `/run investigation fix [check]` and `/run investigation report`. All checks use the Methods section above.

### Check 1: Gap — what's missing?

- **Pillar existence.** All 6 pillar files exist and are non-empty. Severity: critical.
- **Section structure.** Each pillar has `## Messaging Blocks`, `## Writing Guidelines`. Position/People/Portfolio/Proof also have `## Collection Tables`. Severity: warning.
- **Pillar subsections.** Every subsection defined in the corresponding template exists in the pillar doc. Severity: warning.
- **Collection population.** At least one file in `personas/`, `products/`, `competitors/`. Severity: warning if empty.
- **Glossary populated.** The glossary block in `profile.md` has at least one row. Severity: warning if empty.
- **Collection Tables rows.** Each pillar's `## Collection Tables` has at least one data row when collections exist. Severity: warning if empty.
- **Substantive content.** Sections contain more than scaffold placeholder text. Look for unreplaced `[Instructions:]` / `[Tips:]` blocks. Severity: warning if placeholder only.

### Check 2: Relationship — do all links resolve?

- **Table-to-file.** Every row in a pillar Collection Table has a matching file in the collection directory. Severity: critical if broken.
- **File-to-table.** Every collection file has a corresponding row in its parent pillar's table. Severity: warning if orphaned.
- **Description quality.** Description columns are populated and differentiated from siblings. Severity: warning.
- **Description sync.** Collection frontmatter `description` matches the table Description. Severity: warning if mismatched.
- **Frontmatter cross-references.** Validate referenced files exist: `story.products[]`, `story.personas[]`, `story.segments[]`; `solution.products[]`; `product.parent`; `competitor.category_overlap[]`; `category.related_categories[]`. Severity: critical if broken.

### Check 3: Schema — does each file follow its template?

- **Required frontmatter.** All required fields from the template are present. Severity: warning if missing.
- **Enum validation.** Constrained fields use valid options (e.g., `stage: emerging|growth|established`, `type: buyer|user|champion|blocker`, story `status`, category `maturity`/`trajectory`, solution `scope`/`theme`). Severity: critical if invalid.
- **Updated field.** Present and valid ISO date (YYYY-MM-DD). Severity: warning if missing/invalid.
- **Filename convention.** Pillar and collection files follow kebab-case. Severity: warning if non-kebab.
- **Array fields.** Fields that should be arrays per the template are arrays, not strings. Severity: warning if wrong type.

### Check 4: Freshness — what's stale?

- **Pillar freshness.** Pillar files with `updated` older than 90 days. Severity: warning.
- **Collection freshness.** Collection files older than 90 days. Severity: info.
- **Story staleness.** Stories with `status: stale` or `updated` older than 18 months. Severity: warning.
- **Pillar-collection drift.** Pillar older than its newest child collection — reference table may be out of sync. Severity: warning.
- **Proof-story drift.** `proof.md` older than the most recent story file. Severity: warning.

### Check 5: Glossary — is terminology healthy?

**Diagnostic mode (default):**

- **Missing terms.** Scan all `## Messaging Blocks` for high-frequency company-specific terms (apply Selection Criteria). Report terms appearing frequently with company-specific meaning but absent from the glossary. Severity: warning.
- **Stale entries.** Glossary terms that no longer appear in the messaging house. Severity: info.
- **Definition drift.** Glossary definitions no longer matching usage. Severity: warning.
- **Terminology conflicts.** Same concept under different terms, or same term under different meanings. Severity: critical.

**Fix mode (`/run investigation fix glossary`):**

After diagnostic, perform full glossary maintenance. The canonical glossary lives in MESSAGE.md's `## Glossary` section.

1. Apply Selection Criteria to candidate terms.
2. Generate definitions for missing terms (1-3 sentences, grounded in messaging docs).
3. Draft updated definitions for drifted entries.
4. Identify entries to remove (no longer in messaging house).
5. Present structured diff:

```
Glossary Update

Added (N):     + [term] — [definition]
Updated (N):   ~ [term] — [reason]
Removed (N):   - [term] — [reason]
Conflicts (N): ! "[term]" — [inconsistency]. Recommend [recommendation].

Total: N terms (was N)
```

6. Write after user approval.

**Selection criteria.**

- **Include:** Terms unique to the company's messaging — coined terms, proprietary concepts, definitions that differ from standard industry usage.
- **Exclude:** Standard industry terms; individual product / UVP / solution / competitor / persona / category names (those live in their dedicated files); single-doc terms; universal acronyms; messaging-system structural terms ("Walk Away Feeling," "Brand Pillars," "Messaging Blocks," etc.); generic marketing concepts ("value proposition," "use case," "differentiation").
- **Litmus test:** Would a new writer encounter this term in customer-facing content and need to understand the company's specific definition?
- **Target:** 15-40 well-defined terms. More than 50 suggests standard terms are being included.
- Every definition traces to at least one messaging doc.

**Writing conventions.**

- Definitions are 1-3 sentences.
- Present tense, declarative: "[Term] is..." not "[Term] refers to..."
- Grounded in company context: "[Term] is [Company]'s approach to..." not "[Term] is an industry practice that..."
- Sorted alphabetically. Each entry: definition, context, see also.

**Conflict resolution.** Don't silently resolve by picking one usage. Present both with sources. Recommend canonical, with reasoning. User decides; then updates source docs to match.

### Check 6: Profile — is context in sync?

- **Profile block exists.** `/MESSAGE.md` Writing Profile Block contains content between markers. Severity: warning if missing/placeholder.
- **Profile-frontmatter sync.** Writing-profile `stage`, `market`, `company` match `profile.md` frontmatter. Severity: warning if out of sync.
- **Company name consistency.** Company name in `profile.md` `title` matches usage across other docs. Severity: warning if inconsistent.
- **Stage-proof alignment.** Emerging-stage company shouldn't claim established-level proof. Check `proof.md` claims against `profile.md` stage. Severity: warning if mismatched.

### Check 7: Journal — is the feedback loop healthy?

- **Journal exists.** `output/journal.md` exists. Severity: info if missing.
- **Entry count.** Entries in last 90 days. Severity: info.
- **Type distribution.** Breakdown by type (content, process, voice, terminology). Severity: info.
- **Deferred entries.** Actions containing "deferred" or "logged" older than 60 days. Severity: info.

All journal check findings are info severity — the journal is an optional feedback loop.

---

## Fix Mode

Standalone remediation via `/run investigation fix [check]`. Runs the named check(s) and categorizes findings.

**Fixable (with user approval):**
- Add missing pillar table rows for existing collection files
- Glossary add/update/remove (see Glossary Check fix mode)
- Add missing `updated` field (set to today's date)
- Fix filename casing (rename to kebab-case)
- Sync Writing Profile Block in MESSAGE.md from `profile.md` frontmatter

**Diagnostic-only (require human judgment):**
- Missing pillar content or thin sections
- Broken cross-references (requires knowing the correct target)
- Wrong enum values (requires choosing the right value)
- Outdated content (requires subject-matter knowledge)
- Stage/proof mismatches (requires strategic decision)

Present fixable items as a list with proposed fixes; user approves all / selectively / skip. Write after approval.

---

## Report Mode

Full health report via `/run investigation report`. Runs all 7 checks; writes results to `output/health-report.md`.

```
Messaging System Health Report
Date: [ISO date]

Summary: [N] checks run | [N] critical | [N] warning | [N] info | [N] passed

Gap Check: [PASS | N findings]
  [severity] [finding]

[... one block per check ...]
```

Conversation mode caps at top 5 findings per check (priority by severity). Report mode includes all findings.

---

## Findings Output Format

All findings files use this frontmatter:

```yaml
---
title: "Scan: 2026-03-10"  # or "Investigation: Competitor Acme Corp" or "Health: 2026-03-10"
source: investigate:scan   # or investigate:targeted, investigate:health, investigate:feedback
scope: broad               # or "competitor acme-corp" or "health:gap,relationship"
date: 2026-03-10
domains_searched: [competitive, market, audience, proof, technology, gtm]
insights_created: 3
insights_updated: 1
insights_resolved: 0
---
```

Body sections:
- **Summary** — key findings overview
- **Detailed Findings** — each finding with severity, type, messaging impact, sources
- **Coverage Gaps** — unavailable MCP sources, domains skipped
- **Tracker Updates** — what changed in the tracker
- **Recommended Actions** — `/design` commands and next steps

### Tracker Updates footer

Every findings file ends with:

```markdown
## Tracker Updates
- Created: INS-005, INS-006, INS-007
- Updated: INS-002 (recurring — last_seen updated)
- Auto-resolved: INS-001 (position.md updated 2026-03-09)
- Stale deferrals: INS-003 (deferred 30+ days, no doc update)
```

---

## Journal Logging

If an investigation surfaces messaging effectiveness learnings beyond external signals — patterns in how messaging is landing, gaps between what the messaging house says and what the market reflects — append a journal entry to `output/journal.md`. Use a type matching the insight domain (content, voice, terminology, process). Skip if findings are purely external signals already in the tracker.

---

## Configuration

Read `insights/config.md` for: enabled domains, investigation cadence, watchlists, MCP source list, severity thresholds.

---

## Tool Scoping

- **Read** — `MESSAGE.md`, `messaging/`, `templates/`, `output/campaigns|launches|plays/` (drift detection), `output/research/` (researcher subagent output), `insights/`
- **Write, Edit** — `messaging/` (user approval required for feedback changes; glossary autonomous after approval in fix-glossary mode), `output/journal.md` (autonomous after approved changes), `insights/tracker.md` and `insights/findings/` (autonomous), `output/health-report.md` (autonomous in report mode)
- **Agent(researcher)** — Dispatched for scan and target modes to isolate web-search/web-fetch context from the orchestrator window
- **Glob, Grep** — Full access (impact tracing, health checks, glossary analysis, cross-reference validation)
- **AskUserQuestion** — Clarifying questions during feedback parsing, approval flow during feedback proposals, insight state management during review
