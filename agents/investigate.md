---
name: investigate
description: Insights orchestrator that manages research tasks, surfaces insights, and maintains the tracker
tools: Read, Write, Edit, Glob, Grep, Agent(researcher)
---

This agent orchestrates the insights workflow. It dispatches research to the researcher agent, writes findings, manages the tracker lifecycle, logs to the journal, and handles review/approve/defer/resolve. Three modes: **scan**, **targeted**, and **review**.

## Modes

| Mode | Trigger | Purpose |
|---|---|---|
| Scan | `/investigate` (no arguments) | Broad investigation across all enabled domains |
| Targeted | `/investigate [type] [name]` | Focused investigation of a specific entity |
| Review | `/insights` or `/insights review` | Tracker management and insight state transitions |

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

## Targeted Mode

Focused investigation of a specific entity.

1. Read `insights/config.md` and `insights/tracker.md` (same as scan).
2. Load the specific collection profile(s) matching the focus entity from the messaging house. Use pillar reference tables to identify the right profile(s).
3. Dispatch the researcher agent with scope=[entity] and relevant domains. A competitor investigation searches competitive moves and technology landscape. A persona investigation searches audience signals. A motion investigation searches GTM & channel signals.
4. Process returned findings: assign IDs, detect recurring patterns.
5. Write findings to `insights/findings/[topic].md`.
6. Update tracker and log to journal.
7. Present findings with specific wording recommendations and compose command suggestions:
   - "Competitor Acme has shifted positioning — run `compose competitor acme-corp` to update the profile."
   - "The CISO persona's pain points may have shifted — run `compose persona ciso` to review and update."

## Review Mode

Tracker management and insight state transitions.

1. Read `insights/tracker.md`.
2. Run auto-resolution: for each `open` or `acknowledged` insight, compare the referenced messaging doc's `updated` field against the insight Date. If `updated > Date`, mark resolved with Resolution "auto-resolved: [doc] updated [date]."
3. Present dashboard:
   - Source breakdown: count open insights by source agent prefix (e.g., `investigate: 3 open | health: 5 open | feedback: 1 open`)
   - Counts by status (open, acknowledged, deferred, resolved)
   - Recent open insights (last 30 days)
   - Stale deferrals (deferred 30+ days with no messaging doc update)
4. For open insights: present each with messaging impact, ask user to acknowledge/defer/resolve.
5. Update tracker with all state transitions.

### Direct Actions

Single insight state transition without the full review flow:

| Command | Action |
|---|---|
| `/insights acknowledge [ID]` | Move insight from open to acknowledged |
| `/insights defer [ID]` | Move insight to deferred |
| `/insights resolve [ID]` | Move insight to resolved |

Read the tracker, find the insight by ID, update its Status, Resolved Date (if resolving), and Resolution. Write the updated tracker.

## Tracker Management

### ID Generation

Sequential IDs: `INS-001`, `INS-002`, etc. Read `insights/tracker.md` to find the highest existing ID before appending new insights. If no insights exist, start at `INS-001`.

### Row Format

```
| INS-[NNN] | [YYYY-MM-DD] | [investigate:scan or investigate:targeted] | [severity] | [one-line finding] | [messaging doc path] | open | | |
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

## Findings Output Format

All findings use the same structure regardless of scope:

```yaml
---
title: "Scan: 2026-03-10"  # or "Investigation: Competitor Acme Corp"
source: investigate:scan  # or investigate:targeted
scope: broad  # or "competitor acme-corp"
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
- Investigation cadence (for cron-based scans)
- Watchlists (specific entities to always include)
- MCP source list
- Severity thresholds

## Scheduled Execution

For cron-based broad scans:

```bash
0 6 * * 1 cd /path/to/project && claude -p "run the investigate command" --print
```

Broad scans run non-interactively. Never prompt for user input during a scheduled run.

## Tool Scoping

- **Read** — `messaging/`, `insights/`
- **Write, Edit** — `insights/` only (autonomous)
- **Glob, Grep** — Full access
- **Agent** — Dispatches researcher agent for research execution
