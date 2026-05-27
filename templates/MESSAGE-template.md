---
company: [Instructions: Company name. Use official capitalization.]
version: [Instructions: ISO date, YYYY.MM.DD. Update on meaningful revisions.]
maintained-by: [Instructions: Owning team, e.g., "marketing".]
last-reviewed: [Instructions: ISO date, YYYY-MM-DD.]
---

# [Instructions: Company name.]

[Instructions: One-paragraph overview, under 100 words. What the company does, who it serves, why it exists.]

MESSAGE.md is the always-on foundation for every messaging and content task in this repository. The agent reads it before loading any pillar, collection, or asset. The sections below set company altitude, audience, terminology, and brand constraints — content that is invariant across content types, audiences, and channels. Per-instance detail (personas, products, competitors, customer stories) lives in `messaging/pillars/` and `messaging/collections/`.

**Run the `/bootstrap` command to populate this file through an interactive Q&A session**

---

## Attributes

*Market framing to set the right altitude for messaging and content generation*

- **Company type**: [Instructions: B2B SaaS / B2B / B2C / B2D / B2G / nonprofit / open-source / hybrid.]
- **Company stage**: [Instructions: Pre-seed / seed / series A / series B / series C+ / growth / pre-IPO / public / mature.]
- **Primary market**: [Instructions: Category or industry. Be specific.]
- **Position in market**: [Instructions: Challenger / leader / category-defining / niche specialist / disruptor / consolidator.]
- **Regions in operation**: [Instructions: Primary geographies. Use tier framing if broad.]
- **Business model**: [Instructions: Subscription / transactional / licensing / advertising / open-source / hybrid.]

---

## Facts

*Stable company identity attributes for direct reference*

- **Founded**: [Instructions: Year.]
- **Headquarters**: [Instructions: City, region. Or "Distributed (HQ: [city])".]
- **Employees**: [Instructions: Count or range.]
- **Funding**: [Instructions: Total + most recent round, or omit.]
- **Customers**: [Instructions: Public count or range, or omit.]

---

## ICP

*Structured buyer criteria for good fit/bad fit accounts. Personas and segments documented as collections.*

### Characteristics

- **Company type**: [Instructions: Shape of companies we sell to.]
- **Size band**: [Instructions: Range with sweet spot.]
- **Growth stage**: [Instructions: Scale-up / enterprise / mature.]
- **Verticals**: [Instructions: Industries served.]
- **Primary buyer**: [Instructions: Title of economic buyer.]
- **Primary champion**: [Instructions: Title of internal advocate.]
- **Primary end-user**: [Instructions: Day-to-day user.]
- **Tenure**: [Instructions: Typical years in role.]

### Behaviors

- **Buying behavior**: [Instructions: Process pattern — committee, single buyer, PLG, sales-led, hybrid.]
- **Methodology**: [Instructions: How the buyer's team works — agile, DevOps, waterfall, mixed.]
- **Tech maturity**: [Instructions: How they adopt technology — bleeding-edge, fast-follower, conservative.]
- **Cultural fit**: [Instructions: What the buyer values.]
- **Anti-fit**: [Instructions: Cultures we don't sell to. Directive.]

### Environmental

- **Existing tooling**: [Instructions: Tools the buyer already has — affects integration messaging.]
- **Regulatory pressures**: [Instructions: Compliance frameworks or regulatory requirements they operate under. Skip if not relevant.]
- **Industry pressures**: [Instructions: Macro forces affecting their business — consolidation, tech shifts, M&A, talent dynamics.]

---

## Glossary

*Global terminology to adhere to.*

[Instructions: Flat list of terms with usage rules. Include:
- Company name capitalization, possessive form, lowercase exceptions
- Industry abbreviations with usage rules (when to spell out, when alternatives are acceptable)
- Prohibited terms with their replacements
- External products commonly mis-typed (e.g., GitHub, not Github)

Do NOT include:
- Product names → `pillars/portfolio.md`
- Competitor names → `collections/competitors/`
- Customer names → `collections/stories/`
- Persona role titles → `collections/personas/`
- Category names → `collections/categories/`

Aim for 10-20 entries. More than 30 usually means the glossary is duplicating content that lives elsewhere.]

- **[Instructions: Term]** — [Instructions: Usage rule or replacement.]

---

## Brand Guardrails

*Constraints to bind every output to*

[Instructions: 4-8 testable rules. Each must be unambiguously verifiable. No "be authentic" or "sound innovative" — those aren't testable.]

- [Instructions: First absolute rule.]
- [Instructions: Continue for 4-8 total.]

---

## Scenarios

*Vocabulary for runtime messaging assembly. Workflows infer the scenario at task time by combining dimensional values; the agent uses these dimensions to set altitude and posture for each task.*

### Dimensions

| Dimension | Values |
|---|---|
| Compelling event | [Instructions: Customize. Common values: funding, analyst-report, competitor-news, customer-win, executive-change, market-event, none.] |
| Topic maturity | nascent, emerging, established, mature *(spec-defined)* |
| Market moment | [Instructions: Customize. Common values: category-disruption, regulatory-shift, competitive-incursion, consolidation, none.] |
| Strategic shape | competitive-takeout, new-product-introduction, brand-campaign, category-creation, customer-expansion, crisis-response, thought-leadership, demand-generation *(spec-defined)* |
| Content lens | Awareness, Acquisition, Activation, Adoption, Advocacy, Amplification *(spec-defined; the six A's framework)* |

---

## Pillars

*Spec-defined. Top-level messaging elements that cover the full landscape.*

| Pillar | File | Description | Load When |
|---|---|---|---|
| Profile | `pillars/profile.md` | Voice attributes, personality | Always |
| Pitch | `pillars/pitch.md` | Core narrative, key messages | Always |
| Position | `pillars/position.md` | Category claim and differentiators | Marketing content |
| People | `pillars/people.md` | Audience framing by tier | Marketing content |
| Portfolio | `pillars/portfolio.md` | Product summary, capability map | References to products |
| Proof | `pillars/proof.md` | Customer wins, analyst recognition | Marketing content |

---

## Collections

*Spec-defined. Individual profiles loaded on-demand for optimal relevance.*

| Collection | Path | Description | Load When |
|---|---|---|---|
| Personas | `collections/personas/` | Buyer and user personas | Named role or tier |
| Products | `collections/products/` | Individual products and capabilities | Named product |
| Competitors | `collections/competitors/` | Competitors and differentiation | Named competitor |
| Segments | `collections/segments/` | Market segments | Named segment |
| Solutions | `collections/solutions/` | Use cases and vertical approaches | Named use case |
| Stories | `collections/stories/` | Customer wins and references | Named customer |
| Categories | `collections/categories/` | Category positioning and frames | Category-level themes |
| Reports | `collections/reports/` | Analyst recognition and research | Cited research |

---

## Assets

*Catalog of asset types. Briefs reference content type; workflows resolve to asset + variant.*

| Content type | Asset | Default variant | Available variants |
|---|---|---|---|
| [Instructions: Brief verb, e.g. `blog`.] | [Instructions: Asset slug from `messaging/assets/`.] | [Instructions: Default variant slug.] | [Instructions: All variants in the asset's `variants/` directory.] |

[Instructions: Populated incrementally by `/design asset`. CI validates against `messaging/assets/`.]

---

*Progressive loading rules for pillars, collections, and assets are defined in `CLAUDE.md`.*
