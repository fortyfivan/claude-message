# Bootstrap Skill

Build a complete messaging system through a guided, collaborative session. The result is a fully populated messaging house — six pillar documents and their associated collection profiles — that the team uses as the foundation for all product marketing.

You are not a scribe. Your job is to find the sharpest, most defensible position this company can own. Generic is failure. Borrowed language is failure. If a claim could appear on a competitor's website, it doesn't belong here. Every synthesis you produce should be identifiable as belonging to this company and no other.

---

## Architecture

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

**Profiles** are collection documents that live under their parent pillar:

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

Each pillar maintains a reference table linking to its collection profiles. When you write a pillar doc, every profile gets a row. When you write a profile, its `description` frontmatter matches its row in the parent pillar's reference table.

---

## Setup

### Step 1: Check for prior session

Check for `messaging/.bootstrap-progress.md`. If it exists, offer to resume:

> "A previous Bootstrap session exists. Resume from [last completed phase], or start fresh?"

Call AskUserQuestion to collect the response. If resuming, read all previously written messaging docs to rebuild context before continuing. If starting fresh, proceed.

### Step 2: Read input materials

Read every file in `input/`. Do not ask the user if they have materials — read what's there and report what you found.

**If files exist:** Produce a coverage map — which phases each file informs, what's well-covered, what's thin. Be specific. "Found a pitch deck covering company positioning and three competitor mentions. Thin on persona detail and GTM motion." Then proceed to Step 3.

**If `input/` is empty:** Tell the user what belongs there and give them a chance to add materials before continuing:

> "The `input/` directory is empty. The more existing material you bring, the less I need to ask and the sharper the output. Drop files directly and tag the filename so I know what it is:
> - `deck-` — Pitch decks or one-pagers
> - `brand-guide-` — Brand or messaging guides
> - `battlecard-` — Competitive intel or battlecards
> - `case-study-` — Customer stories or case studies
> - `prd-` or `release-notes-` — Product docs or release notes
> - `research-` — Market or audience research
>
> Copy anything relevant into `input/` now, or let me know if you'd like to proceed without materials."

Call AskUserQuestion with two options: "I've added materials — read them now" or "Proceed without materials." If the user adds materials, read them and produce the coverage map. If they proceed without, note it and move on.

### Step 3: Collect session context

From the input materials coverage map, extract what you already know: company name, website URL, what they do, company stage, and market space. Only ask for what's missing or ambiguous.

**If input materials are empty or didn't surface these details**, call AskUserQuestion with two select menus and a text question in sequence:

| Question | Options |
|----------|---------|
| What stage is your company at? | Emerging, Growth, Established, Other |
| What market space? | Security, Developer Tools & Infrastructure, Data & AI, Business Software, Other |

> "Tell me about your company — name, what you do, your website URL, and anything else that helps me start."

**If input materials partially answered these**, pre-fill what you know and ask only for what's missing. For example, if the company name and URL are clear but stage is ambiguous, ask only the stage question.

**If input materials fully answered these**, confirm with the user in a single message rather than asking questions:

> "Based on your materials, here's what I'm working with: [company name], [what they do], [URL], [stage], [market]. Anything to correct before I start?"

Store everything as your **session context** — it applies to every phase. You do not ask these questions again.

### Step 4: Extract brand tokens

Fetch the company homepage using the URL from session context. Extract:
- Primary, secondary, and accent colors (from CSS or meta tags)
- Heading and body fonts
- Logo URL

Present what you found via AskUserQuestion for confirmation:

> "Here's what I found from your website. Please confirm or correct:"
> - Primary color: [value or "not found"]
> - Secondary color: [value or "not found"]
> - Accent color: [value or "not found"]
> - Heading font: [value or "not found"]
> - Body font: [value or "not found"]
> - Logo URL: [value or "not found"]

Write confirmed values to `messaging/brand.yml`. Create `messaging/brand/` and download any discovered logo files.

---

## Phase Cycle

Every phase follows the same three-step cycle.

### 1. Discover

Draw from sources in strict priority order:

**First: session context and input materials.** You already have these. Use them. For many phases, this alone is sufficient.

**Second: previously written messaging docs.** Later phases build on earlier ones. Read what's been written before forming your synthesis.

**Third: web research — only for genuine gaps.** If input materials and prior docs don't give you enough to synthesize the phase, search. Be specific about what you're missing before searching. Do not search to confirm what you already know.

**Web search discipline:**
- Maximum 5 searches per phase. If you need more, the gap is real — surface it to the user instead.
- Every query must be anchored to the company name or a known product name.
- Stop as soon as you have enough to synthesize.

Narrate as you discover. What you're finding, what it means, where you see gaps or contradictions. The user should follow your thinking in real time.

### 2. Synthesize

Organize your findings and make them sharp. The synthesis is the strategic argument the document will make — not the document itself.

**Before presenting, pressure-test every claim:**
- Could a competitor say this? If yes, cut it or sharpen it.
- Is there evidence for this? If no, flag it as provisional.
- Is this differentiated from what's in earlier phases? If the same claims keep appearing, you haven't found the differentiation yet.
- What is the single most important thing this phase needs to establish? Lead with it.

**Present challenges as choices, not flags.** For each weak or generic claim, don't just surface the problem — present it as a decision via AskUserQuestion:

- **Option A:** Current framing — "[original]"
- **Option B:** Sharper alternative — "[proposed]" *(Recommended — [reason])*
- **Option C:** Custom input

Present all challenges in a single AskUserQuestion call. Include a final text question: "Any other corrections before I write?"

Incorporate the user's choices before proceeding. **Do not write until challenges are resolved.**

**Synthesis format:**

---
**Phase [N]: [Pillar Name]**

[Structured findings, organized by what matters most — not by template section order]

**Confidence:** [High / Mixed / Low] — [one sentence on why]

**Proposed collection profiles:**
| Name | Type | One-line description |
|------|------|----------------------|

---

### 3. Write

After the user confirms the synthesis, write all files for the phase silently:
- Read the template from `templates/messaging/`
- Write the file to the correct messaging directory
- Confirm each file with one line: `Created messaging/personas/ciso.md — Buyer persona, security leadership`

No previews. No code blocks. The synthesis captured the strategy — the user approved it. Write and move on.

After writing, bridge to the next phase in two or three sentences: what this phase established and how the next phase builds on it.

---

**Multi-collection phases.** When a phase produces multiple collection types, run Discover → Synthesize for each collection type to build the full picture, then present challenges and confirm once before writing everything. If the user confirms a collection type isn't needed, document that decision in the pillar doc rather than silently skipping it.

**Progress.** At the end of each phase, write a progress marker to `messaging/.bootstrap-progress.md` with completed phases, key decisions, and next phase.

---

## Phases

Complete in sequence. Each phase builds on the last.

### Phase 1: Profile

Establish who the company is. Every later phase references this foundation — voice, narrative, mission, belief.

**Output:** `messaging/profile.md`
**Key questions:** What does the company believe that others in the market don't? What is the narrative arc — from market conditions to unique insight to proof of value? What does the voice sound like?
**Web research triggers:** Homepage and product pages if input materials don't contain positioning language. Blog and social if voice is unclear.

Use stage, market, and company basics from session context directly. Do not re-ask.

When naming conventions emerge during research — product names, preferred terms, rejected terms — record them in the progress file for glossary generation at completion.

### Phase 2: Space

Map the competitive landscape. Who the company competes with, where it plays, and what makes it different.

**Output:** `messaging/space.md`, `messaging/competitors/*.md`, `messaging/categories/*.md`
**Key questions:** What category does the company compete in — or create? What are the primary competitors and how does the company beat each one? What positioning can no competitor claim?
**Web research triggers:** Competitor websites and positioning if not covered in input materials. Analyst coverage for category framing.

### Phase 3: Audience

Define who the company sells to and why they buy.

**Output:** `messaging/audience.md`, `messaging/personas/*.md`, `messaging/segments/*.md`
**Key questions:** Who is the economic buyer vs. the end user? What does each persona care about that the others don't? Which segments carry genuinely distinct messaging needs — not just different sizes or industries, but different problems, language, or buying motion?
**Web research triggers:** Role and buying process research only if personas aren't grounded in input materials or prior discovery.

### Phase 4: Portfolio

Define what the company sells and how it maps to audience needs.

**Output:** `messaging/portfolio.md`, `messaging/products/*.md`, `messaging/solutions/*.md`
**Key questions:** What capabilities are genuinely unique? How does the portfolio address the pain points established in Audience? What use cases warrant their own solution messaging?
**Web research triggers:** Product feature comparisons only if competitive differentiation is unclear from input materials.

### Phase 5: Proof

Assemble the evidence that makes claims credible.

**Output:** `messaging/proof.md`, `messaging/stories/*.md`
**Key questions:** What customer stories demonstrate real outcomes? What metrics exist? What third-party validation is available?
**Web research triggers:** "[company] case study", "[company] customer story", "[company] review" — limit to the last 12 months. Cap at 10 story profiles.

Prioritize stories that name a product, match a persona, and include a specific metric or quote. A story without evidence is not a proof point.

### Phase 6: Motion

Define how the company goes to market. Motion orchestrates all prior components into actionable GTM approaches.

**Output:** `messaging/motion.md`, `messaging/plays/*.md`
**Key questions:** What are the primary acquisition channels? What triggers a specific play — what situation, what buyer, what moment? How does messaging shift by channel and motion?
**Web research triggers:** Rarely needed. Motion is synthesized from prior phases, not researched independently.

---

## Completion

After all six phases:

1. **Consistency check.** Read every file written during the session using the Read tool. Do not use shell commands (grep, awk, etc.) for this step — analyze the content in context.

   Check for:
   - **Reference table sync** — Every collection profile has a row in its parent pillar's reference table, and every row has a matching profile file. Descriptions match between frontmatter and table.
   - **Cross-references** — Products, personas, and segments named in one doc exist as profiles. Stories reference real products and personas.
   - **Contradictions** — Claims in one doc that conflict with another (e.g., a competitor listed as "no direct threat" in space.md but treated as primary in a battlecard).
   - **Gaps** — Pillars or profiles that are thin, rely heavily on placeholders, or lack key sections.

   Present a single summary:

   ```
   Consistency Check:
     ✓ [N] docs written, [N] profiles across [N] pillars
     ✓ Reference tables synced
     ⚠ [specific issue — e.g., "story 'acme-corp' references persona 'DevOps Lead' but no persona profile exists"]
     ⚠ [specific issue]

   Recommended next steps:
     - [action]
     - [action]
   ```
2. Delete the progress file.
3. Invoke `/insights fix glossary` to generate the initial glossary from the populated messaging house. Present the proposed glossary for user approval before finalizing.

### Write Profile Block

After glossary approval, write the user's profile into CLAUDE.md:

1. Find `<!-- claude-message:profile:start -->` and `<!-- claude-message:profile:end -->` markers.
2. Read `messaging/profile.md` frontmatter for `{company}`.
3. Using session context values and `{company}`, compose:

```
{company} is a(n) {stage} company in the {market} space. Calibrate all messaging to {company}'s market position, stage, and audience.
```

4. Replace everything between the markers with the composed block.

### Write Initial Journal Entry

Append the first entry to `messaging/journal.md` (create from template if needed):

- **Source:** Bootstrap — initial build
- **Type:** process
- **Learning:** Assumptions made, conflicts surfaced, areas where information was thin, strategic choices that could go either way
- **Action:** Logged — initial messaging house populated.

Suggest running the tune command as the next step.

---

## Reference

### Handling Ambiguity

**User doesn't know.** Propose a working answer based on available evidence. Flag it as provisional. Move on.

**Conflicting information.** Surface the conflict and ask the user to resolve it before writing.

**Incomplete information.** Write what you have. Use bracketed placeholders for missing sections.

### Writing Conventions

- Write in the company's voice when you have enough signal. Default to clear, direct prose when you don't. Never default to marketing filler.
- Sync the parent pillar's reference table after every phase — every collection doc gets a row, every row gets a doc.
- Descriptions in reference tables are routing signals, not summaries. One sentence, ~15 words. Each must differentiate from sibling entries in the same table.
- Collection profiles: `description` frontmatter matches its row in the parent pillar's reference table exactly.