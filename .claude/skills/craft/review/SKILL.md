---
name: review
description: Comprehensive messaging-alignment evaluation framework. Evaluates a content asset against voice, terminology, pitch, positioning, audience appropriateness, persona alignment, proof support, and format conformance. Used by the reader subagent during builder QA and by the user-invocable /review command for evaluating any draft (internal output, external content, partner deliverables, sales drafts).
argument-hint: "[file-path]"
user-invocable: true
---

# Review

This skill governs *whether the writing aligns with the messaging system* — is it grounded in the position, match the persona, cite real proof, follow the asset structure.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona"). If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

## Step 1: Resolve context

Identify what you have on hand. Some context is inlined in the dispatch payload (subagent path), some you read fresh.

| Context | Subagent path | User-invokes path |
|---|---|---|
| Asset to evaluate | `asset file path` in dispatch | First argument to `/review` |
| Target persona | `target persona` in dispatch | Infer from asset frontmatter or ask the user |
| Variant criteria | `variant` in dispatch | Infer from asset frontmatter (`variant:` field) |
| Glossary | Inlined glossary subset if present, else `MESSAGE.md` `## Glossary` | `MESSAGE.md` `## Glossary` |
| Asset envelope | `asset_inline` in dispatch | The asset envelope for the asset's slug |
| Pillars | Inlined `extracted_context` if present; else load the relevant pillars per the asset's domain | Load per the asset's domain |
| Voice gate | Inlined `voice_gate` if present, else load `craft/voice/SKILL.md` | Load `craft/voice/SKILL.md` |

If the asset's frontmatter is missing fields you need (no `persona`, no `variant`, no asset slug), surface the gap before proceeding. Don't score against guesses.

## Step 2: Score the eight dimensions

Score each dimension on a 0–100 band with a 2–3 sentence rationale. Bands:

- **90–100** — Strong; on target with no notable issues
- **70–89** — Acceptable; minor improvements would strengthen
- **50–69** — Mixed; specific revisions needed before publish
- **0–49** — Weak; substantial rework required

| Dimension | What you're assessing | Primary source |
|---|---|---|
| **Voice** | Compliance with the voice gate — banned phrases, structural anti-patterns, AI cadence. Authentic human prose. | The voice craft skill |
| **Terminology** | Glossary terms used as defined; no off-glossary substitutes for canonical terms; no invented company terminology. | `MESSAGE.md` `## Glossary` (or inlined subset) |
| **Pitch** | Claims trace to a UVP or key message; quantitative claims pull numbers from the pitch pillar's measures; narrative logic preserved (perspective shifts intact, no claim invention). | The pitch pillar |
| **Positioning** | Category framing matches the position pillar; competitive contrasts trace to positioning or a loaded competitor profile; differentiators backed by evidence. | The position pillar + competitor profiles |
| **Audience appropriateness** | Altitude matches the target persona's seniority and altitude; vocabulary matches the persona's altitude (executive vs. practitioner vs. developer); CTA matches expected next step. | The people pillar |
| **Persona alignment** | Persona-specific framing applied; pain points and language come from the persona profile; "Lead with" and "Avoid leading with" honored; no merging of multiple personas. | The target persona collection |
| **Proof support** | Every claim that should carry evidence has it; quotes are verbatim from approved sources; metrics carry attribution; thin claims flagged honestly. | The proof pillar + story / report collections |
| **Asset conformance** | Structure matches the variant's `## Structure` section; required `content-keys` present in frontmatter; conventions (length, headings, CTA placement) honored. | The asset envelope + variant |

Dimensions can be N/A. A press release with no persona target doesn't get a Persona alignment score — note "N/A — no persona-specific framing required" and skip.

## Step 3: Verdict

Aggregate the dimensions into one of three verdicts:

- **Ready to publish** — All dimensions ≥70; no critical messaging-house violations (false claim, missing attribution, off-glossary terms, voice gate fail).
- **Needs revision** — One or more dimensions in 50–69 OR any critical violation that can be fixed without restructuring. The directives below specify what changes.
- **Major rework** — Multiple dimensions <50 OR a structural mismatch (wrong persona, wrong format, fabricated positioning). Restart at the brief, don't patch.

## Step 4: Output format

Return a structured verdict. Be concrete — every score has a rationale, every directive points to a specific section.

```
Persona assumed: [persona slug, e.g., security-executives]
Asset applied: [asset slug + variant from asset frontmatter]
Asset path: [path]

## Scores

| Dimension | Score | Rationale |
|---|---|---|
| Voice | 88 | One structural pattern flag — em-dash overuse in §2. No banned phrases. |
| Terminology | 92 | All glossary terms used correctly. "Asset Cloud" capitalization consistent. |
| Pitch | 75 | UVP1 framing solid; UVP3 metric pulled from internal estimate not pitch.md — re-check. |
| Positioning | 90 | Category framing matches position.md. Competitive contrast honest. |
| Audience appropriateness | 70 | Altitude lands executive in §1–3 but drifts technical in §4. Sharpen §4. |
| Persona alignment | 85 | Lead-with frame correct (outcome). Avoids feature lists. |
| Proof support | 60 | Two claims unattributed: the "40% reduction" stat (no source) and the customer quote (not in stories/). |
| Asset conformance | 95 | All blog-post content-keys present. Within length band. |

## Top 3 recommendations

1. Attribute the "40% reduction" claim to a specific story or report — currently floating.
2. Revise §4 to executive altitude — pull capability detail to a supporting paragraph.
3. Reduce em-dashes in §2 to one per paragraph.

## Revision directives

- §2, second paragraph — Cut 3 of the 4 em-dashes; integrate the parenthetical asides into the sentence flow. (Voice gate structural pattern #8.)
- §3, "40% reduction" — Either pull from a specific story (cite by name and date) or replace with a directional claim ("customers typically see meaningful MTTR reduction"). (Proof support, citation discipline.)
- §4 — Compress capability detail (currently 2 paragraphs) into one sentence; restore executive altitude. (Audience appropriateness, altitude mismatch.)

## Verdict: Needs revision
```

## Revision budget

When the verdict is "Needs revision," the writer applies the directives and re-runs voice validation (one pass, no further review cycle). The reader is NOT re-dispatched after a "Needs revision" verdict. "Major rework" verdicts escalate to the user (standalone mode) or the orchestrator (campaign mode); they do not loop.

Hard budget: maximum 3 total drafts per asset (initial + voice revision + post-reader revision).
