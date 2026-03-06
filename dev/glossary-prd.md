# PRD: Glossary Agent

## Overview

The glossary agent maintains `messaging/glossary.md` — a curated list of terms with company-specific definitions extracted from the messaging house. It runs on demand, scanning all messaging documents to identify terms that are used meaningfully and repeatedly, then adds, updates, or removes entries to keep the glossary current.

The glossary is a derived artifact, not an authored document. Every definition traces back to how the term is actually used in the messaging house. It's not a dictionary — it's a messaging consistency tool. When the company says "exposure management," the glossary defines what that means in the company's context, grounded in the positioning, product capabilities, and audience language documented across the pillars.

The glossary is distinct from Naming and Terminology in profile.md. Naming and Terminology is prescriptive — it governs word choice ("always say X, never say Y"). The glossary is definitional — it captures meaning ("here's what we mean when we say X"). A term can appear in both: Naming says "always say 'exposure management' not 'vulnerability scanning'" and the glossary defines what exposure management means in your context.

## What Ships

```
.claude/
  agents/
    glossary.md            → Glossary agent definition
  commands/
    glossary.md            → /project:glossary slash command

messaging/
  glossary.md              → Curated term definitions (generated and maintained by agent)
```

## Glossary File Format

`messaging/glossary.md` is a flat, scannable reference file. No frontmatter. No collection of profiles. One file, one purpose.

```markdown
# Glossary

Terms and definitions as used in this company's messaging. Definitions reflect how terms are used across the messaging house — they are company-specific, not industry-generic. When generating content, use these definitions as the baseline for term consistency.

## Terms

### [Term]

[1-3 sentence definition grounded in how the company uses this term.]

**Context:** [which pillar or collection doc this term is most associated with]
**See also:** [related terms in the glossary, if any]

---

### [Term]

...
```

Each entry is brief — a definition, not an explanation. The definition should be specific enough that a writer encountering the term knows exactly how to use it, and an editor reviewing content can check consistency. The Context field traces the term back to its source in the messaging house. See Also connects related terms for navigation.

### What Gets Included

Not every term in the messaging house warrants a glossary entry. The agent applies a selection filter:

**Include:**
- Terms with company-specific meaning that differs from or sharpens the generic industry definition
- Terms that appear across multiple pillars or collections (signals cross-cutting importance)
- Category and product names that carry positioning weight
- Technical terms that the audience uses and the company has a specific take on
- Terms from the Naming and Terminology section of profile.md that benefit from a definition alongside the usage rule

**Exclude:**
- Common industry terms used with their standard meaning
- Terms that appear in only one document and are self-explanatory in context
- Internal jargon that doesn't appear in external-facing content
- Acronyms that are universally understood by the target audience

### What Gets Updated

On each run, the agent compares the current glossary against the current messaging house:

**Add** — Terms that meet the inclusion criteria but aren't in the glossary yet. This happens when new messaging docs are created (new products, new competitors, new categories) or when existing docs are revised to introduce new terminology.

**Edit** — Terms whose definition has drifted from how they're currently used. If space.md repositions the company from "vulnerability management" to "exposure management" and the product docs follow, the glossary definition should reflect the new framing.

**Remove** — Terms that no longer appear meaningfully in the messaging house. A deprecated product name, a retired category term, or a competitor that's been removed from the landscape.

**Flag** — Terms where usage is inconsistent across the messaging house. If profile.md uses "platform" but product docs use "product suite," the glossary agent surfaces the conflict rather than silently picking one.

---

## Agent Process

### Step 1: Read the Messaging House

Read all pillar docs, all collection profiles, and the current glossary (if it exists). Build a term frequency map — which terms appear where, how often, and in what context.

### Step 2: Apply Selection Criteria

For each candidate term, evaluate against the inclusion/exclusion criteria. Terms that appear across multiple documents or carry company-specific meaning are strong candidates. Terms that are standard usage with no company-specific nuance are excluded.

### Step 3: Generate Definitions

For each included term, write a 1-3 sentence definition grounded in how the term is used in the messaging house. Do not write generic definitions — the definition should reflect the company's specific usage, positioning, and context.

For terms already in the glossary, compare the current definition against current messaging house usage. If usage has shifted, draft an updated definition.

### Step 4: Detect Conflicts

Scan for terms used inconsistently across the messaging house. If the same concept is referred to by different terms in different documents, or if a term is used with different meanings in different contexts, flag it.

### Step 5: Present Changes

Present the proposed changes to the user as a structured diff:

```
Glossary Update

Added (4):
  + exposure management — [definition]
  + runtime context — [definition]
  + attack surface — [definition]
  + continuous validation — [definition]

Updated (1):
  ~ platform — definition updated to reflect portfolio restructuring

Removed (1):
  - vulnerability scanning — term deprecated in favor of "exposure management"

Conflicts (1):
  ⚠ "agent" — used to mean "software agent" in product docs but "sales agent" in
    motions.md. Recommend clarifying in both documents.

Total: 23 terms (was 20)
```

The user can approve all, approve selectively, or edit before the agent writes.

### Step 6: Write

After approval, write the updated `messaging/glossary.md`. Entries are sorted alphabetically. Each entry follows the standard format (definition, context, see also).

---

## System Prompt

```markdown
You are a glossary agent that maintains a curated list of terms and company-specific definitions extracted from the messaging house. You scan all messaging documents, identify terms that are used meaningfully and repeatedly, write definitions grounded in actual usage, and present changes for approval.

## How You Work

1. Read all files in messaging/ — pillars, collections, and the current glossary.md if it exists.
2. Build a term frequency map. Identify terms that appear across multiple documents, terms with company-specific meaning, category and product names, and technical terms the audience cares about.
3. For each candidate term, evaluate against selection criteria:
   - Include: company-specific meaning, cross-pillar usage, positioning weight, technical terms with a company-specific take
   - Exclude: standard industry terms with no company nuance, single-document terms that are self-explanatory, internal jargon, universally understood acronyms
4. For included terms, write a 1-3 sentence definition reflecting how the company uses the term. Trace each definition to the messaging doc(s) where the term is most prominent.
5. Compare against the existing glossary:
   - New terms → add
   - Changed usage → update definition
   - Removed from messaging house → remove
   - Inconsistent usage across docs → flag as conflict
6. Present the full change set (adds, updates, removes, conflicts) to the user. Wait for approval before writing.
7. After approval, write messaging/glossary.md with entries sorted alphabetically.

## Selection Principles

- The glossary is a messaging consistency tool, not a dictionary. Include terms that affect how content is written.
- Definitions are company-specific. "Exposure management" in the glossary doesn't mean what Wikipedia says — it means what this company's messaging house says.
- Fewer, higher-quality entries beat comprehensive coverage. 15-40 well-defined terms is the target range for most companies. If you're including more than 50, you're probably including standard terms that don't need company-specific definitions.
- Every definition must trace to at least one messaging doc. If you can't point to where a term is used, it doesn't belong in the glossary.

## Conflict Resolution

When you detect inconsistent usage:
- Do not silently resolve the conflict by picking one usage
- Present both usages with their source documents
- Recommend which usage should be canonical, with reasoning
- The user decides — then updates the source documents to match

## Writing Conventions

- Definitions are 1-3 sentences. If a definition needs more than 3 sentences, the term might need its own messaging section rather than a glossary entry.
- Write in present tense, declarative voice. "[Term] is..." not "[Term] refers to..." or "[Term] can be defined as..."
- Ground in the company's context. "Exposure management is [Company]'s approach to..." not "Exposure management is an industry practice that..."
- Do not duplicate Naming and Terminology guidance. If profile.md says "never say vulnerability scanning," the glossary entry for exposure management doesn't need to repeat that rule. It just defines the term.
```

---

## Tool Scoping

- **Read** — `messaging/` (all pillars and collections). Full access to scan for terms and usage.
- **Write** — `messaging/glossary.md` only (with user approval).
- **Glob, Grep** — Full access. Used for term frequency analysis across the messaging house.
- **WebSearch, WebFetch** — Not used. The glossary is derived from local messaging context, not external definitions.

---

## Command

### /project:glossary

```markdown
Scan the messaging house and update the glossary.

Read all files in messaging/. Identify terms that are used meaningfully and
repeatedly with company-specific definitions. Compare against the current
glossary.md. Present proposed additions, updates, removals, and conflicts.
Write after user approval.

/agents glossary $ARGUMENTS
```

### /project:glossary --check

```markdown
Check glossary health without making changes.

Read all files in messaging/ and the current glossary.md. Report terms that
are missing, outdated, or inconsistently used. Do not modify any files.

/agents glossary --check $ARGUMENTS
```

---

## Integration Changes

### Bootstrap Agent

Add glossary invocation at the end of the bootstrap completion flow. After all six phases are complete and the consistency check has run:

```
Add to .claude/agents/bootstrap.md completion section:

After the consistency check, invoke the glossary agent to generate the initial
glossary from the freshly populated messaging house:

/agents glossary

Present the proposed glossary to the user for approval before finalizing
the bootstrap process.
```

The glossary is the final step of bootstrap because it's derived from everything else.

### Writer Agent

Add glossary.md to the writer's always-load list. Currently the writer always loads `profile.md` (voice) and `space.md` (positioning). Add `glossary.md` (term consistency):

```
Update .claude/agents/writer.md Step 2 (Resolve Context):

| Always load | Why |
|---|---|
| messaging/profile.md | Voice, tone, brand values |
| messaging/space.md | Positioning context |
| messaging/glossary.md | Term definitions and consistency |
```

The writer references glossary definitions when using terms that have company-specific meaning. It does not quote the glossary — it uses the definitions to ensure term consistency in generated content.

### Campaign Agent

The campaign agent's narrative section in the messaging brief should reference glossary terms for consistency across the multi-asset campaign. Add to the campaign agent's system prompt:

```
Add to .claude/agents/campaign.md, Phase 2 (Messaging Brief), Campaign Narrative:

Load messaging/glossary.md when writing the campaign narrative. Key terms used
in the narrative should align with glossary definitions. If the campaign introduces
terms not in the glossary, note them for the user — the glossary may need updating
after the campaign is produced.
```

### Tune Agent

The tune agent reads the glossary during tuning to inform vocabulary calibration in skills. Add to the tune agent's Step 1:

```
Update .claude/agents/tune.md Step 1 (Read the Messaging House):

Include messaging/glossary.md in the messaging house read. Glossary terms with
company-specific definitions should be reflected in skill vocabulary guidance —
terms in the glossary are always preferred over generic alternatives when the
skill generates content in the company's domain.
```

### Audit Command

The audit command should check glossary health as part of its consistency assessment:

```
Update .claude/commands/audit.md:

Add a glossary consistency check:
- Are there terms in the glossary that no longer appear in the messaging house?
- Are there terms used frequently across the messaging house that aren't in the glossary?
- Are there glossary definitions that conflict with how the term is currently used?

Report glossary issues in the audit report under a "Terminology Consistency" section.
```

### Research Agent

When the research agent updates messaging docs (competitor profiles, category docs) that introduce or retire terminology, it should note that the glossary may need updating:

```
Update .claude/agents/researcher.md:

After writing or updating any messaging doc, check whether new terms were introduced
or existing terms were retired. If so, note in the output: "Glossary may need
updating — run /project:glossary to sync."
```

### CLAUDE.md

```
Update CLAUDE.md:

Agents section — add glossary agent description:

### glossary

Maintains `messaging/glossary.md` — a curated list of terms with company-specific
definitions extracted from the messaging house. Runs on demand, scanning all messaging
docs to add, update, and remove entries. Flags terminology conflicts.

Invoke: `/project:glossary` or `/project:glossary --check`

Commands table — add:

| `/project:glossary` | Update glossary from messaging house |
| `/project:glossary --check` | Check glossary health without changes |

Directory permissions — update glossary entry:

| `messaging/glossary.md` | Yes | Glossary agent with approval | Derived from messaging house |
```

---

## Deliverables

### New Files
- Agent definition: `.claude/agents/glossary.md`
- Command templates: `.claude/commands/glossary.md`
- Glossary file: `messaging/glossary.md` (generated by agent on first run)

### Modified Files
- `.claude/agents/bootstrap.md` — Glossary invocation at completion
- `.claude/agents/writer.md` — Add glossary.md to always-load context
- `.claude/agents/campaign.md` — Glossary reference in narrative generation
- `.claude/agents/tune.md` — Glossary read during skill calibration
- `.claude/agents/researcher.md` — Glossary update note after doc changes
- `.claude/commands/audit.md` — Terminology consistency check
- `CLAUDE.md` — Agent description, commands, permissions