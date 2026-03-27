---
title: ""
description: ""
products: []
personas: []
segments: []
status: ""  # approved | draft | stale
updated: ""
---

# Story: [Name]

This profile captures a customer's proof arc — who they are, what they were dealing with, why they acted, what they achieved, and the specific quotes that can be embedded directly in content. Stories are the primary proof artifacts in the messaging system.

## Messaging Blocks 

### Customer Profile

[Instructions:
The essential facts about this customer — enough context to assess whether the story is relevant for a given persona, segment, or product without reading the full narrative.]

[Format:
- **Company:** [name or anonymized descriptor]
- **Industry:** [vertical]
- **Size:** [employee count or revenue range]
- **Region:** [geography]
- **Environment:** [relevant technical or operational context — what they had in place before]]

### Scenario

[Instructions:
What the customer was dealing with before they engaged — the conditions, pressures, and constraints that made the status quo untenable. Write from the customer's perspective. This should feel recognizable to the target persona.]

[Tips:
- Ground in specifics — "managing 12,000 assets across 4 cloud providers with a team of 3" not "struggling with scale"
- Connect to persona pain points — the scenario should map to challenges defined in at least one persona profile]

[Format:
1-2 paragraphs in narrative form]

### Why They Acted

[Instructions:
The compelling event, inflection point, or initiative that moved them from "we know this is a problem" to "we're solving it now." This is the urgency trigger — distinct from the ongoing pain described in Scenario.]

[Tips:
- Good triggers: audit finding, board mandate, security incident, compliance deadline, contract renewal, team scaling
- This connects to the Maturity section in audience.md — the "what moves them forward" at whatever level this customer was at]

[Format:
1 paragraph describing the trigger]

### Outcome

[Instructions:
The measurable results — quantitative and qualitative — that the customer achieved. Before/after framing makes the impact concrete. Outcomes should support the Value Evidence metrics in proof.md.]

[Tips:
- Quantitative outcomes should be specific: "reduced from X to Y" or "achieved Z% improvement" — not "significant improvement"
- Qualitative outcomes should describe observable operational changes, not feelings
- If outcomes are partial or early (customer is still in deployment), say so]

[Format:
**Before:** [the measurable state before]
**After:** [the measurable state after]

**Quantitative**
- [specific metric and result]

**Qualitative**
- [observable operational change]]

### Quotes

[Instructions:
The specific, attributed statements from this customer that can be embedded directly in content — emails, social posts, landing pages, battlecards, sales decks. Each quote should be tagged with the messaging context it's best used in so the writer can filter without reading the full story.

Quotes are the atomic proof unit. A customer story is the narrative arc. A quote is the fragment that gets pulled out and dropped into content.]

[Tips:
- Each quote should stand on its own without requiring the full story context
- Tag with persona and product relevance — a quote about risk reduction tagged to CISO + vuln-mgmt is instantly filterable
- Note approval status — has the customer approved this specific quote for external use?
- A good story has 2-5 usable quotes; more than that and you're probably including filler]

[Format:
For each quote:
- **Quote:** "[exact words]"
- **Speaker:** [name, title]
- **Context:** [what the quote is about — the claim it supports]
- **Best for:** [personas, products, journey stages, or content types where this quote lands hardest]
- **Approved:** [yes | pending | internal-only]]

## Writing Guidelines

- Quotes must be exact — do not paraphrase or adapt attributed statements. If the exact words don't fit the context, choose a different quote
- Approval status is a hard constraint — only quotes marked "approved" can appear in external content. "Pending" and "internal-only" quotes are for sales enablement and internal use only
- Story relevance is determined by the frontmatter tags (products, personas, segments) — keep these current so the writer can filter efficiently
- Stories age — flag profiles as "stale" when the outcomes are more than 18 months old or when the customer's situation has materially changed. Stale stories can still be used but should be supplemented with current proof
- Each story should support at least one Value Evidence metric from proof.md — a story that doesn't connect to a measurable claim is an anecdote, not proof
- Before/after framing is always stronger than standalone metrics — use it whenever the data supports it

## Messaging Rules

[Instructions:
This section is populated during bootstrap with company-specific rules about how the messaging in this document should be applied. These rules encode positioning decisions, constraints, and strategic choices unique to the company.

Writing Guidelines (above) tell agents how to interpret the document structure. Messaging Rules tell agents what company-specific constraints to honor when using the content.]
