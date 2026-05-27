# One-Pager Template — Author Guidance

Calibrates `asset.md` for `one-pager` to the company's design system and broader one-page-collateral conventions.

## Ownership rule

The asset envelope (`asset.md`) carries only the **company conventions** for one-pagers — page-cap discipline, design system constraints, persona-bound rule, brand styling. Variants do the editorial heavy lifting (Structure, CTA conventions, Voice notes, Examples).

| Lives in `asset.md` | Lives in `variants/[name].md` |
|---|---|
| Frontmatter (slug, content-keys, array-keys, publishing, default-variant) | When to use |
| Conventions (page cap, design system, persona-bound rule, brand styling) | Voice notes |
| Frontmatter requirements (PDF generator fields, page size, brand theme) | Structure (a sales pitch differs sharply from a battlecard or datasheet) |
| Variants table | CTA conventions (calendar link, docs link, partner portal — varies by variant) |
|  | Examples |

## Common variants

Typical variants for this asset: `sales`, `battlecard`, `datasheet`, `partner-overview`, `executive-brief`. Add via `/design asset one-pager --add-variant [name]`.

## When this template is generated

- `/bootstrap` Phase 8 with "one-pager" selected.
- `/design asset one-pager` directly.
- `/design asset one-pager --add-variant [name]` to add a variant.

## What makes a good asset spec

- **One-page discipline.** The envelope should enforce the printed-page constraint, not just suggest it. The design template is what makes it real — name the template explicitly in Conventions.
- **Champion-forwardable.** Test: a director receives this and can forward to their CISO without explaining. Every variant should produce that.
- **Persona-bound.** One persona per one-pager; multi-persona pages dilute.

## Common pitfalls

- Feature lists masquerading as differentiators (mostly a sales-variant issue — variant guidance should enforce claim + proof).
- Generic CTA. "Learn more" is not a CTA. Each variant carries its own specific CTA pattern.
- Forgetting design system constraints. PDFs render from templates; name the design template in Conventions.
- Cramming multiple variants into one one-pager (combined sales + datasheet). Create two variants instead.

## What stays in the template (do not delete during generation)

- The `slug`, `status`, `content-keys`, `array-keys`, `publishing`, and `default-variant` frontmatter fields.
- The three section headers: `## Conventions`, `## Frontmatter requirements`, `## Variants`.
- The `[Instructions: ...]` blocks (deleted on generation; replaced with populated content).
- The `variants/` subdirectory and `variant-template.md` scaffold.
