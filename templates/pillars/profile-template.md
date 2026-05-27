---
title: ""
updated: ""
---

# Company Profile

This pillar carries the company's voice — how it sounds, what it stands for, and the narrative it returns to. Company-level attributes, facts, glossary, and brand guardrails live in `MESSAGE.md` (always-on); this file holds the voice and personality content that shapes how every asset reads.

## Messaging Blocks

### Mission

[Instructions:
Define the concrete drumbeat your company hits every day. Value messaging will show up later — keep this elevated to action statements.]

[Tips:
- Emphasize verbs and ongoing behavior
- Align to the Vision with the how
- Avoid abstract language]

[Format:
1-2 sentences describing a continuous discipline]

### Vision

[Instructions:
Describe the future world your company is driving towards. This is the North Star of your positioning and messaging.]

[Tips:
- Focus on external market forces
- Be directional and opinionated
- Avoid generic phrases that could be anyone]

[Format:
1-2 sentences describing a changed future state]

### Boilerplate

[Instructions:
Provide the canonical About statement used across press releases, social profiles, partner listings, marketplaces, and any external surface that needs a fixed description of the company. Write it once here; the system tunes it for specific surfaces (marketplace listings, partner catalogs, etc.) at generation time.]

[Tips:
- Write in third person
- Keep it concise and authoritative
- Avoid campaign-specific phrasing
- Optional: short, medium, and long versions if different surfaces consistently need different lengths]

[Format:
1 short paragraph suitable for copy-paste.
Optional: short, medium, and long versions.]

### Brand Voice

#### Tone

[Instructions:
Define the personality of the brand voice through specific attribute pairs — what you are and what you're explicitly not. Vague descriptors like "professional" aren't useful. Contrasts are.]

[Tips:
- Frame as "We are X but not Y" — e.g., "technically authoritative but not academic," "direct but not aggressive," "confident but not arrogant"
- 3-5 attribute pairs is enough to establish a distinctive voice]

[Format:
3-5 attribute pairs:
- We are [attribute] but not [contrast]
- We are [attribute] but not [contrast]]

#### Technical Depth

[Instructions:
Define the default level of technical depth your messaging should assume. This establishes a baseline so content is neither over-explained nor under-explained.]

[Tips:
- Specify the default altitude and when to adjust
- If your audience spans executives to developers, state the default and the conditions that shift it]

[Format:
- **Default altitude:** [where most content should land]
- **Go deeper when:** [conditions that warrant more technical detail]
- **Simplify when:** [conditions that warrant less]]

#### Brand Pillars

[Instructions:
List 3-5 durable identity tenets that define what the brand stands for. Brand pillars are who the company is in spirit — recurring themes that color voice, design, and storytelling across every asset. They are not value propositions (what you deliver — see Pitch) and not customer outcomes (what customers achieve — see Pitch's UVPs and Differentiators).]

[Tips:
- Brand pillars persist across product changes and market shifts; UVPs do not
- Frame as identity statements, not promises — "We treat operators like first-class users" is a brand pillar; "We reduce MTTR by 60%" is a UVP
- These should still be opinionated — if a generic competitor could adopt the same pillar, it's not distinctive enough]

[Format:
Numbered list of 3-5 identity tenets]

## Writing Guidelines

- Brand Voice (Tone, Technical Depth, Brand Pillars) is always-on unless explicitly overridden by a skill
- Company attributes (stage, type, market, position) live in `MESSAGE.md` Attributes — load that for stage-calibrated proof burden and positioning boldness
- The canonical Glossary lives in `MESSAGE.md` — never duplicate terms here
- Brand Guardrails (absolute output constraints) live in `MESSAGE.md` — voice violations are caught at validation, not declared here
- Strategic narrative, UVPs, and differentiators live in `messaging/pillars/pitch.md` — load it for any narrative-led or value-led content

## Messaging Rules

[Instructions:
This section is populated during bootstrap with company-specific rules about how the voice in this document should be applied. These rules encode voice and narrative decisions unique to the company.

Keep to 3-5 rules. Only encode constraints that are genuinely unique to this company and not derivable from the content itself.

Writing Guidelines (above) tell agents how to interpret the document structure. Messaging Rules tell agents what company-specific constraints to honor when using the content.]
