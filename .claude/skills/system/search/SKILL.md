---
name: search
description: Query the messaging house for content matching natural-language intent. Navigate intelligently through pillars, collections, and assets to return cited, structured results. Invoked via /search [query] or dispatched by other skills.
---

# search

Search the messaging house for content matching a user's intent. Returns synthesized, cited results — not a raw grep dump.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona"). If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## Inputs

- **query**: natural-language string describing what the user is looking for
- **scope** (optional): `pillars`, `collections`, `assets`, or `all`. Defaults to `all`.

## Outputs

Structured markdown:

- Synthesized answer when sources support one
- Per-source citations with file references and section anchors
- Confidence indication when results are partial or speculative
- Suggestions for related queries or content gaps

## How to navigate

The messaging house has a structured catalog. Use it to scope the search instead of scanning blindly.

1. **Read MESSAGE.md first** to understand what's available — the Pillars and Collections catalog tables declare what content exists.
2. **Identify likely sources** based on the query:
   - Voice / brand / glossary questions → the profile pillar, MESSAGE.md Glossary
   - Positioning / category questions → the position pillar, category collections
   - Audience / persona questions → the people pillar, persona collections
   - Product / capability questions → the portfolio pillar, product collections
   - Proof / customer / analyst questions → the proof pillar, story and report collections
   - Competitive questions → competitor collections
   - Use case / solution questions → solution collections
   - Asset format / variant questions → asset envelopes and variants
3. **Load only the relevant files** — don't pull the entire messaging house.
4. **Synthesize across sources** when multiple files contribute.
5. **Surface gaps** when relevant content doesn't exist.

## How to handle ambiguity

If the query is ambiguous, ask one clarifying question before searching:

- "I can interpret 'positioning on AI' as either competitive positioning (competitor collections) or category positioning (category collections). Which did you mean?"
- "Are you looking for proof points for sales (story collections) or analyst recognition (report collections)?"

One clarifying question only. If still ambiguous after the answer, return results from both interpretations with the ambiguity noted.

## How to handle no-result cases

When the query has no good matches:

1. Confirm the gap explicitly — "No content matches X."
2. Return the closest available content — "Closest matches are Y and Z."
3. Suggest action — "Consider running `/design competitor [slug]` to capture this content."

Don't fabricate content. Don't claim relevance that doesn't exist.

## Output format

```markdown
## Query: [restated query]

## Summary

[1–2 sentence synthesis of what was found.]

## Findings

### [Source category, e.g., "Positioning"]

- **[Claim]** ([source-reference]#[section])

### [Source category, e.g., "Proof"]

- **[Claim]** ([source-reference]#[section])

## Gaps

[Optional. List content that would be relevant but doesn't exist.]

## Related

[Optional. Suggest related queries or content to explore.]
```

Sources are always cited inline. Synthesis is welcome; fabrication is not.

## Execution pattern

1. **Parse the query.** Identify intent type (lookup, find-matching, synthesize-across), extract entities (named persons, products, competitors), determine scope.
2. **Read MESSAGE.md catalog.** Get the populated pillars and collections; understand what's available.
3. **Identify candidate sources** using the navigation guide above.
4. **Load candidates progressively.** Read selected files only.
5. **Score relevance** based on content matches and contextual fit. Reading does the work — no algorithm.
6. **Synthesize** into the output format. Preserve source attribution. Note conflicts if sources disagree.
7. **Surface gaps and suggestions** when appropriate.

## Tool scoping

- **Read** — full read access to the messaging house
- **Glob, Grep** — full access for content discovery
- **AskUserQuestion** — single clarifying question for ambiguous queries
- **Write, Edit** — none (read-only skill)
- **WebSearch, WebFetch** — none (search is internal to the messaging house; the researcher subagent handles external)

## What this skill does not do

- **Generate content.** Returns existing content; producing new content is the job of the builders.
- **Edit content.** Read-only. Updates happen through `/design`.
- **External research.** Internal to the messaging house. For external research, dispatch the researcher subagent.
- **Multi-step orchestration.** Single-query, single-response. Builders handle orchestration.

## Use cases

### Human invocation

```
/search "what's our position on AI in regulated industries?"
```

Returns a Summary + Findings broken out by source category, with citations.

### Skill invocation

The build-campaign builder during scenario inference can invoke search to find relevant proof:

```
search query="proof points for enterprise security buyers in regulated industries" scope=["collections"]
```

Results populate the brief's Extracted Context block.
