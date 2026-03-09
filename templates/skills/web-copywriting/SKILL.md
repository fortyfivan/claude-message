---
name: web-copywriting
description: Create high-converting website copy for product pages, solution pages, and other web properties that balance positioning clarity with conversion optimization
---

# Web Copywriting

## Instructions

1. **Identify Page Type:** Determine from user input which type applies
2. **Load Type Guide:** Read the corresponding file from `page-types/`
3. **Review the Brief:** Session should include target audience, page objective, primary CTA, and SEO requirements
4. **Reference Messaging House:** Extract relevant context from `/messaging` using the table below
5. **Load Glossary:** Read `messaging/glossary.md` — web copy is the most terminology-sensitive content type. Naming errors on the website are visible to every prospect
6. **Draft Structure:** Create the page structure following the type-specific wireframe
7. **Write Copy:** Apply type-specific guidelines with a focus on clarity, scannability, and conversion
8. **Self-Evaluate:** Review against the validation checklist

## Web Type Guides

After identifying the page type, load the corresponding guide:

- **Product Page:** See `page-types/product-page.md`
- **Solution Page:** See `page-types/solution-page.md`

## Messaging House Context

Look for the following when referencing messaging elements in `/messaging`:

| Context Type       | What to Extract                                          | Source Files                              |
|--------------------|----------------------------------------------------------|-------------------------------------------|
| Product Detail     | Capabilities, use cases, architecture, differentiation    | products/[name].md                        |
| Solution Context   | Use case, approach, components, value delivered           | solutions/[name].md                       |
| Persona & Audience | Target reader, pain points, decision criteria, altitude   | audience.md, personas/[name].md           |
| Voice & Naming     | Brand voice, product naming, controlled vocabulary        | profile.md, glossary.md                   |
| Value Framework    | Propositions, differentiators, positioning                | space.md                                  |
| Evidence           | Customer stories, quotes, metrics                         | proof.md, stories/[name].md              |
| Pricing            | Pricing model, CTA implications                           | portfolio.md (pricing_model)              |

## Web Writing Principles

Web copy is the most constrained content type. Every word competes for attention with navigation, visuals, and the back button. The principles are different from long-form content:

- **Clarity beats cleverness.** The reader should understand the product or solution within 5 seconds of landing on the page. If they have to think about what you do, they'll leave.
- **Structure is content.** Headers, subheaders, and visual hierarchy do as much work as the prose. Write the headers first — if someone reads only the H1 and H2s, they should understand the value proposition.
- **One CTA per page section.** Every scroll depth should have one clear next action. Don't compete with yourself.
- **Proof inline, not deferred.** Don't send the reader to a case study page — put the quote, the metric, or the logo bar right next to the claim it supports.
- **Persona-aware, not persona-exclusive.** Product and solution pages serve multiple personas. Write to the primary buyer persona but don't alienate the technical evaluator or the champion who's forwarding the page.
- **SEO is structural, not decorative.** Keywords belong in headers, meta descriptions, and first sentences — not forced into body copy where they break the natural voice.

## Validation Checklist

```
Web Copy Quality Check:
- [ ] Clarity: Page purpose is obvious within 5 seconds
- [ ] Value Prop: Clear what you do, for whom, and why it matters — above the fold
- [ ] Scannability: Headers alone tell the full story
- [ ] CTA: Clear primary action at every scroll depth
- [ ] Proof: Evidence appears inline next to claims, not deferred
- [ ] Naming: Product and feature names match glossary.md exactly
- [ ] Voice: Tone matches profile.md across all sections
- [ ] SEO: Keywords in headers, meta description, and first sentences
- [ ] Type Alignment: Follows structure from type guide
```

## Output Format

ALWAYS use this exact template structure:

```markdown
## Content Brief
**Page Type:** [Type]
**Target Audience:** [Primary persona with secondary audiences noted]
**Page Objective:** [What the page should accomplish]
**Primary CTA:** [The one action you want the visitor to take]
**SEO Target:** [Primary keyword and search intent]

## Page Structure
[Section-by-section wireframe with content purpose per section]

## Copy Draft
[Full page copy organized by section, with H1/H2/H3 hierarchy, body copy, CTAs, and proof placement noted]

## Meta Content
- **Page Title:** [SEO-optimized title tag, 50-60 characters]
- **Meta Description:** [150-160 characters optimized for search and AI summarization]
- **OG Title:** [Social sharing title]
- **OG Description:** [Social sharing description]

## Messaging References
- **Product/Solution:** [product or solution docs referenced]
- **Persona:** [personas referenced]
- **Value Framework:** [space.md sections referenced]
- **Evidence:** [proof and stories referenced]

## Evaluation
**Clarity:**        [Assessment]
**Value Prop:**     [Assessment]
**Scannability:**   [Assessment]
**CTA Strength:**   [Assessment]
**Proof Density:**  [Assessment]
**SEO Readiness:**  [Assessment]
```