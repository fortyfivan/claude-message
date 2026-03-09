# Product Page

The canonical web page for a specific product. Where a prospect goes to understand what the product does, how it's different, and whether it's worth evaluating. This page does more sales qualification than most sales reps — it either pulls the prospect deeper or loses them.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Hero | What it is and why it matters | H1 should state what the product does in outcome terms, not feature terms. Subhead adds the "how" or "for whom." Primary CTA here — above the fold |
| Problem | The pain this product solves | 2-3 sentences describing the status quo pain the target persona lives with. The reader should recognize themselves |
| Capabilities | What the product does | Lead with unique capabilities, follow with core capabilities. Use capability names from the product profile. Each capability should be outcome-framed: "Continuous asset discovery" → "Know your full attack surface — including the assets nobody provisioned" |
| How It Works | Architecture or workflow | Visual-friendly section. Deployment model, integration approach, data flow. Keep it simple — the reader should understand the product's mechanism in 30 seconds |
| Differentiation | Why this, not that | 2-3 differentiators from the product profile, framed as contrast. Use the "Unlike / We" format adapted for web — shorter, punchier than a paper |
| Proof | Evidence it works | Customer quote, key metric, or logo bar. Inline, not deferred. Pull from stories tagged to this product |
| Use Cases | Who uses it for what | 2-3 primary use cases from the product profile. Each should name the persona and the outcome |
| CTA | Next step | Repeat the primary CTA. Match to pricing model: freemium → "Start free," per-seat → "Start a trial," platform → "Request a demo" |

## Tone & Style

- **Voice:** Clear, confident, precise. The page should feel like talking to a smart product person, not reading a brochure
- **Length:** 800-1,200 words of copy (excluding repeated elements). Every word has to earn its place
- **Altitude:** Buyer-accessible with practitioner depth available. Write for the person deciding whether to evaluate, knowing the technical team will also read this page

Don't open with the company name. Don't open with the product category. Open with what the reader gets.

## Key Sources

| Source | What to Extract |
|--------|----------------|
| `products/[name].md` | Tagline, capabilities (unique and core), architecture, differentiation, use cases, value messages |
| `space.md` | Positioning context, key differentiators to reference |
| `personas/[name].md` | The primary buyer persona — pain points, goals, altitude for framing |
| `stories/[name].md` | Product-specific customer quotes and metrics |
| `portfolio.md` | Pricing model for CTA alignment |
| `glossary.md` | Product naming and terminology — critical for web copy |

## SEO/GEO Optimization

- H1 should include the product name and primary keyword naturally
- Each capability section should use the capability name as an H3 for search indexing
- Meta description should state what the product does and for whom in one sentence
- Alt text for any described visuals should include the product name and key terms
- Structure the page so AI engines can extract: what it does, who it's for, how it's different, and one proof point

## Example

**Input:** Write product page copy for the Vulnerability Management module

**Output:**
```markdown
## Hero

# Know What's Exposed. Fix What Matters.

Vulnerability management that prioritizes by real exploitability —
not just severity scores. See your actual risk, act on what's reachable,
and prove remediation to your board.

[Request a Demo →]

## Problem

Your scanner found 10,000 vulnerabilities last week. Your team fixed 50.
Not because they're slow — because they have no way to know which 50
actually matter. Severity scores don't account for your environment,
your architecture, or whether an attacker can actually reach the asset.

## Capabilities

### Runtime Exploitability Analysis
Know which vulnerabilities are reachable in your live environment —
not which ones are theoretically critical. [Company] correlates
vulnerability data with runtime context to surface the findings
that represent real risk.

### Automated Remediation Workflows
Assign, track, and verify fixes without spreadsheet handoffs...

[Continues with How It Works → Differentiation → Proof → Use Cases → CTA]
```

## Evaluation Criteria

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| 5-Second Test | Visitor understands what the product does and who it's for within 5 seconds | Hero requires industry knowledge to parse, opens with company name or category jargon |
| Outcome Framing | Capabilities described as outcomes, not features | Feature list without "so what" — "asset discovery" without "know your full attack surface" |
| Differentiation Clarity | 2-3 clear reasons this product is different from alternatives | No contrast, no "unlike," just self-referential claims |
| Proof Placement | At least one customer quote or metric visible without scrolling past capabilities | Proof deferred to a separate page or buried at the bottom |
| CTA Alignment | Primary CTA matches the pricing model and appears at least twice | Generic "Learn More" instead of action-specific CTA, or CTA only at the bottom |
| Naming Accuracy | Every product name, feature name, and term matches glossary.md | Inconsistent capitalization, alternate names, or deprecated terminology |