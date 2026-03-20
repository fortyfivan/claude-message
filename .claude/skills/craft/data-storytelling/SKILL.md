---
name: data-storytelling
description: Apply data analysis and narrative craft to content built around datasets, findings, or quantitative claims. Load this skill when the primary evidence for a piece is numerical — customer telemetry, survey data, market research, benchmark studies, or operational metrics. Adds the analyst's perspective to any copywriting skill that handles data-heavy content.
---

# Data Storytelling

This is a craft skill. It is loaded alongside a copywriting skill — not instead of one. The copywriting skill determines structure and output format. This skill determines how data is interrogated, sequenced, visualized, and interpreted.

## The Analyst's Mindset

Before writing a single word of copy, the analyst asks a different set of questions than the writer. The writer asks "how do I structure this?" The analyst asks "does this data actually say what we think it says?"

Work through these before beginning:

**What is the unit of analysis?**
What exactly was measured — individual assets, organizations, time periods, transactions? A finding stated at the wrong unit of analysis is misleading even if the numbers are accurate. "15% of assets lack coverage" and "15% of organizations have uncovered assets" are different claims. Know which one the data supports.

**What does the denominator include?**
Every percentage has a denominator that can be hidden or misread. "23% of cloud assets" — cloud assets in what scope? Customer environments? A specific product? A sample of publicly visible infrastructure? Unstated denominators are where data storytelling loses credibility. State yours.

**Is this correlation or causation?**
The data shows a pattern. Does it show a mechanism? "Organizations with continuous discovery find more vulnerabilities" is a correlation. "Continuous discovery causes more vulnerability detection" is a causal claim. Write the claim that matches the evidence. If causation is implied but unproven, say "associated with" not "causes."

**What's the comparison?**
A number without comparison is an assertion. "15% of assets lack coverage" — compared to what? Last year? Industry average? Theoretical maximum? The comparison is often where the actual finding lives. If no comparison exists, say so rather than presenting the number as if context is self-evident.

**What does the distribution look like?**
Averages hide variance. A mean of 15% could describe a world where everyone is at 15%, or a world where half are at 0% and half are at 30%. If the distribution matters — and it usually does — report it. Quartiles, ranges, or a simple "the highest-risk quartile saw X" adds more information than the average alone.

**What can't this data tell us?**
Every dataset has a scope and the scope has an edge. Telemetry from your product population may skew toward a specific company size, industry, or maturity level. Survey data reflects stated behavior, not necessarily actual behavior. Acknowledging the limitation doesn't weaken the finding — it signals that the analyst knows where the data ends.

## Finding Hierarchy

Not all findings are equal. Before sequencing a findings section, rank every data point on two dimensions:

**Significance:** How much does this change how the reader thinks or acts? A finding that confirms what everyone already knows scores low. A finding that contradicts assumption scores high. A finding that reveals a pattern the reader has felt but never quantified scores highest.

**Evidence strength:** How directly does the data support the claim? Strong: the data directly measures the phenomenon described. Moderate: the data is a proxy for the phenomenon. Weak: the data is suggestive but could support multiple interpretations.

Findings with high significance and strong evidence lead. Findings with low significance or weak evidence don't make the cut — they dilute the report and invite skepticism about the findings that do belong.

**The finding hierarchy:**
1. The headline finding — the one claim the report will be remembered for
2. Supporting findings — 2-4 findings that add dimension to the headline
3. Contextual findings — patterns that explain why the headline finding exists
4. Benchmark findings — comparisons that let the reader locate themselves in the data

## The So-What Standard

Every finding must pass the "so what?" test before it appears in copy. A finding that fails the test is an observation, not a finding.

**Observation:** "73% of organizations have assets they don't know about."
**Finding:** "73% of organizations have assets they don't know about — and those unknown assets are 2.8x more likely to have critical exposures than known assets."

The difference is the implication. The observation describes a state. The finding describes a consequence. Always push through to the consequence.

Apply the test at every level:
- "So what if 73% of organizations have unknown assets?" → They're the highest-risk assets in the environment
- "So what if they're the highest-risk assets?" → They're the ones most likely to be involved in a breach or audit finding
- "So what if they're most likely to be involved?" → Your security posture is determined more by what you don't know about than what you do

Keep pushing until you hit an implication the reader can act on or a risk they recognize. That's where the finding ends.

## Sequencing Findings for Narrative Impact

Data reports fail when they present findings in the order the analyst discovered them, or in the order they rank by statistical significance, or in the order that happens to be convenient. Findings should be sequenced to build an argument.

**The building-tension arc:**
1. Start with the finding that most directly describes the reader's world — creates recognition
2. Show the finding that reveals the problem is bigger than they thought — creates tension
3. Reveal the finding that identifies the specific mechanism or root cause — creates understanding
4. Close with the finding that points toward resolution — creates direction

**The contrast pattern:**
Lead with expectation, follow with reality. "Teams are deploying more security tools than ever. The number of unprotected assets has grown anyway." The gap between expectation and reality is where the reader's attention lives.

**The zoom pattern:**
Start at the population level, then zoom into the subgroup where the finding is most acute. "73% of organizations have unknown assets. In regulated industries, that number rises to 84%. For organizations in their first cloud migration, it reaches 91%." Each layer adds precision and lets the reader find themselves in the data.

## Visualization Logic

Every chart is an argument. Before selecting a chart type, name the argument the visualization needs to make. Then select the chart that makes that argument most directly.

| Argument | Chart Type | Notes |
|---|---|---|
| This is bigger than that | Bar chart (horizontal) | Sort descending. Never use 3D. |
| This is growing over time | Line chart | Show the full time range. Don't truncate the y-axis to exaggerate slope. |
| These things add up to a whole | Stacked bar or area chart | Avoid pie charts — humans are poor at comparing arc lengths |
| There's a relationship between X and Y | Scatter plot | Include a trend line only if the correlation is meaningful |
| Here's how things are distributed | Histogram or box plot | Box plots are underused and carry more information than histograms |
| Here's the breakdown of one thing | Single bar or donut (max 4-5 segments) | If you need a legend, reconsider the chart |
| Here's how one subgroup compares to another | Small multiples or grouped bars | Side-by-side comparison is more honest than overlaid lines |

**Chart anti-patterns to avoid:**

- **Truncated y-axes** — Starting the y-axis above zero exaggerates differences. Use full scale unless there's a methodological reason not to, and label it explicitly if you do
- **Cherry-picked time windows** — Starting the time series at the moment that flatters your narrative. Show the full available range
- **Dual axes** — Two y-axes almost always create a misleading visual correlation. Use two charts instead
- **Chartjunk** — 3D effects, gradients, shadows, and decorative elements reduce precision and signal low analytical confidence
- **Missing error bars** — For sampled data, showing confidence intervals or ranges is more honest than point estimates presented as precise

**Writing chart captions:**

A caption is not a label. "Figure 3: Coverage by asset type" is a label. "Cloud assets show 2x the coverage gap of on-premises assets, with container workloads showing the highest exposure rates" is a caption. Captions interpret. Labels describe. Write captions.

## Statistical Honesty

The data storytelling craft includes knowing where statistical conventions apply and following them.

**Sample size matters.** A finding from 10,000 organizations is more credible than a finding from 50. State the sample size and let the reader evaluate. If the sample is small, qualify the finding: "preliminary data suggests" or "in our initial analysis of 40 deployments."

**Confidence intervals exist.** Survey findings especially carry margin of error. "47% of respondents said X" in a survey of 500 has a margin of error of ±4.4 percentage points at 95% confidence. When precision matters, report it.

**Correlation requires careful language.** "Associated with," "linked to," "correlated with," and "predicts" are all different claims. Use the one that matches what the analysis actually established.

**Base rates matter.** "3x more likely" sounds dramatic. "3x more likely than a 1% baseline" is 3%. Always evaluate relative risk against the absolute rate.

**Outliers should be reported, not hidden.** If one subgroup is driving a finding, say so. If removing outliers changes the conclusion, the conclusion is sensitive to outlier handling and readers deserve to know that.

## The Methodology Section

Write the methodology section for a skeptical peer, not for a credulous reader. The reader who most needs to trust your data is the one who knows enough to evaluate it.

**What to include:**
- Data source (what system, database, or collection mechanism produced the data)
- Population scope (what the sample includes and excludes)
- Time period
- Analytical approach (how findings were derived from raw data)
- Limitations (what the data can't tell you and why)

**What to avoid:**
- Vague sourcing ("based on our data" without defining what "our data" means)
- Limitations buried or softened to the point of invisibility
- Methodology that appears after findings — put it before so readers can evaluate findings with full context

Limitations are trust-builders. "This analysis reflects our customer population, which skews toward enterprise organizations in North America. Results may differ for mid-market or EMEA populations" is honest. It also signals that the analyst knows where the data ends, which is itself a credibility signal.

## Invocation

This skill is loaded alongside the relevant copywriting skill. It does not replace the type guide — it layers analyst discipline on top of the writer's structure.

**Applied to a data findings report:** Load `paper-copywriting` for structure and output format. Load this skill to interrogate the dataset before writing, sequence findings for maximum impact, and write chart captions that interpret rather than label.

**Applied to a data study blog:** Load `blog-copywriting / data-study` for structure. Load this skill to apply the so-what standard to each finding and select visualization types.

**Applied to a business value assessment:** Load `assessment-copywriting / business-value` for framework structure. Load this skill to ensure improvement assumptions are grounded in real distribution data, not point estimates, and to write output narratives that interpret the score in context.

**Applied to a predictions post:** Load `blog-copywriting / predictions` for structure. Load this skill when predictions are anchored in data trends — to ensure the evidence-to-claim relationship is stated correctly and base rates are included.