---
name: email-copywriting
description: Generate high-value, high-converting emails and email sequences for outbound prospecting, inbound nurture, event promotion, and product communications targeting specific personas with personalized, brand-consistent messaging. Use when the user asks for email copy, email sequences, outreach templates, or any email marketing asset.
---

[Note for the user: tune this skill and the asset types to your requirements - this is a generic example as a starting point]

# Email Copywriting

## Instructions

1. **Identify Email Type:** Determine which type applies to the request
2. **Load Type Guide:** Read the corresponding file from `email-types/`
3. **Review the Brief:** Session should include messaging brief with target persona, objective, and key message
4. **Reference Messaging House:** Extract specific messaging blocks from `/messaging`
5. **Conduct Research (If Needed):** Use WebSearch for real-time market and competitive intelligence
6. **Draft Email Copy:** Apply type-specific guidelines from the loaded guide
7. **Self-Evaluate:** Review against the validation checklist and type-specific evaluation criteria

## Email Type Guides

After identifying the email type, load the corresponding guide:

- **Single Outbound:** See `email-types/single-outbound.md`
- **Outbound Sequence:** See `email-types/outbound-sequence.md`
- **Inbound Sequence:** See `email-types/inbound-sequence.md`
- **Event Promotion:** See `email-types/event-promotion.md`
- **Product Newsletter:** See `email-types/product-newsletter.md`

## Messaging House Context

Look for the following when referencing messaging elements in `/messaging`:

| Context Type    | What to Extract                                    | Source Files                 |
|-----------------|----------------------------------------------------|------------------------------|
| Persona & Pain  | ICP signals, personas and segments, value messages | audience.md                  |
| Voice & Tone    | Narrative, brand voice, style guidelines           | profile.md (voice section)   |
| Value Messaging | Core value propositions, products and solutions    | space.md, portfolio.md       |
| Market Context  | Industry trends, positioning, narrative hooks      | space.md                     |
| Credibility     | Social proof, customer wins, use cases             | proof.md, portfolio.md       |
| GTM Alignment   | Campaign strategy, motion-specific messaging       | motion.md                   |


## Email Copy Guidelines

### Subject Lines
**Character count:** 6-8 words (40-50 characters)

**Effective patterns:**
- Curiosity-driven: Tease the insight ("The action gap plaguing teams")
- Value-driven: Promise an outcome ("Cut your vuln investigation time in half")
- Question-based: Surface persona pain ("Still using spreadsheets for asset management?")

### Cold Outreach
First-touch emails earning attention through signal-driven relevance and insight-led credibility.

**Opening (1 sentence):**
- Lead with a signal (funding, job posting, industry event, company news) or shared challenge
- Or lead with contrarian insight: "The conventional approach to [problem] actually makes [pain] worse"
- Never company introduction or credentials

**Body (2-3 sentences):**
- Explain why the pain matters (cost, risk, opportunity loss)
- One clear value proposition from space.md, tied to persona altitude
- Optional: Brief proof point (customer example, data point)

**CTA:**
- Ask for 15 minutes, not a demo
- Tie to their specific context: "Worth a call to see if this applies to your Q2 compliance timeline?"
- Single, clear, low-friction action

**Format:**
- Word count: 75-150 words max
- Signature: Title that reinforces credibility
- Paragraph breaks every 2-3 sentences

### Nurture Sequences
Multi-touch email series building narrative arc across the sequence.

**Sequence architecture:**
- **Email 1:** Problem awareness + insight (introduce the pain they may not fully realize)
- **Email 2:** Solution framing + your differentiation (how to think about solving it)
- **Email 3:** Proof point + soft CTA (evidence it works, low-friction next step)
- **Email 4+:** Time-based urgency or alternative angle (event, deadline, expanded use case)

**Consistency:**
- Maintain thread continuity (same subject with "Re:" or evolving theme)
- Reference previous emails subtly ("Last week I shared...")
- Build value across the sequence, not in a single email

**Format:**
- Word count: 150-250 words per email
- Each email can layer additional value propositions

### Event Promotion
Driving registration or attendance for events, webinars, or workshops.

**Structure:**
- **Hook:** Why this matters to their world 
- **What's happening:** The event/webinar in plain language
- **Why it matters:** Specific outcome or insight for this persona
- **CTA:** Register, save the date, learn more

**Value framing:**
- Tie to known pain point from persona profile
- Use customer quotes for credibility
- Focus on what they'll gain, not event logistics

**Format:**
- Word count: 100-175 words
- Clear date, time, format (virtual/in-person)
- Low-friction registration

## Evaluation Criteria
- **Relevance:** Speaks directly to persona pain points using relevant signals 
- **Clarity:** Value proposition and CTA immediately understandable, no jargon
- **Consistency:** Matches brand voice/tone, aligns with positioning
- **Specificity:** Uses concrete proof, quantified outcomes, named capabilities vs. generic claims
- **Credibility:** Claims are accurate, altitude matches persona, no overpromising
- **Actionability:** CTA is clear, low-friction, email structure naturally drives to it
- **Deliverability-Friendly:** Natural language, avoids spam triggers, conversational tone
- **Brevity:** 75-125 words, no scrolling required, every word earns its place

## Tropes to Avoid

- Leading with "We" or company introduction
- Multiple CTAs or unclear next steps
- Mismatched altitude (technical to executives, high-level to practitioners)
- Generic pain points that apply to anyone
- Too long (if you need to scroll, you've lost them)
- Weak or missing CTA

## Guidelines

- Optimize for reply rate and conversion, not completeness
- Brutal editing essential - every word must earn its place
- Consult Messaging House for persona and value decisions, never guess
- Generate multi-email sequences one at a time
- If persona not specified, ask before drafting

## Output Format

```markdown
## Campaign Brief
**Type:** [Cold outreach / Nurture email X of Y / Event promotion]
**Persona:** [Target persona]
**Objective:** [Reply, meeting, registration, etc.]
**Key Insight:** [The hook or value angle]
**Key Message:** [The main point to get across]
**CTA:** [Specific action requested]

## Subject Line Options
1. [Primary]
2. [Alternative]
3. [Alternative]

## Email Body

[Plain-text email copy with natural line breaks]

## Follow-Up Angle
[Next email theme or alternative message if CTA not taken]
```
