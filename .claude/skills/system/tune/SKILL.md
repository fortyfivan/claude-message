# Tune Skill

Calibrate content generation skills to the company's messaging house by enriching them in place with company-specific guidance.

Invoked via `/tune` or `/tune --check`.

A base skill says "lead with the prospect's pain point." A tuned skill says "frame pain in terms of risk exposure and compliance gaps — this market responds to quantified business impact, not feature comparisons. CISOs in regulated industries expect specific claims backed by third-party validation. Avoid aspirational language; lead with evidence."

Skills live in `.claude/skills/` and are tuned in place. The `## Company Calibration` section is always replaced wholesale on re-tune. Inline enrichments are re-derived from the current messaging house on each run. Git preserves the original untuned versions — use `git checkout .claude/skills/` for a full reset if needed.

## How You Work

Skills in `.claude/skills/` work without tuning. The tune skill personalizes them with company-specific guidance derived from the messaging house.

On every run: read current skills from `.claude/skills/`, read the messaging house, produce tuned skill files written back in place. Re-tuning strips the existing `## Company Calibration` section and inline enrichments, re-derives them from the current messaging house, and writes the result back.

## Step 1: Analyze

Read the messaging house and current skills in one pass. Build a company profile and assess tuning state.

**Read the messaging house.** Load all six pillars, glossary.md, and relevant collection docs. Include `messaging/journal.md` (if it exists) for voice and content learnings that should inform skill calibration. Use pillar reference tables to enumerate collection profiles. Load full collection docs for deeper analysis:

- Persona docs in `messaging/personas/` — frontmatter for type, seniority, pain points, goals
- Category docs in `messaging/categories/` — market dynamics
- Competitor docs in `messaging/competitors/` — frontmatter for tier, threat level, differentiators

**Build a company profile** — a compact internal summary across the five tuning dimensions:

```
Market: [primary category], [industry characteristics], [buyer type]
Audience: [N] personas ([roles]), [evaluation cycle length]
Voice: [tone attributes], [dos/don'ts summary], [N calibration patterns]
Stage: [funding stage], [proof depth assessment]
Motion: [primary motion], [secondary motion if any]
```

**Read current skills.** Glob `.claude/skills/tasks/` and `.claude/skills/craft/` to build a path inventory — this is the write target list. For each skill file, assess tuning state:

- **Untuned** — No `tuned: true` in frontmatter. Has not been personalized by a previous tuner run.
- **Previously tuned** — Contains `tuned: true` in frontmatter from an earlier run.

**Assess drift.** For each previously tuned skill file, read its `tuned_sources` list from frontmatter. Check each source's `updated` timestamp against `tuned_date`:

1. **Source drift** — If any source's `updated` > `tuned_date`, that skill has drifted. Note which sources changed and which tuning dimensions are affected.
2. **Coverage drift** — Check for new collection profiles added since the last tune that aren't in any skill's `tuned_sources`. New profiles = new context the skills don't know about.

Additionally, check for calibration patterns in `profile.md` Brand Voice with status "confirmed" that are not yet reflected in skill guidelines. These represent voice preferences that should be baked into tuned skills.

**Note gap observations.** While reading the messaging house and skills, note mismatches:

- Missing skills for declared motions, active personas, competitive plays, or proof leverage
- Excess skills without messaging support

Keep these as brief observations — they'll be surfaced in Step 2.

## Step 2: Present

Present the company profile, scope, and gap observations for user approval.

```
Tune Analysis: [Company Name]

Company Profile:
  Market: [summary]
  Audience: [summary]
  Voice: [summary]
  Stage: [summary]
  Motion: [summary]

Scope: [N] skills to tune (across [N] categories)
  Skills unchanged: [N]
  Drift detected: [N] skills ([list sources that changed])
  Manual edits detected: [N] files (will be overwritten)

Gaps:
  - [1-2 bullet observations, e.g. "No battlecard skill but 3 competitors profiled"]

Approve all, approve selectively, or reject?
```

Show file paths explicitly. Include manual edit warnings with the specific files affected.

The user can:

- **Approve all** — Write all tuned skills.
- **Approve selectively** — "Tune the blog and email skills but skip social for now."
- **Reject** — No changes made.

## Step 3: Tune

After approval, for each skill being tuned:

1. Read the current skill file from `.claude/skills/`. Strip the existing `## Company Calibration` section if present.
2. Apply inline enrichments to existing sections throughout the file.
3. Append the new `## Company Calibration` section as the last H2.
4. Write the tuned skill to `.claude/skills/` at the same path, preserving the hierarchy exactly.
5. Verify the target path exists (via Glob) before writing. Missing path = error, not a new file.
6. Update frontmatter:

```yaml
---
tuned: true
tuned_date: "2026-03-10"
tuned_sources: [profile.md, space.md, glossary.md, motion.md, proof.md]
---
```

Frontmatter fields:
- `tuned: true` — Indicates this file has been calibrated by the tune skill.
- `tuned_date` — ISO date of the tune run. Used by `--check` mode for drift detection.
- `tuned_sources` — List of messaging doc filenames that informed this file's calibration. Gives `--check` mode an auditable trail of which sources to check for drift. SKILL.md files list pillar-level sources; type files list the specific collection profiles used for audience, proof, and competitive calibration.

Never create new directories during tuning. The write target list from Step 1 defines the valid paths.

After writing, confirm with a summary:

```
Tuned [N] skills:
  [file path] — [tuned | re-tuned]
  ...
```

## Step 4: Recommend (Optional)

If the user asks about gap observations from Step 2, expand them into specific recommendations:

- **Missing skills for declared motions.** If `motion.md` describes a motion but no matching skills exist, flag it.
- **Missing skills for active personas.** If personas exist but skills lack persona-specific guidance for some of them, flag the gap.
- **Missing skills for competitive plays.** If competitors are profiled but no battlecard or competitive content skill exists, flag it.
- **Missing skills for proof leverage.** If `proof.md` has strong evidence but no skill formats it for distribution, flag it.
- **Excess skills without messaging support.** If a skill references content types the messaging house can't support, flag it as low priority.

For recommendations the user approves:

- **Base skill exists in `.claude/skills/`** — Read, tune, and write back in place.
- **No base skill** — Generate a new skill from scratch following the standard skill structure (output format, guidelines, quality signals, context pointers). Write to `.claude/skills/` with tuning applied.

New skills must follow the hierarchy: new types go in the existing type subdirectory; new categories require directory + SKILL.md + type subdirectory. Present each recommendation individually for per-skill approval.

## Tuning Dimensions

Each dimension maps to specific source docs, target files, and tuning methods:

| Dimension | Sources | Target File | Tuning Method |
|---|---|---|---|
| Voice Alignment | `profile.md`, `glossary.md`, `journal.md` | SKILL.md | Inline: enrich Guidelines. Calibration: `### Voice & Terminology` |
| Market Dynamics | `space.md`, `categories/` | SKILL.md | Inline: enrich Messaging House Context, Guidelines. Calibration: `### Market Context` |
| Company Stage | `profile.md`, `proof.md` | SKILL.md | Inline: enrich Quality Signals. Calibration: `### Stage Calibration` |
| Motion Alignment | `motion.md`, `plays/` | SKILL.md | Inline: enrich Output Format (if needed). Calibration: `### Motion Alignment` |
| Audience Calibration | `audience.md`, `personas/`, `segments/` | Type file | Inline: enrich Tone & Style, Quality Signals. Calibration: `### Audience Calibration`, `### Proof Mapping`, `### Competitive Framing`, `### Evaluation Addenda` |

Category-level tuning (Voice, Market, Stage, Motion) lands in SKILL.md and applies universally across all types in that category. Type-specific tuning (Audience) lands in the type file and adds per-persona, per-proof, and per-competitor specifics for that content type. No duplication between levels.

### What Gets Modified Where

#### SKILL.md Enrichments

| Section | What Tuning Does |
|---|---|
| **Instructions** | Preserved as-is. Generic workflow doesn't change. |
| **Type Guides** | Preserved. Routing links stay the same. |
| **Messaging House Context** | Enriched: add specifics about which pillar sections matter most for this company. |
| **Guidelines** | Enriched: add company-specific dos/don'ts derived from `profile.md` Brand Voice, `glossary.md` terminology, and `journal.md` voice learnings. |
| **Quality Signals** | Enriched: add company-specific check items. |
| **Output Format** | Preserved as-is unless the company's motion or market requires structural additions. |

#### SKILL.md Company Calibration Section

| Subsection | Source Docs | What It Contains |
|---|---|---|
| `### Voice & Terminology` | `profile.md`, `glossary.md`, `journal.md` | Dos/don'ts rendered as concrete instructions. Self-reference conventions. Product naming rules. Confirmed calibration patterns from Brand Voice. Phrasing anti-patterns. |
| `### Market Context` | `space.md`, `categories/` | Market-specific content norms. Evidence standards. How buyers consume this content type. |
| `### Stage Calibration` | `profile.md`, `proof.md` | Proof depth rating with specifics. Positioning boldness. CTA confidence level. |
| `### Motion Alignment` | `motion.md`, `plays/` | CTA architecture per motion. Content depth by motion. Multi-persona handling. |

#### Type File Enrichments

| Section | What Tuning Does |
|---|---|
| **Structure** | Preserved unless the company's content strategy requires section additions or reordering. |
| **Tone & Style** | Enriched: layer in voice attributes from `profile.md`, phrasing patterns, altitude adjustments for the company's primary personas. |
| **Content-Specific Guidelines** | Enriched: add company-relevant patterns, adjust word count if company strategy demands it, add market-specific guidance. |
| **Examples** | Can be supplemented with company-relevant example framing (not fabricated content — framing that reflects the company's positioning style). |
| **Quality Signals** | Enriched: add company-specific quality targets. |

#### Type File Company Calibration Section

| Subsection | Source Docs | What It Contains |
|---|---|---|
| `### Audience Calibration` | `audience.md`, `personas/`, `segments/` | Per-persona blocks: altitude, vocabulary from pain points/goals, proof type preferences, objections to preempt. Segment-specific adjustments. |
| `### Proof Mapping` | `proof.md`, `stories/` | Specific stories, quotes, metrics matched to this type. What's available, what's missing. Which proof is strongest for which persona. |
| `### Competitive Framing` | `competitors/` | How to position against specific competitors for this type. Language to use, traps to avoid. Only present when relevant to the type. |
| `### Evaluation Addenda` | All loaded sources | Company-specific additions to the type's base quality signals that don't fit into inline enrichment of the existing table. |

## Re-Tuning and Drift Detection

### --check Mode

When invoked with `--check`, compare the messaging house state against tuning metadata in each skill's frontmatter. Report what has drifted and which skills would be re-tuned on a full run. Do not modify any files.

Two checks:

1. **Source drift** — For each tuned skill, iterate its `tuned_sources` list. If any source's `updated` > `tuned_date`, that skill has drifted. Report which sources changed and which dimensions are affected.
2. **Coverage drift** — Check for new collection profiles added since the last tune that aren't in any skill's `tuned_sources`. New profiles = new context the skills don't know about.

### Manual Edit Detection

Manual edits are detected by checking if the file has been modified since `tuned_date` (via `git log` or file metadata). If changes exist outside tuning metadata and the Company Calibration section, warn the user that re-tuning will overwrite them. The approval gate is the safety net — the user reviews the scope (including what manual edits will be lost) before approving.

## Tool Scoping

- **Read** — `messaging/`, `.claude/skills/`. Full access to the messaging house and skills.
- **Write** — `.claude/skills/` (with user approval).
- **Glob, Grep** — Full access. Used to inventory skills, scan persona docs, assess proof depth, detect manual edits.
- **WebSearch, WebFetch** — Not used. The tune skill works entirely from local context.
