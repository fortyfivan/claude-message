---
name: enablement
description: Create internal sales and GTM enablement assets including competitive battlecards, discovery guides, and playbook walkthroughs that arm revenue teams with messaging-aligned, actionable content
---

# Enablement Copywriting

## Instructions

1. **Identify Asset Type:** Determine from user input which enablement type applies
2. **Load Type Guide:** Read the corresponding file from `types/`
3. **Review the Brief:** Session should include messaging brief with target internal audience, scenario context, and objectives
4. **Reference Messaging House:** Extract relevant context from `/messaging` using the table below
5. **Load Glossary:** Read `messaging/glossary.md` for term consistency — enablement content is where terminology drift starts
6. **Draft Structure:** Create structured outline following the type-specific template
7. **Write Asset:** Apply type-specific guidelines with a focus on scannability and in-the-moment usability
8. **Self-Assess:** Review against quality signals

## Enablement Type Guides

After identifying the asset type, load the corresponding guide:

- **Competitive Battlecard:** See `types/competitive-battlecard.md`
- **Discovery Guide:** See `types/discovery-guide.md`
- **Playbook Walkthrough:** See `types/playbook-walkthrough.md`
- **Partner Joint Solution:** See `types/partner-joint-solution.md`

## Messaging House Context

Look for the following when referencing messaging elements in `/messaging`:

| Context Type          | What to Extract                                           | Source Files                              |
|-----------------------|-----------------------------------------------------------|-------------------------------------------|
| Competitor Intel      | Strengths, weaknesses, win/loss patterns, differentiation | competitors/[name].md, space.md           |
| Persona & Audience    | Pain points, goals, objections, decision criteria, altitude | personas/[name].md, audience.md          |
| Plays & Motions       | Trigger conditions, play narratives, campaign structure   | plays/[name].md, motions.md              |
| Value Framework       | Propositions, differentiators, product capabilities       | profile.md, space.md, products/[name].md |
| Voice & Terminology   | Brand voice, naming conventions, glossary terms           | profile.md, glossary.md                  |
| Evidence              | Customer stories, quotes, metrics, analyst recognition    | proof.md, stories/[name].md             |
| Solutions             | Use cases, outcomes, components                           | solutions/[name].md, portfolio.md        |

## Enablement Writing Principles

Enablement content is consumed under pressure — mid-call, pre-meeting, between deal stages. Every design decision should optimize for a rep who has 30 seconds to find what they need.

- **Scannability over prose.** Headers, tables, and bold key phrases. A rep skimming during a call should find the right section in seconds.
- **Actionable over informational.** "Say this" beats "understand this." Provide exact language, not background reading.
- **Honest over optimistic.** Reps lose trust in enablement content the first time it fails them in a live conversation. If a competitor is strong somewhere, say so and provide the redirect.
- **Scenario-driven over comprehensive.** Organize around situations reps encounter, not abstract categories. "When they bring up [competitor]" is better than "Competitive Landscape."
- **Messaging-grounded over invented.** Every claim, differentiator, and objection response must trace to the messaging house. Do not introduce positioning that isn't supported by space.md or proof.md.

## Quality Signals

Quality signals for this content type. Use during generation as a compass; the reader agent evaluates against these during review.

```
Enablement Quality Signals:
- [ ] Scannability: Can a rep find what they need in under 30 seconds?
- [ ] Actionability: Does every section provide language they can use?
- [ ] Honesty: Are competitor strengths and limitations acknowledged?
- [ ] Grounding: Do all claims trace to messaging house sources?
- [ ] Scenario Coverage: Are the common real-world situations addressed?
- [ ] Terminology: Consistent with glossary.md and naming conventions?
- [ ] Type Alignment: Follows structure from type guide?
```

## Output Format

ALWAYS use this exact template structure:

```markdown
## Content Brief
**Asset Type:** [Type]
**Internal Audience:** [Sales, SE, SDR, CS — who uses this]
**Scenario:** [When this asset gets pulled up]
**Key Sources:** [Primary messaging docs referenced]

## Outline
[Section-by-section structure]

## Asset Draft
[Full formatted enablement asset following type-specific template]

## Messaging References
- **Competitor:** [competitors/name.md sections used]
- **Persona:** [personas/name.md sections used]
- **Play:** [plays/name.md sections used]
- **Space:** [space.md sections used]
- **Proof:** [stories/name.md, proof.md sections used]
- **Other:** [Additional references]

## Self-Assessment
**Scannability:**       [Notes on grounding and context strength]
**Actionability:**      [Notes on grounding and context strength]
**Honesty:**            [Notes on grounding and context strength]
**Grounding:**          [Notes on grounding and context strength]
**Scenario Coverage:**  [Notes on grounding and context strength]
**Terminology:**        [Notes on grounding and context strength]
```