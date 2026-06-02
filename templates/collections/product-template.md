---
title: ""
description: ""
type: ""  # platform | product | module | add-on | service
parent: ""  # slug of parent product, if module or add-on (optional)
status: ""  # ga | beta | planned | deprecated
updated: ""
---

# Product: [Name]

This profile defines how to message a specific product — what it does, how it's different, and who it's for. Product profiles are loaded by the writer agent when content requires product-level specificity. For portfolio-level or solution-level messaging, use portfolio.md or the relevant solution profile instead.

## Messaging Blocks

### Overview

[Instructions:
Establish the essential identity of this product — what it is in one sentence, and the practical reference links.]

[Tips:
- The tagline should be usable as-is in product pages, listing descriptions, and briefs
- Category should match a category profile in `messaging/collections/categories/` if one exists]

[Format:
- **Tagline:** [one-liner description]
- **Category:** [market category it fits]
- **Pricing model:** [per-product model if different from portfolio default — freemium | per-seat | platform | usage | contact-sales]
- **Web:** [public-facing product page]
- **Docs:** [public-facing documentation]]

### Use Cases

[Instructions:
The jobs-to-be-done this product helps customers accomplish. Each use case should describe a real scenario, not a capability. "Continuously monitor external attack surface for unknown assets" is a use case. "Asset discovery" is a capability.]

[Tips:
- Use cases should connect to persona pain points — if a use case doesn't map to a challenge a defined persona has, it may not belong in messaging
- If a use case is substantial enough to have its own messaging (distinct audience, distinct proof, distinct value framing), it should be a solution profile instead]

[Format:
Bulleted list — each use case is one scenario described from the buyer's perspective]

### Capabilities

[Instructions:
The critical capabilities that drive value — not a feature matrix. Distinguish between unique capabilities (things only this product does, or does differently than alternatives) and core capabilities (table stakes that buyers expect).]

[Tips:
- Unique capabilities are what the writer leads with in competitive and differentiation content
- Core capabilities are included in comprehensive content (product pages, datasheets) but don't lead the narrative
- Every unique capability should be provable — if you can't point to product evidence or customer proof, it's aspirational]

[Format:
**Unique Capabilities**
- [capability] — [why it's unique]

**Core Capabilities**
- [capability]]

### Architecture

[Instructions:
How the product works at a structural level — deployment model, integration approach, data flow, and technical decisions that affect the buyer. Only invest in this section when architecture is a meaningful differentiator or a common evaluation criterion.]

[Tips:
- Cloud-native vs. on-prem, agent vs. agentless, API-first vs. UI-driven — these are architectural decisions that affect messaging
- If the product's architecture is not a competitive differentiator, keep this section brief
- For modules and add-ons, describe how they integrate with the parent platform]

[Format:
1-2 paragraphs, or a structured breakdown if architecture is a key differentiator:
- **Deployment:** [how it's deployed]
- **Integration:** [how it connects to the customer's environment]
- **Data:** [what data it ingests, generates, or connects]]

### Differentiation

[Instructions:
How this product is different from the alternatives buyers evaluate. These should derive from the key differentiators defined in pitch.md, made specific to this product. Each differentiation point should contrast the alternative approach with yours.]

[Tips:
- Frame as approach contrast, not feature comparison — "Unlike [alternative approach], we [our approach]" 
- Multiple differentiation points are expected — most products differentiate on 2-4 dimensions
- Connect each point back to a capability (ideally a unique capability) that makes the differentiation real]

[Format:
For each differentiation point:
- **Unlike:** [alternative approach or competitor pattern]
- **We:** [our unique approach]
- **Backed by:** [the capability or architecture decision that makes this real]]

### Value Messages

[Instructions:
3-5 specific messages conveying why this product is different and what unique value it delivers. These should be usable in content as-is — specific enough to resonate, grounded enough to be credible.]

[Tips:
- Each message should trace to a use case, unique capability, or differentiation point above
- Messages should work at this product's altitude — don't restate portfolio-level or company-level claims here
- If this is a module or add-on, at least one message should articulate the value of this product within the parent platform context]

[Format:
Numbered list of 3-5 messages]

### Personas Aligned

[Instructions:
Which personas this product is relevant to and why. "Why It Matters" should capture what this specific product means to this specific persona — not the general value proposition, but the product-level relevance.]

[Format:
| Persona | File | Why It Matters |
|---|---|---|
| | | |]

### Product Proof

[Instructions:
Proof points specific to this product — customer results, deployment metrics, benchmarks, or testimonials that reference this product specifically. Portfolio-wide proof lives in proof.md; this section captures what's attributable to this product alone.]

[Tips:
- If this product is new (beta or recently GA), proof may be thin — note what exists and what's in progress
- Reference quotes from `messaging/collections/stories/` if they're product-specific]

[Format:
Bulleted list of proof points, each with source or attribution]

## Writing Guidelines

[Instructions:
Populated during bootstrap with 3-5 rules for how this document's messaging should be applied — interpretation calls, constraints, and strategic choices unique to this company.

Encode only what is specific to this company and not derivable from the content itself or the system architecture. Cut anything generic: if a competitor could write the same rule for their own messaging system, it doesn't belong here. Favor rules that change what an agent produces — what to lead with, what to avoid leading with, which claims are off-limits, and what to defer to when sources conflict.]

[Format:
3-5 bullets]