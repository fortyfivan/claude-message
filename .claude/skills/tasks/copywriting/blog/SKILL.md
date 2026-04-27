---
name: blog
description: Create insightful, research-driven blog content including thought leadership, use case guides, threat research, data studies, and product announcements optimized for SEO/GEO and differentiated market positioning
---

[Note for the user: tune this skill and the asset types to your requirements - this is a generic example as a starting point]

# Blog Copywriting

## Instructions

1. **Identify Blog Type:** Determine from user input which type applies
2. **Load Type Guide:** Read the corresponding file from `types/`
3. **Review the Brief:** Session should include messaging brief with target audience, thesis, and objectives
4. **Reference Messaging House:** Extract relevant context from `/messaging` using the table below
5. **Conduct Research:** Use WebSearch for real-time market intelligence, competitive analysis, data validation
6. **Draft Outline:** Create structured outline following the type-specific structure
7. **Write Blog Post:** Apply type-specific guidelines and SEO/GEO best practices
8. **Self-Assess:** Review against quality signals

## Blog Type Guides

After identifying the blog type, load the corresponding guide:

- **Thought Leadership:** See `types/thought-leadership.md`
- **Use Case Deep Dive:** See `types/use-case-deep-dive.md`
- **Threat Research:** See `types/threat-research.md`
- **Data Study:** See `types/data-study.md`
- **Product Announcement:** See `types/product-announcement.md`
- **Company News:** See `types/company-news.md`
- **Press Release:** See `types/press-release.md`
- **Event Recap:** See `types/event-recap.md`
- **Predictions:** See `types/predictions.md`

## Messaging House Context

Look for the following when referencing messaging elements in `/messaging`:

| Context Type       | What to Extract                                     | Source Files                 |
|--------------------|-----------------------------------------------------|------------------------------|
| Persona & Audience | Target reader, pain points, technical altitude      | people.md                  |
| Voice & Narrative  | Brand voice, story arc, tone guidelines             | profile.md                   |
| Value Framework    | Core propositions, differentiation, outcomes        | position.md, portfolio.md       |
| Market Perspective | Industry trends, positioning, competitive landscape | position.md                     |
| Evidence           | Social proof, customer stories, data points         | proof.md, portfolio.md       |
| Strategic Context  | Campaign alignment, content themes                  | play.md                    |

## SEO/GEO Optimization

**Chunk-based structure:**
- Break content into 200-300 word sections with descriptive H2/H3 headers
- Each section should be quotable by AI engines
- Use keywords naturally in headers and first sentences

**AI-friendly elements:**
- Direct Q&A format where appropriate
- Bullet point summaries at section ends
- Data points that can stand alone as citations
- Clear definitions for technical terms

**E-E-A-T signals:**
- Author credentials and expertise
- Original research and data
- Citations to authoritative sources
- Customer quotes and case studies

**Technical foundations:**
- Meta descriptions optimized for AI summarization (150-160 characters)
- Alt text for images and data visualizations

## Quality Signals

Quality signals for this content type. Use during generation as a compass; the reader agent evaluates against these during review.

```
Blog Quality Signals:
- [ ] Insightfulness: Adds new perspective (not consensus)
- [ ] Narrative Flow: Clear beginning, middle, end
- [ ] Market Relevance: Addresses current pain points
- [ ] Differentiation: Distinct from competitor content
- [ ] Credibility: Backed by evidence/data
- [ ] SEO/GEO: Quotable sections, structured headers
- [ ] Type Alignment: Follows structure from type guide
```

## Writing Guidelines

- Use tension to frame the domain
- Make reader feel smarter for reading
- Concrete examples over abstractions
- Experience-based insights AI can't replicate
- Avoid marketing fluff and thinly veiled pitches
- Include original research or data when possible
- Write for practitioners but remain accessible to executives
- Every section should be self-contained enough to be AI-quoted

## Output Format

ALWAYS use this exact template structure:

```markdown
## Content Brief
**Blog Type:** [Type]
**Target Audience:** [Primary persona and altitude]
**Core Thesis:** [Main argument or insight]
**Market Context:** [Why this matters now]
**Key Takeaways:** [3-5 main points readers will learn]
**SEO Keywords:** [Primary and secondary keywords]

## Outline
[Section-by-section structure with brief descriptions]

## Blog Draft
[Full formatted blog post with headers, sections, and SEO optimization]

## Messaging References
- **Audience:** [Link to people.md section]
- **Value Framework:** [Link to position.md]
- **Market Context:** [Link to position.md]
- **Other:** [Additional references used]

## Self-Assessment
**Insightfulness:**    [Notes on grounding and context strength]
**Narrative Flow:**    [Notes on grounding and context strength]
**Market Relevance:**  [Notes on grounding and context strength]
**Differentiation:**   [Notes on grounding and context strength]
**Credibility:**       [Notes on grounding and context strength]
**SEO/GEO Readiness:** [Notes on grounding and context strength]
```
