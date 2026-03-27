# Compose Skill

Create and update any document in `messaging/` on demand — pillar docs and any collection profile type. Research informs composition but is not an end in itself.

Invoked via `/compose [type] [name]`.

## Document Types

You handle all 14 document types with templates in `templates/messaging/`:

**6 pillars:** profile, space, audience, portfolio, proof, motion
**8 collection types:** competitor, category, persona, segment, product, solution, story, play

## How You Work

Four steps: Resolve → Research → Plan → Write.

### Step 1: Resolve

Parse the user's request for document type and whether this is a create or update.

Load the always-load pillars (profile.md, space.md, glossary.md).

**For collection profiles, also load the parent pillar:**

| Collection Type | Parent Pillar |
|---|---|
| competitor, category | `messaging/space.md` (already loaded) |
| persona, segment | `messaging/audience.md` |
| product, solution | `messaging/portfolio.md` |
| story | `messaging/proof.md` |
| play | `messaging/motion.md` |

**Then:**

- Read the template from `templates/messaging/[type].md` to understand the schema and sections to populate.
- Check `messaging/[collection]/` for an existing file if updating.
- Check all `input/` subdirectories (`input/messaging/`, `input/docs/`, `input/research/`, `input/transcripts/`, `input/examples/`) and the `input/` root for existing material relevant to this document. Prioritize `input/messaging/` for positioning context. Also check `output/research/` for agent-generated reports.

### Step 2: Research

Fill gaps bounded by what the template sections require. Research serves composition — gather only what you need to write the document well.

Maximum 10 web searches per task. Each query must include a specific company name, product name, or entity name from the messaging house.

**Query construction:**
- Competitors: "[name] product", "[name] pricing", "[name] vs [our company]", "[name] funding"
- Personas: "[role] responsibilities", "[role] buying criteria", "[role] pain points [industry]"
- Products: "[company] [product] features", "[company] [product] reviews"
- General: "[company] [topic]", "[topic] [industry/category from space.md]"

**Present findings and gaps to the user.** Show what you found, where it came from, and what's missing. This sets up the plan step.

### Step 3: Plan

Propose changes before writing anything. Present a structured plan using AskUserQuestion:

```
Composition Plan

What was found:
- [Source 1]: [key finding]
- [Source 2]: [key finding]
- Gaps: [what's missing or thin]

Documents to create/update:
- messaging/[path] — [one-line summary]

Key decisions:
- [Decision 1 — e.g., "Position as challenger to incumbent X"]
  Challenge: [if applicable — generic positioning, unsubstantiated claim, missing differentiation]
  Recommendation: [sharper alternative or question]
- [Decision 2]

For updates — what's changing vs. preserved:
- Changing: [sections being modified]
- Preserved: [sections left intact]
```

Use AskUserQuestion for choices, confirmations, and plan approval. The user can approve, adjust, or redirect before any writes happen.

### Step 4: Write

After user approval:

1. **Write or update the file(s).** Follow the template schema. Populate YAML frontmatter and all markdown sections.
2. **Set `updated` to today's date** (ISO format) in frontmatter.
3. **Update the parent pillar reference table.** Ensure the corresponding row exists with a Description column entry (~15 words) that differentiates from sibling entries. The profile's frontmatter `description` and the table Description must match — if updating one, update both.
4. **Note glossary impact.** If new terms were introduced or existing terms retired, note: "Glossary may need updating — run `/investigate fix glossary` to sync."
5. **Confirm each file** with a one-line summary: `Created messaging/competitors/acme-corp.md — Primary competitor, enterprise security platform`

## Pillar Updates

When updating a pillar doc, read downstream pillars that reference it. Include impact analysis in the plan:

- Which downstream pillar docs reference this one
- Which collection profiles might be affected
- What specific claims or positioning might need revision

After writing, note downstream drift: "Updated space.md positioning. The following docs may need review: [list of affected downstream docs]."

## Open-Ended Requests

When the user's request doesn't specify a clear document type (e.g., `compose research [topic]`):

1. Research the topic using the Step 2 process.
2. In the plan step, recommend specific documents to create or update based on findings.
3. The user decides what to write — the plan is where you make recommendations.

If the messaging house is empty (no profile.md or mostly placeholder content), recommend running bootstrap instead: "The messaging house doesn't have enough foundation for on-demand composition. I'd recommend running `/bootstrap` to build the system from scratch."

## Relationship to Bootstrap

Bootstrap builds the full messaging system from scratch in 7 ordered phases. Compose handles on-demand creation and updates — no phase ordering, no progress file. They don't interact.

## Tool Scoping

- **Read** — `messaging/`, `templates/messaging/`, `input/`, `output/research/`, `insights/`
- **Write, Edit** — `messaging/` (user confirmation required), `output/research/` (autonomous)
- **WebSearch, WebFetch** — Bounded by task (max 10 searches)
- **Glob, Grep** — Full access
- **AskUserQuestion** — Interactive composition workflow: presenting findings, proposing plans, collecting decisions
