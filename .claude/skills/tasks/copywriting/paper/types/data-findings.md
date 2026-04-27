# Data Findings

A report built around a specific dataset or analysis — product telemetry, customer benchmarks, threat intelligence, market data, or operational metrics. Lighter on methodology than a research study, heavier on visualization and pattern recognition.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Key Findings | The headlines | 5-7 data points that tell the story. Each should be a standalone quotable statistic with context. This is the section that gets shared |
| Context | Why this data matters now | The market moment, industry challenge, or operational trend that makes these findings relevant. Connect to position.md market trends |
| The Data | What we looked at | Data source, scope, time period. Not a full methodology section — just enough for the reader to trust the numbers |
| Findings in Depth | Pattern by pattern | Each major finding gets its own section: the data point, what it means, why it's surprising or significant, and what the reader should do about it |
| Benchmarks | Where you stand | If the data supports it, provide benchmarks the reader can compare against. "If your MTTR is above X, you're in the bottom quartile" — this makes the report a tool, not just a read |
| Outlook | Where this is heading | What the data suggests about the next 6-12 months. Grounded extrapolation, not speculation |

## Tone & Style

- **Voice:** Data-forward, pattern-oriented. Let the numbers talk, then interpret
- **Length:** 2,000-4,000 words
- **Altitude:** Practitioner-friendly with executive-extractable headlines

Data findings reports are the most shareable long-form asset. The key findings section will travel furthest — invest the most writing energy there. Every finding should work as a LinkedIn post or email subject line.

## SEO/GEO Optimization

- Key findings should be structured as standalone claims with numbers: "[X]% of [population] [finding]"
- Each depth section should have an H2 that states the finding as a headline
- Include benchmark tables — these are high-value for search and AI extraction
- Numbers in headlines outperform narrative headlines for this content type

## Example

**Input:** Write a data findings report on attack surface trends from our platform telemetry

**Output:**
```markdown
# 2026 Attack Surface Report: What 10,000 Enterprise Environments Reveal

## Key Findings

1. **Average external attack surface grew 34% year-over-year** — driven
   primarily by cloud migration and shadow IT, not organic growth
2. **73% of organizations have assets they don't know about** — unknown
   assets account for 12% of the average attack surface
3. **Cloud assets change 3.2x faster than on-prem** — the average cloud
   asset has a 14-day lifecycle versus 45 days for on-prem
4. **The most exploited assets are the most recently provisioned** — assets
   under 7 days old are 2.8x more likely to have critical exposures

## Context

Enterprise attack surfaces are no longer defined by what IT provisions.
They're defined by everything the organization touches...

[Continues with The Data → Findings in Depth → Benchmarks → Outlook]
```

## Quality Signals

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Data Credibility | Source, scope, and time period are clear. Numbers are specific | Vague sourcing ("our data shows"), rounded numbers without precision |
| Finding Impact | Each finding changes the reader's understanding or validates a suspicion | Confirming obvious trends with no new angle |
| Shareability | Key findings work as standalone social posts or email subject lines | Findings that require 3 sentences of context to make sense |
| Benchmark Utility | Reader can compare their own situation against the data | Data presented without reference points |
| Product Restraint | Data speaks for itself. Product appears as one possible response, not the point | Findings that conveniently lead to a product pitch |
| Visual Guidance | Clear direction for charts, tables, and data visualizations | Wall of text with no visualization guidance for design team |