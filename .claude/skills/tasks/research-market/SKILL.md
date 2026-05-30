---
name: research-market
description: Market research patterns — TAM analysis, growth trends, segment definitions, industry report sources. Loaded by the researcher subagent when task_type is "market". Not user-invocable; dispatched by /run investigation, /design --research, or other workflows.
---

# Research: Market

Type-specific patterns for market research. The researcher agent handles the general protocol (search vs. fetch decisions, source evaluation, synthesis structure, citation conventions); this file carries the market-specific patterns.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## What market research surfaces

Findings should answer one or more of:

- **Size** — How big is the addressable market? What's the growth trajectory?
- **Segmentation** — What sub-markets exist? Who plays where? What's growing fastest?
- **Inflection** — Is the category being redefined? By whom? On what dimension?
- **Maturity** — Where on the adoption curve? What's the dominant buyer behavior?
- **Adjacent threats** — Which adjacent categories are encroaching?

## Source classes (ordered by authority)

| Source | What it gives | Use for |
|---|---|---|
| **Primary analyst reports** (Gartner Magic Quadrant, Forrester Wave, IDC MarketScape) | Market sizing, vendor positioning, category definitions | Highest-authority claims; cite explicitly |
| **Public market research** (Pitchbook, Crunchbase, CB Insights summaries) | Funding flows, M&A activity, vendor counts | Trajectory signals; corroborate with multiple |
| **Industry trade press** (TechCrunch for B2B SaaS, SC Magazine for security, etc.) | Recent moves, narrative framing | Recency; cross-check claims |
| **Vendor SEC filings** (10-Ks for public players, S-1s for IPO candidates) | Verified revenue, growth, customer counts | Hard numbers; segment with caution |
| **Earnings call transcripts** (via Seeking Alpha, Motley Fool) | Forward-looking vendor positioning | Strategic intent; not market truth |
| **Survey-based research** (Stack Overflow, JetBrains, ESG) | Practitioner sentiment, tooling preferences | Adoption signals; check methodology |
| **Conference content** (RSA, KubeCon, AWS re:Invent keynotes) | Vendor positioning, category narrative | Trends in vendor messaging |

## Query patterns

**Category sizing:**
- `"[category]" market size 2025` — surface analyst figures
- `[category] TAM forecast 2030` — projection horizon
- `[category] growth rate CAGR` — growth trajectory

**Segmentation:**
- `"[category]" segments enterprise vs SMB` — buyer-segment splits
- `[category] vendors comparison` — vendor landscape
- `[category] leaders challengers 2025` — positioning quadrants

**Inflection:**
- `"[category]" 2026 trends predictions` — narrative shift signals
- `"[category]" redefining` — category-creation signals
- `analyst "[category]" emerging` — new categories splitting from old

**Adjacent threat:**
- `[adjacent-category] vs [category]` — encroachment signals
- `[adjacent-category] expanding into [category]` — vendor cross-over

## TAM analysis pattern

When asked for market size:

1. Find 2-3 analyst-derived TAM figures. Note: methodology varies wildly (top-down vs. bottom-up).
2. Note the segmentation each analyst uses — if Gartner sizes "exposure management" at $X and Forrester sizes "attack surface management" at $Y, those may be the same market or overlapping markets. Be explicit.
3. Surface the highest-credibility figure as primary; cite others as corroboration or alternative framing.
4. If figures diverge by more than 2x, that's the finding — the market is poorly defined, not poorly measured.

## Segmentation heuristics

Look for:
- **Buyer size** (enterprise vs. mid-market vs. SMB) — often determines pricing model
- **Vertical** — regulated industries (financial services, healthcare) often carry their own sub-market
- **Geography** — APAC vs. NA/EMEA often have different incumbents
- **Use case** (within category) — "vulnerability management for cloud" vs. "for on-prem" may be different effective markets

A category with one clean segmentation axis is rare. Two intersecting axes (size × vertical) is common. Three is over-segmented; collapse to the most actionable two.

## Maturity signals

Look for the dominant buyer pattern:
- **Nascent** — buyers are educating themselves; few RFPs; lots of pilots
- **Emerging** — RFPs starting; 3-5 vendors competing; pricing volatile
- **Established** — clear leader set (3-5); pricing stabilizing; M&A activity
- **Mature** — consolidation; new growth from adjacent extensions; pricing pressure

Match the maturity finding to MESSAGE.md Scenarios `Topic maturity` enum: nascent, emerging, established, mature.

## Output additions

Beyond the researcher's default synthesis structure, market research findings should include:

- **Market sizing table** — analyst, figure, methodology note, date
- **Segmentation map** — primary segmentation axis with key players in each cell
- **Maturity assessment** — single value (nascent/emerging/established/mature) with rationale

## Common pitfalls

- **TAM inflation.** Analysts size for their own narrative — a vendor's quoted TAM is often the sum of multiple analyst categories. Cite the analyst's own segment, not the vendor's interpretation.
- **Recency bias on inflection.** A single new analyst report doesn't mean category inflection. Look for corroboration: 2+ analysts framing similarly, vendor messaging shifts, M&A pattern.
- **Vendor framing as market truth.** A vendor's product page tells you what the vendor sells, not what the market needs. Cross-check with practitioner sources before treating vendor language as the category vocabulary.
