---
title: ""
updated: ""
---

# Target Audience

This pillar defines who the company sells to and how it communicates to them — the ICP (who fits, who doesn't), the cross-functional dynamics that shape how messaging needs to land, the customer journey, and the routing tables for personas and segments. The ICP anchors everything downstream: if a company isn't ICP-fit, the messaging considerations here don't apply.

## ICP

*Structured buyer criteria for good fit/bad fit accounts. Personas and segments documented as collections.*

### Characteristics

- **Company type**: [Instructions: Shape of companies we sell to.]
- **Size band**: [Instructions: Range with sweet spot.]
- **Growth stage**: [Instructions: Scale-up / enterprise / mature.]
- **Verticals**: [Instructions: Industries served.]
- **Primary buyer**: [Instructions: Title of economic buyer.]
- **Primary champion**: [Instructions: Title of internal advocate.]
- **Primary end-user**: [Instructions: Day-to-day user.]
- **Tenure**: [Instructions: Typical years in role.]

### Behaviors

- **Buying behavior**: [Instructions: Process pattern — committee, single buyer, PLG, sales-led, hybrid.]
- **Methodology**: [Instructions: How the buyer's team works — agile, DevOps, waterfall, mixed.]
- **Tech maturity**: [Instructions: How they adopt technology — bleeding-edge, fast-follower, conservative.]
- **Cultural fit**: [Instructions: What the buyer values.]
- **Anti-fit**: [Instructions: Cultures we don't sell to. Directive.]

### Environmental

- **Existing tooling**: [Instructions: Tools the buyer already has — affects integration messaging.]
- **Regulatory pressures**: [Instructions: Compliance frameworks or regulatory requirements they operate under. Skip if not relevant.]
- **Industry pressures**: [Instructions: Macro forces affecting their business — consolidation, tech shifts, M&A, talent dynamics.]

## Messaging Blocks

### Buying Considerations

[Instructions:
Capture the cross-functional dynamics that shape how messaging needs to land across a buying group. This is not a persona-by-persona breakdown (those live in `messaging/collections/personas/`) — it's the messaging considerations that emerge when the conversation goes cross-functional, and the patterns that guide how messaging supports the deal beyond the first conversation.]

[Cover:
- **Cross-functional dynamics** — How to message when champions, evaluators, and approvers each need different framing of the same value. What stays consistent across the group, and what flexes per role.
- **Champion enablement** — What the internal champion needs to win the deal: proof points, objection handling, ROI framing, and the "armor" that holds up when they're not in the room.
- **Common consensus blockers** — Recurring objections that surface when a deal goes wide (security, procurement, finance, legal, IT), and how messaging should preempt them.
- **Influence patterns** — Who typically convinces whom, which content earns trust at which stage, and where the conversation tends to stall.
- **Hand-off moments** — Transitions where messaging changes register: champion to wider committee, evaluator to executive sponsor, individual buyer to vendor review.]

[Tips:
- Keep this general — specific persona-level depth belongs in the persona profiles in `messaging/collections/personas/`
- Focus on what the messaging system needs to do differently when stakes go cross-functional, not on cataloguing every role
- A handful of named patterns (e.g., "Security-led deal," "Operator-led deal") is more useful than an exhaustive committee taxonomy]

[Format:
Prose with subheadings — no rigid table. Name 2-4 recurring deal patterns if they meaningfully differ.]

### Buying Process

#### Customer Journey

[Instructions:
Document each stage of the customer journey from a messaging perspective. Each stage has a different emotional register, information need, and bar for proof.]

[Tips:
- Only craft focused messages that matter to this stage — avoid watering down consistent value messaging
- Internalize the "walk away feeling" to get a sense for how to move the customer from one phase to the next
- The journey applies to individual personas, teams, and the organization as a whole
- Keep this focused on messaging — save marketing attribution, sales stages, and technical maturity phases for internal documentation]

[Format:
For each journey stage, include:
- **Primary Goal:** your messaging intent for this stage
- **Walk Away Feeling:** what the customer should be feeling to move forward
- **Key Messaging:** specific messages that apply to this stage
- **Best Proof:** proof types that work best — with examples if you have them
- **Best Channels:** content types and distribution channels most effective at this stage
- **Common Objections:** objections that typically surface at this stage]

## Collection Tables

Reference tables routing to deeper collection detail. The pillar carries the substantive messaging above; collections carry the per-instance detail. Each row resolves to a file in `messaging/collections/<type>/`.

### Personas

| Persona | File | Type | Seniority | Priority | Description |
|---|---|---|---|---|---|
| | | | | | |

[Instructions:
List the personas that apply to your GTM. Grounded in real responsibilities, pressures, and motivations — not generic demographic or personality-based descriptions. For each, carve out a distinct profile in `messaging/collections/personas/[persona-name].md`. Description should be a routing signal — one sentence (~15 words) capturing what makes this persona distinct, their domain, and why they matter for messaging.]

### Segments

| Segment | File | Type | Defining Trait | Description |
|---|---|---|---|---|
| | | | | |

[Instructions:
List segments that carry particular messaging considerations. Only create segments when you need additional contextual clarifiers — compliance regulations, regional differences, scale implications, etc. For each, carve out a distinct profile in `messaging/collections/segments/[segment-name].md`. Description should be a routing signal — one sentence (~15 words) capturing the segment's key constraint or context that differentiates its messaging needs.]

## Writing Guidelines

[Instructions:
Populated during bootstrap with 3-5 rules for how this pillar's audience messaging should be applied — interpretation calls, constraints, and strategic choices unique to this company.

Encode only what is specific to this company and not derivable from the content itself or the system architecture. Cut anything generic: if a competitor could write the same rule for their own messaging system, it doesn't belong here. Favor rules that change what an agent produces — what to lead with, what to avoid leading with, which claims are off-limits, and what to defer to when sources conflict.]

[Format:
3-5 bullets]
