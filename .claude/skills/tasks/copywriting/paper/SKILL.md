---
name: paper
description: Create long-form research and analysis content including research studies, data findings reports, industry trend analyses, and topic deep dives designed to establish authority, generate leads, and serve as anchor assets for campaigns
---

# Paper Copywriting

## Instructions

1. **Identify Paper Type:** Determine from user input which type applies
2. **Load Type Guide:** Read the corresponding file from `types/`
3. **Review the Brief:** Session should include messaging brief with target audience, thesis, research scope, and objectives
4. **Reference Messaging House:** Extract relevant context from `/messaging` using the table below
5. **Conduct Research:** Use WebSearch extensively — papers demand more external evidence than blog content
6. **Draft Outline:** Create detailed outline following the type-specific structure. Papers are long — the outline is the approval gate before investing in the full draft
7. **Write Paper:** Apply type-specific guidelines, maintaining depth and rigor throughout
8. **Self-Assess:** Review against quality signals

## Paper Type Guides

After identifying the paper type, load the corresponding guide:

- **Research Study:** See `types/research-study.md`
- **Data Findings:** See `types/data-findings.md`
- **Industry Trend:** See `types/industry-trend.md`
- **Topic Deep Dive:** See `types/topic-deep-dive.md`

## Messaging House Context

Look for the following when referencing messaging elements in `/messaging`:

| Context Type       | What to Extract                                           | Source Files                          |
|--------------------|-----------------------------------------------------------|---------------------------------------|
| Persona & Audience | Target reader, technical altitude, information depth      | audience.md, personas/[name].md       |
| Voice & Narrative  | Brand voice, strategic narrative, theme pillars           | profile.md                            |
| Value Framework    | Core propositions, differentiation, unique approach       | space.md, portfolio.md                |
| Market Perspective | Category dynamics, trends, competitive landscape          | space.md, categories/[name].md        |
| Evidence           | Customer stories, metrics, analyst recognition            | proof.md, stories/[name].md           |
| Product Context    | Capabilities, architecture, use cases                     | products/[name].md, solutions/[name].md |
| Terminology        | Controlled vocabulary, naming conventions                 | glossary.md, profile.md               |

## Paper Writing Principles

Papers are authority assets. They take longer to produce, generate more trust, and have longer shelf lives than blog content. Every design decision should optimize for depth, rigor, and durability.

- **Depth over brevity.** Papers earn the reader's time by going places shorter content can't. If the insight can be communicated in 800 words, it's a blog post, not a paper.
- **Evidence-dense.** Every major claim should be supported by data, research, customer evidence, or expert perspective. Unsupported assertions that pass in blog content fail in papers.
- **Methodology-transparent.** If you conducted research, surveyed customers, or analyzed data — show your work. The reader should be able to evaluate your conclusions.
- **Positioning through expertise, not pitching.** The company's product should appear naturally in context, not as the conclusion every section builds toward. A paper that reads like a product pitch dressed in research clothing damages the asset and the brand.
- **Designed for campaign orchestration.** Papers are anchor assets — the thing a digital campaign is built around. Blog posts reference them, emails CTA to them, social promotes them. Write knowing this asset will be the foundation other content builds on.

## Quality Signals

Quality signals for this content type. Use during generation as a compass; the reader agent evaluates against these during review.

```
Paper Quality Signals:
- [ ] Depth: Goes meaningfully deeper than available blog content on this topic
- [ ] Evidence: Every major claim supported by data, research, or customer proof
- [ ] Methodology: Research approach is transparent and defensible
- [ ] Authority: Establishes genuine expertise, not borrowed credibility
- [ ] Balance: Product appears in context, not as the forced conclusion
- [ ] Structure: Clear sections that build a progressive argument
- [ ] Durability: Content will remain relevant for 6-12 months
- [ ] Type Alignment: Follows structure from type guide
```

## Output Format

ALWAYS use this exact template structure:

```markdown
## Content Brief
**Paper Type:** [Type]
**Target Audience:** [Primary persona and altitude]
**Core Thesis:** [Main argument or finding]
**Research Scope:** [What was studied, analyzed, or explored]
**Market Context:** [Why this topic matters now]
**Key Findings:** [3-5 main takeaways]

## Outline
[Detailed section-by-section structure — this is the approval gate before full draft]

## Paper Draft
[Full formatted paper with headers, sections, evidence, and citations]

## Messaging References
- **Audience:** [personas and segments referenced]
- **Value Framework:** [space.md and product docs referenced]
- **Market Context:** [categories and trends referenced]
- **Evidence:** [proof.md, stories, and external sources used]

## Self-Assessment
**Depth:**          [Notes on grounding and context strength]
**Evidence:**       [Notes on grounding and context strength]
**Methodology:**    [Notes on grounding and context strength]
**Authority:**      [Notes on grounding and context strength]
**Balance:**        [Notes on grounding and context strength]
**Durability:**     [Notes on grounding and context strength]
```