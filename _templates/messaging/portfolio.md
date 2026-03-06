---
title: ""
portfolio_structure: ""  # platform | product-suite | single-product | product-and-services
pricing_model: ""     # freemium | per-seat | platform | usage | contact-sales
---

# Portfolio

This pillar defines the products, solutions, and the structure of the company's offering. The Portfolio operates at three altitudes. The portfolio level speaks broadly about the offering and its structure. The product level introduces specific capabilities and differentiation. The solution level grounds everything in real jobs-to-be-done and measurable outcomes. Most content should start at the solution or portfolio level and introduce product specifics only when they're needed to support a claim.

## Messaging Blocks

### Portfolio Overview

[Instructions:
Describe the high-level structure of your offering — the relationship between products, how they compose into a whole, and what the buyer is actually purchasing. This is especially important for multi-product companies, platform + module architectures, and product-led companies with free and paid tiers.]

[Tips:
- Prioritize structure over detail — feature-level discussion belongs in product profiles
- Make hierarchy explicit: what's the platform, what's a module, what's an add-on, what's standalone
- If the portfolio has evolved through acquisition, note which products are native vs. acquired — this affects integration messaging]

[Format:
- **Structure:** [single product | multi-product | platform + modules | product + services]
- **Hierarchy:** [describe the relationship — e.g., "Platform is the core, vuln-mgmt and asset-inventory are modules, professional services is standalone"]
- **Packaging:** [how it's sold — bundled, à la carte, tiered, enterprise-only]

1 paragraph expanding on the structure and how products relate to each other]

### Products

Products are the canonical units of offering within the portfolio. Reference products intentionally — only when they're relevant to the scenario, persona, or use case. When specific products are related to your task, extract the respective profile in `messaging/products/` for in-depth messaging.

| Product | File | Type | Status | Parent | Pricing |
|---|---|---|---|---|---|
| | | | | | |

[Instructions:
List each product as a row in the reference table and create a discrete profile in `messaging/products/[product-name].md`. Type and Status are enums. Parent references the parent product for modules and add-ons (leave empty for top-level products). Pricing captures the per-product model if it differs from the portfolio-level default.]

[Tips:
- Type: platform | product | module | add-on | service
- Status: ga | beta | planned | deprecated
- Parent makes the hierarchy navigable — a module launch campaign needs to reference its parent platform
- Only create product profiles for offerings with distinct messaging — if two products always go to market together with identical positioning, they may be one profile]

### Solutions

Solutions are the use cases of the product in practice — real jobs-to-be-done scenarios where the portfolio delivers meaningful and measurable value. They bridge the gap between product capabilities and buyer outcomes.

Use solutions to ground messaging in what teams are trying to accomplish. A product profile says what it does. A solution profile says what you can achieve with it.

When specific solutions are related to your task, extract the respective profile in `messaging/solutions/` for in-depth messaging.

| Solution | File | Scope | Products | Theme |
|---|---|---|---|---|
| | | | | |

[Instructions:
Document repeatable, outcome-oriented solutions. Solutions may span multiple products or apply to a single product. For each, carve out a distinct profile in `messaging/solutions/[solution-name].md`.]

[Tips:
- Scope: single-product (one product delivers this) | cross-product (requires multiple products) | platform (the platform as a whole delivers this)
- Products: which product(s) power this solution — reference by slug
- Theme: the strategic narrative this solution connects to — e.g., "consolidation," "risk reduction," "developer velocity"
- Only create a solution profile when the use case has its own messaging — distinct audience, distinct proof, distinct value framing. If a use case is just a feature of a product, it belongs in the product profile, not here
- When you have many solutions, group them by theme to avoid messaging sprawl]

## Rules and Guidelines

- Portfolio defines altitude — use it to speak broadly about the offering when product specifics aren't needed
- Products define scope — introduce them only when specificity is required by the persona, scenario, or skill
- Solutions define application — they are the preferred entry point for outcome-led messaging
- Default to solution-level or portfolio-level messaging — drop to product level only when the content requires specific capabilities, architecture, or differentiation
- For platform + module architectures, always reference the parent platform when messaging a module — the module's value is contextual to the platform it extends
- Pricing model informs CTA — freemium products lead with self-serve activation ("try it free"), platform-priced products lead with sales engagement ("request a demo"), per-seat products lead with team evaluation ("start a trial for your team")
- Capabilities justify value — use them to explain why outcomes are achievable, not as standalone claims
- Technical details support credibility — include them selectively, after establishing value
- Avoid long feature lists — introduce capabilities sparingly when they're additive to a value-led narrative
- Prefer buyer outcomes and use cases over product mechanics






## Portfolio Overview

[Instructions:
Describe the high-level structure of your offering. This may be a single product, a multi-product portfolio, a platform with add-ons, or a combination of products and services.

Claude will use this to determine whether to speak at the platform, portfolio, or product level in messaging.]

[Tips:
- Prioritize structure over detail
- Clarify relationships between products (core vs add-on, platform vs application, bundled vs standalone)
- Avoid feature-level discussion here]

[Format:
1 short paragraph describing the portfolio structure and relationships]

## Products

Products are the canonical units of offering within the portfolio.

Reference products intentionally and only when they are relevant to the scenario, persona, or use case.

When specific products are related to your task workflow, extract the respective profile in `messaging/products/` for in-depth messaging.

| Product | File | Type | Status |
|---|---|---|---|
| | | | |

[Instructions:
Document each product as a discrete profile in `messaging/products/[product-name].md`.

Claude will use this to introduce or reference specific offerings when applicable.]

## Solutions

Solutions are the use cases of the product in practice.

Use these to ground messaging in real jobs-to-be-done scenarios and desired outcomes.

When specific solutions are related to your task workflow, extract the respective profile in `messaging/solutions/` for in-depth messaging.

| Solution | File | Scope | Theme |
|---|---|---|---|
| | | | |

[Instructions:
Document repeatable, outcome-oriented solutions where the portfolio delivers meaningful and measurable value. Solutions may span multiple products or apply to a single product. For each solution, carve out a distinct profile in `messaging/solutions/[solution-name].md`.

Claude will use these as tip of the spear messaging, and to anchor business and technical value to what teams are looking to accomplish.]

[Tips:
- Aim for solutions that are both hands-on practical for practitioners and valuable to the business
- When you have a lot of solutions, try to logically group them to avoid messaging sprawl]

## Rules and Guidelines

- Portfolio defines altitude — use it to speak broadly about the offering
- Products define scope — introduce them only when specificity is required
- Capabilities justify value — use them to explain why outcomes are achievable
- Technical details support credibility — include them selectively and last
- Avoid long feature lists; introduce capabilities sparingly when they're additive to a value-led narrative
- Prefer buyer outcomes and use cases over product mechanics
- Elevate product value to meaningful, measurable business or technical impact
