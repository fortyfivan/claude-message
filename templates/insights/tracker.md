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

**open** — New insight from a scan. Not yet reviewed.
**acknowledged** — Reviewed and accepted as relevant. Action pending.
**deferred** — Relevant but not actionable now. Will resurface on next scan.
**resolved** — Addressed by updating the relevant messaging doc, or determined to be not actionable.

Insights auto-resolve when the underlying messaging doc's `updated` date is newer than the insight date.

## ID Convention

Insights use sequential IDs: `INS-001`, `INS-002`, etc. The investigate agent reads the tracker to find the highest existing ID before appending new insights.

## Tracker

| ID | Date | Source | Insight | Messaging Doc | Status | Resolved Date | Resolution |
|---|---|---|---|---|---|---|---|
