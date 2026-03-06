# Discovery Guide

A conversation blueprint a rep uses before and during discovery calls. Operates in two modes depending on the input:

**Single Persona Mode** — A guide for discovering against one specific persona. Deep on that persona's pain points, language, and signals. Use when the rep has a single contact and needs to run a focused discovery.

**Committee Mode** — A guide for navigating a buying committee across multiple personas. Maps the discovery journey across stakeholders — who to talk to first, what to learn from each, how to hand context between conversations, and how to identify who's actually driving the decision. Use when the deal involves multiple contacts or the rep needs to expand from one contact into the full committee.

The skill determines the mode from the input. If the user specifies one persona, generate single mode. If the user specifies multiple personas or references a buying committee, generate committee mode. If ambiguous, ask.

## Structure: Single Persona Mode

| Section | Purpose | Guidance |
|---------|---------|----------|
| Persona Snapshot | Quick orientation before the call | Role, altitude, what they care about, what they don't have patience for — in 5 bullet points |
| Opening Framework | How to start the conversation | 2-3 opening questions that establish credibility and get the persona talking about their world. Calibrated to their altitude |
| Discovery Questions by Theme | Structured conversation paths | Group questions by the themes that matter to this persona — organized around their pain points and goals, not your product categories |
| Signals to Listen For | What tells you the deal is real | Specific phrases, complaints, or descriptions that indicate urgency, budget, authority, or active evaluation. Map signals to next actions |
| Language to Mirror | How they talk about their problems | The vocabulary this persona uses for their pain — so the rep can reflect it back. Include terms to use and terms to avoid |
| Objection Previews | What they'll push back on and when | The 3-5 objections this persona typically raises during discovery (not evaluation — those are later). With in-the-moment redirects |
| Qualification Signals | Is this deal worth pursuing | Positive and negative indicators specific to this persona that help the rep qualify in or out quickly |
| Committee Expansion | How to get to the rest of the buying committee | Questions that reveal other stakeholders, and language for asking to be introduced. Who else should the rep be talking to and how to get there from this persona |
| Handoff Notes | What to capture for the next stage | The specific information this discovery should produce that downstream stakeholders (SE, AE, CS) need |

## Structure: Committee Mode

| Section | Purpose | Guidance |
|---------|---------|----------|
| Committee Map | Who's involved and their dynamics | Visual or table showing each persona, their committee role, influence chain, and when they typically engage. Pull from audience.md buying committee patterns |
| Engagement Sequence | Who to talk to first and why | Ordered list of personas with rationale. Usually starts with the champion or evaluator and works toward the decision-maker |
| Per-Persona Discovery Blocks | What to learn from each person | For each persona in the committee: snapshot, opening framework, 3-5 key questions, signals to listen for, and what this conversation should unlock for the next one |
| Cross-Persona Signals | Patterns that emerge across conversations | Signals that only become visible when you talk to multiple stakeholders — alignment or misalignment between what different personas say. "If the CISO says X but the DevOps lead says Y, the deal is at risk because..." |
| Information Threading | How to carry context between conversations | What to reference from earlier conversations when talking to later stakeholders. "When you meet the CISO, reference what the DevOps lead told you about [pain point] — it validates urgency from the practitioner level" |
| Committee Objection Map | Objections by persona and how they interact | How objections from different stakeholders compound or conflict. The CISO's budget concern plus the DevOps lead's integration concern is a different problem than either alone |
| Decision Dynamics | How this committee actually decides | Who has veto power, who defers to whom, where the real decision happens (formal meeting, Slack thread, 1:1 between champion and decision-maker). Help the rep understand the invisible process |
| Qualification Matrix | Committee-level qualification | Not just "is this deal real" but "is this committee aligned enough to buy." Positive signals: stakeholders referencing each other's concerns. Negative signals: personas contradicting each other, key roles not engaged |
| Handoff Notes | What the full discovery should produce | The complete picture downstream stakeholders need — not per-call notes, but the synthesized committee view |

## Tone & Style

- **Voice:** Coaching a colleague before a call. Practical, experienced, specific
- **Length:** Single mode: 1-2 pages. Committee mode: 2-4 pages (more personas, more structure)
- **Altitude:** Match the persona's altitude in single mode. In committee mode, match each persona in their respective block and use neutral operational language in the cross-persona sections

Questions should be written as the rep would actually ask them — conversational, not interrogative. "How does your team handle X today?" not "Describe your current process for X."

## Key Sources

| Source | What to Extract |
|--------|----------------|
| `personas/[name].md` | Pain points, goals, objections, decision criteria, messaging guidance (altitude, lead with, language cues) |
| `audience.md` | Buying committee patterns (committee mode), customer journey stage context, ICP signals |
| `products/[name].md` | Capabilities to probe for need alignment — framed as questions, not pitches |
| `solutions/[name].md` | Use cases to validate during discovery — does their scenario match? |
| `glossary.md` | Terms each persona uses and expects to hear |

## Example: Single Persona Mode

**Input:** Create a discovery guide for the Enterprise CISO

**Output:**
```markdown
# Discovery Guide: Enterprise CISO

## Persona Snapshot
- **Altitude:** Executive — leads with business risk, not technical detail
- **Cares about:** Board reporting, risk quantification, team efficiency, compliance posture
- **Doesn't have patience for:** Feature walkthroughs, technical deep-dives, unsubstantiated ROI claims
- **Reports to:** CRO, CEO, or Board directly
- **Evaluates based on:** Risk reduction metrics, analyst validation, peer references

## Opening Framework

- "What's driving your team's priorities this quarter — is it a specific initiative, an audit finding, or something the board flagged?"
- "How does your team currently report risk posture to the board, and how confident are you in that picture?"

Do NOT open with product capabilities, company background, or "tell me about your security stack."

## Discovery Questions by Theme

### Risk Visibility
- "If I asked you right now how many externally exposed assets your organization has, how close could you get to the real number?"
- "When a new vulnerability drops, how long does it take to know whether you're affected?"

[Continues with remaining themes, signals, objections, committee expansion...]

## Committee Expansion
- "Beyond your team, who else would need to weigh in on a decision like this?"
- "Is there a technical team that would run an evaluation, or does that stay within your org?"
- "How does procurement typically get involved — early or after the technical team has a recommendation?"
```

## Example: Committee Mode

**Input:** Create a discovery guide for the enterprise security buying committee (CISO, VP Engineering, DevOps Lead)

**Output:**
```markdown
# Discovery Guide: Enterprise Security Committee

## Committee Map

| Persona | Committee Role | Engages | Influence | Key Concern |
|---------|---------------|---------|-----------|-------------|
| DevOps Lead | Evaluator | First — feels daily pain | → VP Eng (technical validation) | Integration burden, alert fatigue |
| VP Engineering | Champion | Second — validates technical fit | → CISO (budget recommendation) | Team capacity, implementation timeline |
| CISO | Decision-maker | Last — approves budget and risk | ← VP Eng, ← Board pressure | Risk posture, board reporting, ROI |

## Engagement Sequence

1. **DevOps Lead first.** They feel the daily pain and can validate whether the problem is real at the practitioner level. If their pain isn't acute, the deal isn't real.
2. **VP Engineering second.** The DevOps lead's champion. They translate practitioner pain into a business case. Ask the DevOps lead for the introduction.
3. **CISO last.** They approve budget but rely on VP Eng's recommendation. Arriving at the CISO with practitioner validation and VP-level sponsorship is the play.

## Per-Persona Discovery Blocks

### DevOps Lead

**Snapshot:** Practitioner altitude. Cares about tooling, workflow, and not drowning in alerts.

**Opening:** "Your team is running remediation across [their environment] — how much of that is reactive vs. planned?"

**Key Questions:**
- "How many alerts does your team process in a typical week, and what percentage are actionable?"
- "Walk me through what happens when a critical vulnerability is found — how many handoffs before it's fixed?"
- "What tools are you stitching together today to get a complete picture?"

**Signals:** "We're drowning in alerts" → urgency is real. "We built something in-house" → evaluate build-vs-buy framing. "My VP is asking for metrics I can't produce" → champion path to VP Eng.

**Unlock for next conversation:** Get the specific pain metrics (alert volume, remediation time, tool count) to reference when talking to VP Engineering.

### VP Engineering

**Snapshot:** Technical leadership altitude. Translates practitioner pain into resource and risk decisions.

**Opening:** "Your DevOps team mentioned they're spending [X hours/week] on vulnerability triage — is that sustainable given what's on the roadmap?"

**Key Questions:**
- "If you could get that time back, where would it go?"
- "How do you currently make the case for security tooling investment to [CISO]?"

**Signals:** "I've been telling [CISO] we need to address this" → champion is active. "We can't hire fast enough" → efficiency framing will land.

**Unlock for next conversation:** Get the business framing (team cost, opportunity cost, risk exposure) to present to the CISO in their language.

[Continues with CISO block...]

## Cross-Persona Signals

| Signal Pattern | What It Means | Action |
|----------------|---------------|--------|
| DevOps says "we're fine" but VP says "we need to fix this" | Top-down mandate without practitioner buy-in — implementation risk | Explore why the disconnect exists before proceeding |
| CISO says "budget is tight" but DevOps says "we just had an incident" | Incident creates urgency that can unlock budget — arm the champion with the ROI data | Connect the incident cost to the investment ask |
| All three personas mention the same competitor | Active competitive evaluation — switch to displacement play | Load the battlecard and adjust discovery to competitive framing |

## Information Threading

- **DevOps → VP Eng call:** "Your DevOps lead mentioned the team spends [X hours] on manual triage weekly. That's [Y FTEs] worth of capacity — is that consistent with what you're seeing?"
- **VP Eng → CISO call:** "[VP name] walked me through the team capacity constraints and estimated [cost/risk]. They believe [our approach] could recover [metric]. I'd like to show you how that maps to your board reporting requirements."
```

## Evaluation Criteria

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Mode Fit | Structure matches the input — single persona or committee, not a hybrid | Committee structure for a single persona, or single-person depth for a committee guide |
| Persona Accuracy | Questions map to documented pain points and goals | Generic discovery questions that could apply to any persona |
| Conversation Flow | Questions build naturally — each answer opens the next question | Random list of questions with no logical progression |
| Altitude Match | Language and framing match each persona's seniority | Executive questions phrased like practitioner interrogation |
| Signal Specificity | Listening signals are real phrases reps hear in calls | Vague signals like "they seem interested" |
| Committee Dynamics (committee mode) | Cross-persona signals and information threading are specific | Personas treated independently with no connection between conversations |
| Actionability | Rep can read this 5 minutes before a call and be ready | Background reading that requires study, not a call prep sheet |