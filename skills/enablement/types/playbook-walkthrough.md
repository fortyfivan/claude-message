# Playbook Walkthrough

A step-by-step operational guide that translates a play from `messaging/plays/` into a sequence of actions a rep or GTM team follows to execute it. Not the strategy — that lives in the play profile. This is the field manual. When the trigger fires, what do you do first, second, third?

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Play Summary | Remind the rep what this play is about | One paragraph: the trigger, the scenario, the outcome. Pull directly from the play profile — do not rewrite positioning |
| Trigger Recognition | How to spot the play in the wild | Specific, observable signals a rep would see in CRM, on a call, or in a prospect's behavior that indicate this play applies. More concrete than the play profile's trigger conditions |
| Execution Sequence | Step-by-step actions | Numbered steps from first touch through conversion. Each step includes: what to do, which asset to use, which persona to target, and what success looks like before moving to the next step |
| Messaging by Stage | What to say at each step | The core message for each stage of the play, adapted to the persona in the conversation. Pull from the play pitch and persona messaging guidance |
| Assets & Where to Find Them | Content the rep needs | Table mapping each step to the specific asset (email template, battlecard, one-pager, etc.) with file location or link. Gaps should be flagged |
| Objection Map | Stage-specific objections | Objections that surface at each stage of the play (not general objections — those live in persona profiles). With stage-appropriate responses |
| Handoff Points | When to bring in reinforcements | Where an SE, executive sponsor, or CS resource enters and what context they need. Include the specific information the rep should pass along |
| Success Metrics | How to know it's working | Leading and lagging indicators for the play — both deal-level (this opportunity) and portfolio-level (this play across all opportunities) |
| Common Mistakes | What goes wrong | The 3-5 ways reps typically misexecute this play and how to avoid each one |

## Tone & Style

- **Voice:** Experienced teammate walking a newer rep through the motion. Practical, direct, no theory
- **Length:** 2-3 pages. Longer than a battlecard because it covers a multi-step sequence, but still scannable
- **Altitude:** Operational — this is a how-to, not a why-to

Write in imperative voice. "Send the competitive comparison email." "Wait 48 hours before the follow-up." "If they mention [competitor], switch to the battlecard." The rep should be able to follow this like a recipe.

## Key Sources

| Source | What to Extract |
|--------|----------------|
| `plays/[name].md` | Trigger conditions, canonical scenario, play pitch, solution set, people alignment, campaign structure |
| `personas/[name].md` | Messaging guidance, objections, decision criteria — for each persona in the play |
| `competitors/[name].md` | If competitive play — strengths, weaknesses, killer questions, differentiation messages |
| `stories/[name].md` | Proof points to embed at specific stages — quote-level fragments the rep can paste |
| `motions.md` | Channel strategy context — which channels support this play's execution |
| `audience.md` | Buying committee for multi-persona sequencing, journey stage alignment |

## Example

**Input:** Create a playbook walkthrough for the Competitive Displacement play targeting Acme Corp

**Output:**
```markdown
# Playbook: Competitive Displacement — Acme Corp

## Play Summary
This play activates when an existing Acme customer's contract is approaching renewal
(within 90 days) and they've shown signals of dissatisfaction — support tickets,
feature requests for capabilities Acme lacks, or internal champions exploring
alternatives. The goal is to position our platform as the upgrade path and close
before the renewal auto-triggers.

## Trigger Recognition

You're in this play when you see any combination of:

- **CRM signal:** Acme listed as current vendor, contract renewal date within 90 days
- **Intent signal:** Prospect visited our competitive comparison page or pricing page
- **Champion signal:** Technical contact downloaded our whitepaper or attended a webinar
- **Complaint signal:** G2 review from the prospect's company mentioning Acme limitations
- **Direct signal:** Prospect mentioned evaluating alternatives on a call or in email

If you see 2+ of these signals, this play is live. Move to Step 1.

## Execution Sequence

### Step 1: Champion Engagement (Day 1-3)

**Action:** Reach out to the technical contact who's shown interest — not the
CISO, not procurement. The person who's feeling the pain daily.

**Asset:** Competitive comparison one-pager (not the full battlecard — that's
for you, not them)

**Message:** Frame around their pain, not our product. "I noticed your team has
been exploring alternatives to Acme. A lot of teams we work with hit a wall
around [specific Acme weakness]. Is that what you're seeing?"

**Success signal:** They confirm dissatisfaction and agree to a technical conversation.

**If stalled:** Send the data study showing the capability gap. Wait 5 business
days before following up.

### Step 2: Technical Validation (Day 4-10)

**Action:** Bring in an SE for a focused technical session. This is NOT a demo.
It's a "let me show you how we handle the specific thing that's frustrating you."

**Asset:** Targeted demo environment configured for their use case. Pre-load
with scenarios that highlight Acme's specific weakness.

**Message:** "Let me show you how we handle [pain point] differently. You tell
me if this actually solves the problem."

**Handoff to SE:** Brief them on: which Acme weaknesses the champion confirmed,
the prospect's environment, and the technical criteria they'll evaluate on.

**Success signal:** Champion says "I need to show this to [decision-maker]."

[Continues through Steps 3-5: Internal Selling, Executive Engagement, Close...]

## Common Mistakes

1. **Going to the CISO first.** The CISO didn't choose Acme and doesn't feel
   the daily pain. Start with the practitioner who does. The CISO enters at Step 4.
2. **Leading with our full platform story.** This is a displacement play, not
   a platform pitch. Lead with the specific gap that Acme can't close.
3. **Ignoring the renewal timeline.** If the contract auto-renews in 30 days
   and you haven't reached Step 3, escalate or accept the loss and set up
   for next cycle.
```

## Evaluation Criteria

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Executability | A rep can follow the steps without interpretation | Vague actions like "engage the prospect" without specifying how |
| Trigger Clarity | Rep recognizes the play from real signals they'd see in their workflow | Abstract conditions that require analysis to identify |
| Stage Transitions | Clear success signals that indicate readiness for the next step | Steps that bleed into each other or have no defined exit criteria |
| Asset Mapping | Every step references a specific, existing asset | Steps that require assets that haven't been created yet (flag the gap) |
| Mistake Prevention | Common failure modes named with specific avoidance guidance | Generic advice like "be prepared" or "do your research" |