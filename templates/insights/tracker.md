---
title: Insight Tracker
updated: 2026-03-06
---

## Lifecycle

```
open -> acknowledged -> resolved
         |
       deferred
```

**open** — New insight from a scan, health check, or logged signal. Not yet reviewed.
**acknowledged** — Reviewed and accepted as relevant. Action pending.
**deferred** — Relevant but not actionable now. Will resurface on next review.
**resolved** — Addressed by updating the relevant messaging doc, or determined to be not actionable.

Insights auto-resolve when the underlying messaging doc's `updated` date is newer than the insight date.

## ID Convention

Insights use sequential IDs: `INS-001`, `INS-002`, etc. Agents read the tracker to find the highest existing ID before appending new insights.

## Source Convention

Source uses `[agent]:[mode]` format to identify the contributing agent and its operating mode:

| Agent | Source values |
|---|---|
| investigate | `investigate:scan`, `investigate:targeted` |
| health | `health:check`, `health:fix` |
| feedback | `feedback:signal`, `feedback:log` |

## Severity Scale

Four unified levels across all contributing agents:

| Level | Meaning |
|---|---|
| critical | Requires immediate attention — broken references, contradictory messaging, system integrity failures |
| warning | Should be addressed soon — stale content, missing sections, positioning drift |
| opportunity | Actionable improvement — new proof points, market shifts, positioning gaps to exploit |
| info | Informational — context for future decisions, no action required |

## Tracker

| ID | Date | Source | Severity | Insight | Messaging Doc | Status | Resolved Date | Resolution |
|---|---|---|---|---|---|---|---|---|
