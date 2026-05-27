# Customer Story Template — Author Guidance

Calibrates `asset.md` for `customer-story` to the company's website and proof conventions.

## Ownership rule

The asset envelope (`asset.md`) carries only the **company conventions** for customer stories — sourcing rules, metric provenance, approval workflow, length bands. Variants do the editorial heavy lifting (Structure, CTA conventions, Voice notes, Examples).

| Lives in `asset.md` | Lives in `variants/[name].md` |
|---|---|
| Frontmatter (slug, content-keys, array-keys, publishing, default-variant) | When to use |
| Conventions (length bands, source-grounded rule, approval workflow, permissions) | Voice notes |
| Frontmatter requirements (CMS field details) | Structure (section sequence — anchor case study vs. mini-story differ) |
| Variants table | CTA conventions (similar-segment CTAs, demo, peer reference) |
|  | Examples |

## When this template is generated

- `/bootstrap` Phase 8 with "customer-story" selected.
- `/design asset customer-story` directly.
- `/design asset customer-story --add-variant [name]` to add a variant (e.g., `anchor`, `mini`, `video-companion`).

## What makes a good asset spec

- **Source-grounded.** The format produces a deliverable; the source-of-truth story lives in `messaging/collections/stories/[slug].md`. The format should reference the source file and require quote/metric provenance.
- **Approved quotes only.** External customer stories carry attributed quotes. The format should enforce the `approved: yes` check on the source story.
- **Never gated.** Customer stories are proof. Gating them turns proof into lead bait and erodes trust.

## Common pitfalls

- Inventing metrics. The format must enforce trace-to-source.
- Logo without permission. The format should require permissions check.
- Putting variant-specific guidance in asset.md. Anchor case studies and mini-stories have different Structure and CTA conventions — those live in `variants/`, not the envelope.

## What stays in the template (do not delete during generation)

- The `slug`, `status`, `content-keys`, `array-keys`, `publishing`, and `default-variant` frontmatter fields.
- The three section headers: `## Conventions`, `## Frontmatter requirements`, `## Variants`.
- The `[Instructions: ...]` blocks (deleted on generation; replaced with populated content).
- The `variants/` subdirectory and `variant-template.md` scaffold.
