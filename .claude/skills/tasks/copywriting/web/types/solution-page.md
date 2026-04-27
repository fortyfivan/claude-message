# Solution Page

A page organized around a buyer outcome — a job-to-be-done, a use case, or a problem space — rather than a specific product. Where a prospect goes when they're searching by problem ("how do I manage my attack surface") rather than by product name. Solution pages typically rank higher for pain-driven search queries than product pages.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Hero | The outcome in one sentence | H1 should state the outcome the buyer achieves, not the solution name. Subhead names the problem being solved. Primary CTA here |
| The Challenge | The problem space in the buyer's words | Describe the pain using the persona's language. Reference ICP environment and maturity. The reader should feel seen, not sold to |
| The Approach | How you solve it | Lead with the method, not the product. "We solve this by [approach]" — the unique approach from the solution profile. Products appear as the enabling capabilities, not the headline |
| Components | What makes it work | Map to the solution's component table — which products and capabilities compose this solution. Keep it visual and scannable |
| Outcomes | What the buyer gets | Before/after framing from the solution profile's Value Delivered section. Quantitative first, qualitative second. Each outcome should be a standalone proof point |
| Proof | Evidence from customers | Customer quote and metric from a story tagged to this solution. Ideally from the same persona viewing this page |
| Who It's For | Personas and segments | Short descriptions of who uses this solution and what it means for each. Connect to persona profiles — the technical evaluator and the business buyer should both see themselves |
| Related Solutions | Cross-sell context | If applicable, 2-3 related solutions that complement this one. Light touch — a sentence and a link, not a pitch |
| CTA | Next step | Repeat primary CTA. Solution pages typically serve mid-funnel prospects — CTAs should reflect evaluation stage (demo, assessment, technical deep-dive) rather than top-of-funnel (whitepaper, webinar) |

## Tone & Style

- **Voice:** Empathetic and credible. You understand the problem because you've seen it across hundreds of organizations — not because you're trying to sell something
- **Length:** 800-1,400 words. Slightly longer than product pages because the problem framing requires more context
- **Altitude:** Buyer persona by default, with supporting depth for technical evaluators

Solution pages should be the highest-empathy content on the website. The Challenge section is where trust is built — if you describe the problem better than the prospect can articulate it themselves, they'll believe you can solve it.

## Key Sources

| Source | What to Extract |
|--------|----------------|
| `solutions/[name].md` | Overview, use case (before/problem/after), unique approach, components, value delivered, personas aligned |
| `products/[name].md` | Capabilities referenced in the components section |
| `personas/[name].md` | Pain points, language cues, altitude — for the Challenge section voice |
| `people.md` | ICP environment context, maturity level for framing |
| `position.md` | Positioning and differentiation context |
| `stories/[name].md` | Solution-specific customer proof |
| `glossary.md` | Terminology — especially for the problem space naming |

## SEO/GEO Optimization

- H1 should target the outcome-driven search query: "Attack Surface Management" or "Continuous Exposure Monitoring" — the terms prospects type when searching by problem
- Challenge section should use the prospect's language for the problem — these are the long-tail keywords
- Outcome metrics should be structured for AI extraction: standalone data points with context
- Meta description should answer "what does [company] do for [problem]" in one sentence
- Solution pages should interlink with related product pages and blog posts for topic authority

## Example

**Input:** Write solution page copy for the Exposure Management solution

**Output:**
```markdown
## Hero

# See Your Real Risk. Act on What Matters.

Every security team finds vulnerabilities. The question is which
ones represent actual exposure — and whether you can fix them before
someone else finds them too.

[See How It Works →]

## The Challenge

You're not short on findings. Your scanner generates thousands of
vulnerabilities a week. Your cloud security tool flags hundreds of
misconfigurations. Your penetration test produced a 200-page report.

The problem isn't detection. It's knowing what to do next.

Which of those 10,000 findings can an attacker actually reach? Which
ones sit behind compensating controls? Which ones matter to the assets
your board cares about? Without that context, your team is triaging
by severity score — and severity scores don't know your environment.

## The Approach

Exposure management starts from the attacker's perspective, not the
scanner's output. Instead of asking "what's vulnerable," we ask
"what's exploitable, reachable, and valuable."

[Company] combines vulnerability data with runtime context,
asset criticality, and network reachability to show you which
findings represent real business risk...

[Continues with Components → Outcomes → Proof → Who It's For → Related → CTA]
```

## Quality Signals

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Problem Empathy | Challenge section describes the pain better than the prospect can | Generic problem statement that could apply to any vendor's solution page |
| Approach Clarity | Reader understands the method before seeing product names | Product-first framing, capabilities before context |
| Outcome Specificity | Before/after metrics with concrete numbers | Vague outcomes ("improve your security posture") |
| Persona Inclusivity | Both the buyer and the technical evaluator see themselves on the page | Written exclusively for one audience, alienating the other |
| Proof Relevance | Customer evidence matches the solution and the likely viewer persona | Generic company proof not specific to this solution |
| Search Intent Match | Page answers the problem-driven query the prospect searched for | Page optimized for brand terms instead of pain-driven keywords |