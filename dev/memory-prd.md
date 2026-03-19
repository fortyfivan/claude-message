# PRD: Memory System and Feedback Agent

## Overview

This PRD covers two related additions: a memory layer that tracks learnings across sessions, and a feedback agent that processes real-world signals into messaging system updates.

The messaging house generates content. Content goes into the market. The market responds. Today, those responses have no structured path back into the messaging system. A sales rep discovers that the compliance angle isn't landing with CISOs anymore. A campaign reveals that mid-market buyers respond to a different value prop than expected. A customer uses language to describe their problem that's sharper than anything in the persona profile. These signals are gold — and they evaporate in Slack threads, call notes, and quarterly reviews.

The memory system captures learnings. The feedback agent acts on them.

---

## Memory System

### Purpose

Track content learnings, process learnings, and voice calibration across sessions. The memory system is not a conversation log — it records refined insights, the source they came from, and any action taken. Ten sessions might produce one entry if only one meaningful learning emerged.

### Files

```
messaging/
  journal.md              → Append-only learning log
  voice-calibration.md    → Observed content style patterns
```

Both files are version-controlled and persist across sessions. Any agent can read them. Writing is scoped to specific agents.

### Journal

`messaging/journal.md` is an append-only log of learnings discovered through usage — content iteration, campaign execution, research scans, audits, and direct user feedback.

```markdown
# Journal

Learnings, observations, and refinements discovered through usage.

## Entries

### 2026-03-15
**Source:** Campaign — Q1 vuln-mgmt launch
**Type:** process
**Learning:** Mid-market campaigns don't need an executive brief. The champion
and decision-maker are often the same person.
**Action:** Updated plays/competitive-displacement.md campaign structure.

### 2026-03-12
**Source:** Feedback — sales team input
**Type:** content
**Learning:** Leading with compliance framing in CISO cold outreach gets lower
engagement than leading with board reporting visibility. Three reps confirmed
this independently.
**Action:** Updated personas/enterprise-ciso.md — Lead with changed from
"Risk reduction / Compliance" to "Board reporting visibility / Risk quantification."

### 2026-03-10
**Source:** Tune — skill calibration observation
**Type:** voice
**Learning:** Blog thought leadership drafts consistently start too soft.
User strengthens the hook in every first edit.
**Action:** Noted for next tune run — strengthen hook guidance in
blog-copywriting skills.
```

Each entry has:
- **Date** — when the learning was recorded
- **Source** — which agent, session, or user input produced it
- **Type** — content | process | voice | terminology
- **Learning** — the refined insight in 1-3 sentences
- **Action** — what was done about it (messaging doc updated, noted for future tune, flagged for feedback agent)

The journal is not structured for querying — it's structured for reading. An agent scanning the journal reads recent entries to understand what's been learned and changed. The tune agent reads it during calibration. The audit command reads it to understand context behind recent changes. The feedback agent appends to it after processing user input.

### Voice Calibration

`messaging/voice-calibration.md` captures observed patterns in how the user edits generated content. These are implicit style preferences that emerge from revision patterns rather than explicit instructions.

```markdown
# Voice Calibration

Observed patterns from content editing and user feedback. The tune agent
reads this to refine skill voice guidance.

## Patterns

### [Pattern Name]
- **Observation:** [what the user consistently does]
- **Examples:** [content types where this was observed]
- **Frequency:** [how often — once is a preference, three times is a pattern]

## Active Patterns

### CTA Style
- **Observation:** Prefers direct, short CTAs under 8 words.
  "Request a demo" over "Schedule a personalized demonstration"
- **Examples:** 4 email sequences, 2 landing pages
- **Frequency:** Consistent

### Hedging Language
- **Observation:** Consistently removes hedging language (might, could,
  potentially). Replaces with direct assertions
- **Examples:** 6 blog posts, 3 one-pagers
- **Frequency:** Consistent

### Hook Strength
- **Observation:** Strengthens opening hooks in every first blog revision.
  Prefers provocative statements over contextual scene-setting
- **Examples:** 5 thought leadership posts
- **Frequency:** Consistent

### Company Reference
- **Observation:** Prefers "we" over company name in blog and email content.
  Uses company name only in formal contexts (press, boilerplate)
- **Examples:** Consistent across all content types
- **Frequency:** Consistent
```

Patterns graduate from implicit observation to system-level rules through two paths:

1. **Tune agent** reads voice calibration during skill refinement and bakes patterns into skill guidelines — "prefer direct CTAs under 8 words" becomes a guideline in the email-copywriting skill.
2. **Feedback agent** can promote a voice pattern to profile.md → Brand Voice → Tips & Tricks when the user explicitly confirms it as a permanent preference.

### Agent Access

| Agent | Reads Journal | Writes Journal | Reads Voice Cal | Writes Voice Cal |
|---|---|---|---|---|
| Writer | Yes (recent learnings) | No | Yes (style patterns) | No |
| Campaign | Yes (process learnings) | Yes (post-campaign observations) | No | No |
| Tune | Yes (all learnings) | No | Yes (primary consumer) | No |
| Research | Yes (recent context) | Yes (when scan leads to a learning) | No | No |
| Glossary | Yes (terminology shifts) | Yes (when conflicts resolved) | No | No |
| Audit | Yes (learning history) | Yes (audit findings as learnings) | No | No |
| Feedback | Yes (primary writer) | Yes (primary writer) | Yes | Yes |
| Bootstrap | No (first run) | Yes (initial observations) | No | No |

---

## Feedback Agent

### Purpose

The feedback agent processes real-world signals — from sales conversations, campaign performance, customer interactions, market observations, or any source — and translates them into proposed changes to the messaging system. It's the "voice of the field" pipeline.

The agent doesn't assume the feedback is correct. It analyzes what was said, traces the impact across the messaging house, proposes specific changes with reasoning, and waits for the user to approve, reject, or iterate. It's the only agent besides bootstrap whose primary purpose is modifying messaging docs.

### What Ships

```
.claude/
  agents/
    feedback.md            → Feedback agent definition
  commands/
    feedback.md            → /project:feedback slash command
```

### Invocation

```
/project:feedback [input]
```

The input is unstructured — the user relays what they've heard, observed, or concluded. The agent's job is to structure it.

Examples of input:
- "Sales is saying the compliance angle doesn't land with CISOs anymore. They're responding better to board reporting and risk quantification."
- "Our last three mid-market campaigns all underperformed on the email sequence. Prospects aren't engaging past email 2."
- "A customer described their problem as 'we're drowning in findings but starving for context.' That's sharper than anything in our persona profiles."
- "The competitive displacement play against Acme isn't working. Their new free tier is neutralizing our PLG advantage."
- "Our analyst briefing went well — Gartner is moving us from 'niche' to 'visionary' in the next MQ."

### Agent Process

#### Step 1: Parse the Input

Extract the signal from the user's input:

- **What changed** — the observation, data point, or feedback
- **Source** — where this came from (sales, campaign data, customer conversation, analyst briefing, user observation)
- **Confidence** — is this a pattern (multiple sources confirm) or an anecdote (single data point)?

If the input is ambiguous, ask clarifying questions before proceeding — but keep them focused. "Is this something multiple reps are hearing, or one deal?" matters. "Tell me more about the competitive landscape" does not.

#### Step 2: Trace the Impact

Read the messaging house and identify every doc the feedback touches:

```
Feedback: "Compliance angle doesn't land with CISOs anymore.
Board reporting and risk quantification work better."

Impact analysis:
- personas/enterprise-ciso.md
  → Messaging Guidance → Lead with: currently "Risk reduction / Compliance"
  → Proposed: "Board reporting visibility / Risk quantification"
  → Key Messages: message #3 leads with compliance — may need reframing

- audience.md
  → Customer Journey → Consideration stage → Key Messaging:
    includes compliance framing — may need adjustment

- plays/competitive-displacement.md
  → Play Pitch: opens with compliance risk — needs new opening frame

- skills impact:
  → email-copywriting skills currently tuned with compliance as CISO hook
  → tune agent should recalibrate after messaging update
```

The impact trace should be exhaustive across the messaging house — every doc that references the affected concept. The user needs to see the full blast radius before approving changes.

#### Step 3: Propose Changes

For each impacted doc, propose a specific change:

```markdown
## Proposed Changes

### 1. personas/enterprise-ciso.md (HIGH impact)

**Section:** Messaging Guidance → Lead with
**Current:** "Risk reduction / Compliance"
**Proposed:** "Board reporting visibility / Risk quantification"
**Reasoning:** Multiple sales reps confirm compliance framing isn't
opening doors. Board reporting creates urgency at the executive level
because it connects to their accountability — compliance is downstream.

### 2. personas/enterprise-ciso.md (MEDIUM impact)

**Section:** Key Messages → Message #3
**Current:** "Achieve continuous compliance with automated evidence collection"
**Proposed:** "Give your board real-time risk visibility instead of quarterly
spreadsheets"
**Reasoning:** Reframes the same capability (automated evidence) through
the board reporting lens instead of the compliance lens.

### 3. audience.md (LOW impact)

**Section:** Customer Journey → Consideration → Key Messaging
**Current:** Includes "compliance-driven evaluation criteria"
**Proposed:** Add "board reporting and risk visibility" alongside compliance
(don't remove compliance entirely — it still matters in later stages)
**Reasoning:** Compliance still matters in evaluation, but it's not the
hook that opens the conversation anymore.

### 4. plays/competitive-displacement.md (MEDIUM impact)

**Section:** Play Pitch → opening paragraph
**Current:** Opens with regulatory pressure
**Proposed:** Open with board-level risk visibility gap
**Reasoning:** Aligns the play's opening with the updated CISO messaging
guidance.

## Downstream Effects

- **Tune agent:** Skills calibrated to CISO messaging will need re-tuning.
  Run `/project:tune` after these changes are approved.
- **Campaign agent:** Active campaigns targeting CISOs may need brief updates.
  Check output/campaigns/ for in-progress campaigns.
- **Glossary:** No terminology changes.

## Journal Entry (will be appended after approval)

**Source:** Feedback — sales team input
**Type:** content
**Learning:** Compliance framing no longer opens doors with CISOs.
Board reporting visibility and risk quantification are the effective hooks.
**Action:** Updated persona, key messages, journey stage, and play pitch.
```

Each proposed change carries:
- **Doc and section** — exactly where the change happens
- **Current → Proposed** — the specific text change
- **Reasoning** — why this change follows from the feedback
- **Impact level** — HIGH (core messaging guidance), MEDIUM (supporting content), LOW (contextual reference)

#### Step 4: User Approval

Present the full proposal:

```
Feedback Impact: CISO messaging — compliance → board reporting

Affected docs: 4
  HIGH:   personas/enterprise-ciso.md (Messaging Guidance, Key Messages)
  MEDIUM: plays/competitive-displacement.md (Play Pitch)
  LOW:    audience.md (Journey — Consideration)

Downstream: tune agent re-run recommended, check active campaigns

Approve all, approve selectively, or edit?
```

The user can:
- **Approve all** — all changes applied, journal entry appended
- **Approve selectively** — "apply changes 1 and 2, skip 3 and 4"
- **Edit** — "change the proposed key message to [different wording]"
- **Reject** — no changes, but the observation can still be logged in the journal as a noted signal
- **Defer** — "log this but don't change anything yet — I want to see more data"

#### Step 5: Execute

After approval, the agent:

1. Makes the approved changes to each messaging doc
2. Appends a journal entry documenting the feedback, the learning, and the actions taken
3. Notes downstream effects that need follow-up (tune re-run, campaign updates)
4. If voice calibration patterns were part of the feedback, updates voice-calibration.md

### System Prompt

```markdown
You are a feedback agent that processes real-world signals and translates
them into proposed changes to the messaging system. Your job is to close
the loop between what the market is telling us and what the messaging
house says.

## How You Work

1. Parse the user's input to extract the signal, source, and confidence level.
   Ask focused clarifying questions if the input is ambiguous.

2. Read the messaging house and trace every document the feedback impacts.
   Be exhaustive — check pillars, personas, segments, competitors, plays,
   and the glossary. The user needs to see the full blast radius.

3. Propose specific changes for each impacted doc. Show the current text,
   the proposed text, and the reasoning. Classify each change as HIGH,
   MEDIUM, or LOW impact.

4. Identify downstream effects — does the tune agent need to re-run? Are
   there active campaigns that may be affected? Does the glossary need
   updating?

5. Present the full proposal and wait for the user to approve, reject,
   edit, or defer.

6. After approval, make the changes, append a journal entry, and note
   any follow-up actions.

## Principles

- Feedback is a signal, not a directive. Analyze it critically. One rep's
  anecdote is different from a pattern across five deals.
- Trace the full impact before proposing changes. A change to a persona's
  Lead With affects every skill that targets that persona and every
  campaign that includes them.
- Propose specific text changes, not vague directions. "Update the CISO
  messaging" is not a proposal. "Change Lead With from X to Y" is.
- When feedback contradicts established messaging, surface the tension
  explicitly. "The feedback says X, but space.md positions us as Y.
  Changing this would affect our core differentiation. Are you sure?"
- Log everything. Even rejected feedback gets a journal entry if the
  user agrees — it's a data point that may matter later when more
  evidence accumulates.
- Do not modify messaging docs without explicit user approval. Present
  the plan, get the green light, then execute.

## What You Can Modify

- Any file in messaging/ (pillars, collections, glossary) — with user approval
- messaging/journal.md — append entries autonomously after approved changes
- messaging/voice-calibration.md — update patterns based on feedback about style

## What You Cannot Modify

- _templates/ — never modify templates
- .claude/skills/ — suggest tune agent re-run instead
- output/ — generated content is a downstream effect, not a feedback target
- insights/ — the research agent manages intelligence
```

### Tool Scoping

- **Read** — `messaging/` (full access to trace impact), `output/campaigns/` (check for affected active campaigns), `insights/` (cross-reference with research agent findings)
- **Write** — `messaging/` (with user approval), `messaging/journal.md` (autonomous after approved changes), `messaging/voice-calibration.md` (with user approval)
- **Glob, Grep** — Full access. Used during impact tracing to find every reference to the affected concept
- **WebSearch, WebFetch** — Not used. Feedback is internal signal, not external research

---

## Commands

### /project:feedback [input]

```markdown
Process real-world feedback and propose messaging system changes.

Parse the input for the signal, source, and confidence. Read the
messaging house and trace every doc the feedback impacts. Propose
specific changes with current → proposed text and reasoning.
Present the full impact analysis and wait for user approval before
making any changes. Append a journal entry after execution.

/agents feedback $ARGUMENTS
```

### /project:feedback --log [input]

```markdown
Log an observation in the journal without proposing changes.

For signals that are worth recording but don't warrant immediate
action — early anecdotes, unconfirmed patterns, or observations
the user wants to accumulate before acting on.

Append to messaging/journal.md with type, source, and the observation.
Mark action as "Logged — no changes proposed."

/agents feedback --log $ARGUMENTS
```

---

## Integration Changes

### Writer Agent

Add journal.md and voice-calibration.md to the writer's context loading:

```
Update .claude/agents/writer.md Step 2 (Resolve Context):

| Always load | Why |
|---|---|
| messaging/profile.md | Voice, tone, brand values |
| messaging/space.md | Positioning context |
| messaging/glossary.md | Term definitions and consistency |
| messaging/voice-calibration.md | Content style patterns |

Before generating, scan messaging/journal.md for recent entries (last 30 days)
related to the persona, product, or competitor being targeted. Recent learnings
may affect messaging guidance that hasn't been fully propagated yet.
```

### Tune Agent

The tune agent reads journal.md and voice-calibration.md during calibration:

```
Update .claude/agents/tune.md Step 1 (Read the Messaging House):

Include messaging/journal.md and messaging/voice-calibration.md in the
messaging house read. Journal entries with type "voice" and all voice
calibration patterns should inform skill guidelines. Journal entries with
type "content" may indicate messaging shifts that skills should reflect.
```

### Campaign Agent

Post-campaign observations should be logged:

```
Update .claude/agents/campaign.md Phase 3 (Production), completion:

After all assets are generated and the campaign is complete, review the
campaign execution for process learnings. If patterns were observed
(asset types that weren't needed, sequencing that should change, persona
targeting that should adjust), append a journal entry with type "process."
```

### Audit Command

The audit should read the journal and report on feedback loop health:

```
Update .claude/commands/audit.md:

Add a "Feedback Loop Health" section to the audit report:
- How many journal entries in the last 90 days?
- What percentage of entries resulted in messaging changes?
- Are there deferred entries that should be revisited?
- Are there voice calibration patterns that haven't been promoted to
  profile.md or skill guidelines?
```

### Bootstrap Agent

Bootstrap appends initial observations to the journal:

```
Update .claude/agents/bootstrap.md completion:

After the glossary is generated, append a journal entry noting any
observations from the bootstrap process: assumptions made, conflicts
surfaced, areas where information was thin. Type: "process."
```

### CLAUDE.md

```
Update CLAUDE.md:

Agents section — add feedback agent:

### feedback

Processes real-world signals (sales feedback, campaign performance, customer
language, competitive observations) and proposes specific changes to the
messaging system. Traces impact across all affected docs, presents a plan
with current → proposed text, and executes after user approval. Appends
learnings to the journal.

Invoke: `/project:feedback [input]` or `/project:feedback --log [input]`

Commands table — add:

| `/project:feedback [input]` | Process feedback into messaging changes |
| `/project:feedback --log [input]` | Log an observation without proposing changes |

Directory structure — add:

messaging/
  journal.md             → Append-only learning log (all agents read, select agents write)
  voice-calibration.md   → Observed content style patterns (tune + feedback agents)
```

---

## Deliverables

### New Files
- Agent definition: `.claude/agents/feedback.md`
- Command templates: `.claude/commands/feedback.md`
- Memory files: `messaging/journal.md`, `messaging/voice-calibration.md` (created on first use)

### Modified Files
- `.claude/agents/writer.md` — Add journal + voice calibration to context loading
- `.claude/agents/tune.md` — Add journal + voice calibration to messaging house read
- `.claude/agents/campaign.md` — Post-campaign journal logging
- `.claude/agents/bootstrap.md` — Initial journal entry at completion
- `.claude/commands/audit.md` — Feedback loop health check
- `CLAUDE.md` — Agent description, commands, directory structure