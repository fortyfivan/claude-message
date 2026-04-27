---
title: ""
slug: ""
format: ""  # informational: target downstream rendering (e.g., md, deck, pdf, web)
owner: ""
version: 0.0.0
last_updated: ""
---

# [Artifact Name]

[Instructions: Replace the heading with the artifact's display name. This manifest declares the artifact's dependencies on the messaging house, the conditions that trigger a review, and the section-to-source mapping used by the Update skill to scope changes.]

## Dependencies

[Instructions: List messaging components this artifact draws from. Changes to any of these should trigger a drift review. Use file paths relative to the project root. Add optional filters after a dash to narrow scope within a dependency.]

[Format:
- messaging/[pillar].md
- messaging/[pillar].md — [filter]: [value]
- messaging/[collection]/ — [filter]: [value]]

## Trigger Conditions

[Instructions: Define what warrants a review of this artifact beyond dependency changes. Include competitive triggers, insight severity thresholds, and any scheduled review cadence.]

[Format:
Bulleted list of conditions:
- Any [event type] that affects [scope]
- Insight severity: critical (immediate), warning (next scheduled review)
- Scheduled: [cadence]]

## Structure

[Instructions: Map artifact sections to their messaging sources. The Update skill uses this table to determine which sections are affected by upstream changes and to scope surgical patches vs. full regeneration.]

[Format:
| Section | Source |
|---|---|
| [Section name] | [messaging doc path(s)] |]

## Notes

[Instructions: Context the Update skill should carry across versions — decisions made, sections intentionally excluded, format constraints, special handling instructions. Initially empty for new artifacts.]
