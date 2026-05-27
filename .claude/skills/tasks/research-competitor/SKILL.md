---
name: research-competitor
description: Competitor research patterns — pricing pages, product positioning, customer reviews, win/loss heuristics, public filings. Loaded by the researcher subagent when task_type is "competitor". Not user-invocable; dispatched by /run investigation, /design competitor --research, or other workflows.
---

# Research: Competitor

Type-specific patterns for competitor research. The researcher agent handles the general protocol; this file carries the competitor-specific patterns.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, ICP, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## What competitor research surfaces

Findings should answer one or more of:

- **Positioning** — How does the competitor describe themselves? What's their stated category?
- **Differentiation** — What's their primary differentiator? What proof do they cite?
- **Pricing** — Pricing model (per-seat, per-resource, tiered, hybrid)? Published or sales-led?
- **Customer base** — Who's the named customer set? Logos, sizes, verticals?
- **Recent moves** — Product launches, M&A, pricing changes, executive moves, layoffs, pivots in the past 6-12 months
- **Weaknesses** — What do customers complain about? What's the consistent objection?
- **Roadmap signals** — Where are they investing? Hiring patterns, conference talks, public commits

## Source classes

| Source | What it gives | Pattern |
|---|---|---|
| **Competitor's website (product, pricing, customers pages)** | Self-described positioning, claimed differentiators, named logos | WebFetch directly; primary source for stated positioning |
| **Competitor's blog + resources** | Narrative arc, content priorities, persona targeting | Read recent posts (past 3 months) for current narrative |
| **Customer review platforms** (G2, TrustRadius, PeerSpot, Gartner Peer Insights) | Strengths/weaknesses from buyers; competitive comparisons | Read 10-20 reviews; look for repeated themes (3+ mentions = pattern) |
| **Earnings calls** (public competitors) | Forward strategy, segment growth, customer commentary | Past 4 quarters; note segment-by-segment growth |
| **SEC filings** (public competitors) | Revenue mix, customer concentration, risk factors | 10-K for annual; 10-Q for quarterly |
| **Job listings** | Roadmap hints (hiring for X → building X), team composition shifts | LinkedIn jobs page; cross-reference with eng blog |
| **Conference talks + analyst interviews** | Strategic narrative, public positioning | YouTube + analyst sites; past 6 months |
| **Customer wins/losses (your CRM, if accessible)** | Live competitive dynamics | MCP-bridged when available; not part of public research |

## Query patterns

**Positioning + claimed differentiation:**
- WebFetch the homepage, product page, and "Why us" / "vs. competitors" pages directly
- WebSearch: `"[competitor]" positioning OR vs OR alternative` — surfaces comparison content

**Pricing:**
- WebFetch the pricing page
- If "Contact sales" only: WebSearch `"[competitor]" pricing site:reddit.com OR site:news.ycombinator.com` — practitioner reports

**Customer base:**
- WebFetch the customers page
- WebSearch: `"[competitor]" customer case study OR success story`

**Recent moves:**
- WebSearch: `"[competitor]" news 2025` — recent events
- WebSearch: `"[competitor]" funding OR acquisition OR launch OR pivot` — material events
- WebSearch: `"[competitor]" layoffs OR restructuring` — disruption signals

**Weaknesses:**
- WebSearch: `"[competitor]" review G2 OR TrustRadius` — surfaced from review platforms
- WebSearch: `"[competitor]" complaints OR issues OR alternative` — buyer pain

**Roadmap signals:**
- WebSearch: `"[competitor]" job listing engineering` — what they're building
- WebSearch: `site:linkedin.com/jobs "[competitor]"` — current hiring

## Win/loss heuristics

When competitor research is in service of an active deal or campaign, look for:

- **Their strongest pitch** — Read their homepage + first 2 product pages. What's the dominant frame? That's their messaging anchor.
- **Their weakest spot** — Read 10+ G2 reviews. What's the consistent complaint? That's the displacement vector.
- **Their reference customers** — Read 3-5 case studies. What kind of customer succeeds? That's their ICP — not yours.
- **Their pricing posture** — If transparent, note the model. If hidden, that's a finding ("sales-led pricing").
- **Their roadmap heat map** — Where are they hiring? That's where they're investing. Where they're NOT hiring is where they're vulnerable to disruption.

## Output additions

Beyond the researcher's default synthesis structure, competitor research findings should include:

- **Positioning summary** — 1-2 sentences in the competitor's own words (with citation)
- **Differentiation claims** — bullet list of their stated differentiators with sources
- **Pricing model** — structured: model, transparency, observed price points (if any)
- **Named customers** — list with citations (case study URL, customer page URL)
- **Recent material events** — table: date, event, source, impact
- **Weakness patterns** — themes from review aggregation with count + 1 representative quote each
- **Roadmap signals** — what they appear to be investing in based on hiring + public commits

## Common pitfalls

- **Treating their marketing as truth.** Competitor product pages oversell. Always cross-check claimed differentiators against a customer source (case study, review, public reference) before recording.
- **Stale information.** Competitor positioning shifts fast. Anything older than 6 months is reference-only unless corroborated by recent activity.
- **Single-source weakness claims.** One bad G2 review is noise. A pattern of 5+ reviews with the same complaint is a finding.
- **Overreading job listings.** Hiring patterns are forward-looking signals but not proof. Confirm with public commits, product page additions, or roadmap mentions before treating a hire as a roadmap fact.
