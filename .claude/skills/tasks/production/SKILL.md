---
name: production
description: Produce finished deliverables from approved content. Routes to the correct production type, loads brand tokens and asset templates, discovers platform skills for rendering, and outputs designed files. Use when the user asks to produce, format, or design a deliverable from existing content.
---

# Production

## Instructions

1. **Identify Production Type:** Determine which type applies from the content file's `schema` frontmatter field or from the user's request
2. **Route to Track:** Check if a type guide exists in `types/` for this production type. If yes, use the **template track** (steps 3-5). If no, use the **model track** (skip to step 6).
3. **Load Type Guide (template track):** Read the corresponding file from `types/`
4. **Load Brand Tokens:** Read `messaging/brand.yml` for design tokens
5. **Load Asset Template (template track):** Read the matching template from `templates/assets/` and validate the content file against the schema from `templates/schemas/`
6. **Discover Platform Skills:** Check for available rendering skills using the discovery table below
7. **Produce:** Template track — follow the type guide's design conventions to assemble the deliverable. Model track — generate self-contained HTML directly from the content markdown + brand tokens.
8. **Write Manifest:** Track provenance alongside the produced file

## Production Type Guides (Template Track)

If a type guide exists for the production type, load it and follow the template track. These types have predefined templates and schemas:

- **Datasheet:** See `types/datasheet.md`
- **One-Pager:** See `types/one-pager.md`
- **Executive Brief:** See `types/executive-brief.md`
- **Slide Deck:** See `types/slide-deck.md`
- **Battlecard:** See `types/battlecard.md`

## Model-Driven Production

When no type guide matches the production type, the model track activates. Instead of loading a predefined template, the producer generates a self-contained HTML deliverable directly from the content:

1. Read the full content file (markdown with frontmatter)
2. Load brand tokens from `messaging/brand.yml`
3. Generate complete, self-contained HTML with inline CSS using brand token CSS custom properties
4. Infer the appropriate layout for the asset type — clean, professional design suited to the content
5. The output is fully self-contained with no external dependencies

The model track extends production to any asset type — blog posts, emails, social content, enablement guides, or any other content the system generates. Predefined templates are optional accelerators, not requirements.

## Platform Skill Discovery

The production system delegates rendering to platform skills when available. Check these locations in order and use the first match:

| Format | Discovery Order | Fallback |
|--------|----------------|----------|
| PDF | `.claude/skills/pdf/SKILL.md` -> `/mnt/skills/public/pdf/SKILL.md` | Self-contained HTML (open in browser, print to PDF) |
| Slides (PPTX) | `.claude/skills/pptx/SKILL.md` -> `.claude/skills/frontend-slides/SKILL.md` -> `.claude/skills/revealjs/SKILL.md` -> `/mnt/skills/public/pptx/SKILL.md` | Self-contained HTML slide deck (zero dependencies, works offline) |
| DOCX | `.claude/skills/docx/SKILL.md` -> `/mnt/skills/public/docx/SKILL.md` | Deferred — output HTML instead |

**What we own vs. what platform skills own:**
- **We own:** Content schemas, brand tokens, production type guides (design conventions, content-to-zone mapping), asset HTML templates (document structure + brand application)
- **Platform skills own:** File format rendering (HTML-to-PDF conversion, PPTX assembly, slide framework integration)

When a platform skill is found, read its SKILL.md for format-specific rendering instructions. When no platform skill is available, output self-contained HTML that works in any browser.

## Brand Token Application

Brand tokens from `messaging/brand.yml` map to CSS custom properties in HTML templates:

| Token | CSS Custom Property |
|-------|-------------------|
| `colors.primary` | `--color-primary` |
| `colors.secondary` | `--color-secondary` |
| `colors.accent` | `--color-accent` |
| `colors.text` | `--color-text` |
| `colors.text-light` | `--color-text-light` |
| `colors.background` | `--color-background` |
| `typography.heading` | `--font-heading` |
| `typography.body` | `--font-body` |

If `brand.yml` has empty values, use the template's built-in defaults. Note which values are defaults in the production manifest.

## Content Parsing

The content file must follow the schema defined in `templates/schemas/[type].md`:

- **Required fields:** Must be populated. If missing, flag and stop — the content needs revision.
- **Optional fields:** If present, include in the output. If missing, omit the corresponding zone gracefully.
- **Schema field in frontmatter:** The `schema` field in the content file's YAML frontmatter identifies the production type.

## Production Manifest

Write a manifest file alongside each produced deliverable:

```yaml
---
asset: "[asset-name]"
type: "[production-type]"
format: "[.html | .pdf | .pptx]"
template: "[template-name] or model-generated"
template_version: "[version from template comment] or n/a"
brand_tokens: "messaging/brand.yml"
brand_defaults_used: [list of tokens that used defaults]
content_source: "[path to content file]"
platform_skill: "[path to platform skill used, or 'none (HTML fallback)']"
messaging_docs: [list from content source's frontmatter]
produced: "[ISO date]"
status: "draft"
---
```

## Output Locations

- **Standalone production:** `output/assets/`
- **Campaign production:** `output/campaigns/[campaign-name]/assets/`
- **Launch production:** `output/launches/[launch-name]/assets/`

## Evaluation Criteria

- **Brand compliance:** All tokens applied, no deviations from brand.yml
- **Content fidelity:** All required schema fields present in output, no content modifications
- **Template integrity:** Zones populated correctly, layout renders as intended
- **Platform skill adherence:** If a platform skill was used, its rules were followed exactly
- **Manifest completeness:** Every provenance field populated, template version recorded
