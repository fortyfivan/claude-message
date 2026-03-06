# PRD: Tune Agent

## Overview

The tune agent calibrates the content generation system to a specific company. It reads the messaging house, reads the base skill templates, and writes tuned skills that encode the company's market dynamics, audience expectations, voice, stage, and selling motions directly into the skill instructions. It also identifies gaps — skills the company needs but doesn't have.

The writer agent generates content by resolving messaging context and applying a skill. The quality of that output depends on two things: the richness of the messaging context and the specificity of the skill instructions. The messaging house handles context. The tune agent handles skill specificity.

A base skill says "lead with the prospect's pain point." A tuned skill says "frame pain in terms of risk exposure and compliance gaps — this market responds to quantified business impact, not feature comparisons. CISOs in regulated industries expect specific claims backed by third-party validation. Avoid aspirational language; lead with evidence."

The tune agent runs on demand. It reads everything, proposes changes, and waits for approval before modifying any skill.

## Architecture

### Templates as Base Layer

The repo ships with two template directories:

```
_templates/
  messaging/             → Canonical schemas for messaging docs (already exists)
    profile.md
    space.md
    ...
  skills/                → Base generic skills (new)
    blog-copywriting/
      SKILL.md
      blog_types/
        thought-leadership.md
        data-study.md
        product-update.md
    email-copywriting/
      SKILL.md
      email_types/
        cold-outreach.md
        nurture-sequence.md
        customer-announcement.md
    social-copywriting/
      SKILL.md
      social_types/
        linkedin-post.md
        linkedin-series.md
    sales-copywriting/
      SKILL.md
      sales_types/
        battlecard.md
        talking-points.md
        one-pager.md
    brief-copywriting/
      SKILL.md
      brief_types/
        creative-brief.md
        campaign-brief.md
    ...
```

Base skill templates are generic. They contain the universal structure of a content type — output format, standard guidelines, basic evaluation criteria — without market-specific, audience-specific, or company-specific calibration. They work out of the box for any company but produce generic output.

Base templates are never modified by agents. They ship with the repo and update with new releases.

### Active Skills as Tuned Layer

Messaging skills live under a `messaging/` namespace within `.claude/skills/`. This scopes the tune agent to its own skills and avoids collisions with other plugins that may install skills at the same level.

```
.claude/skills/
  messaging/                       ← tune agent's scope
    blog-copywriting/
      SKILL.md
      blog_types/
        thought-leadership.md      → Tuned: market-aware, audience-calibrated, voice-aligned
        data-study.md
        product-update.md
    email-copywriting/
      SKILL.md
      email_types/
        cold-outreach.md           → Tuned: motion-aligned CTAs, persona-specific hooks
        ...
    ...
  frontend-design/                 ← other plugin, untouched
  code-review/                     ← other plugin, untouched
```

The writer agent reads from `.claude/skills/messaging/`. The tune agent reads and writes within this namespace only. Skills from other plugins are invisible to both agents.

This namespace boundary is the scoping mechanism. The tune agent operates on a skill if and only if it lives under `.claude/skills/messaging/` and has a corresponding base template in `_templates/skills/`. No base template match, no tuning — even within the namespace.

### The Tune Agent's Job

```
Read _templates/skills/ (base)           ──┐
Read messaging/ (company context)        ──┤──→ Write .claude/skills/messaging/ (tuned)
Read .claude/skills/messaging/ (current) ──┘
```

On first run: the tune agent copies base templates to `.claude/skills/messaging/` and enriches them with company-specific calibration.

On subsequent runs: the tune agent reads the current tuned skills, compares them against the messaging house (which may have changed), and proposes updates. This handles messaging drift — when the company repositions, adds personas, or shifts motions, the skills need to reflect those changes.

---

## What Ships

```
_templates/
  skills/                        → Base generic skill templates (read-only)
    [category]/
      SKILL.md
      [type]/
        [type].md

.claude/
  agents/
    tune.md                      → Tune agent definition
  commands/
    tune.md                      → /project:tune slash command
```

---

## Tuning Dimensions

The tune agent reads the messaging house and derives calibration across five dimensions. Each dimension maps to specific sections within skill files.

### 1. Market Dynamics

**Source:** `space.md`, `categories/`

The market the company operates in shapes what buyers expect from content. Regulated industries (healthcare, finance, government) demand conservative claims, compliance context, and third-party validation. Security markets expect threat-informed language and technical credibility. Developer markets expect code-level depth and anti-marketing directness. Horizontal SaaS markets expect ROI framing and cross-functional appeal.

**What gets tuned:**

- **Guidelines** — Market-specific content norms. "This market penalizes vague claims. Every capability assertion must cite a specific product feature or customer metric." Or: "Developer audiences distrust marketing language. Use precise technical vocabulary. Avoid superlatives."
- **Evaluation criteria** — "Are claims grounded in evidence appropriate for a regulated market?" replaces "Are claims clear?"
- **Output format** — Structural additions where the market demands them. A "Compliance Implications" section in blog templates for healthcare markets. A "Technical Architecture" section in product content for developer markets. A "Risk Context" framing section for security markets.

**Derivation logic:**

Read `space.md` for `primary_category` and `adjacent_categories`. Read matching docs in `categories/` for category-specific dynamics. Cross-reference with `proof.md` to understand what kinds of evidence the company has (quantitative metrics, analyst validation, customer quotes) and calibrate proof expectations accordingly — don't demand analyst citations if the company doesn't have them.

### 2. Audience Calibration

**Source:** `audience.md`, `personas/`

Different personas consume content differently. The tune agent writes persona-specific guidance into each skill so the writer knows how to adapt altitude, vocabulary, proof emphasis, and structure for each audience.

**What gets tuned:**

- **Audience-specific instruction blocks** — New sections within each skill type mapping persona archetypes to content adaptations. Not "adjust for the reader" but "when targeting a CISO: lead with business risk, quantify exposure, use compliance and governance vocabulary, keep technical detail in a separate section they can forward to their team."
- **Altitude guidance** — Maps persona seniority to content depth. Executive personas get strategic framing, outcome language, and concise proof. Practitioner personas get implementation detail, integration specifics, and technical proof. Champion personas get internal-selling ammunition — ROI summaries, competitive comparisons, and executive one-pagers they can forward.
- **Vocabulary calibration** — Specific words and phrases to use or avoid for each audience. Derived from the persona's `pain_points`, `goals`, and `decision_criteria` fields. If the CISO persona lists "consolidate tooling" as a pain point, the tuned skill says "frame product value in terms of platform consolidation — this resonates more than feature comparison."

**Derivation logic:**

Read `audience.md` for ICP-level signals (`icp_industries`, `icp_company_size`). Read all persona docs. For each persona, extract `type` (buyer/user/champion/blocker), `seniority`, `pain_points`, `goals`, `decision_criteria`, and `objections`. Group personas by the type of content adaptation they require and write consolidated guidance blocks.

### 3. Voice Alignment

**Source:** `profile.md`

The skill should encode the company's actual voice, not "professional tone." Voice alignment means translating the brand's tone attributes into concrete writing instructions with dos and don'ts.

**What gets tuned:**

- **Voice guidelines** — Specific dos and don'ts derived from `voice_tone` and `brand_values` in profile.md. If the voice is "technically authoritative but approachable," the tuned skill says: "Use precise technical language but explain implications in plain terms. Avoid jargon without context. Don't hedge with 'may' or 'might' — state capabilities directly. Don't use exclamation marks or marketing superlatives."
- **Phrasing patterns** — How the company refers to itself, its products, and its market. First person plural ("we") vs. company name. Product names with or without "the." Category language the company uses vs. avoids.
- **Differentiation language** — How the company talks about competitors (directly by name, indirectly by approach, or not at all). Derived from `profile.md` brand values and `space.md` competitive positioning.

**Derivation logic:**

Read `profile.md` for `voice_tone[]`, `brand_values[]`, and the Brand Voice section. If the profile includes specific voice examples or a "we say / we don't say" list, encode those directly. Cross-reference with `space.md` positioning statement for the language patterns the company uses to describe its market position.

### 4. Company Stage

**Source:** `profile.md` (`funding_stage`, `company_size`), `proof.md`

Company stage determines the proof burden, the positioning boldness, and the narrative arc. This is the most structural dimension — it affects not just language but what a skill can reasonably ask a writer to produce.

**What gets tuned:**

| Stage | Proof posture | Positioning posture | Narrative arc |
|---|---|---|---|
| **Emerging** (seed, series A) | Thin — rely on vision, early adopter stories, founder credibility. Skills should not demand extensive proof sections. | Bold — category creation language is appropriate. "We believe" framing. | Aspirational. The company is defining a new way. Skills should encourage forward-looking claims grounded in first principles. |
| **Growth** (series B-D) | Building — customer metrics exist but may be limited. Skills should demand proof but accept smaller sample sizes. | Competitive — direct differentiation language is appropriate. "Unlike X, we Y" framing. | Momentum. The company is winning in the market. Skills should emphasize traction, growth metrics, and competitive wins. |
| **Established** (late-stage, public) | Deep — extensive case studies, analyst validation, industry benchmarks. Skills should demand robust proof sections. | Authoritative — market leadership language. "The leading X" framing. | Trust. The company is the safe choice. Skills should emphasize ecosystem, stability, and breadth. |

- **Proof requirements per skill** — Adjust how much evidence each content type demands. An emerging company's blog post skill might say "include one customer reference or data point if available; if not, ground claims in product capability." An established company's skill says "include at least two proof points per major claim — case study metrics, analyst quotes, or customer testimonials."
- **Positioning boldness** — Calibrate claim strength. Emerging companies can make visionary claims ("we're building the future of X"). Established companies should make evidence-backed claims ("trusted by 500+ enterprises").
- **CTA calibration** — Stage affects what CTAs are credible. Emerging companies push for conversations ("talk to us," "join the beta"). Growth companies push for evaluation ("see a demo," "start a trial"). Established companies push for adoption ("get started," "contact sales").

**Derivation logic:**

Read `profile.md` for `funding_stage` and `company_size`. Read `proof.md` to assess proof depth — count case studies, check for analyst mentions, evaluate metric specificity. The proof inventory determines what skills can realistically demand. A company that says it's "growth stage" but has one case study should be tuned closer to emerging proof posture.

### 5. Motion Alignment

**Source:** `motions.md`

The company's selling motion determines how content converts. PLG companies need self-serve activation framing. Sales-led companies need multi-stakeholder content and demo CTAs. Event-led companies need pre/post event sequences. Partner-led companies need co-marketing frameworks.

**What gets tuned:**

- **CTA architecture** — The default CTA for each content type, aligned to the primary motion. A PLG company's blog post ends with "Try it free" or "See it in your environment." A sales-led company's blog ends with "Schedule a demo" or "Talk to an expert." Skill templates encode the CTA pattern rather than leaving it to the writer's judgment.
- **Content depth expectations** — PLG content tends shorter and more action-oriented (get to the "try it" moment fast). Sales-led content tends longer and more comprehensive (the reader is evaluating, not activating). Skills calibrate expected length and depth per format.
- **Conversion context** — Skills include awareness of where content sits in the funnel. "This email type is mid-funnel: the reader has engaged with top-of-funnel content but hasn't committed to evaluation. Frame the CTA as a next step, not a commitment."
- **Multi-persona handling** — Sales-led motions often require content that addresses multiple stakeholders. Skills for these motions include guidance on "forwarding sections" — content the primary reader can send to their CFO, CISO, or VP Engineering. PLG motions rarely need this.

**Derivation logic:**

Read `motions.md` for primary and secondary motions, channels, and conversion patterns. Map each motion to CTA defaults and depth expectations. Cross-reference with `audience.md` to understand buying process complexity — long evaluation cycles with multiple stakeholders need different content architecture than self-serve activation.

---

## Agent Process

### Step 1: Read the Messaging House

Load and analyze:

- `profile.md` — voice, stage, identity
- `space.md` — market, positioning, differentiation
- `audience.md` — ICP, buying process
- `portfolio.md` — product ecosystem
- `motions.md` — GTM motions, channels, conversion patterns
- `proof.md` — evidence inventory (depth assessment, not full content)
- All persona docs in `personas/` — frontmatter for type, seniority, pain points, goals
- All category docs in `categories/` — market dynamics
- All competitor docs in `competitors/` — frontmatter for tier, threat level, differentiators

Build a **company profile** — an internal summary of the five tuning dimensions:

```
Market: Enterprise cybersecurity, regulated industries, technical buyers
Audience: 3 personas (CISO/buyer, VP Eng/champion, DevOps Lead/user), long evaluation cycle
Voice: Technically authoritative, direct, evidence-first, no marketing superlatives
Stage: Growth (Series C), moderate proof depth (4 case studies, 1 analyst mention)
Motion: Sales-led primary, PLG secondary for developer adoption
```

### Step 2: Read Current Skills

Load all skills from `.claude/skills/messaging/`. For each skill category and type, assess current tuning state:

- **Untuned** — Matches the base template exactly (or `.claude/skills/messaging/` is empty / newly copied from templates).
- **Previously tuned** — Contains company-specific calibration from an earlier tune run.
- **Manually modified** — Contains changes the user made directly. The agent should preserve these and tune around them.

Compare each skill against the company profile to identify what needs tuning.

### Step 3: Read Base Templates

Load matching base templates from `_templates/skills/`. These are the generic starting point. For skills that are untuned, the base template is the input. For previously tuned skills, the agent compares the current tuned version against both the base template and the current messaging house to identify what's drifted.

### Step 4: Generate Tuning Plan

For each skill, produce a tuning specification:

```markdown
## blog-copywriting / thought-leadership

**Current state:** Untuned (matches base template)

**Proposed changes:**

### Market Dynamics
- Add: "Enterprise cybersecurity audiences expect threat-informed framing.
  Ground thought leadership in specific threat vectors or attack patterns,
  not abstract trends."
- Add: "Regulated industry readers expect compliance context. Include a
  section on regulatory implications when the topic intersects compliance."

### Audience Calibration
- Add persona block for CISO: "When targeting CISOs: lead with business
  risk quantification. Frame technical capabilities in terms of risk
  reduction. Use governance vocabulary (posture, exposure, remediation SLA).
  Keep implementation detail in a forwardable section."
- Add persona block for DevOps Lead: "When targeting DevOps: lead with
  workflow integration. Frame capabilities in terms of CI/CD pipeline
  impact. Use infrastructure vocabulary (agents, scanners, APIs, webhooks).
  Include code-level examples where possible."

### Voice Alignment
- Replace: Generic "professional tone" → "Technically authoritative, direct.
  State capabilities without hedging. Avoid superlatives and marketing
  language. Explain implications in plain terms after using technical
  vocabulary."
- Add: "Use first-person plural ('we') for company references. Refer to
  products by name without 'the'. Never reference competitors by name in
  thought leadership — differentiate by approach."

### Company Stage
- Modify proof requirements: "Include at least one quantitative proof
  point per major claim. Acceptable evidence: customer deployment metrics,
  time-to-value data, analyst findings. If only one case study is relevant,
  supplement with product capability evidence."
- Modify positioning posture: "Competitive differentiation is appropriate
  but should be framed as approach difference, not feature comparison.
  'Unlike legacy approaches that rely on...' not 'Unlike [Competitor]...'"

### Motion Alignment
- Modify CTA: Default CTA for thought leadership → "Request a technical
  briefing" or "See how [Company] approaches [topic]" (sales-led motion).
  Secondary CTA for developer readers → "Try it in your environment"
  (PLG secondary motion).
- Add: "Thought leadership should establish expertise that feeds the
  sales-led pipeline. Include a 'What this means for your security program'
  section that transitions from insight to product relevance."

### Evaluation Criteria (additions)
- "Does the post demonstrate genuine technical depth appropriate for
  enterprise security practitioners?"
- "Are proof points sourced from the company's actual evidence base?"
- "Does the CTA align to the primary selling motion?"
```

### Step 5: Gap Analysis

While reading the messaging house and the current skill set, identify mismatches:

**Missing skills for declared motions.** If `motions.md` describes an event-led motion but no event-specific skills exist, flag it. If outbound is a primary motion but there's no cold email skill, flag it.

**Missing skills for active personas.** If there are 4 personas but skills lack persona-specific guidance for some of them, flag the gap. If a persona type (champion) is defined but no content type exists for internal-selling materials (executive summary, ROI calculator), flag it.

**Missing skills for competitive plays.** If `competitors/` has 3 primary competitors but there's no battlecard skill, flag it.

**Missing skills for proof leverage.** If `proof.md` has strong case study content but there's no case study skill to format and distribute it, flag it.

**Excess skills without messaging support.** If a skill references content types the messaging house can't support (e.g., a webinar script skill but no event motion, no event-focused personas), flag it as low priority.

Produce a gap report:

```markdown
## Skill Gap Analysis

### Recommended New Skills (high priority)
- **event-copywriting / session-abstract** — motions.md lists event-led as
  secondary motion. No event skills exist. Base template available: No.
  Recommendation: Create from scratch with event + CISO audience calibration.
- **sales-copywriting / battlecard** — 3 primary competitors defined.
  No battlecard skill exists. Base template available: Yes.
  Recommendation: Tune from base template.

### Recommended New Skills (medium priority)
- **sales-copywriting / executive-summary** — champion persona
  (VP Engineering) defined. No internal-selling content skill.
  Base template available: No.

### Skills with Low Messaging Support
- **social-copywriting / twitter-thread** — No social-specific motion
  or distribution channel defined in motions.md. Consider removing or
  deferring tuning.
```

### Step 6: Present Tuning Plan for Approval

Present the complete tuning plan to the user:

```
Tune Analysis: [Company Name]

Company Profile:
  Market: Enterprise cybersecurity, regulated industries
  Audience: 3 personas (CISO, VP Eng, DevOps Lead)
  Voice: Technically authoritative, direct, evidence-first
  Stage: Growth (Series C), moderate proof depth
  Motion: Sales-led primary, PLG secondary

Skills to tune: 12 (across 5 categories)
Skills unchanged: 0
New skills recommended: 3 (2 high priority, 1 medium)

Tuning preview written to output/tune-plan.md.
Review the proposed changes and approve, edit, or reject.
```

The full tuning plan (every proposed change per skill, plus gap analysis) is written to `output/tune-plan.md` for review. The user can:

- **Approve all** — Agent writes all tuned skills to `.claude/skills/messaging/`.
- **Approve selectively** — "Tune the blog and email skills but skip social for now."
- **Edit** — Modify the plan, then approve.
- **Reject** — No changes made.

### Step 7: Write Tuned Skills

After approval, for each skill being tuned:

1. Start from the base template (if untuned) or the current skill (if re-tuning).
2. Apply the approved tuning changes.
3. Preserve any manual modifications the user made outside of tune runs.
4. Write the tuned skill to `.claude/skills/messaging/[category]/[type]/[type].md`.
5. Add tuning metadata to the skill's frontmatter:

```yaml
---
tuned: true
tuned_date: "2026-03-03"
tuned_from: "_templates/skills/blog-copywriting/blog_types/thought-leadership.md"
company_profile_hash: "abc123"
tuning_dimensions:
  market: "enterprise-cybersecurity"
  stage: "growth"
  motion: "sales-led"
  personas_calibrated:
    - enterprise-ciso
    - devops-lead
---
```

The `company_profile_hash` is a fingerprint of the messaging house state at tune time. On subsequent runs, the agent compares the current messaging house hash against the stored hash to identify what's drifted and which skills need re-tuning.

### Step 8: Create Recommended Skills (Optional)

For gap analysis recommendations the user approves:

- **Base template exists** — Copy from `_templates/skills/`, tune immediately.
- **No base template** — Generate a new skill from scratch, following the standard skill structure (output format, guidelines, evaluation criteria, context pointers). Write to `.claude/skills/messaging/` with tuning applied. Also write a base version to `_templates/skills/` so future installs have it available.

Creating new skills is optional and requires per-skill approval. The agent presents each recommendation individually: "I recommend creating a battlecard skill. Here's the proposed structure. Want me to create it?"

---

## Re-Tuning

The tune agent is designed to run repeatedly as the messaging house evolves.

### Drift Detection

On subsequent runs, the agent compares:

1. **Messaging house vs. last tune** — Has `profile.md` changed voice? Has `audience.md` added a persona? Has `motions.md` shifted the primary motion? Has `space.md` repositioned?
2. **Proof inventory vs. last tune** — Has the company accumulated more case studies? Gained analyst validation? The proof posture may have graduated from "emerging" to "growth."
3. **Skills vs. messaging house** — Are persona-specific blocks still aligned with current persona docs? Do CTA patterns still match the declared motion?

The agent reports what's drifted and proposes targeted re-tuning — only the skills affected by the change, only the sections that need updating.

### Preserving Manual Edits

Users may modify skills directly between tune runs. The agent detects manual changes by comparing the skill against the last tune output (stored via the tuning metadata). Manual changes are preserved during re-tuning unless they conflict with a messaging house change. Conflicts are flagged for user resolution.

---

## Tool Scoping

- **Read** — `messaging/`, `_templates/skills/`, `.claude/skills/messaging/`, `output/tune-plan.md`. Full access to the messaging house and both skill layers.
- **Write** — `.claude/skills/messaging/` (with user approval), `_templates/skills/` (only when creating new base templates for gap-fill skills), `output/tune-plan.md` (autonomous — the plan is a preview artifact).
- **Glob, Grep** — Full access. Used to inventory skills, scan persona docs, assess proof depth.
- **WebSearch, WebFetch** — Not used. The tune agent works entirely from local context. Market dynamics, audience expectations, and voice are derived from the messaging house, not external research.

---

## Command

### /project:tune

```markdown
Tune the content generation skills to the company's messaging house.

Step 1: Read the full messaging house (all pillars, all collection frontmatter,
proof inventory). Build a company profile across five dimensions: market dynamics,
audience calibration, voice alignment, company stage, motion alignment.

Step 2: Read current skills from .claude/skills/messaging/ and base templates from
_templates/skills/. Assess tuning state of each skill.

Step 3: Generate a tuning plan — proposed changes per skill across all five
dimensions, plus gap analysis of missing skills.

Step 4: Write the tuning plan to output/tune-plan.md. Present a summary and
ask for user approval before modifying any skill files.

Step 5: After approval, write tuned skills to .claude/skills/messaging/ with tuning
metadata. Optionally create new skills from gap analysis recommendations.

/agents tune $ARGUMENTS
```

### /project:tune --check

```markdown
Check for tuning drift without making changes.

Read the messaging house and current skills. Compare against tuning metadata
in each skill's frontmatter. Report what has drifted and which skills would
be re-tuned on a full run. Do not modify any files.

/agents tune --check $ARGUMENTS
```

---

## Integration Changes

This PRD introduces two structural changes that ripple across the existing system: the `messaging/` skills namespace and the consolidated `_templates/` directory. Every affected file is listed below.

### 1. Templates Directory Restructure

**Current:** Messaging doc templates live at `messaging/_templates/`.

**New:** All templates consolidate under a root-level `_templates/` directory with two subdirectories:

```
_templates/
  messaging/          → Was messaging/_templates/ (pillar and collection schemas)
  skills/             → New (base generic skill templates)
```

**What changes:**

| File | Change |
|---|---|
| `.claude/agents/bootstrap.md` | All template path references change from `messaging/_templates/[type].md` to `_templates/messaging/[type].md`. Every phase's "Template:" line and the "Read the template from messaging/_templates/" instruction in the system prompt. |
| `.claude/commands/competitor.md` | Template reference `messaging/_templates/competitor.md` → `_templates/messaging/competitor.md` |
| `.claude/commands/persona.md` | Template reference `messaging/_templates/persona.md` → `_templates/messaging/persona.md` |
| `CLAUDE.md` | Directory structure listing, file conventions section ("Follow the schema in `_templates/messaging/`"), permissions table (add `_templates/` row, read-only) |
| `prd-plugin.md` | Target state directory tree, templates section description, bootstrap agent system prompt |

### 2. Skills Namespace

**Current:** Skills live at `.claude/skills/[category]/`.

**New:** Messaging skills live at `.claude/skills/messaging/[category]/`. Other plugins' skills remain at `.claude/skills/[other-plugin]/`.

**What changes:**

| File | Change |
|---|---|
| `.claude/agents/writer.md` | System prompt Step 3 ("Load the Skill"): path changes from `.claude/skills/[category]/SKILL.md` to `.claude/skills/messaging/[category]/SKILL.md`. All skill references in context resolution examples (battlecard, nurture sequence, thought leadership examples). |
| `.claude/agents/campaign.md` | System prompt: skill paths in campaign type defaults, asset manifest examples, and skill-not-found edge case handling all update to `.claude/skills/messaging/`. |
| `.claude/commands/generate.md` | "Load the skill from .claude/skills/" → "Load the skill from .claude/skills/messaging/" |
| `.claude/commands/brief.md` | Same path update if it references skills directly |
| `.claude/commands/audit.md` | If the audit checks for skill coverage, update the scan path |
| `CLAUDE.md` | Skills section directory listing, directory permissions table (`.claude/skills/messaging/` replaces `.claude/skills/`), content generation rules |
| `prd-plugin.md` | Target state directory tree, skills structure section, writer agent system prompt, campaign agent system prompt |
| `prd-campaign.md` | Skill references in asset manifest examples, skill-not-found edge case, tool scoping |

### 3. Bootstrap Agent Completion

**Current:** Bootstrap finishes with a consistency check and recommended next steps.

**New:** The completion message should suggest running `/project:tune` as the natural next step after populating the messaging house:

```
Add to .claude/agents/bootstrap.md completion section:

"Your messaging house is populated. The next step is tuning the content
generation skills to your company's market, audience, voice, and motions.
Run /project:tune to calibrate skills based on what we just built."
```

### 4. Research Agent Scan Context

**Current:** The scan agent reads `.claude/skills/` to understand available content types.

**New:** If the scan agent references skill availability (e.g., in coverage gap analysis), update the path to `.claude/skills/messaging/`. The scan agent doesn't modify skills, so this is read-path only.

### 5. CLAUDE.md Updates

The following sections of CLAUDE.md need updating:

**Repository Structure** — Add `_templates/` as a root-level directory. Update `messaging/_templates/` reference. Update `.claude/skills/` to show the `messaging/` namespace:

```
_templates/
  messaging/           → Canonical schemas for messaging docs
  skills/              → Base generic skill templates (read-only)

.claude/
  agents/              → bootstrap, researcher, writer, campaign, tune
  commands/            → Slash commands for messaging workflows
  skills/
    messaging/         → Tuned content generation skills (messaging namespace)
```

**File Conventions** — "Follow the schema in `_templates/messaging/`" (was `messaging/_templates/`).

**Content Generation Rules** — "Load the relevant skill from `.claude/skills/messaging/`" (was `.claude/skills/`).

**Directory Permissions** — Update table:

| Directory | Read | Write | Notes |
|---|---|---|---|
| `_templates/` | Yes | No | Base schemas and skills. Never modify. |
| `.claude/skills/messaging/` | Yes | Tune agent with approval | Tuned skills. Writer reads, tune agent writes. |

**Agents** — Add tune agent. Update writer description to reference `.claude/skills/messaging/`.

**Commands** — Add `/project:tune` and `/project:tune --check`.

**Skills** — Update directory listing to show namespace:

```
.claude/skills/
  messaging/
    blog-copywriting/
      SKILL.md              → Routes to the right blog type
      blog_types/
        thought-leadership.md
        data-study.md
    email-copywriting/
      SKILL.md
      email_types/
        cold-outreach.md
```

### Summary of Path Changes

| Old Path | New Path | Reason |
|---|---|---|
| `messaging/_templates/` | `_templates/messaging/` | Consolidated templates directory |
| (new) | `_templates/skills/` | Base generic skill templates |
| `.claude/skills/[category]/` | `.claude/skills/messaging/[category]/` | Namespace scoping |

---

## Interaction with Other Agents

**Writer agent** — The writer reads from `.claude/skills/messaging/` and follows whatever instructions it finds. It doesn't know whether a skill is tuned. Tuned skills make the writer's output better by providing company-specific guidance that the writer would otherwise have to infer from raw messaging docs on every invocation.

**Campaign agent** — The campaign agent maps assets to skills during brief generation. Tuned skills mean the campaign's per-asset specs don't need to repeat company-specific guidance — it's already baked into the skill. The campaign agent can focus on per-asset context resolution and narrative coordination.

**Bootstrap agent** — After bootstrap completes and the messaging house is populated, the natural next step is running `/project:tune` to calibrate skills. The bootstrap agent's completion message should suggest this.

**Research agent** — When a scan surfaces a critical insight (e.g., "competitor launched a free tier, your PLG differentiator is weakened"), the resolution may involve re-tuning skills that reference that differentiator. The research agent doesn't trigger re-tuning directly, but the insight tracker creates the signal that a tune run would pick up via drift detection.

---

## Deliverables

### New Files
- Agent definition: `.claude/agents/tune.md`
- Command templates: `.claude/commands/tune.md`
- Base skill templates in `_templates/skills/` for all shipped skill categories
- Tuning plan output convention: `output/tune-plan.md`

### Structural Changes
- Move `messaging/_templates/` → `_templates/messaging/`
- Create `_templates/skills/` with base generic skill templates
- Move `.claude/skills/[category]/` → `.claude/skills/messaging/[category]/`

### Modified Files
- `.claude/agents/bootstrap.md` — Template paths, completion message
- `.claude/agents/writer.md` — Skill loading paths
- `.claude/agents/campaign.md` — Skill reference paths
- `.claude/commands/generate.md` — Skill path
- `.claude/commands/competitor.md` — Template path
- `.claude/commands/persona.md` — Template path
- `CLAUDE.md` — Directory structure, permissions, skills section, agents, commands