---
title: ""
updated: ""
---

# Proof

This pillar is the evidence layer of the messaging system — the measurable outcomes, customer stories, analyst recognition, and community validation that back up every claim made in Pitch, Position, and Portfolio. Without Proof, positioning is opinion and differentiation is assertion. Proof operates on a spectrum. Early-stage companies have thin proof — a handful of design partners, projected metrics, and founder credibility. Growth-stage companies have building proof — customer deployments, initial analyst recognition, and real metrics with limited sample sizes. Established companies have deep proof — extensive case studies, analyst leadership positions, and statistically significant benchmarks. The messaging system should use the proof it has honestly and never overclaim beyond it.

## Messaging Blocks

### Value Evidence

[Instructions:
Document the measurable business and technical outcomes customers achieve. These should reflect real impact, not activity metrics. For each measure, note whether it's proven (backed by customer data) or projected (based on internal analysis or modeling) — the writer needs to know which claims require hedging.]

[Tips:
- Focus on outcomes executives and practitioners care about
- Prefer ranges or directional impact over overly precise figures
- Tie measures back to specific UVPs in `messaging/pillars/pitch.md`
- Be honest about the evidence basis — a projected metric presented as proven damages credibility in late-stage evaluation]

[Format:
For each measure:
- **Metric:** [what's measured and the direction — e.g., "mean time to remediation," "decrease"]
- **Impact:** [range or benchmark — e.g., "40-60% reduction"]
- **Evidence basis:** [proven | projected]
- **Context:** [where this applies — products, solutions, segments]
- **Source:** [customer data, internal analysis, third-party study]]

### Community Evidence

[Instructions:
Capture how end users talk about your product or approach in the wild — on social, forums, review sites, community channels, and events. Focus on patterns over individual quotes. A single positive review is a data point. A recurring theme across multiple sources is proof.]

[Tips:
- Authenticity matters more than blanket positivity
- Negative patterns are valuable too — recurring complaints signal messaging gaps or proof that needs addressing
- Aggregate patterns first, then cite representative examples
- Include quotable fragments inline for patterns with strong representative examples]

[Format:
For each pattern:
- **Theme:** [the recurring sentiment or observation]
- **Sources:** [where this shows up — G2, Reddit, community Slack, Twitter, conference hallway, etc.]
- **Strength:** [strong pattern | emerging pattern | anecdotal]
- **Representative example:** [one specific quote or observation that captures the theme]
- **Sentiment:** [positive | mixed | negative]]

## Collection Tables

Reference tables routing to deeper collection detail. The pillar carries the substantive messaging above; collections carry the per-instance detail. Each row resolves to a file in `messaging/collections/<type>/`.

### Customer Stories

Customer stories are the primary proof artifacts in the messaging system. Each story captures a customer's journey from problem to outcome, with embedded quotes that can be extracted and used directly in content.

When specific stories are related to your task, extract the respective profile in `messaging/collections/stories/`.

| Story | File | Customer | Products | Personas | Segments | Description |
|---|---|---|---|---|---|---|
| | | | | | | |

[Instructions:
Document customer stories as discrete profiles in `messaging/collections/stories/[story-name].md`. Each story should capture the full arc — who the customer is, what they were dealing with, why they acted, and what they achieved. Quotes embedded within each story profile are the atomic fragments that get dropped into emails, social posts, landing pages, and battlecards.

Tag each story in the reference table with products, personas, and segments so the writer can filter by relevance without opening every file. Description should capture the proof arc in one sentence (~15 words) — the problem domain and the measurable outcome.]

### Reports

External validation lives in `messaging/collections/reports/` — analyst research, market studies, surveys, benchmarks, and trend reports the company cites in messaging. Reports differ from Stories: Stories are our customer evidence; Reports are third-party authority. When specific reports are related to your task, extract the respective profile in `messaging/collections/reports/`.

| Report | File | Source | Type | Description |
|---|---|---|---|---|
| | | | | |

[Instructions:
Document reports as discrete profiles in `messaging/collections/reports/[report-name].md`. The table serves as a reference index. Description should capture what the report covers and why it's load-bearing for our messaging — one sentence (~15 words).]

[Tips:
- Type: analyst | research | survey | benchmark | trend
- Source is the publishing organization (Gartner, Forrester, IDC, McKinsey, internal team) — not a person
- If you're not in analyst coverage yet, say so in the pillar — this is common for emerging-stage companies and affects how proof is framed
- Reports have shelf lives — note the published date in each report profile and watch for expiration]

## Writing Guidelines

[Instructions:
Populated during bootstrap with 3-5 rules for how this document's messaging should be applied — interpretation calls, constraints, and strategic choices unique to this company.

Encode only what is specific to this company and not derivable from the content itself or the system architecture. Cut anything generic: if a competitor could write the same rule for their own messaging system, it doesn't belong here. Favor rules that change what an agent produces — what to lead with, what to avoid leading with, which claims are off-limits, and what to defer to when sources conflict.]

[Format:
3-5 bullets]
