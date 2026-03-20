# Customer Story

A narrative proof asset — the published case study — that takes a prospect through a real customer's journey from problem to outcome. This is the external-facing version of the story profile in `messaging/stories/`. The profile stores the facts; this type guide structures how to tell them.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Headline | Hook the reader with the outcome | Lead with the business result, not the company or product name |
| Customer Snapshot | Establish who this is | Industry, size, and the one-line environment fact that makes the scenario recognizable |
| The Situation | Set the before state | Paint the conditions that made the status quo untenable — specific, grounded in the customer's reality |
| The Trigger | Show what forced action | The specific event or pressure that moved them from "aware" to "acting" |
| Why They Chose Us | Address the evaluation briefly | What differentiated the decision — not a product pitch, a decision rationale |
| The Outcome | Deliver the proof | Before/after metrics, qualitative operational changes, and the customer voice |
| Looking Ahead | Signal momentum | What they're doing next — expansion, new use cases, broader rollout |

## Tone & Style

- **Voice:** Third-person narrative, customer-led. The company is referenced but not the subject.
- **Length:** 600-1,200 words for web; 800-1,500 for PDF
- **Altitude:** Match the target persona — practitioner stories lean operational, executive stories lean strategic

Use active voice and past tense for the situation and trigger. Shift to present tense for outcomes that are ongoing.

## Headline Patterns

Lead with the measurable or observable outcome:

- "[Customer] Cut Vulnerability Remediation Time by 60% with [Product]"
- "How [Customer] Gained Visibility Across 40,000 Assets in 30 Days"
- "[Customer] Eliminated Manual Asset Reconciliation — and Found 800 Unknown Devices"

Avoid:
- "[Company] Helps [Customer] Improve Security Posture" (vague, no outcome)
- "[Customer] Chooses [Company] for Asset Management" (decision, not result)

## Situation Writing

The situation section is where the reader decides if this story is for them. Write to be recognized, not to impress:

- Name the specific environment, team size, or scale that creates the constraint
- Reference the tools or processes they were relying on and why those broke down
- Connect the pain to the persona — what specifically was hard for someone in this role

Avoid: "faced increasing complexity in their IT environment" → write: "managing 28,000 endpoints across four cloud providers with a security team of six and no central source of truth."

## Outcome Section

The outcome section must have three components:

1. **Quantitative results** — Specific metrics with before/after anchoring. Pull from the `Outcome` section of the story profile.
2. **Qualitative changes** — Observable operational shifts — what's different about how the team works now.
3. **Customer voice** — At least one approved quote from the story profile embedded here.

If before metrics are unavailable, say "from an unknown baseline" rather than inventing a baseline.

## Example

**Input:** Write a customer story for a Fortune 500 financial services company that deployed the asset management platform and reduced unmanaged device count by 78% in 60 days.

**Output:**
```markdown
# [Customer] Closed Its Asset Coverage Gap — and Found 3,200 Devices It Didn't Know About

**Industry:** Financial Services | **Size:** 45,000+ employees | **Region:** North America

## The Situation

[Customer]'s security operations team was responsible for maintaining compliance across a hybrid environment spanning on-premises infrastructure, four cloud providers, and a growing fleet of contractor-managed devices. Their asset inventory lived in three systems — a legacy CMDB, their endpoint agent platform, and manual spreadsheets maintained by individual business units.

When assets weren't in all three, they effectively didn't exist from a security standpoint. The team estimated their true asset count was somewhere between 80,000 and 95,000 devices. They didn't know which.

## The Trigger

A routine external audit revealed that 12% of sampled endpoints lacked current EDR coverage. For a regulated financial institution, that finding triggered a board-level directive: establish a verified, continuous asset inventory within 90 days.

## Why They Chose [Company]

The evaluation came down to coverage and speed. [Customer]'s security architect needed a solution that could ingest data from their existing tools without ripping anything out. After a two-week proof of concept, [Company] correlated 14 data sources and surfaced 3,200 previously unknown devices — before the contract was signed.

"We ran the POC expecting to validate the concept. We didn't expect it to immediately show us assets our CMDB had never seen." — [Security Architect, Customer]

## The Outcome

**Before:** Three disconnected asset inventories. Unknown coverage gaps. Manual reconciliation taking 20+ hours per week.

**After:** A single, continuously updated asset view correlated from 14 sources. Unmanaged device count reduced by 78% within 60 days of deployment.

**Quantitative:**
- 78% reduction in unmanaged devices in 60 days
- 3,200 previously unknown devices identified in the first 24 hours
- 20+ hours/week of manual reconciliation eliminated

**Qualitative:**
- Security team shifted from reactive inventory chasing to proactive coverage enforcement
- Audit response time reduced — evidence packages now generated in hours, not days

"We can now tell the board exactly what we have, where it is, and whether it's covered. That conversation used to take a week to prepare." — [CISO, Customer]

## Looking Ahead

[Customer] is expanding the deployment to cover OT assets in its manufacturing facilities — a segment previously excluded from security tooling entirely.
```

## Quality Signals

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Recognition | Prospect thinks "that's my situation" | Generic pain that applies to every company |
| Trigger Specificity | Clear, named event that forced action | Vague "growing complexity" as the trigger |
| Outcome Anchoring | Before and after states both explicit | Outcome without baseline, improvement without scale |
| Quote Placement | At least one quote in the outcome section | No customer voice, or quotes only at the end |
| Product Role | Product is the enabler, not the hero | Story reads like a feature brochure |
| Persona Match | Language and proof type match the target reader | Executive metrics in a practitioner story, or vice versa |