# Data Study

Examine trends from customer telemetry or market data to surface insights that inform strategy and validate market positioning.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Research Question | What you set out to learn | Frame as a question readers also have |
| Methodology | Data sources and approach | Transparent about scope, limitations, and sampling |
| Key Findings | Top 3-5 insights with visualizations | Lead with the most surprising or impactful finding |
| Analysis | What the data means | Interpret patterns, explain anomalies, connect dots |
| Implications | Actions readers should consider | Translate insight into business decisions |

## Tone & Style

- **Voice:** Analytical, data-driven, objective
- **Length:** 1,200-2,000 words
- **Altitude:** Strategic for executives, methodological transparency for practitioners

Let data lead. Avoid editorializing findings—present what the numbers show, then offer interpretation as a separate layer.

## SEO/GEO Optimization

- Statistics as standalone citations (e.g., "Organizations with continuous asset discovery detect 47% more vulnerabilities")
- Data visualization alt text describing key takeaways
- Methodology transparency for credibility
- Downloadable summary or infographic reference

## Example

**Input:** Write a data study on agent deployment coverage across enterprise environments

**Output:**
```markdown
# The Agent Coverage Gap: What 500 Enterprise Deployments Reveal

## Research Question

How complete is security agent coverage across enterprise environments, and what patterns explain the gaps?

## Methodology

We analyzed anonymized telemetry from 500 enterprise environments spanning 12.3 million endpoints over a 90-day period. Coverage was measured by comparing discovered assets against assets with active security agents reporting within the observation window.

**Scope:** Enterprises with 5,000+ endpoints across North America and EMEA
**Data period:** Q3 2024
**Limitations:** On-premises bias; excludes pure-cloud environments

## Key Findings

### Finding 1: The 15% Blind Spot

On average, 15% of discovered assets lacked any security agent coverage. This represents approximately 1.8 million unprotected endpoints across our sample.

### Finding 2: Cloud Workloads Lead the Gap

Cloud-based assets showed 23% coverage gaps compared to 11% for on-premises assets. Container workloads were particularly underrepresented at 31% gap rate.

### Finding 3: Coverage Decay Is Predictable

Agent coverage degraded at a consistent 2.3% per month without active remediation...

[Continues with analysis and implications]

## Data Summary

| Metric | Value | Context |
|--------|-------|---------|
| Average coverage gap | 15% | Unprotected endpoints |
| Cloud workload gap | 23% | vs. 11% on-premises |
| Monthly decay rate | 2.3% | Without remediation |
```

## Evaluation Criteria

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Methodological Rigor | Clear sampling, transparent limitations | Cherry-picked data, hidden methodology |
| Insight Quality | Non-obvious findings that change thinking | Confirming the obvious without new data |
| Data Visualization | Charts and tables that clarify, not decorate | Misleading scales, unnecessary complexity |
| Statistical Accuracy | Proper use of percentages, averages, significance | Conflating correlation and causation |
| Actionable Implications | Data connects to decisions | Interesting trivia without business relevance |
