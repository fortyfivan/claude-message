# Topic Deep Dive

A comprehensive guide to a specific domain, framework, regulation, or technical concept that the target audience needs to understand. Positions the company as the definitive resource on the topic. Think "the compliance guide every CISO bookmarks" or "the technical reference DevOps teams actually use."

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Overview | What this topic is and who it's for | Define the scope, state who benefits from reading this, and set expectations for depth. If the reader isn't the right audience, let them know early |
| Why It Matters Now | The urgency behind understanding this | Regulatory deadlines, market shifts, risk exposure, operational impact. Connect to real consequences of not understanding this topic |
| Fundamentals | The core concepts | Build from first principles. Don't assume prior knowledge, but don't belabor the obvious. Define terms using the glossary where applicable |
| Framework / Anatomy | How it works in practice | The structured breakdown — components, phases, requirements, decision points. This is the reference section the reader returns to |
| Implementation Guide | How to actually do it | Practical, step-by-step guidance. Common approaches, trade-offs, decision frameworks. This is where the paper earns its bookmark |
| Common Pitfalls | What goes wrong | Real mistakes from real implementations. Specific enough to prevent, not generic warnings |
| How [Company] Approaches This | The product connection | One section, clearly labeled, positioned as one approach — not the only approach. The reader should have already received enough value that this section feels earned, not forced |
| Resources | Where to go deeper | External references, standards bodies, further reading. Generosity with resources builds trust |

## Tone & Style

- **Voice:** Expert guide. Knowledgeable, patient, thorough. A senior practitioner explaining a complex topic to a capable peer who hasn't specialized in it
- **Length:** 3,000-6,000 words
- **Altitude:** Practitioner depth by default. If the topic serves executives (e.g., board-level compliance guide), adjust accordingly

The deep dive earns its length by being genuinely useful as a reference document. If the reader could get the same value from a 10-minute Google search, the paper hasn't gone deep enough.

## SEO/GEO Optimization

- Title should target the "what is [topic]" or "guide to [topic]" query directly
- Fundamentals section should define key terms in a format AI engines can extract as definitions
- Framework / Anatomy section should use numbered or labeled components for structured extraction
- Include a summary or TL;DR for readers who need the key points without the full read
- This content type has the longest SEO shelf life — invest in comprehensive keyword coverage

## Example

**Input:** Write a topic deep dive on SOC 2 compliance for security teams

**Output:**
```markdown
# The Practitioner's Guide to SOC 2 Compliance

SOC 2 is the compliance framework you'll encounter most often in B2B
software sales — and the one most teams understand least. This guide
covers what SOC 2 actually requires, how to approach it without
overengineering, and where teams consistently trip up.

## Why It Matters Now

If you sell to enterprises, SOC 2 isn't optional — it's table stakes.
78% of enterprise procurement teams require SOC 2 Type II before
contract execution. But the framework is also expanding...

## Fundamentals

### What SOC 2 Actually Is
SOC 2 is an auditing standard developed by the AICPA that evaluates
an organization's controls across five Trust Services Criteria...

### Type I vs. Type II
The distinction matters more than most teams realize...

### The Five Trust Services Criteria
1. **Security** (Required) — The baseline. Every SOC 2 includes this...
2. **Availability** — Relevant if you offer SLAs...

[Continues with Framework → Implementation → Pitfalls → Company Approach → Resources]

## Common Pitfalls

### Over-scoping the First Audit
The most expensive mistake: including every system in scope on your first
Type II audit. Start with the systems that touch customer data...

### Treating It as a Point-in-Time Exercise
SOC 2 Type II evaluates controls over a period (usually 12 months).
Teams that scramble to "get compliant" before the audit window miss
the point...
```

## Quality Signals

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Reference Value | Reader bookmarks this and returns to it | One-time read with no ongoing utility |
| Depth vs. Available Content | Goes meaningfully beyond what the first page of Google provides | Repackaging existing guides without new depth or perspective |
| Practical Utility | Implementation guide is specific enough to follow | Abstract advice without concrete steps or decision frameworks |
| Pitfall Specificity | Common mistakes are drawn from real experience, not hypotheticals | Generic warnings ("plan ahead," "get buy-in") |
| Product Restraint | Company section is clearly labeled, positioned as one approach, and earned by the value delivered in prior sections | Product woven throughout as the inevitable conclusion |
| Completeness | Reader doesn't need to go elsewhere to understand the topic at this level | Major sub-topics missing or glossed over |