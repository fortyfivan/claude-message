---
name: assessment
description: Create structured evaluation frameworks — business value, risk, and technical assessments — that help prospects or customers quantify their current state, score readiness, and build an internal case for action. Use when the user asks for an assessment, scorecard, readiness evaluation, maturity model, ROI framework, or risk audit tool.
---

# Assessment Copywriting

## Instructions

1. **Identify Assessment Type:** Determine from user input which type applies
2. **Load Type Guide:** Read the corresponding file from `assessment-types/`
3. **Review the Brief:** Session should include the target audience, the decision or action this assessment supports, and what the output (report, score, recommendation) should look like
4. **Reference Messaging House:** Extract relevant context from `/messaging` using the table below
5. **Load Glossary:** Read `messaging/glossary.md` — assessment terminology must align with how the company frames the problem space
6. **Draft Assessment Structure:** Build the question framework, scoring model, and interpretation guide following the type-specific structure
7. **Write Framing Copy:** Apply type-specific guidelines for section headers, guidance text, and output narratives
8. **Self-Assess:** Review against quality signals

## Assessment Type Guides

After identifying the assessment type, load the corresponding guide:

- **Business Value Assessment:** See `assessment-types/business-value.md`
- **Risk Assessment:** See `assessment-types/risk.md`
- **Tech Assessment:** See `assessment-types/tech.md`

## Messaging House Context

Look for the following when referencing messaging elements in `/messaging`:

| Context Type          | What to Extract                                             | Source Files                              |
|-----------------------|-------------------------------------------------------------|-------------------------------------------|
| Value Evidence        | Outcome metrics used to anchor ROI and value claims         | proof.md (Value Evidence section)         |
| Persona & Pain        | What the target audience measures, cares about, and fears   | personas/[name].md, people.md             |
| Problem Framing       | How the company defines the problem space                   | position.md                               |
| Product Capabilities  | What the solution addresses in the assessment dimensions    | products/[name].md, solutions/[name].md   |
| Voice & Terminology   | Category language, naming conventions                        | profile.md, messaging/glossary.md                 |
| Customer Proof        | Benchmarks and outcomes to anchor scoring interpretation     | proof.md, stories/[name].md              |

## Assessment Writing Principles

Assessments earn credibility by being useful before the product is ever mentioned. A good assessment helps the prospect understand their situation more clearly — not just confirm a problem so you can sell them the solution.

- **Diagnostic first, commercial second.** The assessment should provide genuine insight. If the only output is "you need our product," it's a lead capture form, not an assessment.
- **Questions reveal, not lead.** Questions should surface actual current-state information. Avoid leading questions designed to engineer a specific score.
- **Scoring must be interpretable.** Every score band should map to a meaningful state description and a clear implication. "Score: 42/100" with no interpretation is noise.
- **Benchmarks add context.** Where possible, anchor scores to what the company sees across customer deployments. "Most enterprises at your stage score between 30-50" is more useful than an absolute number.
- **Recommendations must be actionable.** The output should tell the prospect what to do next — whether that's talking to you, addressing a specific gap, or understanding a priority.
- **Altitude matters.** A CISO assessment and a practitioner assessment ask fundamentally different questions. The same problem looks different from different altitudes.

## Assessment Structure Convention

All assessment types follow this general architecture, adapted per type:

1. **Introduction block** — What this assessment measures, who it's for, and what they'll get from completing it
2. **Section headers** — Named dimensions of the problem space being evaluated
3. **Questions** — Structured inputs (scored scale, multiple choice, or yes/no) organized within each dimension
4. **Scoring model** — How raw inputs translate to a dimension score and overall score
5. **Interpretation guide** — What each score band means in plain language
6. **Output narrative** — The text that generates (or guides the writer to generate) based on the score
7. **Recommendations** — The next-step framing tied to the score outcome

## Quality Signals

Quality signals for this content type. Use during generation as a compass; the reader agent evaluates against these during review.

```
Assessment Quality Signals:
- [ ] Diagnostic Value: Questions surface real insight, not just confirm a problem
- [ ] Question Neutrality: No leading questions engineered to produce a specific score
- [ ] Scoring Clarity: Every score band maps to a plain-language state description
- [ ] Benchmark Anchoring: Scores contextualized against population benchmarks where available
- [ ] Recommendation Specificity: Output includes actionable next steps, not just a score
- [ ] Altitude Match: Questions and framing calibrated to the target persona
- [ ] Terminology: Consistent with glossary.md and category language
- [ ] Type Alignment: Follows structure from type guide
```

## Output Format

ALWAYS use this exact template structure:

```markdown
## Assessment Specification
**Assessment Type:** [Business Value | Risk | Tech]
**Target Audience:** [Persona and altitude — who completes this]
**Decision Supported:** [What action or decision this assessment informs]
**Output Format:** [Score report / Recommendations brief / Facilitated conversation guide]
**Delivery Mode:** [Self-serve digital / Sales-assisted / Workshop]

## Assessment Framework
[Full question set organized by dimension, with scoring instructions]

## Scoring Model
[How dimension scores are calculated and combined into an overall score]

## Interpretation Guide
[Score band descriptions and implications]

## Output Narratives
[The text blocks that generate based on score — one per score band per key dimension]

## Recommendations Framework
[Next-step language tied to score outcomes]

## Messaging References
- **Value Evidence:** [proof.md metrics used to anchor scoring]
- **Persona:** [personas referenced]
- **Problem Framing:** [position.md sections used]
- **Product Context:** [products/solutions docs referenced]

## Self-Assessment
**Diagnostic Value:**          [Notes on grounding and context strength]
**Question Neutrality:**       [Notes on grounding and context strength]
**Scoring Clarity:**           [Notes on grounding and context strength]
**Benchmark Anchoring:**       [Notes on grounding and context strength]
**Recommendation Specificity:** [Notes on grounding and context strength]
**Altitude Match:**            [Notes on grounding and context strength]
```