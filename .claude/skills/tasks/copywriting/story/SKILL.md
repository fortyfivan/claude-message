---
name: story
description: Write published customer and partner success stories — narrative-form proof assets that move prospects through the funnel by showing real-world outcomes. Use when the user asks for a case study, customer story, partner story, success story, or proof-based content asset.
---

# Story Copywriting

## Instructions

1. **Identify Story Type:** Determine from user input which type applies
2. **Load Type Guide:** Read the corresponding file from `story-types/`
3. **Review the Brief:** Session should include the story subject (customer or partner name), key products or solutions involved, outcome data, and available quotes
4. **Load Source Profile:** Read the relevant profile from `messaging/stories/[name].md` — this is the primary source of facts, quotes, and outcome data. If no profile exists, gather the raw inputs from the user before writing
5. **Reference Messaging House:** Extract relevant context from `/messaging` using the table below
6. **Load Glossary:** Read `messaging/glossary.md` — product and solution names must be exact in published proof content
7. **Draft Narrative:** Build the story arc following the type-specific structure
8. **Embed Quotes:** Pull approved quotes directly from the story profile — do not paraphrase attributed statements
9. **Self-Assess:** Review against quality signals

## Story Type Guides

After identifying the story type, load the corresponding guide:

- **Customer Story:** See `story-types/customer.md`
- **Partner Story:** See `story-types/partner.md`

## Messaging House Context

Look for the following when referencing messaging elements in `/messaging`:

| Context Type       | What to Extract                                              | Source Files                              |
|--------------------|--------------------------------------------------------------|-------------------------------------------|
| Story Profile      | Customer/partner facts, scenario, outcome data, quotes       | stories/[name].md                         |
| Product Context    | Capabilities, use cases, architecture details                | products/[name].md                        |
| Solution Context   | Use case framing, approach, components, outcomes             | solutions/[name].md                       |
| Persona & Audience | Which buyer this story resonates with, pain point alignment  | personas/[name].md, people.md           |
| Value Framework    | Propositions this story validates, outcome claims            | position.md, proof.md                        |
| Voice & Naming     | Brand voice, product naming, glossary terms                  | profile.md, glossary.md                   |

## Story Writing Principles

Proof content lives or dies by specificity. A good story makes a skeptical buyer think "that's exactly my situation." A generic one gets skimmed and forgotten.

- **Start with the customer, not the product.** The reader is evaluating whether the story reflects their world. Get them nodding before you introduce your solution.
- **Specifics over generics.** "Managing 14,000 assets across three cloud providers with a team of two" beats "struggling with scale." Every vague phrase should become a concrete number or scenario.
- **Before/after is the proof unit.** The outcome section must be measurable and anchored to a starting state. A metric without a baseline is an assertion, not evidence.
- **Quotes are facts, not decoration.** Pull approved quotes verbatim. They are the customer's voice — don't smooth them into marketing copy.
- **Let the customer be the hero.** The company made a smart decision, took action, and achieved results. The product was the enabler. Don't make it the protagonist.
- **One story, one proof arc.** Resist the urge to layer multiple use cases or multiple products into a single story. One tight arc lands harder than three shallow ones.
- **Approval gates are hard constraints.** Only quotes and facts marked "approved" in the story profile can appear in external content.

## Quality Signals

Quality signals for this content type. Use during generation as a compass; the reader agent evaluates against these during review.

```
Story Quality Signals:
- [ ] Customer-First: Opens with the customer's world, not the product
- [ ] Specificity: Scenario includes concrete details (team size, volume, environment)
- [ ] Trigger: Clear compelling event that drove action
- [ ] Before/After: Outcome section has measurable before and after states
- [ ] Quote Accuracy: Quotes pulled verbatim from approved story profile
- [ ] Approval Status: No pending or internal-only content in external draft
- [ ] Naming: Product and solution names match glossary.md exactly
- [ ] Type Alignment: Follows structure from type guide
```

## Output Format

ALWAYS use this exact template structure:

```markdown
## Content Brief
**Story Type:** [Customer | Partner]
**Subject:** [Customer or partner name or anonymized descriptor]
**Products/Solutions:** [What was deployed]
**Target Persona:** [Who this story is written for]
**Core Proof Arc:** [Problem → trigger → outcome in one sentence]
**Approval Status:** [Approved | Draft — pending customer review]

## Story Draft
[Full narrative following the type-specific structure]

## Embedded Quotes
[List of all quotes used, with speaker, approval status, and source reference]

## Messaging References
- **Story Profile:** [stories/name.md]
- **Products/Solutions:** [products and solutions docs referenced]
- **Persona:** [personas referenced]
- **Value Evidence:** [proof.md metrics validated by this story]

## Self-Assessment
**Customer-First:**   [Notes on grounding and context strength]
**Specificity:**      [Notes on grounding and context strength]
**Before/After:**     [Notes on grounding and context strength]
**Quote Integrity:**  [Notes on grounding and context strength]
**Naming Accuracy:**  [Notes on grounding and context strength]
```