# Competitive Battlecard

A single-page reference a rep pulls up mid-deal when a specific competitor enters the conversation. Not a competitive analysis — a fight card. Everything a rep needs to hold their ground, redirect the conversation, and advance the deal.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Quick Read | 15-second orientation | Competitor in one sentence, their angle, our angle, the one thing to remember |
| Their Pitch | What the prospect just heard | How the competitor positions themselves — use their language, not yours. The rep needs to recognize what they're up against |
| Where They're Strong | Honest assessment | Acknowledge real strengths so the rep doesn't get blindsided. For each strength, provide the redirect — not a dismissal, but a reframe |
| Where They're Weak | Exploitable gaps | Specific, verifiable weaknesses the rep can probe with questions. Frame as discovery questions, not attacks |
| Head-to-Head | Capability comparison | Focused comparison table on the dimensions that actually matter in competitive evaluations. Include "Advantage" column |
| Win Scenarios | When we win and why | Specific deal conditions where we consistently win — the rep should recognize their current deal in one of these |
| Loss Scenarios | When they win and why | Honest assessment of where we lose. Helps reps qualify out early or develop counter-strategies |
| Objection Handling | "But they said..." | The 3-5 things the competitor's champion will say about us, paired with reframes the rep can deliver verbatim |
| Killer Questions | Discovery questions that expose gaps | Questions the rep asks the prospect that surface the competitor's weaknesses naturally, without badmouthing |
| Proof Ammunition | Evidence to close with | Customer quotes, metrics, and stories filtered for this competitive context — ready to drop into a follow-up email |
| Landmines | What to avoid | Things not to say, claims not to make, and traps the competitor sets. What gets us in trouble in this matchup |

## Tone & Style

- **Voice:** Direct, confident, honest. A trusted colleague briefing you before a meeting — not a marketing document
- **Length:** 1-2 pages max. If a rep can't consume it in 3 minutes, it's too long
- **Altitude:** Sales conversation level — consultative, not technical deep-dive

Write in the second person. "When they bring up X, redirect to Y." "Ask the prospect: 'How are you currently handling Z?'" The rep should be able to read a sentence and say it in a meeting.

## Key Sources

| Source | What to Extract |
|--------|----------------|
| `competitors/[name].md` | Their approach, strengths, weaknesses, win/loss patterns, differentiation messages |
| `space.md` | Key differentiators, competitive advantages, positioning |
| `personas/[name].md` | Objections, decision criteria, language cues for the buyer in this deal |
| `stories/[name].md` | Quotes and outcomes filtered for this competitive matchup |
| `products/[name].md` | Capability comparison data, unique vs. core capabilities |

## Example

**Input:** Create a battlecard for Acme Corp targeting enterprise CISO buyers

**Output:**
```markdown
# Battlecard: Acme Corp

## Quick Read
Acme is a legacy vulnerability scanner repositioning as a "unified security platform."
They lead with breadth of coverage. We lead with depth of context.
**Remember:** Acme can't correlate runtime context with vulnerability data — ask about prioritization.

## Their Pitch
"One platform for all your security needs. 15,000 customers. Most comprehensive
coverage in the market." They'll show a dashboard with impressive asset counts
and a long integration list.

## Where They're Strong (and How to Redirect)

| Strength | Reality | Redirect |
|----------|---------|----------|
| Breadth of coverage | Real — they cover more asset types out of the box | "Coverage without context creates noise. How many of those findings are you actually acting on?" |
| Brand recognition | 15 years in market, strong analyst presence | "They built their reputation on scanning. The question is whether scanning is still the right approach." |
| Enterprise installed base | Large customer count, strong references | "Many of those customers are also evaluating alternatives. Ask them about their remediation workflow." |

## Killer Questions
- "How long does it take your team to go from finding a vulnerability to knowing whether it's actually exploitable in your environment?"
- "When your scanner finds 10,000 vulnerabilities, how does your team prioritize which 50 to fix this sprint?"

[Continues with remaining sections...]
```

## Quality Signals

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Speed to Value | Rep finds what they need in under 30 seconds | Dense paragraphs, buried key points, no visual hierarchy |
| Honest Assessment | Competitor strengths acknowledged with redirects | Dismissive of competitor, overpromising on weaknesses |
| Actionable Language | "Say this" and "ask this" phrasing throughout | Abstract descriptions of competitive positioning |
| Scenario Specificity | Win/loss scenarios match real deal patterns | Generic "we're better because..." without conditions |
| Proof Readiness | Quotes and metrics ready to paste into follow-up emails | Proof referenced but not included verbatim |