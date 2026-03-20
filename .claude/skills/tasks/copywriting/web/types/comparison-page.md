# Comparison Page

A bottom-funnel web page designed to capture prospects who are actively evaluating alternatives — "[Company] vs. [Competitor]" or "[Company] vs. [Category Approach]" — and convert them through honest, structured differentiation. Comparison pages rank for high-intent, bottom-funnel search queries and serve buyers at the moment of active decision.

## When to Use

- Named competitor pages: "[Company] vs. [Competitor Name]"
- Category comparison pages: "[Company] vs. [Generic Approach]" (e.g., "vs. spreadsheets", "vs. building in-house")
- Evaluation-stage landing pages used in paid search or ABM programs

## What This Is Not

Comparison pages are not hit pieces. A comparison page that misrepresents a competitor or reads as a one-sided attack damages credibility — buyers know the vendor is biased and will discount the page accordingly. Effective comparison pages are honest about where the competitor is strong and precise about where you win. That honesty is what makes the differentiation believable.

## Competitor Context

Before writing, load the relevant competitor profile from `messaging/competitors/[name].md`. The competitor's strengths, weaknesses, and win/loss patterns from the competitor profile determine what goes in the comparison table and how the differentiation narrative is framed. Do not introduce claims about a competitor that aren't grounded in the competitor profile.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Headline | State the comparison directly | "[Company] vs. [Competitor]: [Differentiating Claim]" — don't bury the point of view |
| Quick Summary | 3-4 sentence orientation | Who each company is, and the one-sentence version of why a buyer might choose one over the other |
| Comparison Table | Structured head-to-head | Evaluation dimensions that matter to the buyer — honest on both sides |
| Where [Competitor] Wins | Honest competitive acknowledgment | The things the competitor does well — typically 2-3 genuine strengths |
| Where [Company] Wins | Your differentiation | The specific, evidence-grounded reasons to choose you — tied to what you know from the competitor profile |
| Who Should Consider Each | Buyer segmentation | The customer profile that fits each option — helps self-select and pre-qualifies inbound |
| Customer Proof | Validation from real buyers | Quotes or metrics from customers who evaluated both and chose you |
| CTA | Next step for an active evaluator | Demo, competitive brief, ROI calculator, or proof of concept offer |

## Tone & Style

- **Voice:** Honest, confident, and direct. The reader is actively evaluating — they want the facts, not marketing.
- **Length:** 900-1,600 words
- **Altitude:** Practitioner and manager — the people doing the evaluation, not the exec signing off

## Headline Patterns

Lead with the differentiating claim, not just the comparison:

- "[Company] vs. [Competitor]: Why Security Teams Switch"
- "[Company] vs. [Competitor]: Asset Coverage Without the Blind Spots"
- "Comparing [Company] and [Competitor]: What 300 Security Teams Found"

Avoid:
- "[Company] vs. [Competitor]: See the Difference" (no point of view)
- "Why [Company] Is Better Than [Competitor]" (too overt — will be discounted)

## Comparison Table

The comparison table is the most-read section of the page. Design it to be skimmable by someone who scrolls directly to it.

**Dimension selection:**
- Include 6-10 dimensions that buyers actually use in evaluations
- Source dimensions from the competitor profile's Product Comparison section
- Include dimensions where the competitor is stronger — omitting them signals bias
- Organize from most to least important for the primary buyer persona

**Cell formatting:**
- Use plain language, not marketing phrases
- ✓ / ✗ or "Full" / "Partial" / "None" for binary and gradient comparisons
- Short phrases (5-8 words) for dimensions that need nuance
- Never bold or highlight only your company's column — it reads as manipulation

**Example dimensions for security/IT tooling:**
- Asset discovery coverage (managed, unmanaged, cloud, IoT)
- Integration depth (native vs. API vs. connector)
- Deployment model (SaaS, on-prem, hybrid)
- Time to first value
- Data freshness / update frequency
- Supported frameworks / compliance mapping
- Support model and SLA

## Where Competitor Wins Section

This section is the trust-builder. If you skip it or write it dismissively, the page's credibility collapses. 2-3 genuine strengths, written accurately:

> **[Competitor] has deep strengths in:**
> - **Established market presence** — [Competitor] has been in the market for 15+ years and is well-known to procurement teams at large enterprises
> - **Professional services depth** — for organizations that want a managed implementation, [Competitor] offers a mature PS organization
> - **[Specific capability]** — particularly strong for organizations whose primary use case is [narrow context]

## Where Company Wins Section

Ground differentiation in the competitor profile's win patterns and your company's specific capabilities. Avoid generic differentiators that any vendor could claim. Each point should be:

- Specific to the comparison (not just a general company claim)
- Evidence-backed (a customer metric, a technical architecture fact, a coverage breadth comparison)
- Relevant to the buyer who searched this comparison

## Who Should Consider Each

This section converts the comparison into a self-selection tool. Frame each option as a genuine fit for a specific buyer profile:

**Choose [Competitor] if:**
- [Honest profile of buyer who is better served by the competitor]

**Choose [Company] if:**
- [Profile of buyer who is better served by you]

This section demonstrates confidence and helps the right buyers convert faster. It also pre-qualifies inbound — a buyer who matches the competitor profile isn't a good prospect anyway.

## SEO/GEO Optimization

- Include both company names in H1, meta title, and meta description
- Target: "[Company] vs [Competitor]", "[Competitor] alternative", "compare [Company] [Competitor]"
- Comparison table should be structured so AI engines can extract it as a side-by-side comparison
- Meta description should name the comparison and the primary differentiating claim
- Page title: "[Company] vs. [Competitor] | [Differentiating Frame]"

## Example

**Input:** Write a comparison page for [Company] vs. [Competitor] in the cybersecurity asset management space. The competitor is stronger on legacy enterprise relationships. We win on coverage breadth and integration depth.

**Output:**
```markdown
# [Company] vs. [Competitor]: Asset Coverage Without the Gaps

**The short version:** [Competitor] is a mature platform with strong enterprise relationships. [Company] finds more assets — including the unmanaged, cloud, and IoT devices that traditional tools miss — and connects to more of the security stack. For teams that have realized their asset inventory has blind spots, that difference matters.

## Side-by-Side Comparison

| Capability | [Company] | [Competitor] |
|---|---|---|
| Managed endpoint coverage | ✓ Full | ✓ Full |
| Unmanaged device discovery | ✓ Full | Partial |
| Cloud asset coverage | ✓ Full (multi-cloud) | Partial |
| IoT / OT asset visibility | ✓ Full | ✗ |
| Integration count | 700+ | 200+ |
| Deployment | SaaS | SaaS / On-prem |
| Time to first inventory | < 24 hours | 2-4 weeks |
| Compliance framework mapping | ✓ | ✓ |

## Where [Competitor] Is Strong

[Honest competitor strengths — 2-3 points]

## Where [Company] Wins

[Specific, evidence-grounded differentiation]

## Who Should Consider Each

**Choose [Competitor] if:** [Honest buyer profile]
**Choose [Company] if:** [Your buyer profile]

## What Teams Who Evaluated Both Found

[Customer proof — quotes or metrics]

[Primary CTA: Request a competitive brief / See a proof of concept / Talk to someone who switched]
```

## Quality Signals

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Competitor Accuracy | Claims about competitor grounded in competitor profile | Claims that misrepresent or exaggerate competitor weaknesses |
| Table Honesty | Comparison table includes dimensions where competitor is stronger | All checkmarks in the company column, all X's in the competitor column |
| Competitor Strengths | Genuine strengths acknowledged and written fairly | Backhanded compliments that read as dismissal |
| Differentiation Specificity | Win areas are specific, evidence-backed, and relevant | Generic "we're better at everything" framing |
| Self-Selection Utility | "Who should consider each" helps buyer route correctly | Framed so that no one would ever choose the competitor |
| Bottom-Funnel Fit | CTA appropriate for an active evaluator | Generic newsletter subscribe or top-of-funnel CTA |