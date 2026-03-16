# Bootstrap Skill

Build a complete messaging system through six sequential phases. Each phase produces a pillar document and its associated collection profiles. The result is a fully populated messaging house the team can use to generate on-brand content.

This is a collaborative session. At two points in every phase — after synthesis and after planning — you pause for user input before writing anything. You do not run phases autonomously from start to finish.

---

## Messaging System Architecture

The messaging system has two tiers.

**Pillars** are the six top-level documents that define the company's messaging foundation:

| Pillar | Purpose |
|--------|---------|
| Profile | Company identity, mission, voice, and strategic narrative |
| Space | Competitive landscape, category positioning, and differentiation |
| Audience | Buyers, users, and segments with distinct messaging needs |
| Portfolio | Products, services, and solutions mapped to customer needs |
| Proof | Customer stories, metrics, and third-party validation |
| Motion | GTM channels, plays, and how the company acquires customers |

**Profiles** are collection documents that live under their parent pillar and capture individual entities in detail:

| Profile | Parent Pillar |
|---------|--------------|
| Persona | Audience |
| Segment | Audience |
| Competitor | Space |
| Category | Space |
| Product | Portfolio |
| Solution | Portfolio |
| Story | Proof |
| Play | Motion |

Each pillar maintains a reference table linking to its collection profiles. When you write a pillar doc, every profile gets a row. When you write a profile, its `description` frontmatter field matches its row in the parent pillar's reference table.

Bootstrap builds both tiers in phase order. Each phase produces one pillar and its associated profiles.

---

## Step 1 — Workspace Setup

Always run the onboard script — it is idempotent and safe to run on existing workspaces.

Determine the plugin root using this resolution order:

1. **Fast path:** Read `.claude/.plugin-root` in the project root. If it exists, use its contents as the plugin root path.
2. **First-run path:** Read `~/.claude/plugins/installed_plugins.json`. Find the entry whose key starts with `claude-message@`. Use the `installPath` value.

Then run:

```bash
bash [plugin-root]/skills/messaging/bootstrap/scripts/onboard.sh [plugin-root] [project-root]
```

If any `WARNING:` lines appear, present them to the user and resolve before proceeding. If the workspace already exists and is clean, proceed.

**Opening message.** Once the workspace is confirmed, tell the user:
- Which phase you're starting (or resuming from, if a progress file exists)
- That you'll read their input materials, search the web, and synthesize findings before asking anything
- That you'll pause for their review before writing any files

---

## Step 2 — Gather Profile Context

Call AskUserQuestion with these four select menus in a single call:

| Question | Header | Options |
|----------|--------|---------|
| What is your role? | Role | Product Marketer, Founder, Marketing Leader, Growth / Demand Gen, Other (Input) |
| What stage is your company at? | Stage | Emerging, Growth, Established, Other (Input) |
| What type of business? | Type | B2B, B2C, B2B2C, Services |
| What market space? | Market | Security, Developer Tools & Infrastructure, Data & AI, Business Software, Other (Input) |

---

## Step 3 — Gather Company Basics

Call AskUserQuestion with a single text question:

> "Tell me about your company — name, what you do, your website URL, and anything else that helps me start researching."

Store all values from Steps 2 and 3. They are used throughout the session and written into `profile.md` frontmatter and the CLAUDE.md profile block at completion.

---

## Step 4 — Input Materials

The `input/` directory is now ready for any existing materials. Tell the user:

> The `input/` directory is ready for any existing materials you'd like me to work from — pitch decks, one-pagers, brand guides, competitive intel, customer stories. If you have materials to add, drop them in now and let me know when they're ready. Otherwise, we'll move straight into Phase 1.

If the user confirms they have materials, wait for them to indicate files are added, then read all files in `input/` and summarize what you found. If the user has no materials, proceed directly to Phase 1.

---

## How You Work

Every phase follows the same five-step cycle. Complete each step fully before moving to the next.

### Phase Step 1 — Discover

Gather information from three sources in this order:

**a. Input materials.** Read all files in `input/` and `research/`. These files won't follow messaging doc conventions — extract what you can (company facts, product descriptions, positioning language, competitive mentions, voice samples) and map each finding to the current phase. Read everything before searching the web.

**b. Web research.** Use WebSearch to find the company website, product pages, customer stories, community discussions, and practitioner reviews. Use analyst coverage as secondary context. Anchor every query to known context — company name, product names, competitor names. See Web Search Guidelines for limits and query patterns.

**c. Targeted questions.** If you reach a critical decision point where available evidence is insufficient to proceed, call AskUserQuestion. Use select menus for bounded choices. Use text questions for open-ended input. For non-critical gaps: make your best judgment, document your reasoning, and flag the decision as "provisional — review recommended."

**Narrate as you go.** Share what you're finding and what it means. When input materials surface useful signal, say so. When web research reveals something about positioning or differentiation, explain it. When you spot a gap or conflict, surface it immediately. The user should be able to follow your thinking in real time.

### Phase Step 2 — Synthesize + Challenge

Organize your findings, pressure test them, and present them to the user.

**Synthesize.** Structure your findings into the sections required by the phase template. For each section, note whether the content came from input materials, web research, or prior phases.

**Challenge.** Before presenting, actively identify and flag:
- **Generic positioning** — Claims any competitor could make. Prepare a sharper alternative.
- **Unsubstantiated claims** — Assertions without evidence. Note what proof would be needed.
- **Missing differentiation** — Value props that overlap with competitors.
- **Logical gaps** — Connections assumed but not articulated.
- **Assumed audience fit** — Personas or segments included by convention, not evidence.

**Present using this format:**

---
**Phase [N] Synthesis: [Pillar Name]**

[Structured findings organized by section]

**Challenges:**
- [Challenge] → Proposed alternative → **Recommended: [choice] — [reason]**

**Confidence:** [High / Mixed / Low] — [one sentence explaining why]

---

Explain why you structured the synthesis the way you did — what source drove each section, which claims are strong vs. thin, where you made a judgment call. The synthesis should read like a strategist walking through their analysis, not a document dump.

**Gate 1 — Hard stop.** After presenting the synthesis, call AskUserQuestion with a single text question:

> "Does this framing look right? Any corrections before I write the plan?"

Do not proceed to Phase Step 3 until the user responds.

### Phase Step 3 — Plan

After the user confirms the synthesis, present a phase plan using this format:

```
Phase [N]: [Pillar Name]

Key messages:
- [Strategic takeaway — one line, e.g. "Position as the only platform that unifies X and Y"]
- [Strategic takeaway]
- [Strategic takeaway]

Key decisions:
- [Decision — e.g., "Positioning as category creator, not incumbent challenger"]
- [Decision — e.g., "Three personas: CISO (buyer), Security Engineer (user), VP Eng (champion)"]

Collection profiles:
| Name | Type | Description |
|------|------|-------------|
| [name] | [type] | [one-line routing description] |

Open questions: [unresolved items, or "None"]
```

Key messages are strategic takeaways that will shape the pillar doc — one line each, not full copy. Collection profiles are shown as a table so the user can see the full scope before anything is written.

**Gate 2 — Hard stop.** After presenting the plan, call AskUserQuestion with a single text question:

> "Ready to write? Let me know if anything needs adjusting."

Do not proceed to Phase Step 4 until the user confirms. If the user requests changes, revise the plan and present it again before proceeding.

### Phase Step 4 — Write

Write all files listed in the plan. Write silently:
- Read the template from `templates/messaging/`
- Write the file to the correct messaging directory
- Confirm each file with a single line: `Created messaging/personas/ciso.md — Buyer persona, security leadership`

Do not show document previews, full file contents, or code blocks. The synthesis and plan already captured the strategic content — the user approved it. Write the files and move on.

### Phase Step 5 — Bridge

Before moving to the next phase, summarize how this phase's output connects to what comes next. This maintains narrative continuity across the messaging system. Incorporate any corrections or feedback the user has provided before proceeding.

---

**Multi-collection phases.** When a phase produces multiple collection types (e.g., Audience produces both personas and segments), run Discover → Synthesize + Challenge for each collection type to build the full picture, then present a single Plan covering the pillar doc and all collection profiles. One approval gate, then write everything. If the user confirms a collection type isn't needed, document that decision in the pillar doc rather than silently skipping it.

---

## Phase Order

The six phases build on each other. Complete them in sequence.

### Phase 1: Profile

Establish who the company is — its identity, mission, voice, and strategic narrative. Everything in later phases references this foundation.

**Template:** `templates/messaging/profile.md`
**Output:** `messaging/profile.md`
**Key questions:** What does the company do? What is its mission and vision? What tone and voice does the brand use? What does the company believe that others in the market don't? What is the strategic narrative — the arc from market conditions to unique insight to proof of value?
**Web research:** Homepage, about page, and product pages for positioning language and voice samples. Blog posts and social media for tone calibration. Do not search for corporate history, funding, investors, or founder bios — these don't inform messaging decisions.

Use the `role`, `stage`, `type`, `market`, and company basics collected in Steps 2–3 directly. Do not re-ask these questions.

### Phase 2: Space

Map the competitive landscape. Space depends on Profile to articulate where the company plays and how it's different.

**Templates:** `templates/messaging/space.md`, `templates/messaging/competitor.md`, `templates/messaging/category.md`
**Output:** `messaging/space.md`, `messaging/competitors/*.md`, `messaging/categories/*.md`
**Key questions:** What market category does the company compete in? Is it creating or redefining a category? Who are the primary and secondary competitors? What is the unique positioning? What are the key differentiators?
**Web research:** Competitors, analyst reports, category definitions, competitive landscape.

### Phase 3: Audience

Define who the company sells to. Audience depends on Profile and Space to identify buyers and users within competitive context.

**Templates:** `templates/messaging/audience.md`, `templates/messaging/persona.md`, `templates/messaging/segment.md`
**Output:** `messaging/audience.md`, `messaging/personas/*.md`, `messaging/segments/*.md`
**Key questions:** Who is the ideal customer? Who are the buyers vs. the users? What are their roles, goals, pain points, and decision criteria? What segments does the company target? What segments carry distinct messaging needs — industries, regions, company size tiers, or maturity levels that change how you talk about value?
**Web research:** Industry role descriptions, buying process insights, segment-specific trends.

### Phase 4: Portfolio

Define what the company sells. Portfolio comes after Space and Audience because market context and audience understanding shape how you describe the offering.

**Templates:** `templates/messaging/portfolio.md`, `templates/messaging/product.md`, `templates/messaging/solution.md`
**Output:** `messaging/portfolio.md`, `messaging/products/*.md`, `messaging/solutions/*.md`
**Key questions:** What are the products and services? How do they differ? What are the primary use cases? What capabilities are unique? How does the portfolio map to customer needs? What repeatable use cases warrant their own messaging — distinct audiences, distinct proof, or distinct value framing beyond what individual product profiles cover?

### Phase 5: Proof

Assemble evidence. Proof depends on everything before it — evidence must support claims about position, audience, and portfolio.

**Templates:** `templates/messaging/proof.md`, `templates/messaging/story.md`
**Output:** `messaging/proof.md`, `messaging/stories/*.md`
**Key questions:** What customer success stories exist? What metrics demonstrate value? What third-party validation exists? What quotes or testimonials are available?
**Web research:** Press coverage, case studies, analyst mentions, review site data.

**Customer story research.** During Discover for this phase:
1. Read `input/` and `research/` for customer references, case studies, or testimonials.
2. Search the web for "[company] case study", "[company] customer story", "[company] customer success". Limit to the last 12 months.
3. For each story with sufficient detail, create a profile in `messaging/stories/` using the story template.
4. Prioritize stories that reference portfolio products, match audience personas, and include specific metrics or quotes.
5. Cap at 10 story profiles per bootstrap run. The user can add more later with the compose command.

### Phase 6: Motion

Define how the company goes to market. Motion is the capstone phase — it orchestrates all prior components into actionable GTM approaches.

**Templates:** `templates/messaging/motion.md`, `templates/messaging/play.md`
**Output:** `messaging/motion.md`, `messaging/plays/*.md`
**Key questions:** What are the primary GTM channels? How does the company acquire customers today? What messaging motions map to which audiences and products? What's the sales-led vs. product-led balance? What are the key plays — specific buyer situations or initiatives that trigger a focused selling motion?

---

## Session Management

At the end of each phase, write a progress marker to `messaging/.bootstrap-progress.md` with completed phases, key decisions, and next steps. If you detect a progress file at the start of a session, offer to resume from the last completed phase. Read all previously written messaging docs to rebuild context before continuing.

---

## Completion

After all six phases are complete:

1. Read all written files and perform a consistency check. Flag contradictions or gaps and present a summary with recommended next steps.
2. Delete the progress file.
3. Invoke the health agent to generate the initial glossary from the populated messaging house. Present the proposed glossary to the user for approval before finalizing.

```
/agents health --fix glossary
```

### Write Profile Block

After the glossary is approved, write the user's writing profile into the project's CLAUDE.md:

1. Read the project's CLAUDE.md. Find the `<!-- claude-message:profile:start -->` and `<!-- claude-message:profile:end -->` markers.
2. Read `messaging/profile.md` frontmatter to get `{company}` from the `title` field.
3. Using `{role}`, `{stage}`, `{type}`, `{market}` from Step 2 and `{company}` from profile.md, compose:

```
{company} is a(n) {stage} {type} company in the {market} space. The primary user is a {role}. Calibrate all messaging to {company}'s market position, stage, and audience.
```

4. Replace everything between the markers (exclusive of the markers) with the composed block.
5. Confirm the update to the user.

### Write Initial Journal Entry

After writing the profile block, append the first journal entry to `messaging/journal.md`. Create the file from `templates/messaging/journal.md` if it doesn't exist.

Entry fields:
- **Source:** Bootstrap — initial build
- **Type:** process
- **Learning:** Key observations — assumptions made, conflicts surfaced, areas where information was thin, strategic choices that could go either way
- **Action:** Logged — initial messaging house populated.

Suggest running the tune command as the next step to calibrate content generation skills to the company's market, audience, voice, stage, and motions.

---

## Reference

### Handling Ambiguity

**User doesn't know.** Propose a working answer based on available evidence and flag it as provisional.

**Conflicting information.** Surface the conflict explicitly and ask the user to resolve it.

**Incomplete information.** Write what you have with bracketed placeholders for missing sections.

### Writing Conventions

- Write in the company's voice when you have enough signal. Default to clear, professional prose when you don't.
- After completing the Bridge for each phase, sync the parent pillar's reference table — every collection doc needs a corresponding row with a Description, and every row needs a corresponding doc.
- In pillar docs, populate the Description column for every collection profile. Descriptions are routing signals — one sentence (~15 words) capturing what the entity does, why it matters for messaging, and key themes. Each Description must differentiate from sibling entries in the same table.
- In collection profiles, populate the `description` frontmatter field with the same text used in the parent pillar's reference table.

### Web Search Guidelines

**Per-phase limits:**
- Maximum 10 searches per phase. If you haven't found what you need in 10 searches, synthesize what you have and ask the user.
- Each query must be specific and anchored to known context. No speculative or exploratory queries.
- Stop searching when you have sufficient signal to synthesize.

**Query construction:**
- Always include the company name or a known product name.
- Use specific patterns: "[company] [topic]", "[company] vs [competitor]", "[product] features", "[company] case study [customer]".
- Avoid generic industry queries not anchored to the company.

**Customer signal priority:**
- Prioritize practitioner sources (community forums, review sites, technical blogs) over analyst reports.
- Look for how customers describe the problem in their own words.
- Search for "[company] review", "[company] vs [alternative]", "[product] experience" alongside standard queries.

**When to stop:**
- You've found the company website, product pages, and relevant press or analyst coverage.
- Additional searches return diminishing results.
- You have enough to form a structured synthesis for the user to validate.