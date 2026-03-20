# Risk Assessment

A structured framework that helps a prospect or customer identify, surface, and prioritize the risks created by their current state — gaps in coverage, blind spots in their environment, exposures to compliance or operational failure. Risk assessments are typically used at the top of the funnel to create urgency, or in early discovery to help the prospect articulate their risk profile in language their leadership understands.

## When to Use

- Early in the sales cycle, to surface risk the prospect may not have fully quantified
- When the buyer's primary motivator is threat or compliance, not efficiency or cost
- As a self-serve awareness tool for practitioners who suspect they have a problem but can't yet size it
- To arm a champion with risk language to present to a CISO or board

## Primary Audience

Practitioners who will complete the assessment + executives who will receive the output. The questions are written for the practitioner (specific, operational). The output narrative is written for the executive (risk framing, business impact language).

Design for this two-audience pattern: the person who fills it out is not always the person who reads the report.

## Risk Assessment vs. Business Value Assessment

| | Risk Assessment | Business Value Assessment |
|---|---|---|
| Funnel stage | Top / early discovery | Mid / late cycle |
| Primary motivator | Fear, compliance, threat | ROI, efficiency, justification |
| Output tone | Risk exposure, urgency | Financial return, payback |
| Primary reader | CISO, security leadership | CFO, budget committee |
| Anchor metric | Risk score / exposure level | Dollar value / payback period |

## Structure

### 1. Introduction Block

Frame the stakes clearly without being alarmist:

- What this assessment evaluates (which risk domains)
- Who should complete it (specific role, environment scope)
- What the output is (a risk profile with prioritized exposure areas)
- An honest caveat — this is a self-reported assessment; it surfaces likely risks based on inputs, not a formal audit

### 2. Risk Domains

Organize the assessment around 3-6 named risk domains. Each domain should:

- Correspond to a distinct category of exposure the product addresses
- Have a clear plain-language name (not internal product category names)
- Carry a weight in the overall scoring model if certain domains are more critical

**Example risk domains for a cybersecurity asset management context:**

| Domain | What It Measures | Weight |
|---|---|---|
| Coverage Completeness | Percentage of assets under active security tool management | High |
| Discovery Accuracy | How current and complete the asset inventory is | High |
| Vulnerability Exposure | Known vulnerabilities across the visible asset surface | Medium |
| Compliance Readiness | Current state against required framework controls | Medium |
| Operational Resilience | Ability to detect and respond to asset-related incidents | Medium |

### 3. Question Design

Questions within each domain should:

- Be answerable by a practitioner with direct knowledge of their environment
- Use relative scale options that reflect real operational states ("We have [this process] defined and consistently enforced" vs. "We have [this process] informally or inconsistently")
- Avoid binary yes/no where the honest answer is "partially" — force the ambiguous middle to surface
- Be grouped in 3-5 questions per domain (15-25 questions total for the full assessment)

**Scoring scale options:**

For operational maturity questions, a 4-point Likert works well and avoids the "safe middle" of a 5-point scale:
- 4: Fully implemented and consistently enforced
- 3: Implemented but inconsistently applied
- 2: In progress or planned but not yet live
- 1: Not in place

For coverage/inventory questions, percentage ranges work better:
- All or nearly all (>90%)
- Most (70-90%)
- About half (40-70%)
- Less than half (<40%)
- Unknown

**Unknown is always a valid answer.** "I don't know" is itself a risk signal. Build it as a selectable option for coverage questions, and score it as the highest-risk response.

### 4. Domain Scoring

For each domain:

1. Sum the raw question scores
2. Normalize to a 0-100 scale (or a categorical level: Critical / High / Medium / Low)
3. Weight by domain priority if applicable
4. Produce a domain-level risk rating

**Risk level definitions:**

| Level | Score Range | What It Means |
|---|---|---|
| Critical | 0-25 | Significant exposure with high likelihood of impact. Immediate action warranted. |
| High | 26-50 | Material gaps that create meaningful risk. Address within 30-60 days. |
| Medium | 51-75 | Partial controls in place but inconsistently enforced. Plan to close. |
| Low | 76-100 | Controls in place. Monitor and maintain. |

### 5. Overall Risk Profile

Combine domain scores into an overall risk profile. Present as:

- A composite score or level
- A heat map or radar by domain (for visual formats)
- The 1-2 highest-risk domains called out explicitly

Avoid averaging out the picture. A "Low" overall score that hides a "Critical" domain is misleading. Always surface Critical or High domain ratings regardless of the overall score.

### 6. Output Narratives

Write one output narrative per risk level per domain. Each narrative:

- Names the specific exposure the score reflects
- States the likely consequence if unaddressed
- References benchmarks where available ("Organizations at this level typically experience [X] within [timeframe]")
- Is written in risk language the executive can forward to a board

**Example — Coverage Completeness domain, Critical level:**

> Your coverage completeness score indicates significant gaps in your asset inventory. At this level, the likelihood of an unmanaged asset being involved in an incident or audit finding is high. Across enterprise deployments, organizations with similar scores report discovering 15-25% more assets than they had previously inventoried — assets that were operating without active security tool coverage. This represents the highest-risk dimension in your current assessment.

### 7. Recommendations

Each output narrative closes with a risk-level-appropriate recommendation:

- **Critical:** Immediate assessment or POC — this risk warrants rapid evaluation
- **High:** Prioritized discovery — schedule a scoping conversation within 30 days
- **Medium:** Planned remediation — include this in your next planning cycle
- **Low:** Maintenance mode — continue current approach and monitor for drift

## Tone & Style

- **Voice:** Analytical and direct. Risk content should be honest — don't soften findings that are genuinely high-risk.
- **Length:** Question section: 1-2 pages. Output report: 1 page per domain, 1 page summary.
- **Altitude:** Dual-audience — questions written for practitioner, output written for executive

## Delivery Modes

**Self-serve digital:** Practitioner completes online, receives scored report automatically. Optimized for awareness stage — gets the prospect to identify their risk profile before talking to sales.

**Sales-assisted discovery:** AE uses the framework as a structured discovery guide, scoring in real time with the prospect. Output becomes the discovery summary and the basis for the next meeting.

**Executive briefing:** Full report delivered in a 30-minute executive briefing, with the practitioner's inputs and an analyst's interpretation. Used for CISO or board-level engagement.

## Example

**Input:** Create a risk assessment for security teams to evaluate their asset visibility coverage gaps.

**Output:**
```markdown
## Asset Visibility Risk Assessment

This assessment surfaces the risk created by gaps in your current asset visibility program — which assets you may not be seeing, which controls may not be applied consistently, and where your exposure is highest. Complete all sections for the most accurate profile. Most respondents finish in 10 minutes.

_This is a self-reported assessment. It identifies likely risk areas based on your inputs. It is not a formal security audit._

---

### Domain 1: Asset Discovery Coverage

**1.1** What percentage of your total asset footprint (including cloud, contractor, and IoT devices) do you believe is currently reflected in your asset inventory?
_[ ] >90%  [ ] 70-90%  [ ] 40-70%  [ ] <40%  [ ] Unknown_

**1.2** How frequently is your asset inventory updated?
_[ ] Continuously (real-time)  [ ] Daily  [ ] Weekly  [ ] Monthly or less  [ ] Manually on demand_

**1.3** When a new cloud instance or device is provisioned, how quickly does it appear in your inventory?
_[ ] Within hours  [ ] Within a day  [ ] Within a week  [ ] It often doesn't  [ ] Unknown_

---

### Domain 2: Security Tool Coverage

**2.1** What percentage of your known assets have an active EDR agent installed?
_[ ] >90%  [ ] 70-90%  [ ] 40-70%  [ ] <40%  [ ] Unknown_

**2.2** When an asset lacks EDR coverage, how quickly is this detected?
_[ ] Immediately (automated alert)  [ ] Within a day  [ ] Within a week  [ ] Often not detected  [ ] Unknown_

**2.3** Do you have a defined process for bringing newly discovered unmanaged devices under coverage?
_[ ] Yes, defined and consistently followed  [ ] Yes, but inconsistently applied  [ ] Informal / ad hoc  [ ] No defined process_

---

[Continues with remaining domains...]

---

## Your Risk Profile

### Domain Scores

| Domain | Score | Risk Level |
|---|---|---|
| Asset Discovery Coverage | [calculated] | [Critical / High / Medium / Low] |
| Security Tool Coverage | [calculated] | [Critical / High / Medium / Low] |
| Vulnerability Exposure | [calculated] | [Critical / High / Medium / Low] |
| Compliance Readiness | [calculated] | [Critical / High / Medium / Low] |

### Summary

[Output narrative for highest-risk domain]

### Priority Areas

**Immediate attention:** [Domain(s) rated Critical or High, with brief description]

### Recommended Next Step

[Risk-level-appropriate CTA]
```

## Quality Signals

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Unknown as Valid Answer | "Unknown" is a selectable, scored option for coverage questions | Binary questions that force false certainty |
| Domain Independence | Each domain measures a distinct risk category | Overlapping domains that double-count the same risk |
| Score Transparency | Prospect understands how their inputs translate to a score | Black-box score with no explanation |
| Critical Surface Guarantee | Critical domain ratings always surfaced regardless of overall score | Averaged overall score that hides a critical domain |
| Dual-Audience Output | Questions for practitioners, output narratives for executives | Output written at the same altitude as the questions |
| Non-Alarmist Framing | Risk levels are accurate without manufactured urgency | Risk described in apocalyptic terms designed to frighten rather than inform |