---
name: investigate
description: A unified messaging system intelligence engine. Performs external research, processes field feedback, inspects and validates the system, and manages the lifecycle os messaging insights. Invoked via command. Load if the user is looking for insights or has questions about the messaging system.
---

# Investigate Skill

Unified intelligence and system health workflow. Consolidates external research, field feedback processing, system health validation, and insight lifecycle management into a single skill.

Invoked via `/investigate [mode]`.

## Modes

| Mode | Invocation | Purpose |
|---|---|---|
| Scan | `/investigate scan` | Broad investigation across all enabled domains |
| Target | `/investigate target [type] [name]` | Focused investigation of a specific entity |
| Feedback | `/investigate feedback [input]` or `--log` | Process field signals into messaging changes |
| Review | `/investigate review` or `/investigate` | Tracker dashboard + health check summary |
| Fix | `/investigate fix [check]` | Health check remediation |
| Report | `/investigate report` | Full health report to output/ |
| State mgmt | `/investigate acknowledge/defer/resolve [ID]` | Direct insight state transitions |

---

## Scan Mode

Broad investigation across all enabled domains.

1. Read `insights/config.md` for enabled domains, thresholds, and watchlists.
2. Read `insights/tracker.md` for open insights. Run auto-resolution check (see Tracker Management below).
3. Dispatch the researcher agent with scope=broad and the enabled domains from config. Pass open insights context so the researcher can avoid surfacing duplicates.
4. Process returned findings: assign IDs, detect recurring patterns, check auto-resolution.
5. Write consolidated findings to `insights/findings/scan-YYYY-MM-DD.md`.
6. Update tracker: append new insights as `open`, update recurring insights with `last_seen`, auto-resolve stale insights.
7. Log to journal if findings include messaging effectiveness learnings (see Journal Logging below).
8. Present summary to user with key findings, tracker updates, and recommended actions.
9. **Produced asset drift summary.** Check all produced asset locations for messaging drift:

   **Artifacts.** If `artifacts/` exists, scan for subdirectories with `manifest.md`. Read each manifest's frontmatter and compare dependency `updated` dates against `last_updated`. An empty `last_updated` means "not yet produced."

   **Campaigns.** If `output/campaigns/` exists, scan for subdirectories with `brief.md`. Read each brief's `shared_context.messaging_docs_loaded` and compare doc `updated` dates against `created`. Skip campaigns with `status: in-progress`.

   **Launches.** Same as campaigns but in `output/launches/`.

   **Standalone assets.** If `output/assets/` exists, scan for `.md` files with `messaging_docs_loaded` frontmatter. Compare doc `updated` dates against `generated`.

   Append a grouped summary to the scan output:

   ```
   ## Produced Asset Drift

   ARTIFACTS
   | Artifact | Version | Last Updated | Status |
   |---|---|---|---|
   | [title] | [version] | [date or "Never"] | [N dependencies changed / Current / Not yet produced] |

   CAMPAIGNS
   | Campaign | Created | Assets | Status |
   |---|---|---|---|
   | [folder] | [date] | [count] | [N assets affected / Current] |

   LAUNCHES
   | Launch | Created | Assets | Status |
   |---|---|---|---|
   | [name] | [date] | [count] | [N assets affected / Current] |

   STANDALONE ASSETS
   | Asset | Generated | Status |
   |---|---|---|
   | [filename] | [date] | [N docs changed / Current] |
   ```

   Omit any section where the directory doesn't exist or contains no assets.

   - For items with detected drift, note: "Run `/update` to review drift across all produced assets, or target a specific item with `/update [slug]`, `/update campaign [folder]`, or `/update launch [name]`."
   - This is read-only — the scan does not modify any assets or manifests.

## Target Mode

Focused investigation of a specific entity.

1. Read `insights/config.md` and `insights/tracker.md` (same as scan).
2. Load the specific collection profile(s) matching the focus entity from the messaging house. Use pillar reference tables to identify the right profile(s).
3. Dispatch the researcher agent with scope=[entity] and relevant domains. A competitor investigation searches competitive moves and technology landscape. A persona investigation searches audience signals. A motion investigation searches GTM & channel signals.
4. Process returned findings: assign IDs, detect recurring patterns.
5. Write findings to `insights/findings/[topic].md`.
6. Update tracker and log to journal.
7. Present findings with specific wording recommendations and compose command suggestions:
   - "Competitor Acme has shifted positioning — run `/compose competitor acme-corp` to update the profile."
   - "The CISO persona's pain points may have shifted — run `/compose persona ciso` to review and update."

## Feedback Mode

Process real-world signals — from sales conversations, campaign performance, customer interactions, market observations — and translate them into proposed changes to the messaging system.

The skill doesn't assume the feedback is correct. It analyzes what was said, traces the impact across the messaging house, proposes specific changes with reasoning, and waits for the user to approve, reject, or iterate.

**Full feedback** (default): Parse input → Read messaging house → Trace impact → Propose changes → User approval → Execute changes + journal entry.

**Log-only** (`--log`): Parse input → Append journal entry with Action: "Logged — no changes proposed." → Write tracker entry (source: `feedback:log`, status: `open`) and findings to `insights/findings/feedback-YYYY-MM-DD.md`.

### Step 1: Parse the Input

Extract the signal from the user's input:

- **What changed** — the observation, data point, or feedback
- **Source** — where this came from (sales, campaign data, customer conversation, analyst briefing, user observation)
- **Confidence** — is this a pattern (multiple sources confirm) or an anecdote (single data point)?

If the input is ambiguous, ask clarifying questions before proceeding — but keep them focused. "Is this something multiple reps are hearing, or one deal?" matters. "Tell me more about the competitive landscape" does not.

**Log-only mode:** Skip Steps 2-4. Go directly to Step 5 and append a journal entry with Action: "Logged — no changes proposed."

### Step 2: Trace the Impact

Read the messaging house — all six pillars (`profile.md`, `space.md`, `audience.md`, `portfolio.md`, `proof.md`, `motion.md`), `glossary.md`, and `messaging/journal.md` (if it exists). Use pillar reference tables to identify every collection profile the feedback touches. Load full profiles for confirmed matches.

The impact trace must be exhaustive across the messaging house — every doc that references the affected concept. The user needs to see the full blast radius before approving changes.

### Step 3: Propose Changes

For each impacted doc, propose a specific change:

```
## Proposed Changes

### 1. [doc path] ([HIGH | MEDIUM | LOW] impact)

**Section:** [exact section path]
**Current:** [current text]
**Proposed:** [proposed text]
**Reasoning:** [why this change follows from the feedback]
```

Each proposed change carries:
- **Doc and section** — exactly where the change happens
- **Current → Proposed** — the specific text change
- **Reasoning** — why this change follows from the feedback
- **Impact level** — HIGH (core messaging guidance), MEDIUM (supporting content), LOW (contextual reference)

Include a **Downstream Effects** section noting:
- Whether skills need re-tuning (run `/tune`)
- Whether active campaigns may be affected (check `output/campaigns/` for in-progress campaigns)
- Whether the glossary needs updating
- Whether calibration patterns in profile.md should be updated (for voice-related feedback)

### Step 4: User Approval

Present the full proposal with a summary:

```
Feedback Impact: [summary]

Affected docs: [count]
  HIGH:   [doc paths]
  MEDIUM: [doc paths]
  LOW:    [doc paths]

Downstream: [effects]

Approve all, approve selectively, edit, reject, or defer?
```

The user can:
- **Approve all** — all changes applied, journal entry appended
- **Approve selectively** — "apply changes 1 and 2, skip 3 and 4"
- **Edit** — "change the proposed key message to [different wording]"
- **Reject** — no changes, but the observation is logged in the journal as a noted signal
- **Defer** — "log this but don't change anything yet — I want to see more data"

### Step 5: Execute

After approval, the skill:

1. Makes the approved changes to each messaging doc. Set `updated` to today's date on each modified file.
2. Appends a journal entry to `messaging/journal.md` documenting the feedback, the learning, and the actions taken. Create the file from `templates/messaging/journal.md` if it doesn't exist.
3. If voice calibration patterns were part of the feedback, update the Calibration Patterns subsection under Brand Voice in `messaging/profile.md`.
4. Notes downstream effects that need follow-up (skill re-tune, campaign updates).

For rejected feedback, append a journal entry with action "Rejected — [reason]."

For deferred feedback, append a journal entry with action "Deferred — [reason]," then also:
1. Read `insights/tracker.md` and find the highest existing ID.
2. Append a tracker row: Source `feedback:signal`, severity mapped from impact (HIGH→critical, MEDIUM→warning, LOW→opportunity), one-line observation as Insight, primary affected doc as Messaging Doc, status `deferred`.
3. Write findings to `insights/findings/feedback-YYYY-MM-DD.md` (append if a file exists for today).

### Calibration Patterns

When feedback is voice-related (how content reads, style preferences, editing patterns), update the Calibration Patterns subsection in `messaging/profile.md` under Brand Voice:

- New patterns start with status "observed"
- Patterns with 3+ observations graduate to "confirmed" (with user approval)
- Patterns the user explicitly confirms as permanent can be promoted to authored Brand Voice sections (Tips & Tricks, Tone, etc.) — change status to "promoted"

### Feedback Principles

- Feedback is a signal, not a directive. Analyze it critically. One rep's anecdote is different from a pattern across five deals.
- Trace the full impact before proposing changes. A change to a persona's Lead With affects every skill that targets that persona and every campaign that includes them.
- Propose specific text changes, not vague directions. "Update the CISO messaging" is not a proposal. "Change Lead With from X to Y" is.
- When feedback contradicts established messaging, surface the tension explicitly. "The feedback says X, but space.md positions us as Y. Changing this would affect our core differentiation. Are you sure?"
- Log everything. Even rejected feedback gets a journal entry — it's a data point that may matter later when more evidence accumulates.
- Do not modify messaging docs without explicit user approval. Present the plan, get the green light, then execute.

---

## Review Mode

Tracker management, health check summary, and insight state transitions.

1. Read `insights/tracker.md`.
2. Run auto-resolution: for each `open` or `acknowledged` insight, compare the referenced messaging doc's `updated` field against the insight Date. If `updated > Date`, mark resolved with Resolution "auto-resolved: [doc] updated [date]."
3. Run all 7 health checks (see Health Checks below). Collect findings.
4. Present dashboard:
   - Source breakdown: count open insights by source prefix (e.g., `investigate:scan: 3 open | investigate:health: 5 open | investigate:feedback: 1 open`)
   - Counts by status (open, acknowledged, deferred, resolved)
   - Recent open insights (last 30 days)
   - Stale deferrals (deferred 30+ days with no messaging doc update)
   - Health check summary: `[N] checks run | [N] critical | [N] warning | [N] info | [N] passed`
5. For open insights: present each with messaging impact, ask user to acknowledge/defer/resolve.
6. Update tracker with all state transitions.

### Direct Actions

Single insight state transition without the full review flow:

| Command | Action |
|---|---|
| `/investigate acknowledge [ID]` | Move insight from open to acknowledged |
| `/investigate defer [ID]` | Move insight to deferred |
| `/investigate resolve [ID]` | Move insight to resolved |

Read the tracker, find the insight by ID, update its Status, Resolved Date (if resolving), and Resolution. Write the updated tracker.

---

## Health Checks

Seven checks validate messaging system integrity. Run automatically during Review mode, or standalone via `/investigate fix [check]` and `/investigate report`.

### Reading the Messaging House

Load all files in `messaging/`:
- Read the six pillar files: `profile.md`, `space.md`, `audience.md`, `portfolio.md`, `proof.md`, `motion.md`
- Read `glossary.md` if it exists
- Enumerate all collection directories: `categories/`, `competitors/`, `personas/`, `plays/`, `products/`, `stories/`, `segments/`, `solutions/`
- For each collection file, read frontmatter (you do not need to read the full body for most checks — frontmatter and section headers suffice)

Build an index of:
- Which pillar files exist and their `updated` dates
- Which collection files exist, their frontmatter fields, and their `updated` dates
- Pillar reference tables (parsed from markdown table syntax) with their Name, Description, and other columns
- Cross-reference fields from collection frontmatter

### Reading Templates

Load template files from `templates/messaging/` to determine:
- Required frontmatter fields per document type
- Valid enum values for constrained fields
- Expected sections within `## Messaging Blocks`
- Three-section structure requirements

### Check 1: Gap Check — What's missing?

Evaluate completeness of the messaging system:

- **Pillar existence.** All 6 pillar files exist and are non-empty. Severity: critical if missing.
- **Three-section structure.** Each pillar has `## Messaging Blocks`, `## Writing Guidelines`, and `## Messaging Rules`. Severity: warning if missing.
- **Template subsections.** Every subsection defined in the corresponding template exists in the pillar doc. Compare the `## Messaging Blocks` subsections in the template against the actual file. Severity: warning if missing.
- **Collection population.** At least one file exists in `personas/`, `products/`, and `competitors/`. Severity: warning if empty.
- **Glossary existence.** `messaging/glossary.md` exists. Severity: warning if missing.
- **Reference table rows.** Pillar reference tables have at least one data row. Severity: warning if empty.
- **Substantive content.** Sections contain more than just template placeholder text or instructions. Look for bracketed instructions (`[Instructions:]`, `[Tips:]`) that were never replaced with real content. Severity: warning if placeholder only.

### Check 2: Relationship Check — Do all links resolve?

Validate cross-references between documents:

- **Table-to-file.** Every row in a pillar reference table has a matching file in the collection directory. Match by name/filename. Severity: critical if broken.
- **File-to-table.** Every collection file has a corresponding row in its parent pillar's reference table. Severity: warning if orphaned.
- **Description quality.** Description columns in pillar reference tables are populated and differentiated from sibling entries. Severity: warning if empty or duplicate.
- **Description sync.** Frontmatter `description` in collection profiles matches the Description column in the parent pillar reference table. Severity: warning if mismatched or if one is populated while the other is empty.
- **Frontmatter cross-references.** Validate that referenced files exist:
  - `story.products[]`, `story.personas[]`, `story.segments[]` → files exist in respective directories
  - `solution.products[]` → files exist in `products/`
  - `play.personas[]`, `play.products[]` → files exist in respective directories
  - `product.parent` → file exists in `products/`
  - `competitor.category_overlap[]` → files exist in `categories/`
  - `category.related_categories[]` → files exist in `categories/`
  - Severity: critical if broken reference.

### Check 3: Schema Check — Does each file follow its template?

Validate structural compliance:

- **Required frontmatter.** All required fields from the template are present. Templates define the minimal set — identity, freshness, routing filters, and relationship arrays. Severity: warning if missing.
- **Enum validation.** Fields with constrained values — in frontmatter or body format lines — use valid options (e.g., `stage: emerging|growth|established`, `type: buyer|user|champion|blocker`, story `status`, category `maturity`/`trajectory`, solution `scope`/`theme`). Severity: critical if invalid.
- **Updated field.** `updated` field is present and contains a valid ISO date (YYYY-MM-DD). Severity: warning if missing or invalid.
- **Filename convention.** All files in `messaging/` follow kebab-case naming. Severity: warning if non-kebab.
- **Array fields.** Fields that should be arrays (per template) are arrays, not strings. Severity: warning if wrong type.

### Check 4: Freshness Check — What's stale?

Evaluate currency of messaging documents:

- **Pillar freshness.** Pillar files with `updated` older than 90 days from today. Severity: warning.
- **Collection freshness.** Collection files with `updated` older than 90 days. Severity: info.
- **Story staleness.** Stories with `status: stale` or `updated` older than 18 months. Severity: warning.
- **Pillar-collection drift.** A pillar doc is older than its newest collection doc — the reference table may be out of sync. Severity: warning.
- **Proof-story drift.** `proof.md` is older than the most recent story file — the pillar may be behind its evidence. Severity: warning.

### Check 5: Glossary Check — Is terminology healthy?

Validates terminology health and, in fix mode, proposes and writes glossary updates.

**Diagnostic mode (default):**

- **Missing terms.** Scan all `## Messaging Blocks` sections across the messaging house for high-frequency company-specific terms. Apply the selection criteria below. Report terms that appear frequently with company-specific meaning but are absent from the glossary. Severity: warning.
- **Stale entries.** Glossary terms that no longer appear in the messaging house or whose usage has shifted significantly. Severity: info.
- **Definition drift.** Glossary definitions that no longer match how terms are used in current messaging docs. Severity: warning.
- **Terminology conflicts.** Same concept referred to by different terms in different docs, or same term used with different meanings. Severity: critical.

**Fix mode (`/investigate fix glossary`):**

When fix is active, after running the diagnostic, perform full glossary maintenance:

1. Apply selection criteria to all candidate terms
2. Generate definitions for missing terms (1-3 sentences, grounded in messaging docs)
3. Draft updated definitions for drifted entries
4. Identify entries to remove (no longer in messaging house)
5. Present changes as a structured diff:

   ```
   Glossary Update

   Added (N):
     + [term] — [definition]

   Updated (N):
     ~ [term] — [reason for update]

   Removed (N):
     - [term] — [reason for removal]

   Conflicts (N):
     ! "[term]" — [description of inconsistent usage across docs].
       Recommend [recommendation].

   Total: N terms (was N)
   ```

6. Write after user approval

**Selection Criteria**

- **Include:** Terms and phrases unique to the company's messaging — coined terms, proprietary concepts, and company-specific definitions that differ from standard industry usage.
- **Exclude:** Standard industry terms (even if used frequently), product names (belong in portfolio.md), category names (belong in space.md), single-document terms that are self-explanatory, internal jargon not in external-facing content, universally understood acronyms, messaging system structural terms (section headers, framework labels, template instructions — e.g., "Walk Away Feeling," "Theme Pillars," "Messaging Blocks," "Value Messages," "Key Differentiators," "Positioning Statement," "Internal Selling," "Primary Goal," "Best Proof"), generic marketing and sales concepts that carry no company-specific meaning (e.g., "value proposition," "use case," "differentiation," "go-to-market," "buying committee").
- **Litmus test:** Would a new writer joining the team encounter this term in customer-facing content and need to understand the company's specific definition to use it correctly?
- **Target range:** 15-40 well-defined terms for most companies. More than 50 suggests standard terms are being included.
- Every definition must trace to at least one messaging doc.

**Writing Conventions**

- Definitions are 1-3 sentences. Longer definitions suggest the term needs its own messaging section.
- Write in present tense, declarative voice. "[Term] is..." not "[Term] refers to..."
- Ground in the company's context. "[Term] is [Company]'s approach to..." not "[Term] is an industry practice that..."
- Entries sorted alphabetically. Each entry follows the standard format: definition, context, see also.

**Conflict Resolution**

- Do not silently resolve conflicts by picking one usage.
- Present both usages with their source documents.
- Recommend which usage should be canonical, with reasoning.
- The user decides — then updates the source documents to match.

### Check 6: Profile Check — Is context in sync?

Validate alignment between the messaging house and the project writing profile:

- **Profile block exists.** The project's CLAUDE.md contains content between `<!-- claude-message:profile:start -->` and `<!-- claude-message:profile:end -->` markers. Severity: warning if missing or contains only the default placeholder.
- **Profile-frontmatter sync.** Values in the writing profile (`stage`, `market`, `company`) match `profile.md` frontmatter. Compare `stage`, `market` fields and the company name from the `title` field. Severity: warning if out of sync.
- **Company name consistency.** Company name in `profile.md` `title` matches usage across other messaging docs. Severity: warning if inconsistent.
- **Stage-proof alignment.** An emerging-stage company shouldn't claim established-level proof (e.g., analyst leadership, large enterprise logos). Check `proof.md` claims against `profile.md` stage. Severity: warning if mismatched.

### Check 7: Journal Check — Is the feedback loop healthy?

- **Journal exists.** `messaging/journal.md` exists. Severity: info if missing.
- **Entry count.** Entries in last 90 days. Severity: info.
- **Type distribution.** Breakdown by type (content, process, voice, terminology). Severity: info.
- **Deferred entries.** Entries with action containing "deferred" or "logged" older than 60 days — may warrant revisiting. Severity: info.
- **Calibration pattern status.** In profile.md Brand Voice, check for Calibration Patterns with status "observed" and 3+ observations — may warrant promotion to "confirmed." Severity: info.
- **Ungraduated patterns.** "confirmed" patterns not referenced in tuned skill metadata. Severity: warning if tune has run but patterns post-date last tune.

Note: All journal check findings use info severity except ungraduated patterns. The journal is an optional feedback loop — its absence or low activity is informational, not a problem.

---

## Fix Mode

Standalone remediation via `/investigate fix [check]`. Runs the named check(s) and categorizes findings.

**Fixable (with user approval):**
- Add missing pillar table rows for existing collection files
- Glossary add/update/remove terms (see Glossary Check fix mode above)
- Add missing `updated` field (set to today's date)
- Fix filename casing (rename to kebab-case)
- Sync profile block in project CLAUDE.md from profile.md frontmatter

**Diagnostic-only (require human judgment):**
- Missing pillar content or thin sections
- Broken cross-references in frontmatter (requires knowing the correct target)
- Wrong enum values (requires choosing the right value)
- Content that's actually outdated (requires subject matter knowledge)
- Stage/proof mismatches (requires strategic decision)

Present fixable items as a list:

```
Fixable Items: N items
  [item] — [proposed fix] — [status: proposed]
```

The user can approve all, approve selectively, or skip. Write only after approval.

---

## Report Mode

Full health report via `/investigate report`. Runs all 7 checks and writes results to `output/health-report.md`.

Format:

```
Messaging System Health Report
Date: [ISO date]

Summary
  [N] checks run | [N] critical | [N] warning | [N] info | [N] passed

Gap Check: [PASS | N findings]
  [severity] [finding description]

Relationship Check: [PASS | N findings]
  [severity] [finding description]

Schema Check: [PASS | N findings]
  [severity] [finding description]

Freshness Check: [PASS | N findings]
  [severity] [finding description]

Glossary Check: [PASS | N findings]
  [severity] [finding description]

Profile Check: [PASS | N findings]
  [severity] [finding description]

Journal Check: [PASS | N findings]
  [severity] [finding description]
```

In conversation mode, cap at top 5 findings per check (prioritize by severity). In report mode, include all findings.

---

## Writing Health Insights to Tracker

After any health check run, write trackable insights for findings that require human judgment or composition work.

1. **Filter.** Only `critical` and `warning` findings qualify. Exclude:
   - `info` findings (journal stats, empty directories, story staleness notifications)
   - Auto-fixable items that fix mode can resolve (missing `updated` field, filename casing, missing table rows for existing files)

2. **Read tracker.** Load `insights/tracker.md` and find the highest existing ID.

3. **Detect recurring.** Check if an existing open insight references the same Messaging Doc with a similar description. If so, update the existing row with `last_seen: [date]` in the Resolution column instead of creating a duplicate.

4. **Append rows.** For each qualifying finding, add a tracker row:
   ```
   | INS-[NNN] | [YYYY-MM-DD] | [investigate:health or investigate:fix] | [severity] | [one-line finding] | [messaging doc path] | open | | |
   ```

5. **Write findings file.** Create `insights/findings/health-YYYY-MM-DD.md` with frontmatter:

   ```yaml
   ---
   title: "Health: YYYY-MM-DD"
   source: investigate:health
   date: YYYY-MM-DD
   checks_run: [gap, relationship, schema, freshness, glossary, profile, journal]
   insights_created: N
   insights_updated: N
   ---
   ```

   Body sections: Summary, Detailed Findings (severity, check name, messaging impact), Tracker Updates.

Skip this step entirely if no findings meet the tracker threshold.

---

## Tracker Management

### ID Generation

Sequential IDs: `INS-001`, `INS-002`, etc. Read `insights/tracker.md` to find the highest existing ID before appending new insights. If no insights exist, start at `INS-001`.

### Row Format

```
| INS-[NNN] | [YYYY-MM-DD] | [investigate:scan or investigate:targeted or investigate:health or investigate:feedback] | [severity] | [one-line finding] | [messaging doc path] | open | | |
```

### Auto-Resolution

For each `open` or `acknowledged` insight, compare the referenced messaging doc's `updated` field (from its YAML frontmatter) against the insight's Date column. If `updated > Date`, mark the insight as resolved:
- Status → `resolved`
- Resolved Date → today's date
- Resolution → "auto-resolved: [doc] updated [date]"

### Recurring Detection

When a new finding matches an existing open insight (same Messaging Doc + similar signal type), update the existing insight rather than creating a duplicate. Add a `last_seen: [date]` note to the Resolution column.

### Stale Deferral Detection

`deferred` insights older than 30 days with no messaging doc update since deferral are flagged in the findings output under a **Stale Deferrals** heading.

---

## Findings Output Format

All findings use the same structure regardless of scope:

```yaml
---
title: "Scan: 2026-03-10"  # or "Investigation: Competitor Acme Corp" or "Health: 2026-03-10"
source: investigate:scan  # or investigate:targeted, investigate:health, investigate:feedback
scope: broad  # or "competitor acme-corp" or "health:gap,relationship"
date: 2026-03-10
domains_searched: [competitive, market, audience, proof, technology, gtm]
insights_created: 3
insights_updated: 1
insights_resolved: 0
---
```

Body sections:
- **Summary** — Key findings overview
- **Detailed Findings** — Each finding with severity, type, messaging impact, and sources
- **Coverage Gaps** — Unavailable MCP sources, domains skipped
- **Tracker Updates** — What changed in the tracker
- **Recommended Actions** — Compose commands and next steps

### Tracker Updates Footer

Every findings file ends with a tracker updates section:

```markdown
## Tracker Updates
- Created: INS-005, INS-006, INS-007
- Updated: INS-002 (recurring — last_seen updated)
- Auto-resolved: INS-001 (space.md updated 2026-03-09)
- Stale deferrals: INS-003 (deferred 30+ days, no doc update)
```

## Journal Logging

If the investigation surfaced messaging effectiveness learnings beyond external signals — patterns in how messaging is landing, gaps between what the messaging house says and what the market reflects — append a journal entry to `messaging/journal.md` (if it exists). Use a type that matches the insight domain (content, voice, terminology, or process). Skip this step if all findings are purely external signals already captured in the tracker.

## Configuration

Read `insights/config.md` for:
- Enabled domains (which of the six domains to search)
- Investigation cadence
- Watchlists (specific entities to always include)
- MCP source list
- Severity thresholds

## Tool Scoping

- **Read** — `messaging/` (full access to trace impact), `output/campaigns/` (check for affected active campaigns), `insights/` (cross-reference with research findings), `templates/messaging/` (reference schemas, journal template for first-use creation)
- **Write, Edit** — `messaging/` (with user approval for feedback changes), `messaging/journal.md` (autonomous after approved changes), `insights/tracker.md` (autonomous), `insights/findings/` (autonomous), `output/health-report.md` (autonomous for report mode)
- **Glob, Grep** — Full access. Used during impact tracing, health checks, glossary analysis, and cross-reference validation.
- **AskUserQuestion** — Clarifying questions during feedback parsing, approval flow during feedback proposals, insight state management during review.
- **Agent** — Dispatches researcher agent for scan and target modes.
- **WebSearch, WebFetch** — Not used directly. External research is delegated to the researcher agent.
