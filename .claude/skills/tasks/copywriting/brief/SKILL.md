---
name: brief
description: Create sales enablement and marketing collateral including solution briefs, industry verticals, persona briefs, product datasheets, use case overviews, company overviews, and event companions. Use when the user asks for briefs, one-pagers, datasheets, leave-behinds, sales collateral, or any PDF/document asset for sales or marketing.
---

[Note for the user: tune this skill and the asset types to your requirements - this is a generic example as a starting point]

# Brief Copywriting

## Instructions

1. **Identify Brief Type:** Determine which type applies to the request
2. **Load Type Guide:** Read the corresponding file from `types/`
3. **Review the Brief:** Session should include messaging brief with target audience, objective, and key message
4. **Reference Messaging House:** Extract specific messaging blocks from `/messaging`
5. **Conduct Research (If Needed):** Use WebSearch for industry context, competitive positioning, or validation
6. **Draft Brief Content:** Apply type-specific structure and guidelines from the loaded guide
7. **Self-Assess:** Review against quality signals

## Brief Type Guides

After identifying the brief type, load the corresponding guide:

- **Solution Brief:** See `types/solution-brief.md`
- **Industry Vertical:** See `types/industry-vertical.md`
- **Persona Brief:** See `types/persona-brief.md`
- **Product Datasheet:** See `types/product-datasheet.md`
- **Use Case Overview:** See `types/use-case-overview.md`
- **Company Overview:** See `types/company-overview.md`
- **Event Companion:** See `types/event-companion.md`
- **Session Abstract:** See `types/session-abstract.md`
- **Partner Better Together:** See `types/partner-better-together.md`

## Messaging House Context

Look for the following when referencing messaging elements in `/messaging`:

| Context Type    | What to Extract                                     | Source                         |
|-----------------|-----------------------------------------------------|--------------------------------|
| Persona & Pain  | ICP signals, personas, value messages               | audience.md                    |
| Voice & Tone    | Narrative, brand voice, style guidelines            | profile.md (voice section)     |
| Value Messaging | Core propositions, products, solutions              | space.md, portfolio.md         |
| Market Context  | Industry trends, positioning, competitive landscape | space.md                       |
| Credibility     | Social proof, customer wins, use cases              | proof.md                       |
| GTM Alignment   | Campaign strategy, motion-specific messaging        | motion.md                     |

## Design Principles

- **Scannable in 30 seconds:** Executive skim test—key points visible without reading
- **One takeaway per page:** Don't overload; let each page land a single point
- **Visual hierarchy:** Headlines, subheads, callouts guide the eye
- **Proof in every section:** Data, customer quotes, or specific outcomes
- **Clear CTA:** Reader knows exactly what to do next

## Content Principles

- Lead with the reader's problem, not your product
- Quantify outcomes wherever possible
- Include customer proof or data validation
- Avoid jargon unless audience-appropriate
- Every claim must be supportable

## Tropes to Avoid

- "Leading provider of..." openers
- Feature lists without context
- Generic benefits that apply to any vendor
- Missing or buried CTA
- Inconsistent altitude within the document
- Unsubstantiated superlatives

## Quality Signals

Quality signals for this content type. Use during generation as a compass; the reader agent evaluates against these during review.

```
Brief Quality Signals:
- [ ] Problem-First: Opens with reader's challenge, not product
- [ ] Scannable: Key points visible in 30-second skim
- [ ] Proof Points: Every section includes evidence
- [ ] Outcome Focus: Benefits quantified where possible
- [ ] Altitude Match: Technical depth matches audience
- [ ] CTA Clarity: Clear, specific next step
- [ ] Type Alignment: Follows structure from type guide
```

## Output Format

ALWAYS use this exact template structure:

```markdown
## Brief Specification
**Type:** [Solution brief / Industry vertical / Persona brief / Product datasheet / Use case overview / Company overview / Event companion]
**Target Audience:** [Primary persona and altitude]
**Objective:** [What the reader should do/think/feel after reading]
**Key Message:** [Single most important takeaway]
**Proof Points:** [2-3 evidence items to include]

## Content Outline
[Section-by-section structure following type guide]

## Brief Content
[Full formatted content with headers, callouts, and proof points]

## Design Notes
[Suggestions for visual elements, callout boxes, charts, or imagery]

## Messaging References
- **Audience:** [Link to audience.md section]
- **Value Framework:** [Link to space.md]
- **Proof:** [Link to proof.md]
- **Other:** [Additional references used]

## Self-Assessment
**Problem-First:**    [Notes on grounding and context strength]
**Scannability:**     [Notes on grounding and context strength]
**Proof Points:**     [Notes on grounding and context strength]
**Outcome Focus:**    [Notes on grounding and context strength]
**Altitude Match:**   [Notes on grounding and context strength]
**CTA Clarity:**      [Notes on grounding and context strength]
```
