---
name: production
description: Produce finished deliverables from approved content. Routes to the correct production type, loads brand tokens and asset templates, discovers platform skills for rendering, and outputs designed files. Use when the user asks to produce, format, or design a deliverable from existing content.
---

# Production

## Instructions

1. **Identify Production Type:** Determine which type applies from the content file's `schema` frontmatter field or from the user's request
2. **Load Type Guide:** Read the corresponding file from `types/`
3. **Load Brand Tokens:** Read `messaging/brand.yml` for design tokens
4. **Load Asset Template:** Read the matching template from `templates/assets/`
5. **Parse Content:** Validate the content file against the schema from `templates/schemas/`
6. **Discover Platform Skills:** Check for available rendering skills using the discovery table below
7. **Produce:** Follow the type guide's design conventions to assemble the deliverable
8. **Write Manifest:** Track provenance alongside the produced file

## Production Type Guides

After identifying the production type, load the corresponding guide:

- **Datasheet:** See `types/datasheet.md`
- **One-Pager:** See `types/one-pager.md`
- **Executive Brief:** See `types/executive-brief.md`
- **Slide Deck:** See `types/slide-deck.md`
- **Battlecard:** See `types/battlecard.md`

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
template: "[template-name]"
template_version: "[version from template comment]"
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

## Evaluation Criteria

- **Brand compliance:** All tokens applied, no deviations from brand.yml
- **Content fidelity:** All required schema fields present in output, no content modifications
- **Template integrity:** Zones populated correctly, layout renders as intended
- **Platform skill adherence:** If a platform skill was used, its rules were followed exactly
- **Manifest completeness:** Every provenance field populated, template version recorded
