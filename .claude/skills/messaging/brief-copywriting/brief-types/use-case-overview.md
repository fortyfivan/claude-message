# Use Case Overview

Walk through a specific workflow or outcome, showing how your solution addresses a concrete scenario.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Scenario | Set the context | Who, what, when—make it specific and relatable |
| Challenge | What makes this hard today | Current-state frustrations and limitations |
| Solution Approach | How to address it | Your method, not just your product |
| Workflow | Step-by-step process | Show what the user actually does |
| Outcome | What success looks like | Quantified results and business impact |

## Tone & Style

- **Voice:** Practical, workflow-oriented, instructional
- **Length:** 1-2 pages (400-800 words)
- **Altitude:** Practitioners who will implement this workflow

Focus on the "how"—this document should help someone understand exactly what they'd do and what they'd get.

## Workflow Visualization

Consider including:
- **Numbered steps:** Clear sequence of actions
- **Before/after comparison:** Visual contrast of current vs. future state
- **Diagram placeholder:** Note where a workflow diagram would add value
- **Time savings:** Quantify at each step if possible

## Example

**Input:** Create a use case overview for vulnerability prioritization

**Output:**
```markdown
# Use Case: Vulnerability Prioritization

## The Scenario

Your vulnerability scanner just returned 47,000 findings. The security team has bandwidth to remediate 500 this sprint. How do you decide which 500 matter most?

## The Challenge

Traditional prioritization uses CVSS scores, but CVSS doesn't know your environment:
- A "critical" vulnerability on an air-gapped test server isn't critical
- A "medium" vulnerability on an internet-facing server handling customer data might be
- CVSS can't tell you if compensating controls exist

Teams either over-rotate on CVSS scores (wasting effort on low-risk findings) or under-rotate (missing genuinely dangerous exposures).

## The Approach

Effective vulnerability prioritization requires context:

1. **Asset criticality:** How important is this system to the business?
2. **Exposure:** Is it reachable from the internet? From the internal network?
3. **Exploitability:** Is there active exploitation in the wild?
4. **Compensating controls:** Do existing controls reduce the risk?

By enriching vulnerability data with asset context, you can rank findings by actual risk to your organization—not theoretical severity.

## The Workflow

**Step 1: Correlate Vulnerability + Asset Data**
Connect your vulnerability scanner (Tenable, Qualys, Rapid7) to your asset management platform. Vulnerability findings automatically enrich with asset context.

**Step 2: Define Risk Criteria**
Build a prioritization query:
```
vulnerabilities.cvss >= 7
AND assets.exposure = "internet-facing"
AND assets.criticality = "high"
AND NOT assets.controls.edr = "installed"
```

**Step 3: Generate Prioritized List**
Run the query to surface high-risk vulnerabilities on high-value assets with inadequate protection.

**Step 4: Route to Remediation**
Export to your ticketing system or trigger automated actions. Each ticket includes full asset context for faster remediation.

**Step 5: Track Progress**
Monitor remediation over time. Dashboard shows risk reduction, not just tickets closed.

## The Outcome

Organizations using this approach report:

| Metric | Improvement |
|--------|-------------|
| Time to prioritize | 4 hours → 15 minutes |
| Mean time to remediate critical vulns | 45 days → 12 days |
| Remediation of actual high-risk findings | 34% → 89% |

> "We went from remediating based on CVSS to remediating based on actual business risk. Our auditors noticed."
> — Vulnerability Management Lead, Manufacturing

## Get Started

See how your vulnerability data looks enriched with asset context.

[Request a Proof of Value →]
```

## Evaluation Criteria

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Scenario Clarity | Reader immediately understands the situation | Abstract or overly broad context |
| Workflow Specificity | Steps are concrete and actionable | Vague "then it works" hand-waving |
| Practicality | User can envision doing this | Requires capabilities they don't have |
| Outcome Credibility | Results are believable and specific | Unrealistic claims, no quantification |
| Audience Fit | Appropriate for practitioners | Too high-level for implementers |
