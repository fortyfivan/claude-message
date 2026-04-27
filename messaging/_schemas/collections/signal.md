---
title: ""
description: ""
type: ""  # regulatory | competitive | incident | behavioral | news | partner | seasonal
plays: []
personas: []
updated: ""
---

# Signal: [Name]

This profile defines a compelling event — a market signal that creates urgency for buyers and triggers specific response motions from the company. Signals are the "right time" half of right-message-right-time. When this signal fires for an account, sector, or moment, the linked plays prescribe how to respond. Signals without linked plays have no operational use.

## Messaging Blocks

### Event Pattern

[Instructions:
Define the event class this signal represents. Signals are patterns, not specific incidents — "regulator releases new compliance framework" is a signal; "EU AI Act published Aug 2024" is an instance of that signal.]

[Tips:
- A signal should generalize — if you can only think of one historical instance, the pattern isn't crisp enough
- Be specific about scope — a signal that fires for "any tech company" is too broad; "any FedRAMP-pursuing SaaS company" is sharp
- Signals can be external (regulator, competitor, market) or internal (account behavior, pipeline health) — both belong here]

[Format:
- **Event class:** [what kind of event]
- **Trigger conditions:** [what specifically constitutes a fire]
- **Scope:** [who/what the signal applies to — segment, persona, vertical, geography]
- **Decay:** [how long the signal stays relevant after firing]]

### Detection

[Instructions:
How the company knows the signal has fired. This is the operational piece — without a detection method, signals are vibes.]

[Tips:
- Specify the source — public news, analyst alert, customer disclosure, telemetry, partner notification
- Distinguish detection methods that scale (automated alerts) from those that don't (single sales rep notices)
- If detection requires human judgment (interpretation of an analyst report), say so]

[Format:
- **Source:** [where the signal is detected]
- **Method:** [automated | human-curated | hybrid]
- **Lead time:** [how far in advance of the buyer's response window the signal fires]]

### What It Indicates

[Instructions:
The buyer state inferred when the signal fires. This is the bridge from event to response — what the signal tells you about the buyer's mindset, urgency, or budget.]

[Tips:
- Be honest about confidence — some signals are diagnostic ("they're definitely evaluating"), others are weak ("they might be receptive")
- Map to the buyer's journey — is this an awareness moment, an evaluation moment, an expansion moment?
- Connect to the affected personas via the `personas[]` frontmatter]

[Format:
- **Buyer state:** [what the buyer is doing or feeling when the signal fires]
- **Confidence:** [diagnostic | indicative | weak]
- **Journey stage:** [awareness | consideration | evaluation | expansion | retention]]

### Recommended Response

[Instructions:
The plays to deploy when this signal fires. List each linked play (from `messaging/plays/`) with the rationale for why this play is the right response to this signal.]

[Tips:
- A signal with multiple plays should sequence them — primary response first, secondary if the primary doesn't land
- The rationale matters — a signal-play link without a reason becomes stale fast]

[Format:
For each linked play:
- **Play:** [name and file]
- **Why:** [rationale for this play in response to this signal]
- **Sequence:** [primary | secondary | parallel]]

## Writing Guidelines

- Signals trigger plays — when content responds to a fired signal, load both this signal profile and the linked plays from `plays[]`
- Signal-driven content has a freshness constraint — once the decay window passes, the signal stops creating urgency. Time-bound your assertions accordingly.
- Confidence level governs assertion strength — diagnostic signals justify direct outreach ("we noticed X in your environment"); weak signals only justify thematic content ("companies in your situation often...")
- Do not name specific competitors, customers, or regulators in signal-driven outreach unless the signal explicitly references them and the content respects defamation, privacy, and competitive boundaries
- A signal without a recommended response is a research artifact, not an operational signal — flag for `/investigate fix signal` or remove

## Messaging Rules

[Instructions:
This section is populated during bootstrap with company-specific rules about how the messaging in this document should be applied. These rules encode positioning decisions, constraints, and strategic choices unique to the company.

Writing Guidelines (above) tell agents how to interpret the document structure. Messaging Rules tell agents what company-specific constraints to honor when using the content.]
