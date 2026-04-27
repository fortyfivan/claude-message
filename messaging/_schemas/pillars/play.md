---
title: ""
updated: ""
---

# Play

This pillar defines how the company goes to market — the selling motion, the channels, the plays that turn messaging into pipeline, and the signals that trigger them. The primary motion shapes everything downstream. A sales-led company produces different content at different depths with different CTAs than a product-led company.

## Messaging Blocks

### GTM Overview

[Instructions:
Describe the primary go-to-market approach — how the company acquires, converts, and expands customers. This should cover the selling motion balance, acquisition model, and expansion strategy.]

[Tips:
- Be honest about the primary motion — most companies have one dominant motion with supporting secondary motions
- The motion determines content depth, CTA defaults, and campaign structure across the entire system
- If the motion is shifting (e.g., moving from sales-led to PLG), note the current state and the target state]

[Format:
- **Primary motion:** [sales-led | product-led | partner-led | community-led | event-led]
- **Acquisition model:** [how you get customers in the door — inbound, outbound, PLG, channel, hybrid]
- **Conversion model:** [how prospects become customers — demo→close, trial→convert, freemium→upgrade, partner-referred]
- **Expansion model:** [how customers grow — land-and-expand, upsell modules, cross-sell products, usage growth]

1-2 paragraphs expanding on how these work together]

### Plays

Plays are reusable messaging narratives tied to specific buyer situations, competitive scenarios, or strategic initiatives. Each play explains when the motion applies, why it matters, and how value is created. When specific plays are related to your task, extract the respective profile in `messaging/plays/`.

| Play | File | Type | Status | Description |
|---|---|---|---|---|
| | | | | |

[Instructions:
Document plays as discrete profiles in `messaging/plays/[play-name].md`. The table serves as a reference index. Description should lead with the trigger condition and capture the play's strategic intent — one sentence (~15 words).]

[Tips:
- Type: competitive | expansion | displacement | new-logo | retention | event | partner
- Status: active | draft | retired]

### Signals

Signals are the compelling events that trigger plays — regulatory changes, competitor moves, industry incidents, account-level behavioral shifts, news cycles. Each signal classifies an event pattern and suggests which plays to deploy in response. When a signal fires for an account or moment, extract the respective profile in `messaging/signals/`.

| Signal | File | Type | Description |
|---|---|---|---|
| | | | |

[Instructions:
Document signals as discrete profiles in `messaging/signals/[signal-name].md`. The table serves as a reference index. Description should lead with the event pattern and what it indicates — one sentence (~15 words).]

[Tips:
- Type: regulatory | competitive | incident | behavioral | news | partner | seasonal
- Pair signals with plays explicitly via the `plays[]` relationship array — a signal without a recommended play has no operational use]

## Writing Guidelines

- Primary motion determines CTA defaults across the system — sales-led leads with demo/conversation, product-led leads with trial/self-serve, partner-led leads with joint engagement, event-led leads with registration/meeting
- Content depth follows motion — sales-led content tends longer and more comprehensive (the reader is evaluating), product-led content tends shorter and more action-oriented (get to the "try it" moment fast)
- Plays are the most targeted form of messaging — load the relevant play profile when content is tied to a specific buyer scenario or competitive situation
- Plays should not be loaded for broad awareness or thought leadership content — those should draw from Position and Pitch, not play-specific narratives
- Signals trigger plays — when content responds to a compelling event, load the matching signal profile and the plays it references via `plays[]`
- When motions conflict with persona preferences (e.g., a sales-led motion targeting a developer persona who prefers self-serve), defer to persona — adapt the CTA and engagement model to the audience while maintaining the motion's overall structure

## Messaging Rules

[Instructions:
This section is populated during bootstrap with company-specific rules about how the messaging in this document should be applied. These rules encode positioning decisions, constraints, and strategic choices unique to the company.

Keep to 3-5 rules. Only encode constraints that are genuinely unique to this company and not derivable from the messaging content itself.

Writing Guidelines (above) tell agents how to interpret the document structure. Messaging Rules tell agents what company-specific constraints to honor when using the content.]