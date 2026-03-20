# Business Value Assessment

A structured framework that helps a prospect or customer quantify the financial impact of their current state and model the potential return from addressing it. Business value assessments are typically used in mid-to-late sales cycles to build the internal business case — giving the champion the numbers they need to justify the investment to a budget owner or executive committee.

## When to Use

- Mid-cycle, after the prospect has confirmed problem awareness — to size the opportunity and build the ROI case
- Pre-renewal, to demonstrate realized value and support expansion
- Executive-level engagement, when the champion needs to present to finance or leadership
- As a self-serve tool for early-stage buyers who want to size the problem before engaging sales

## Primary Audience

Budget owners and champions who need to justify an investment. CFOs, CISOs at the budget stage, VPs who are building a business case for their board or finance committee.

The assessment should generate output the champion can forward directly to their CFO or present in a budget review. Write for that downstream reader, not just the person completing the form.

## Structure

### 1. Introduction Block

Set expectations clearly:

- What this assessment measures (what value dimensions it covers)
- What the output is (a quantified estimate of current-state cost and potential return)
- Time to complete (target: 10-15 minutes)
- A confidence caveat — the output is an estimate based on the inputs provided, not a guaranteed ROI

### 2. Current State Inputs

Gather the data needed to calculate current-state cost. Inputs should be:

- Specific enough to calculate with (not "how large is your team?" but "how many FTE hours per week does your team spend on [specific task]?")
- Easy to estimate without perfect data — most prospects won't have exact figures. Provide ranges and prompts.
- Organized by cost category

**Common cost categories for security/IT domains:**

| Category | Input Type | What to Ask |
|---|---|---|
| Labor cost | Hours × FTE cost | Hours per week spent on [specific task], average FTE fully-loaded cost |
| Tool cost | License and maintenance spend | Current spend on tools being replaced or supplemented |
| Risk cost | Incident probability × cost | Estimated cost of a breach or compliance failure, estimated annual probability |
| Productivity loss | Hours × opportunity cost | Hours per week lost to [specific inefficiency], value of that capacity redirected |
| Compliance cost | Audit and remediation spend | Annual cost of compliance activities, penalties at risk |

Only include categories where the product creates measurable impact. Don't ask about costs where the connection to your solution is speculative.

### 3. Improvement Assumptions

Define the improvement rates used to calculate projected value. These should be:

- Grounded in the Value Evidence metrics from `proof.md`
- Presented as ranges, not point estimates ("typical improvement: 40-60% reduction")
- Adjustable — let the prospect modify the assumption if their situation differs from the benchmark
- Sourced — note that these reflect outcomes across [N] customer deployments

**Format for each assumption:**

> **[Metric]:** Customers deploying [solution] typically see a [range]% reduction in [specific metric]. This model uses [conservative | midpoint | aggressive] — [percentage]%.
> _Based on data from [N] deployments. Adjust if your situation differs._

### 4. Calculated Output

Transform the inputs and assumptions into a financial summary:

- **Current-state annual cost** by category
- **Projected savings** by category (input × improvement assumption)
- **Total projected annual value**
- **Payback period** (annual value ÷ estimated solution cost, if available)
- **3-year projected value**

Format the output as a table the champion can screenshot or export. Include a plain-language summary paragraph above the table.

### 5. Interpretation and Framing

The number alone isn't enough. The output narrative should:

- Contextualize the result ("Organizations of your size with [similar profile] typically see annual value of $X–$Y")
- Name the primary value driver ("In your case, the largest component is [category], which represents [%] of total projected value")
- Translate the financial metric to a strategic frame ("That's the equivalent of [N] additional FTEs, or [X] months of runway at current burn")
- Flag the assumptions used ("This estimate uses a conservative [X]% improvement rate — some customers achieve [Y]%")

### 6. Recommendations

Close with the natural next step based on the output:

- **High estimated value ($X+):** "Your estimated annual value of $[amount] is significant enough to warrant a detailed proof of concept. [CTA: Schedule a POC]"
- **Mid estimated value:** "A 30-day proof of concept would validate these estimates against your actual environment. [CTA: Request a POC scoping call]"
- **Lower estimated value / thin inputs:** "Your inputs suggest [specific gap]. Getting a cleaner baseline on [input] would sharpen the model. [CTA: Talk to a value engineer]"

## Tone & Style

- **Voice:** Analytical, credible, and direct. This document will be forwarded to a CFO. It should read like a financial estimate, not a marketing document.
- **Length:** Question section: 1-2 pages. Output report: 1 page.
- **Altitude:** Executive and senior budget-holder — strategic framing, financial language, business outcomes

## Delivery Modes

**Self-serve digital:** The assessment lives on the website or in a sales tool. Inputs → calculated output → summary report. Design for 10-15 minutes to complete with no sales assistance.

**Sales-assisted:** An AE or SE walks the prospect through the inputs during a discovery call, building the model in real time. Design for conversation — inputs should prompt discussion, not just data entry.

**Value engineer facilitated:** A more detailed version run by a dedicated value engineering resource. Includes a deeper data-gathering phase and a customized output report.

## Example

**Input:** Create a business value assessment for a cybersecurity asset management platform targeting CISOs. Key value drivers are: reduced manual remediation effort, faster compliance reporting, and reduced breach risk exposure.

**Output:**
```markdown
## Business Value Assessment: Security Asset Management

This assessment estimates the annual cost of your current asset management approach and models the potential value of complete asset visibility. Complete all inputs for the most accurate estimate. Most respondents finish in 12 minutes.

_Estimates are based on inputs you provide and improvement rates observed across 400+ enterprise deployments. Outputs are projections, not guarantees._

---

### Section 1: Your Environment

- Total endpoints under management: ___
- Estimated unmanaged/unknown devices (if known): ___
- Cloud environments (check all that apply): [ ] AWS [ ] Azure [ ] GCP [ ] On-prem only

---

### Section 2: Remediation Labor

**Q1.** How many FTE hours per week does your security team spend manually tracking and reconciling asset inventory?
_[ ] <5 hrs  [ ] 5-10 hrs  [ ] 10-20 hrs  [ ] 20+ hrs_

**Q2.** What is the average fully-loaded annual cost of a security analyst FTE at your organization?
_[ ] <$100K  [ ] $100-150K  [ ] $150-200K  [ ] >$200K_

**Q3.** How many hours per quarter does your team spend preparing asset data for compliance audits?
_[ ] <10 hrs  [ ] 10-20 hrs  [ ] 20-40 hrs  [ ] 40+ hrs_

---

### Section 3: Risk Exposure

**Q4.** In the past 24 months, has your organization experienced a security incident linked to an unmanaged or unknown asset?
_[ ] Yes  [ ] No  [ ] Unknown_

**Q5.** What is your estimated cost of a significant security incident (breach, ransomware, compliance failure)?
_[ ] <$500K  [ ] $500K-$2M  [ ] $2M-$10M  [ ] >$10M_

**Q6.** How would you estimate your annual probability of such an incident without improved asset visibility?
_[ ] <5%  [ ] 5-10%  [ ] 10-20%  [ ] >20%_

---

### Improvement Assumptions

These rates reflect outcomes across 400+ enterprise deployments. Adjust if your situation differs.

| Category | Conservative | Midpoint | Aggressive | Model Uses |
|---|---|---|---|---|
| Remediation labor reduction | 40% | 55% | 70% | 55% |
| Compliance reporting time reduction | 50% | 65% | 80% | 65% |
| Risk exposure reduction | 20% | 35% | 50% | 35% |

---

### Your Estimated Annual Value

[Calculated output table: inputs × improvement assumptions → projected savings by category → total]

---

### What This Means

Your estimated annual value of $[X] is driven primarily by [labor | risk | compliance]. Organizations with your asset environment typically see $[range] in year-one value.

At your current tool spend of $[Y], your estimated payback period is [Z] months.

---

### Next Steps

[Score-appropriate CTA]
```

## Quality Signals

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Input Specificity | Questions gather data calculable to a dollar figure | Vague inputs like "rate your asset management maturity 1-5" |
| Assumption Transparency | Improvement rates shown, sourced, and adjustable | Black-box calculation with no visible assumptions |
| Output Exportability | Output formatted for forwarding to a CFO or budget committee | Output only makes sense in context of the conversation |
| Benchmark Grounding | Value estimates contextualized against population data | Absolute numbers with no "is this typical?" framing |
| Conservative Defaults | Model defaults to conservative improvement rates | Model defaults to aggressive rates that overstate expected value |
| Recommendation Fit | Next step calibrated to the output — high value gets higher-commitment CTA | Same CTA regardless of estimated value |