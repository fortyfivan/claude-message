---
name: research-company
description: General company research patterns — public records, hiring, news, partnerships, executive moves. Used for customer/partner/prospect research, not for competitor or market research (those have their own task skills). Loaded by the researcher subagent when task_type is "company".
---

# Research: Company

Type-specific patterns for general company research — used when the entity is a customer, prospect, partner, or other named company that isn't a competitor. The researcher agent handles the general protocol; this file carries the company-specific patterns.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, ICP, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## What company research surfaces

Findings should answer one or more of:

- **Identity** — Who are they? Legal name, brand name, sector, size, geography.
- **Trajectory** — Growing, holding, contracting? Recent material events?
- **Strategic posture** — What's their stated strategy or current priority?
- **Buying behavior** — How do they buy (RFP, sales-led, PLG)? Who decides?
- **Tech stack** — What do they already use? Where are integration points or conflicts?
- **Pain or opportunity** — Recent events suggesting acute need (breach, churn, scale event, leadership change)?

## Source classes

| Source | What it gives | Pattern |
|---|---|---|
| **Company website (about, leadership, news)** | Self-described identity, executive team, recent announcements | WebFetch the about + news pages |
| **LinkedIn company page** | Size band, growth signal (employee count delta), recent posts | WebFetch + WebSearch for context |
| **SEC filings** (public) | Verified revenue, customer concentration, stated strategy, risk factors | 10-K annual; 10-Q quarterly |
| **Press releases** | Material events, stated rationale | Past 12 months; longer for partnerships |
| **Trade press** | Industry-perspective coverage | Past 6 months; cross-check claims |
| **Practitioner mentions** (conference talks, blog posts by employees) | What they actually use; cultural signals | Useful for tech-stack signals |
| **Job postings** | Tech stack signals, team composition shifts, hiring priorities | LinkedIn jobs; cross-reference engineering blog |
| **Crunchbase / Pitchbook** | Funding history, investor base, M&A | Background only; not primary source |

## Query patterns

**Identity verification:**
- WebFetch the company's about page directly
- WebSearch: `"[company]" headquarters founded employees`

**Trajectory:**
- WebSearch: `"[company]" news 2025` — recent events
- WebSearch: `"[company]" hiring OR layoffs OR funding` — growth/contraction signals
- WebSearch: `"[company]" earnings OR revenue` (public companies)

**Strategic posture:**
- WebFetch the leadership page + read 2-3 recent CEO/executive posts or interviews
- WebSearch: `"[company]" strategy OR initiative 2025`

**Buying behavior:**
- WebSearch: `"[company]" CIO OR CISO OR "VP engineering"` — decision-maker identification
- WebSearch: `"[company]" rfp OR procurement OR vendor` — process signals
- Search the company's careers page for hints of "head of vendor management" or similar buying-side roles

**Tech stack:**
- WebSearch: `site:linkedin.com/jobs "[company]" engineering` — tech mentions in job descriptions
- WebSearch: `"[company]" engineering blog`
- WebSearch: `"[company]" "uses [tech]" OR "powered by [tech]"`

**Pain or opportunity:**
- WebSearch: `"[company]" breach OR incident OR outage` — security/operational events
- WebSearch: `"[company]" CEO change OR CFO change OR layoffs` — leadership volatility
- WebSearch: `"[company]" acquisition OR merger OR divestiture` — strategic events

## Buying-signal heuristics

When research is in service of an outbound prospect or expansion play:

- **Recent material event** (funding, leadership change, breach, M&A) within past 6 months → high priority signal
- **Stated priority** matching your value prop (e.g., "scaling X" when you sell X-scaling tools) → topical timing
- **Tech-stack adjacency** (use a tool that integrates with yours; use a competitor whose contract is up; use a tool that's deprecating) → integration or displacement opportunity
- **Leadership profile** (champion personality on LinkedIn — public speaker, opinionated, hiring) → champion-fit signal
- **No signal** → de-prioritize; don't fabricate urgency

## Public-record signals (US-centric; adapt regionally)

- **SEC EDGAR** — public filings, executive compensation, ownership changes
- **State business registries** — formation, status, registered agent
- **OSHA / DOL** — workplace incidents (rare but material for some research)
- **Federal contracts** (USAspending.gov, SAM.gov) — gov-sector engagement
- **Patent filings** (USPTO) — innovation signals

Use these sparingly; public-record signals are mostly background context, not primary findings.

## Output additions

Beyond the researcher's default synthesis structure, company research findings should include:

- **Identity card** — Legal name, primary brand, sector, employees, HQ, ownership (public/private/VC-backed/PE-owned), founded
- **Recent material events** — table: date, event, source, implication
- **Strategic posture** — 1-2 sentences in their own words (with citation)
- **Tech stack signals** — list with sources (where each signal came from)
- **Buying-signal summary** — High / Medium / Low / None, with rationale

## Common pitfalls

- **Confusing brand and legal name.** "Alphabet" and "Google" matter for legal/contracts but not for outreach copy. Note both; use the right one per context.
- **Outdated signals.** A 2-year-old funding round isn't a recent event. Apply the time bound strictly.
- **Implying causation from coincidence.** "Hiring a security engineer" doesn't mean "needs security software." Note the signal; don't extrapolate.
- **Privacy boundaries.** Public records and public-facing posts only. Don't use private channels (gated communities, leaked data, scraped private profiles) — flag as inaccessible and move on.
