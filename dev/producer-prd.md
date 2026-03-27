# PRD: Content Production System

## Overview

The content production system turns generated content into finished, designed deliverables — PDFs, slide decks, Word documents — that leave the building. It adds a producer agent, a brand token system, coded asset templates, and an extended campaign pipeline that orchestrates the full journey from messaging context through content generation, quality review, and formatted production.

Today the system generates content as markdown. The campaign agent dispatches writer subagents that produce structured content files. Those files are useful as drafts but they're not deliverables. A sales rep can't hand a prospect a markdown file. A field marketer can't print one for a booth. The production system closes that gap.

## Architecture

### Pipeline

```
Messaging House → Writer → Reader → Producer → Deliverable
                    ↑          ↑         ↑
                 Skills   Evaluation   Asset Template + Brand Tokens
```

The campaign agent orchestrates this pipeline per asset. Each stage is a subagent with a scoped role:

| Stage | Agent | Input | Output |
|---|---|---|---|
| **Write** | Writer | Messaging context + copywriting skill | Structured content markdown |
| **Review** | Reader | Content markdown + skill evaluation criteria | Quality assessment + approval / revision request |
| **Produce** | Producer | Approved content + asset template + brand tokens | Finished file (.pdf, .pptx, .docx) |

The reader gate is optional — the user can skip it for speed or enforce it for quality. The campaign agent respects a `review: true | false` flag in the campaign brief per asset.

### Agents

**Writer** — Exists. Produces structured content markdown using copywriting skills. No changes to the writer agent itself, but the content schema templates (the structured markdown contract between writer and producer) become critical. The writer must output content in the schema the producer expects.

**Reader** — Exists conceptually as the asset-reader agent from the original repo. Expanded role: evaluates content against the skill's evaluation criteria, checks messaging house grounding (do claims trace to docs?), and produces a quality assessment. Returns `approved`, `approved-with-notes`, or `revision-needed`. If revision is needed, the campaign agent re-dispatches the writer with the reader's notes.

**Producer** — New. Takes approved content, loads the matching asset template, applies brand tokens, and produces the finished file. The producer never modifies content — it formats and designs. If the content is wrong, that's the writer's problem. If the design is wrong, that's the producer's problem.

---

## What Ships

```
.claude/
  agents/
    producer.md              → Producer agent definition
    reader.md                → Reader agent definition (expanded from asset-reader)
  commands/
    produce.md               → /project:produce slash command
  skills/
    messaging/
      production/
        SKILL.md             → Production skill router
        production-types/
          datasheet.md
          one-pager.md
          executive-brief.md
          slide-deck.md
          campaign-kit.md

messaging/
  brand.yml                  → Design tokens (colors, fonts, spacing, logos)
  brand/                     → Logo files and brand assets

_templates/
  assets/                    → Coded document templates
    datasheet.html
    one-pager.html
    executive-brief.html
    pitch-deck.pptx
    sales-deck.pptx
  content-schemas/           → Structured markdown contracts between writer and producer
    datasheet.md
    one-pager.md
    executive-brief.md
    slide-deck.md
    battlecard.md

output/
  production/                → Finished deliverables
```

---

## Brand Token System

### Purpose

Brand guidelines in profile.md are prose — voice, tone, theme pillars. A producer agent needs machine-readable values: hex colors, font stacks, spacing scales, logo file paths. The brand token system bridges this gap.

### File: `messaging/brand.yml`

```yaml
colors:
  primary: ""
  secondary: ""
  accent: ""
  text: ""
  text-light: ""
  background: ""

typography:
  heading: ""   # font family for headings
  body: ""      # font family for body text

logo:
  primary: "messaging/brand/logo-primary.svg"
  icon: "messaging/brand/logo-icon.svg"
  white: "messaging/brand/logo-white.svg"
```

That's it. Colors, fonts, logos. The production skills handle type scale, spacing, weights, and layout conventions — those are document design decisions, not brand decisions. If a company needs to override a specific design convention (e.g., unusually wide margins for legal documents), that's a note in the production type guide, not a token.

### Ingestion

The user may provide brand guidelines in any format — a Figma export, a PDF brand book, a style guide doc, a website URL. The tune agent (or a dedicated brand ingestion step during bootstrap) extracts the structured tokens and writes `brand.yml`.

For teams without formal brand guidelines, the bootstrap agent populates `brand.yml` with sensible defaults derived from the company website's colors and typography, noting them as provisional.

### Usage

Every production skill reads `brand.yml` before generating output. The tokens are applied per format:

| Format | How Tokens Apply |
|---|---|
| HTML → PDF | CSS custom properties: `--color-primary`, `--font-heading`, etc. |
| PPTX | Slide master theme colors and font families |
| DOCX | Document style overrides for heading and body fonts, accent colors |

Brand tokens are hard constraints for the producer — it does not deviate from them. If the user wants different colors for a specific asset, they provide an override in the production request, not in the template.

---

## Asset Templates

### Purpose

Coded document templates define the visual layout for each asset type. They carry the structure, zones, and design patterns — but not the content. The producer agent reads the content from the writer's output and injects it into the template, applying brand tokens for the visual layer.

### Template Directory: `_templates/assets/`

#### HTML Templates (for PDF production)

```html
<!-- _templates/assets/datasheet.html -->
<!DOCTYPE html>
<html>
<head>
  <style>
    :root {
      --color-primary: {{colors.primary}};
      --color-secondary: {{colors.secondary}};
      --color-accent: {{colors.accent}};
      --color-text: {{colors.text}};
      --color-text-light: {{colors.text-light}};
      --font-heading: {{typography.heading}};
      --font-body: {{typography.body}};
    }
    
    @page { size: letter; margin: 0.75in; }
    
    /* Zone layout */
    .zone-header { /* top 15% */ }
    .zone-value { /* next 20% */ }
    .zone-capabilities { /* middle 40% */ }
    .zone-proof { /* lower 15% */ }
    .zone-footer { /* bottom 10% */ }
  </style>
</head>
<body>
  <div class="zone-header">
    <img src="{{logo.primary}}" class="logo" />
    <h1>{{tagline}}</h1>
  </div>
  <div class="zone-value">
    {{problem}}
  </div>
  <!-- ... -->
</body>
</html>
```

Templates use a simple token syntax (`{{field}}`) that the producer replaces with content from the content schema and brand tokens. No build tool, no templating engine — the producer agent reads the template, performs string replacement, and hands the result to the platform skill for conversion.

#### PPTX Templates (for slide deck production)

PPTX templates are actual .pptx files with master slides, placeholder layouts, and brand colors pre-configured. The producer agent opens the template, clones slide layouts, and populates content programmatically via python-pptx.

```
_templates/assets/
  pitch-deck.pptx          → Master slides: title, content, two-column,
                              section divider, proof, closing
  sales-deck.pptx          → Same masters, different default slide order
```

The template carries the visual structure. The producer carries the content. Brand tokens are baked into the template's theme colors — when `brand.yml` changes, the templates need regeneration.

### Template Versioning

Each template carries a version in a comment or metadata:

```html
<!-- template: datasheet | version: 1.2 | updated: 2026-03-15 -->
```

The production manifest on each produced file records which template version was used:

```yaml
template: datasheet
template_version: "1.2"
```

When a template is updated, the audit command can identify which produced assets were built from an older version and may need regeneration.

---

## Content Schema Templates

### Purpose

The structured markdown contract between the writer and the producer. The writer outputs content following the schema. The producer reads it and knows exactly where to find each piece for injection into the asset template.

### Directory: `_templates/content-schemas/`

Each producible asset type has a schema:

```markdown
<!-- _templates/content-schemas/datasheet.md -->
---
schema: datasheet
product: ""
persona: ""
---

## Tagline
[one-liner]

## Problem
[2-3 sentences]

## Capabilities
### [Capability Name]
- **Type:** unique | core
- **Description:** [one sentence]

## Architecture
[deployment, integration, data — if applicable]

## Differentiation
### [Point]
- **Unlike:** [alternative approach]
- **We:** [our approach]

## Proof
- **Quote:** ""
- **Attribution:** ""
- **Metric:** ""

## Use Cases
### [Use Case]
- **Persona:** [who]
- **Outcome:** [what they achieve]

## CTA
- **Action:** [matched to pricing model]
- **URL:** [destination]
```

The writer skill's output format section should reference the schema: "Output content following the schema in `_templates/content-schemas/datasheet.md`." The producer reads the schema to parse the writer's output into named fields, then maps those fields into the asset template's zones.

### Schema-to-Template Mapping

Each content schema field maps to a zone in the asset template:

| Schema Field | Datasheet Template Zone |
|---|---|
| Tagline | `.zone-header h1` |
| Problem | `.zone-value` |
| Capabilities | `.zone-capabilities` grid |
| Proof.Quote + Proof.Attribution | `.zone-proof` pull quote |
| Proof.Metric | `.zone-proof` metric callout |
| CTA.Action | `.zone-footer` button |

This mapping lives in the production type guide (e.g., `production-types/datasheet.md`), not in the template itself. The producer agent reads both the type guide and the template to understand how to inject content.

---

## Producer Agent

### Purpose

Takes approved content, loads the matching asset template, applies brand tokens, and produces a finished file. The producer never modifies content — it formats and designs.

### Invocation

```
/project:produce [asset-type] [content-file]
```

Or as a subagent in the campaign pipeline:

```
/agents producer --type datasheet --content output/campaigns/q1-launch/asset-01-datasheet.md
```

### System Prompt

```markdown
You are a producer agent that creates finished, designed deliverables from
approved content. You format and design — you never modify the content itself.
If the content is incomplete or incorrect, flag it and stop. Do not fill gaps
with invented messaging.

## How You Work

### Step 1: Identify the Asset Type

Determine the production type from the input or the content file's frontmatter
schema field. Load the corresponding production type guide from
.claude/skills/messaging/production/production-types/.

### Step 2: Load Brand Tokens

Read messaging/brand.yml. These are hard constraints — every color, font, and
spacing value comes from this file. Do not use defaults if brand.yml exists.
If brand.yml doesn't exist, use sensible defaults and note them in the output.

### Step 3: Load the Asset Template

Read the matching template from _templates/assets/. For HTML→PDF assets,
load the HTML template. For PPTX assets, load the .pptx template file.

### Step 4: Parse the Content

Read the content file and parse it against the content schema from
_templates/content-schemas/. Every field in the schema should be populated.
If a field is missing or empty:
- For optional fields: omit the zone or use a graceful fallback
- For required fields: flag and stop — the content needs revision

### Step 5: Load the Platform Skill

Read the platform format skill for the output format:
- HTML → PDF: /mnt/skills/public/pdf/SKILL.md
- Native PPTX: /mnt/skills/public/pptx/SKILL.md
- Native DOCX: /mnt/skills/public/docx/SKILL.md

Follow the platform skill's rules exactly — they contain format-specific
patterns, library usage, and common pitfalls.

### Step 6: Assemble and Produce

For HTML → PDF:
1. Copy the HTML template
2. Inject brand tokens as CSS custom properties
3. Replace content tokens ({{field}}) with parsed content
4. Render to PDF using the platform skill's conversion method

For PPTX:
1. Open the PPTX template
2. For each slide in the production type's structure, clone the
   appropriate master layout
3. Populate slide content from parsed fields
4. Apply brand token overrides if the template's theme doesn't match
5. Write speaker notes from the content's narrative sections
6. Save the .pptx file

For DOCX:
1. Follow the platform skill's creation or editing workflow
2. Apply brand tokens as document styles
3. Populate content sections
4. Save the .docx file

### Step 7: Write the Production Manifest

Alongside the produced file, write a manifest tracking provenance:

```yaml
---
asset: "vuln-mgmt-datasheet"
type: "datasheet"
format: ".pdf"
template: "datasheet"
template_version: "1.2"
brand_tokens: "messaging/brand.yml"
content_source: "output/campaigns/q1-launch/asset-01-datasheet.md"
messaging_docs: [list from content source's frontmatter]
produced: "2026-03-15"
status: "draft"
---
```

### Step 8: Present for Review

Do not mark the asset as final. Present the produced file and ask the user
to review:
- For PDFs: note the file path and suggest opening in a browser or PDF viewer
- For PPTX: note the file path and suggest opening in PowerPoint or Google Slides
- For DOCX: note the file path and suggest opening in Word or Google Docs

The user confirms "final" or requests revisions. If revisions are visual
(layout, spacing, color), the producer handles them. If revisions are
content-level (messaging, claims, proof), the writer needs to re-run.

## Multi-Format Output

When the same content needs multiple formats (a battlecard as PDF and as a
slide in the sales deck), produce each format separately from the same
content source. Do not regenerate content — read the same content file and
apply different templates.

## What You Can Modify

- Asset templates during production (injecting content and tokens)
- Output files in output/production/ or output/campaigns/

## What You Cannot Modify

- _templates/assets/ — base templates are read-only
- _templates/content-schemas/ — schemas are read-only
- messaging/ — the producer never touches messaging docs
- The content file — if content is wrong, flag it, don't fix it
```

### Tool Scoping

- **Read** — `messaging/brand.yml`, `messaging/brand/`, `_templates/assets/`, `_templates/content-schemas/`, `.claude/skills/messaging/production/`, `/mnt/skills/public/`, content files in `output/`
- **Write** — `output/production/`, `output/campaigns/[name]/production/`
- **Execute** — Platform skill scripts (Puppeteer/Playwright for PDF conversion, python-pptx for slides, docx-js for documents)
- **Glob, Grep** — Full access for finding content files and templates

---

## Reader Agent

### Purpose

Evaluates generated content against the skill's evaluation criteria and messaging house grounding before it goes to production. The reader is the quality gate between writing and producing.

### Invocation

```
/agents reader --content [content-file] --skill [skill-type]
```

### Assessment Output

```markdown
## Quality Assessment

**Asset:** [name]
**Skill:** [skill type used]
**Verdict:** approved | approved-with-notes | revision-needed

### Evaluation Criteria
[Assessment against each criterion from the skill's evaluation table]

### Messaging Grounding
- Claims traced to docs: [list]
- Ungrounded claims: [list — these need revision or removal]
- Proof points verified: [list]
- Missing proof: [where claims need evidence]

### Notes
[Specific observations, strengths, areas for improvement]

### Revision Requests (if verdict is revision-needed)
1. [Specific change needed with reasoning]
2. [Specific change needed with reasoning]
```

The reader doesn't rewrite content — it evaluates and directs. If revision is needed, the campaign agent re-dispatches the writer with the reader's notes as additional context.

---

## Campaign Integration

### Extended Pipeline

The campaign agent's Phase 3 (Production) gains two additional stages:

```
Current:  Brief → [Writer subagent per asset] → Done
Extended: Brief → [Writer → Reader → Producer per asset] → Done
```

### Brief Additions

The campaign brief frontmatter gains production-related fields:

```yaml
assets:
  - id: "asset-01"
    type: "blog-post"
    skill: "blog-copywriting/product-announcement"
    # ... existing fields ...
    
    # Production fields (new)
    produce: true              # whether this asset gets produced
    production_format: "pdf"   # pdf | pptx | docx | none
    production_template: "datasheet"  # which asset template to use
    review: true               # whether reader agent evaluates before production
```

Not every asset gets produced. Blog posts and email sequences stay as markdown — they're published through CMS and email platforms respectively. Datasheets, decks, one-pagers, and briefs get produced.

### Campaign Kit Extension

The campaign kit production type now orchestrates the full pipeline:

```
For each producible asset in the campaign:
  1. Check if content exists in the campaign directory
  2. If not, dispatch writer subagent (existing behavior)
  3. If review: true, dispatch reader subagent
     - If revision-needed, re-dispatch writer with notes
     - Loop until approved (max 2 revision cycles)
  4. If produce: true, dispatch producer subagent
     - Load asset template + brand tokens
     - Produce the file to campaign/production/
  5. Update brief frontmatter with production status
```

### Production Output Structure

```
output/campaigns/q1-launch/
  brief.md
  asset-01-announcement-blog.md       → Content (markdown, not produced)
  asset-02-press-release.md           → Content (markdown, not produced)
  asset-03-customer-email.md          → Content (markdown, not produced)
  asset-04-sales-deck.md              → Content (markdown, writer output)
  asset-05-datasheet.md               → Content (markdown, writer output)
  production/
    asset-04-sales-deck.pptx          → Produced deliverable
    asset-04-sales-deck.manifest.md   → Production manifest
    asset-05-datasheet.pdf            → Produced deliverable
    asset-05-datasheet.manifest.md    → Production manifest
    kit-manifest.md                   → Kit-level manifest
```

---

## Brand Ingestion

### Via Tune Agent

The tune agent's Step 1 (Read the Messaging House) already reads `profile.md` for voice and visual identity signals. Extend this to also read or create `brand.yml`:

```
If messaging/brand.yml exists:
  Read and validate tokens. Flag any missing required fields.
  
If messaging/brand.yml does not exist:
  Check if the user has provided brand materials (PDF, Figma export, 
  style guide, website URL).
  
  If materials provided:
    Extract colors, typography, spacing, and logo references.
    Write brand.yml with extracted tokens.
    Present to user for confirmation.
    
  If no materials provided:
    Attempt to extract from the company website (profile.md → website field).
    Write brand.yml with extracted tokens, marked as provisional.
    Present to user for confirmation.
```

### Via Bootstrap

At the end of the bootstrap process (after glossary generation), prompt the user for brand materials:

```
"Your messaging house is populated and the glossary is generated.
The final step is visual identity. Do you have brand guidelines
(PDF, style guide, Figma export) I can extract design tokens from?
Or I can pull colors and typography from your website as a starting point."
```

### Manual Editing

`brand.yml` is a simple YAML file. Users can edit it directly. The producer reads it fresh on every production run — no caching, no restart required.

---

## Commands

### /project:produce [asset-type] [content-file]

```markdown
Produce a finished deliverable from a content file.

Identify the asset type and load the production type guide. Read brand.yml
for design tokens. Load the matching asset template. Parse the content file
against the content schema. Produce the file using the platform skill.
Present for user review before marking as final.

/agents producer $ARGUMENTS
```

### /project:produce --campaign [campaign-name]

```markdown
Produce all producible assets in a campaign.

Read the campaign brief. For each asset with produce: true, run the
production pipeline (writer → reader → producer). Write produced files
to the campaign's production/ subdirectory. Generate the kit manifest.

/agents producer --campaign $ARGUMENTS
```

### /project:brand

```markdown
Initialize or update brand tokens.

If messaging/brand.yml exists, present current tokens for review and update.
If not, extract tokens from provided materials or the company website.

/agents tune --brand $ARGUMENTS
```

---

## Tooling Requirements

The producer agent needs the following tools available in the execution environment:

| Tool | Purpose | Platform Skill |
|---|---|---|
| Puppeteer or Playwright | HTML → PDF rendering | `/mnt/skills/public/pdf/SKILL.md` |
| python-pptx | Native PPTX creation | `/mnt/skills/public/pptx/SKILL.md` |
| docx-js (npm) | Native DOCX creation | `/mnt/skills/public/docx/SKILL.md` |

These are standard dependencies for Claude Code and Cowork environments. The platform skills document installation and usage patterns. The producer skill's instructions should include a verification step: "Before producing, confirm the required tools are available. If not, provide installation instructions."

---

## Integration Changes

### Campaign Agent

Update Phase 3 (Production) to support the extended pipeline:

```
Update .claude/agents/campaign.md:

Phase 3 now supports three subagent stages per asset:
1. Writer (existing)
2. Reader (new, optional — controlled by review: true in brief)
3. Producer (new, optional — controlled by produce: true in brief)

Add production fields to the brief frontmatter schema:
produce, production_format, production_template, review

Update the completion summary to include production status.
```

### Writer Agent

Update the writer to output content following content schemas when the asset is producible:

```
Update .claude/agents/writer.md:

When the task is part of a campaign with produce: true on the asset,
output content following the matching schema from
_templates/content-schemas/[type].md. The schema ensures the producer
can parse the output reliably.
```

### Tune Agent

Extend to handle brand token ingestion:

```
Update .claude/agents/tune.md:

Step 1 (Read the Messaging House) now includes reading or creating
messaging/brand.yml. If brand materials are provided, extract tokens.
If not, attempt extraction from the company website.
```

### Bootstrap Agent

Add brand ingestion as the final bootstrap step (after glossary):

```
Update .claude/agents/bootstrap.md:

After glossary generation, prompt for brand materials and create
messaging/brand.yml. This is the final step of the bootstrap process.
```

### Audit Command

Extend to check production health:

```
Update .claude/commands/audit.md:

Add a "Production Health" section:
- Are asset templates current?
- Are there produced assets built from outdated template versions?
- Is brand.yml populated and complete?
- Are content schemas aligned with production type guides?
```

### CLAUDE.md

```
Update CLAUDE.md:

Agents — add producer and reader:

### producer
Creates finished deliverables (PDF, PPTX, DOCX) from approved content.
Reads brand tokens, loads asset templates, applies content from writer
output. Never modifies content — formats and designs only.

Invoke: /project:produce [type] [content-file]

### reader
Evaluates generated content against skill criteria and messaging house
grounding. Returns approved, approved-with-notes, or revision-needed.

Commands — add:
| /project:produce [type] [file] | Produce a finished deliverable |
| /project:produce --campaign [name] | Produce all campaign deliverables |
| /project:brand | Initialize or update brand tokens |

Directory structure — add:
messaging/brand.yml          → Design tokens
messaging/brand/             → Logo files and brand assets
_templates/assets/           → Coded document templates
_templates/content-schemas/  → Writer-to-producer content contracts

Directory permissions — add:
| messaging/brand.yml | Yes | Tune/bootstrap agent | Design tokens |
| _templates/assets/ | Yes | No | Base templates, read-only |
| _templates/content-schemas/ | Yes | No | Content schemas, read-only |
```

---

## Deliverables

### New Files
- Agent definitions: `.claude/agents/producer.md`, `.claude/agents/reader.md`
- Command templates: `.claude/commands/produce.md`
- Production skills: `.claude/skills/messaging/production/SKILL.md` and type guides
- Brand token file: `messaging/brand.yml` (created by bootstrap or tune)
- Asset templates: `_templates/assets/` (HTML for PDFs, PPTX for decks)
- Content schemas: `_templates/content-schemas/` (per producible asset type)

### Modified Files
- `.claude/agents/campaign.md` — Extended pipeline (writer → reader → producer)
- `.claude/agents/writer.md` — Content schema output for producible assets
- `.claude/agents/tune.md` — Brand token ingestion
- `.claude/agents/bootstrap.md` — Brand ingestion as final step
- `.claude/commands/audit.md` — Production health checks
- `CLAUDE.md` — New agents, commands, directories, permissions

### Template Files to Create
- `_templates/assets/datasheet.html`
- `_templates/assets/one-pager.html`
- `_templates/assets/executive-brief.html`
- `_templates/assets/pitch-deck.pptx`
- `_templates/assets/sales-deck.pptx`
- `_templates/content-schemas/datasheet.md`
- `_templates/content-schemas/one-pager.md`
- `_templates/content-schemas/executive-brief.md`
- `_templates/content-schemas/slide-deck.md`
- `_templates/content-schemas/battlecard.md`