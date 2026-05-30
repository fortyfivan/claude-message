---
name: voice
description: Writing rules for clean prose — eliminates AI patterns, enforces specificity and directness. Invoked by the writer subagent when content is being generated. 
---

# Voice Gate

Writing rules for all generated content. This is not a content generation skill — it defines writing mechanics that the writer agent applies during generation. The reader agent handles formal evaluation.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## Architecture

**Two layers.** Layer 1 (Brand voice) pulls dynamic content from the messaging system — Brand Guardrails, Glossary, voice attributes from the profile pillar — and applies it as the company-specific gate. Layer 2 (AI cliché patterns) is the static gate against AI-recognizable cadence: banned phrases, structural patterns, diagnostic checks. Both layers apply to every generation.

**Boundary:** The voice gate governs *how to write* — no throat-clearing, no binary contrasts, no AI cadence, no filler, plus the company's specific brand constraints. The messaging house governs *what to say* — positioning, claims, key messages, proof. The writer loads both. They don't overlap.

---

## Layer 1: Brand voice (dynamic)

Load at validation time from the messaging system:

- **Brand Guardrails** — 4-8 testable absolute rules. Any violation → FAIL.
- **Glossary** — cross-cutting term definitions, capitalization rules, prohibited terms with replacements. Mis-uses → record; FAIL when the term has a "prohibited; use X instead" rule.
- **Brand voice attributes** from the profile pillar — tone attribute pairs ("we are X but not Y"), default altitude, brand pillars. Scan for register/tone contradictions.

Layer 1 violations are higher-severity than Layer 2 — they're company-specific commitments.

---

## Layer 2: AI cliché patterns (static)

The rules below are constant across deployments. They catch AI-recognizable cadence regardless of which company is running the gate.

## Rules

Eight foundational rules for clean, human prose.

| # | Rule | What it means |
|---|------|---------------|
| 1 | Eliminate filler | No throat-clearing openers, no adverb crutches, no "it's worth noting." If a sentence works without a word, cut the word. |
| 2 | Break formulas | No binary contrasts ("it's not X, it's Y"), no false setups, no dramatic fragmentation. Predictable structures signal machine writing. |
| 3 | Activate voice | Human subjects performing actions. No passive constructions. No inanimate objects with agency ("the platform enables," "the data reveals"). Name who acts. |
| 4 | Demand specificity | Name things directly. Replace vague declarations ("the implications are significant") with concrete statements. Quantify when possible. |
| 5 | Ground the reader | Use "you" over abstractions. Create presence, not distance. Write to a person, not to the room. |
| 6 | Vary rhythm | Mix sentence lengths. No three-item lists as punchlines. No repetitive structures. Read it aloud — if it sounds like a cadence, break the cadence. |
| 7 | Respect intelligence | State facts plainly. No softening, no hedging, no justifying what doesn't need justification. Don't explain why something matters — show it. |
| 8 | Cut quotables | Rewrite anything that sounds like an AI pull-quote or inspirational poster. If it could go on a motivational mug, it doesn't belong in professional content. |

## Banned Phrases

Phrases that signal AI-generated writing. If you catch yourself reaching for one, stop and rewrite the sentence.

### Openers

- "Here's the thing"
- "The uncomfortable truth is"
- "Let me be clear"
- "I'll say it again"
- "Can we talk about"
- "Let's be honest"
- "Look,"
- "So,"
- "Here's what no one tells you"
- "I need to say this"

### Emphasis crutches

- "Full stop."
- "Let that sink in."
- "Make no mistake."
- "Here's why that matters."
- "Read that again."
- "This is the part that matters."
- "Pay attention to this."

### Jargon

- navigate
- unpack
- lean into
- game-changer
- double down
- deep dive
- circle back
- on the same page
- move the needle
- level up
- synergy
- holistic
- robust

### Filler

- "At its core,"
- "In today's [X],"
- "It's worth noting"
- "At the end of the day,"
- "When it comes to"
- "In a world where"
- "The reality is"
- "Here's the bottom line"
- "What this means is"
- "It goes without saying"
- "Needless to say"
- "To put it simply"

### Meta-commentary

- "Hint:"
- "Plot twist:"
- "Spoiler:"
- "But that's another post"
- "Let me walk you through"
- "Let me break this down"
- "I want to talk about"
- "Let's dive in"
- "Let's unpack this"
- "Let me explain"

### Performative emphasis

- "The result?"
- "The answer?"
- "The takeaway?"
- "This is what X actually looks like"
- "actually matters"
- "The question isn't X — it's Y"
- "And that's the point."
- "That's the real story."

### Vague declaratives

- "The implications are significant"
- "The stakes are high"
- "The consequences are real"
- "The reasons are structural"
- "The shift is happening"
- "The future is [adjective]"
- "This changes everything"
- "This is a big deal"
- "This matters more than you think"

## Structural Patterns

Eight patterns that produce recognizable AI cadence. Identify them, then rewrite.

### 1. Binary contrasts

**Pattern:** "It's not X. It's Y." / "This isn't about X. It's about Y."

**Fix:** Just state Y directly. The contrast format is a crutch — if Y is strong enough, it doesn't need X as a foil.

### 2. Negative listing

**Pattern:** Listing what something *isn't* before what it *is*. "It's not a dashboard. It's not a report. It's not a spreadsheet. It's a..."

**Fix:** State what it is. Readers don't need a process of elimination.

### 3. Dramatic fragmentation

**Pattern:** Single-word or short-fragment sentences for artificial emphasis. "Speed. Accuracy. Scale." / "And then it happened." / "One word: transformative."

**Fix:** Integrate the idea into a full sentence that earns its weight.

### 4. Rhetorical setups

**Pattern:** "What if I told you..." / "Think about it:" / "Imagine this:" / "Picture this:"

**Fix:** State the insight directly. If the insight is strong, it doesn't need a runway.

### 5. Formulaic constructions

**Pattern:** "By the time X, I was Y." / "The more I X, the more I Y." / "Not because X — but because Y."

**Fix:** Restructure. These templates are recognizable because AI defaults to them.

### 6. False agency

**Pattern:** "The platform enables..." / "The data reveals..." / "The solution delivers..." / "The technology empowers..."

**Fix:** Name the human actor. "Security teams detect threats 40% faster" instead of "The platform enables faster threat detection."

### 7. Passive voice

**Pattern:** "Threats are detected by..." / "Compliance is ensured through..." / "Value is delivered via..."

**Fix:** Flip to active. "[Product] detects threats." "Teams maintain compliance with..." Write who does what.

### 8. Weak rhythm

**Pattern:** Three-item lists as punchlines ("faster, smarter, better"), excessive em-dashes (3+ per section), hedging chains ("may potentially help to possibly reduce").

**Fix:** Vary sentence length and structure. Cut em-dashes to one per section maximum. Remove hedging — either state the claim or don't.

## Diagnostic Checklist

Twelve yes/no questions. Run as a quick sanity check before publishing. Any "yes" means revise that section.

1. Any adverbs that can be cut without changing meaning?
2. Any passive voice constructions?
3. Any inanimate objects performing human actions?
4. Any sentences starting with "So," "Look," or "Here's the thing"?
5. Any throat-clearing openers (first sentence doesn't contain the point)?
6. Any "it's not X, it's Y" binary contrasts?
7. Any monotonous rhythm (3+ consecutive sentences with same structure)?
8. Any excessive em-dashes (3+ in one section)?
9. Any vague claims without specific evidence?
10. Any meta-commentary about the writing itself?
11. Any sentence that sounds like an inspirational poster?
12. Any phrases from the banned list?

## Validation Protocol

Criteria for post-generation voice validation. The writer agent runs both layers after drafting content.

**Layer 1 (Brand voice):**
1. Load Brand Guardrails + Glossary from the messaging system (or use Extracted Context's inlined subset when present).
2. For each guardrail rule, run the test. Record violations with location.
3. For each glossary term in the draft, check capitalization + usage against the glossary rule. Record violations with location.
4. Load Brand Voice attributes from the profile pillar. Scan for register/tone contradictions against the declared attribute pairs.

**Layer 2 (AI cliché patterns):**
1. Scan the draft for every phrase in the Banned Phrases section. Record each match with its location.
2. Scan for each of the 8 Structural Patterns. Record each match with its location.
3. Run the 12-item Diagnostic Checklist. Record which items flag.

**Combined verdict:**

**PASS:** 0 Layer 1 violations AND 0 banned phrases AND 0 structural anti-pattern matches AND fewer than 3 diagnostic checklist flags.

**FAIL:** Any Layer 1 violation OR any banned phrase OR any structural anti-pattern OR 3+ diagnostic flags.

When the writer runs voice validation:
1. Run both layers per the steps above.
2. Apply the PASS/FAIL verdict.
3. If FAIL: revise the specific violations (prioritize Layer 1 — company commitments are stricter), then re-scan (max 2 total passes — 1 initial + 1 revision).
4. If still FAIL after pass 2: document remaining issues and proceed. The reader agent will catch them.
