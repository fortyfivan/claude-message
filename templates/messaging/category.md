---
title: ""
description: ""
maturity: ""  # emerging | growing | peak | declining | established
trajectory: ""  # expanding | consolidating | fragmenting | being-redefined
related_categories: []
updated: ""
---

# Category: [Name]

This profile defines the company's relationship to a specific market category — how the category is defined, where it's headed, and how the company positions within it.

## Messaging Blocks

### Definition

[Instructions:
Provide the industry-standard definition of this category and its source. If analysts define it, cite them. If it's an industry term without a formal definition, state that. If your company is defining or redefining the category, explain what it replaces or subsumes.]

[Tips:
- Not every category has an analyst origin — some are industry shorthand, some are self-defined
- If the company's definition differs from the analyst definition, note both and explain the distinction]

[Format:
- **Definition:** [what this category means]
- **Source:** [who defines it — analyst firm, industry convention, or company-defined]
- **Our definition differs:** (optional) [how and why]]

### Category Narrative

[Instructions:
What's happening in this category right now — how it's defined, who the players are, where it's headed, and why that matters to the company's positioning. This is the category's own momentum, distinct from how the company positions within it. The frontmatter `trajectory` field captures the direction as an enum; this section provides the story behind it.]

[Tips:
- Include the forces driving the trajectory — technology shifts, buyer behavior changes, regulatory pressure, vendor consolidation
- Name the major players shaping the category without detailed competitive analysis (that lives in competitor profiles)
- A category in "consolidating" trajectory means different content strategy than one in "emerging" — make the implications clear]

[Format:
2-3 paragraphs]

### Analyst Landscape

[Instructions:
How analysts, industry publications, and community influencers define, evaluate, and shape perception of this category. Include major frameworks (Magic Quadrant, Wave, Market Guide) that buyers reference during evaluation.]

[Tips:
- If the company isn't in analyst coverage yet, say so — this is common for emerging-stage companies and affects how proof is framed
- The useful signal is how the analyst defines the category and evaluates players, not just whether you've spoken to them
- Include influential publications and community voices, not just analyst firms — in some markets, a well-known blog or podcast shapes category perception more than Gartner]

[Format:
| Name | Firm / Publication | Coverage | Key Framework | Our Relationship |
|---|---|---|---|---|
| | | | | |

Our Relationship: recognized | engaged | not-engaged | not-applicable]

### Our Position

[Instructions:
How the company relates to this category — where it fits, where it's headed, and what makes it different from typical category players.]

[Tips:
- Current Position should reflect reality, not aspiration — if you're a new entrant, say so
- Strategic Aim captures intent: lead the category, differentiate within it, converge from an adjacent category, or consume it into a broader platform play
- Differentiation should reference specific capabilities or approaches, not generic claims]

[Format:
- **Where we fit:** [how the company relates to this category]
- **Current position:** [new entrant | emerging player | established player | category leader | adjacent — entering from a neighboring category]
- **Strategic aim:** [lead | differentiate | converge | consume]
- **Differentiation:** [how the company differs from typical players in this category]]

### Key Buyers

[Instructions:
The typical buyer roles active in this category. Reference persona profiles where they exist in the messaging system.]

[Format:
| Role | Persona Profile | Category-Specific Context |
|---|---|---|
| | | |]

[Tips:
- Category-Specific Context captures how this buyer's priorities differ in this category versus generally — a CISO evaluating attack surface management tools has different criteria than a CISO evaluating SIEM]

### Portfolio Alignment

[Instructions:
Which products and solutions map to this category. This connects category-level positioning to specific offerings.]

[Format:
| Product / Solution | File | Role in Category |
|---|---|---|
| | | |]

[Tips:
- Role in Category describes how the product relates — primary offering, supporting capability, adjacent extension
- A product may appear in multiple category profiles with different roles]

### Adjacent Categories

[Instructions:
Related categories that are converging, competing, or complementary. Reference category profiles where they exist.]

[Format:
| Category | File | Relationship |
|---|---|---|
| | | |]

[Tips:
- Relationship types: converging (categories merging), competing (different categories solving the same problem), complementary (frequently purchased together), subsuming (this category absorbing the other), or being-subsumed (the other absorbing this one)]

## Writing Guidelines

- Analyst landscape should be honest about the company's current standing — overclaiming analyst recognition damages credibility in evaluation-stage content
- Differentiation within a category must be backed by evidence — do not introduce claims here that aren't supported elsewhere in the messaging system
- Key buyers in this category may have different priorities than their general persona profile describes — use the Category-Specific Context to capture the delta
- Portfolio alignment determines which product docs to load when generating category-specific content — if a product isn't listed here, it shouldn't be referenced in category-level messaging
- Adjacent category relationships affect competitive content — converging categories mean new competitors, complementary categories mean co-marketing opportunities

## Messaging Rules

[Instructions:
This section is populated during bootstrap with company-specific rules about how the messaging in this document should be applied. These rules encode positioning decisions, constraints, and strategic choices unique to the company.

Writing Guidelines (above) tell agents how to interpret the document structure. Messaging Rules tell agents what company-specific constraints to honor when using the content.]
