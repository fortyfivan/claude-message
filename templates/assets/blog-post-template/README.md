# Blog Post Template — Author Guidance

This template defines how `asset.md` for `blog-post` should be calibrated to a specific company's CMS, brand standards, and publishing destination. `/bootstrap` Phase 8 and `/design asset blog-post` read this template and ask the user to populate each section.

## Ownership rule

The asset envelope (`asset.md`) carries only the **company conventions** for this asset type — content that holds across every variant. Variants do the editorial heavy lifting (Structure, CTA conventions, Voice notes, Examples).

| Lives in `asset.md` | Lives in `variants/[name].md` |
|---|---|
| Frontmatter (slug, content-keys, array-keys, publishing, default-variant) | When to use |
| Conventions (length norms, image cadence, sign-off, platform quirks) | Voice notes |
| Frontmatter requirements (CMS field details) | Structure (section sequence specific to this variant) |
| Variants table (routing + descriptions + default marker) | CTA conventions (placement, destination, button voice) |
|  | Examples |

The `variants/` subdirectory holds the variant scaffold (`variant-template.md`). When the user adds a variant via `/design asset blog-post --add-variant [name]`, the design-asset skill copies this scaffold into `messaging/assets/blog-post/variants/[name].md` and interviews the user on the variant's specifics.

## When this template is generated

- A user runs `/bootstrap` and selects "blog" as a content type they produce.
- A user runs `/design asset blog-post` explicitly.
- A user runs `/design asset blog-post --add-variant [name]` to add a new variant.

## What makes a good asset spec

- **Specific over generic.** "1,200-1,500 words for use-case blogs; 2,000+ for anchor thought-leadership" beats "varies by type."
- **Tied to the publishing destination.** If the CMS is HubSpot, mention HubSpot field constraints. If it's a custom static site, mention the front matter the generator expects.
- **Don't duplicate variant guidance.** The asset spec is *envelope* (CMS, length norms, frontmatter). The variant files (use-case, thought-leadership, product-announcement) are *editorial calibration* (Structure, CTA, voice). Keep the boundary clean.

## Common pitfalls

- Listing every possible CMS field exhaustively. Default to the company's actual needs; users can extend later.
- Vague Conventions. "Quality matters" is not a convention. "Image cadence: one image per ~400 words" is.
- Forgetting the SEO fields. `seo_title` and `seo_description` should reflect what the CMS actually consumes — some CMSs derive these from `title` and `excerpt`; others want them explicit.
- Putting variant-specific guidance in asset.md. If something varies by editorial intent (use-case vs. thought-leadership), it belongs in the variant file.

## What stays in the template (do not delete during generation)

- The `slug`, `status`, `content-keys`, `array-keys`, `publishing`, and `default-variant` frontmatter fields.
- The three section headers: `## Conventions`, `## Frontmatter requirements`, `## Variants`.
- The `[Instructions: ...]` blocks (deleted on generation; replaced with populated content).
- The `variants/` subdirectory and `variant-template.md` scaffold.
