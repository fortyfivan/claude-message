# Messaging Insights Tracker

Rolling tracker of messaging intelligence insights. Updated by the research agent during scans.

## Lifecycle

```
open → acknowledged → resolved
         ↓
       deferred
```

- **Open** — Newly surfaced insight requiring review
- **Acknowledged** — Reviewed by user, stays active for monitoring
- **Deferred** — Parked for later review (includes review date)
- **Resolved** — Messaging updated or signal determined irrelevant

## Auto-Resolution

The research agent auto-resolves insights when the underlying messaging doc has been updated after the insight was created. Users manage judgment calls (acknowledge, defer, resolve) manually.

## Open Insights

<!-- New insights are appended here by the research agent -->

## Acknowledged

<!-- Insights the user has reviewed but not yet resolved -->

## Deferred

<!-- Insights parked for later review -->

## Resolved

<!-- Resolved insights (auto-resolved or manually closed) -->
