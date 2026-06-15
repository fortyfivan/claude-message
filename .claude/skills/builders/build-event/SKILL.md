---
name: build-event
description: Builds a four-phase event program — strategy brief, pre-event, on-site, and post-event waves — with phase-distinct audiences and asset mixes generated in one end-to-end session. Use when the user wants to plan content around a conference, hosted event, partner event, regional event, or hospitality event.
---

# build-event Skill

Build a complete event program through a four-phase production process. The result is a master brief that captures event strategy and asset plan, followed by three time-spaced production waves (pre-event, on-site, post-event) that produce the full asset set.

Events are time-bounded and multi-phased. They have distinct audiences and goals per phase — drive registration before, capture and convert during, follow up after. The builder respects that structure.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona"). If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## Skill Composition

- **Loads at builder level:** the event-type's Context Loading pillar set (see below).
- **Loads after intake:** selected persona, product, partner, competitor collections; supporting stories.
- **Loads once per event (passed inline to writers):** the voice craft skill.
- **Loads once per asset (passed inline):** the asset envelope (and variant, when declared).
- **Dispatches:** the writer subagent per asset (parallel within each wave). Each wave runs independently; the brief is the shared spine across all three.
- **Per-asset reader dispatch:** the reader subagent per asset; reader_mode chosen per asset (subagent for high-stakes booth/exec/hospitality content, inline for derivatives like live social templates).

Invocation: `/build event [event-name]` runs the brief plus all three production waves end-to-end in one session. Add `--brief-only` to produce the brief without dispatching waves.

---

## Context Loading

Load these pillars at the start of brief writing; defer the rest until needed for a specific wave. v1 calibration — tune after the first few real event sessions.

| Event type | Always at brief | Deferred until needed |
|---|---|---|
| **industry-conference** | profile, pitch, position, people | portfolio (load when booth/demo assets enter scope), proof (load when post-event recap assets enter scope) |
| **hosted-conference** | profile, pitch, people, proof | portfolio, position (load when product moments enter the agenda) |
| **partner-event** | profile, pitch, position | people (partner-persona collection), portfolio (joint solution), proof (joint stories) |
| **regional-event** | profile, pitch, people | position, portfolio, proof (load only if the regional agenda surfaces them) |
| **hospitality-event** | profile, people, proof | pitch, position, portfolio (load only if a product moment is on the agenda) |

Brief writing always loads `proof.md` if not already loaded for the chosen type — proof matching for follow-up sequences is non-negotiable. Position loads if the event has a competitive angle (keynote framing, analyst presence, head-to-head moment).

During intake, route through pillar Collection Tables before loading any collection profile. Read frontmatter of candidates first to enrich AskUserQuestion options; load full bodies only after user confirms selection.

---

## What build-event produces

A complete event program organized in `output/events/[event-slug]/`:

- **brief.md** — master event brief covering strategy, audience, positioning, and asset plan across all four phases
- **pre/** — registration push, meeting booking outreach, social promotion, sales enablement, landing pages
- **onsite/** — booth copy, demo scripts, speaker materials, hospitality content, live social templates
- **post/** — segmented follow-up sequences, recap content, customer features, surveys
- **_meta/** — audit trail per asset

---

## Phase 1: Strategy brief

Resolve the event name first: use the argument if provided, otherwise ask for the kebab-case name (becomes the directory slug). Then run a single interview that captures the full event picture — the brief is the source of truth for all subsequent waves.

### Interview structure

Five rounds, batched within each round. Don't interrupt between rounds.

**Round 1: Event identity**
- Event name, dates, location (or virtual)
- Event type (industry conference / hosted conference / partner event / regional event / hospitality event)
- Our role (sponsor + level / exhibitor / host / partner / attendee-only)
- Speaking opportunities (none / session / panel / keynote / multiple)
- Booth presence (none / small / large / experience)
- Budget tier (small / mid / large — informs asset volume)

**Round 2: Goals and audience**
- Primary goal (lead generation / brand exposure / customer love / executive presence / launch moment / pipeline acceleration)
- Measurable success metrics (registrations, meetings booked, MQLs, pipeline, customer satisfaction score, etc.)
- Target audience at this event (which personas, which accounts if ABM-style, what mix of prospects vs. customers)
- Audience size expectation (attendees we'll reach across all touchpoints)

**Round 3: Positioning**
- Event theme or hook (often distinct from steady-state messaging — tied to a product moment, customer story, industry shift, or category claim)
- Key messages specific to this event
- Tie to current campaigns or product launches (if any)
- Differentiation angle for this event specifically

**Round 4: Cross-functional plan**
- Who owns each phase (marketing operations, field marketing, sales, executive sponsors, product, customer marketing, partner marketing)
- Sales engagement model (meeting booking, named accounts, follow-up cadence)
- Executive involvement (which executives, what roles — keynote, dinner host, booth presence)
- Customer participation (are customers attending, speaking, joining hospitality)
- Partner involvement (if joint event or co-marketing)

**Round 5: Asset plan**
The agent infers an initial asset plan from rounds 1-4, then walks it back to the user for confirmation. Asset plan organizes by phase:

- **Pre-event assets**: emails (registration push, meeting booking, customer invitation, partner outreach), social posts (announcement, speaker promotion, booth tease, session promotion), landing page (event hub, meeting booking), sales enablement (account brief, talking points, meeting request templates), press/analyst materials (if hosting or announcing)
- **On-site assets**: booth messaging (backdrop, panels, signage, demo zone), demo scripts (calibrated to expected booth visitors), speaker materials (abstracts, slide narrative, talking points), hospitality content (invitations, conversation starters, briefing docs), live social templates (with placeholders for live moments), press kit
- **Post-event assets**: segmented follow-up sequences by interaction tier (booth visitor, meeting attendee, session viewer, demo recipient, hospitality guest, customer attendee, partner/speaker), sales follow-up templates per tier, recap content (blog post, customer features), session recording promotion, social recap, post-event survey

The agent presents the inferred plan for each phase as a table:

```
Pre-event assets:
1. Email — Registration push (to cold list)
2. Email — Meeting booking outreach (to target accounts)
3. Social — Announcement + speaker promotion (3 posts)
4. Landing page — Event hub with meeting booking
5. Sales enablement — Account brief for top 20 accounts
```

User confirms, adds, or removes assets per phase. The final asset plan locks at the end of Round 5.

### Scenario inference

The brief frontmatter captures the inferred scenario:

```yaml
scenario:
  compelling-event: event-presence
  topic-maturity: [inferred from messaging context]
  strategic-shape: [inferred — typically thought-leadership, new-product-introduction, or brand-campaign]
  content-lens: [shifts per phase — Acquisition pre, Activation onsite, Advocacy post]
```

Content lens varies across phases. The orchestrator applies the appropriate lens to each wave's writer dispatches.

### Brief output

The brief writes to `output/events/[event-slug]/brief.md` with structure:

```markdown
---
event: [name]
slug: [slug]
dates: [start - end]
location: [city / virtual]
event-type: [type]
our-role: [role]
budget-tier: [tier]
status: brief-approved
scenario:
  compelling-event: event-presence
  topic-maturity: [value]
  strategic-shape: [value]
  content-lens-pre: [value]
  content-lens-onsite: [value]
  content-lens-post: [value]
---

# [Event name] Event Brief

## Strategy
[Goals, metrics, positioning, theme]

## Audience
[Target personas, accounts, customer/prospect mix]

## Cross-functional plan
[Who owns what, sales engagement, exec involvement, customer/partner participation]

## Extracted Context
[Positioning passages, key messages, glossary subset, proof passages relevant to this event — inlined for writer dispatches]

## Asset plan

### Pre-event
[Numbered list of assets with type, variant, target audience, owner, due date]

### On-site
[Numbered list of assets]

### Post-event
[Numbered list of assets]
```

User reviews and approves the brief before any wave dispatches.

---

## Phase 2: Pre-event wave

Fires 4-8 weeks before the event (or per the user's preferred lead time). Produces all pre-event assets per the brief.

### Orchestration

For each pre-event asset in the brief:

1. Determine the asset definition and variant (from MESSAGE.md catalog)
2. Compose dispatch payload:
   - Extracted Context from brief
   - Asset definition + variant
   - Asset slice from brief (target audience, key messages for this asset, CTA)
   - Content lens (typically Acquisition for pre-event)
   - Voice gate (inlined)
3. Dispatch writer subagent
4. For high-stakes assets (landing pages, exec-facing emails, sales enablement), dispatch reader subagent after writer
5. For assets declared with HTML production targets (landing page, email), dispatch producer subagent
6. Write outputs to `output/events/[event-slug]/pre/`

### Pre-event asset patterns

Common pre-event assets and their typical characteristics:

| Asset | Audience | Lens | Production |
|---|---|---|---|
| Registration push email | Cold prospects | Acquisition | email |
| Meeting booking outreach | Target accounts | Acquisition | email |
| Customer invitation email | Customers | Advocacy | email |
| Announcement social | General audience | Awareness | none |
| Speaker promotion social | Topic-interested audience | Awareness | none |
| Event hub landing page | All audiences | Acquisition | web |
| Meeting booking page | Sales targets | Acquisition | web |
| Account brief | Internal sales | n/a | none |
| Talking points doc | Internal sales | n/a | none |
| Press release | Press / analysts | Awareness | none |

Hospitality events add: personalized invitation emails per attendee (tier 1), executive briefing docs (tier 1).

---

## Phase 3: On-site wave

Fires 1-2 weeks before the event for assets needing prep (booth copy, demo scripts, speaker materials). Live-fill templates produced in the same wave for use during the event itself.

### Orchestration

For each on-site asset in the brief:

1. Determine asset definition and variant
2. Compose dispatch payload:
   - Extracted Context from brief
   - Asset definition + variant
   - Asset slice (specific purpose — booth panel, demo script for persona X, speaker abstract for session Y)
   - Content lens (typically Activation or Awareness for on-site)
   - Voice gate (inlined)
3. Dispatch writer subagent
4. For high-stakes assets (booth backdrop copy, executive talking points, keynote materials), dispatch reader subagent
5. Producer dispatch for any HTML-bound assets (rare in on-site phase; most assets are physical or presentation-format)
6. Write outputs to `output/events/[event-slug]/onsite/`

### Live-fill templates

Some on-site assets are templates designed for fill-in during the event:

- Live social posts (with placeholders for live moments, executive quotes, customer features)
- Session recap copy (templated by session type)
- Hashtag strategy doc (governance for live social usage)

The writer generates these with explicit placeholder markers and usage notes. Output includes a "during-event playbook" doc that summarizes how to use the live-fill templates in the moment.

### On-site asset patterns

| Asset | Audience | Lens | Production |
|---|---|---|---|
| Booth backdrop copy | Booth visitors | Awareness | none |
| Booth side panel copy | Booth visitors | Awareness | none |
| Demo script | Demo viewers | Activation | none |
| Speaker abstract | Session registrants | Awareness | none |
| Speaker slide narrative | Session attendees | Acquisition | none |
| Talking points doc | Internal speakers | n/a | none |
| Hospitality dinner invitation | Named VIP attendees | Advocacy | email |
| Executive briefing doc | Internal executives | n/a | none |
| Live social templates | Social audience | Awareness | none |
| Hashtag strategy | Internal social team | n/a | none |
| Press kit | Press / analysts | Awareness | none |

---

## Phase 4: Post-event wave

Fires within 48 hours of event close. Produces follow-up sequences and recap content.

### Orchestration

Post-event has the most complex audience segmentation. The user provides interaction data (booth visitors, meetings taken, session attendees, hospitality guests, etc.) or the builder can produce templates for each tier with the user populating specifics later.

For each post-event asset in the brief:

1. Determine asset definition and variant
2. Compose dispatch payload:
   - Extracted Context from brief
   - Asset definition + variant
   - Asset slice (interaction tier — what tier this follow-up serves, what they experienced)
   - Content lens (Adoption for customer follow-up, Advocacy for customer feature recap, Acquisition for prospect follow-up)
   - Voice gate (inlined)
3. Dispatch writer subagent
4. Reader subagent for follow-up sequences (high stakes — these go to real prospects and customers)
5. Producer dispatch for recap blog posts (web target) and email sequences (email target)
6. Write outputs to `output/events/[event-slug]/post/`

### Post-event asset patterns

| Asset | Audience | Lens | Production |
|---|---|---|---|
| Follow-up email — booth visitor | Booth visitors (warm) | Acquisition | email |
| Follow-up email — meeting attendee | Meeting attendees | Acquisition | email |
| Follow-up email — session viewer | Session attendees | Acquisition | email |
| Follow-up email — demo recipient | Demo viewers | Activation | email |
| Follow-up email — hospitality guest | VIP attendees | Advocacy | email |
| Follow-up email — customer attendee | Customers | Adoption | email |
| Follow-up email — partner/speaker | Partners, co-speakers | Advocacy | email |
| Sales follow-up templates | Internal sales | n/a | none |
| Recap blog post | General audience | Awareness | web |
| Customer feature blog | Customer-interested audience | Advocacy | web |
| Session recording promotion email | Session registrants | Acquisition | email |
| Social recap | Social audience | Awareness | none |
| Post-event survey | Attendees | n/a | none |

Each follow-up email gets a matching sales follow-up template — what marketing sends, what sales sends second.

---

## Output Structure

```
output/events/
  [event-slug]/
    brief.md
    pre/
      [id]-[slug].md          ← markdown deliverable
      [id]-[slug].json        ← JSON deliverable (CMS-ready)
      ...
    onsite/
      [id]-[slug].md
      [id]-[slug].json
      ...
    post/
      [id]-[slug].md
      [id]-[slug].json
      ...
    _meta/
      [id]-[slug].md          ← audit trail per asset
      ...
```

Each writer produces both `.md` (clean handoff) and `.json` (CMS ingestion); per-asset audit trails sit in `_meta/`. The team holds the generated assets and deploys at the human-chosen time (pre-event content typically 4–8 weeks out, on-site 1–2 weeks before, post-event within 48 hours of close).

---

## Tool scoping

- Read, Write, Edit: full access for messaging house files and event output
- Glob, Grep: for messaging house content and prior event outputs
- AskUserQuestion: for the five-round interview and asset plan confirmation
- Task: dispatch writer, reader, producer subagents
- WebSearch, WebFetch: minimal use during brief (event-specific research if needed); none during production waves

---

## Reference

### Handling event types

Different event types calibrate the asset plan defaults:

- **Industry conference** (RSA, Dreamforce, Black Hat): emphasize meeting booking pre, booth + demo on-site, segmented follow-up post
- **Hosted conference** (your user summit, customer event): emphasize registration drive pre, keynote and breakout support on-site, recap and recording promotion post
- **Partner event** (joint webinar, co-marketing): emphasize co-branded promotion pre, joint delivery on-site, joint follow-up post — coordinate on shared assets
- **Regional event** (roadshow stop, local meetup): emphasize location-targeted invitation pre, focused agenda on-site, local follow-up post — smaller asset volume
- **Hospitality event** (executive dinner, advisory board): emphasize personalized invitation pre, intimate experience on-site, high-touch follow-up post — account-level personalization throughout

The interview detects event type in Round 1 and pre-populates likely asset patterns accordingly.

### Brief frontmatter status states

- `brief-draft` — interview in progress
- `brief-approved` — brief locked, production proceeds
- `event-complete` — all four phases done

The brief.md frontmatter records what was produced so the team can audit the program after the session ends.

### Multi-event coordination

For organizations running multiple events in parallel or in a series, each event lives in its own `output/events/[slug]/` directory. The builder doesn't coordinate across events; user manages event-to-event learning manually or via the feedback mechanism.

### Cross-functional reminders

The brief captures cross-functional ownership but doesn't enforce it. The builder surfaces ownership in the brief and per-asset metadata so the user and team know who's expected to drive each asset. Sales follow-up templates, executive briefing docs, and account briefs are marked as internal-only deliverables (not customer-facing).

### Writing conventions

- Pre-event assets lead with the event and the value proposition for attending
- On-site assets are concise, tactical, designed for in-the-moment use
- Post-event assets reference the specific interaction (don't be generic)
- Hospitality content is personalized; never templated
- Live-fill templates include explicit placeholder markers and usage notes
- Sales-facing internal docs are operational, not editorial

---

## Edge Cases

- **Asset not in messaging house.** Flag during brief generation; suggest `/design asset [slug]` to define one, or map to the closest existing asset with adaptation notes.
- **Persona not in messaging house.** Flag during Round 2; offer `/design persona [slug]` or fall back to pillar-level context from `people.md` (noted in the brief).
- **No interaction data for post-event.** Generate templated assets per tier with placeholders; the team populates specifics (booth visitor list, meeting attendees, hospitality guests) after the session ends. Brief notes the placeholder state.
- **Hospitality content without per-attendee personalization input.** Refuse to generate generic hospitality copy — request the attendee context (name, role, account, prior interaction) and only then produce. Hospitality assets fail silently when templated.
- **Partner event with conflicting brand guardrails.** Defer to the partner's guidance for joint-facing assets; flag the divergence in `_meta/` so the team can confirm the call before deploying.
- **Context window pressure on multi-wave events.** Pass dependency content as summaries (key messages, positioning, CTAs) rather than full files; the brief's Extracted Context stays canonical on disk.
- **Partial production failure on one asset.** Mark the asset `needs-revision`, continue the wave. Downstream assets see a flagged dependency in the audit trail.
