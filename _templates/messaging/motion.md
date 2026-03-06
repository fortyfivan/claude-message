---
title: ""
primary_motion: ""  # sales-led | product-led | partner-led | community-led | event-led
secondary_motions: []
updated: ""
---

# Motion

This pillar defines how the company goes to market — the selling motion, the channels, the plays, and the repeatable campaign patterns that turn messaging into pipeline. The primary motion shapes everything downstream. A sales-led company produces different content at different depths with different CTAs than a product-led company. 

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

### Channel Strategy

[Instructions:
Describe how messaging is distributed across channels. For each channel, define its role in the GTM motion, the content types that live there, the audience it reaches, and any constraints that affect content creation.]

[Tips:
- Distinguish between primary channels (where you invest most) and supporting channels
- Constraints matter for the tune agent — LinkedIn has character limits and algorithmic preferences, email has deliverability considerations, blog has SEO requirements
- Cadence helps the campaign agent plan — weekly blog, daily social, monthly webinar, etc.]

[Format:
For each channel:
- **Channel:** [name]
- **Role:** [primary | supporting | experimental]
- **Audience:** [who you reach here]
- **Content types:** [what lives on this channel]
- **Cadence:** [frequency of publishing or engagement]
- **Constraints:** [character limits, format requirements, algorithmic preferences, deliverability rules]]

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

## Writing Guidelines

- Primary motion determines CTA defaults across the system — sales-led leads with demo/conversation, product-led leads with trial/self-serve, partner-led leads with joint engagement, event-led leads with registration/meeting
- Content depth follows motion — sales-led content tends longer and more comprehensive (the reader is evaluating), product-led content tends shorter and more action-oriented (get to the "try it" moment fast)
- Plays are the most targeted form of messaging — load the relevant play profile when content is tied to a specific buyer scenario or competitive situation
- Plays should not be loaded for broad awareness or thought leadership content — those should draw from Space and Profile, not motion-specific narratives
- Channel constraints are hard rules — do not generate content that violates the character limits, format requirements, or deliverability rules defined in Channel Strategy
- Campaign playbooks are starting points, not mandates — the campaign agent uses them as defaults but the user can customize the asset list and sequence
- When motions conflict with persona preferences (e.g., a sales-led motion targeting a developer persona who prefers self-serve), defer to persona — adapt the CTA and engagement model to the audience while maintaining the motion's overall structure

## Messaging Rules

[Instructions:
This section is populated during bootstrap with company-specific rules about how the messaging in this document should be applied. These rules encode positioning decisions, constraints, and strategic choices unique to the company.

Writing Guidelines (above) tell agents how to interpret the document structure. Messaging Rules tell agents what company-specific constraints to honor when using the content.]