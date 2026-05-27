---
slug: blog-post
status: active
last-reviewed: ""
content-keys:
  - title
  - slug
  - body
  - excerpt
  - featured_image_url
  - categories
  - tags
  - author
  - seo_title
  - seo_description
array-keys:
  - categories
  - tags
publishing: ""
default-variant: ""
production-targets:
  - web
  - print
---

# Blog Post

[Instructions:
The canonical long-form editorial format for the company. Used for thought leadership, product announcements, technical deep dives, customer-led narratives, and category education. Default for the `blog` content type in MESSAGE.md `## Assets`.

This envelope carries only the company conventions that hold across every blog variant — length norms, CMS quirks, image cadence, frontmatter requirements. Structure and CTA conventions live in each variant under `variants/`, since both genuinely vary by editorial intent.]

## Conventions

[Instructions:
Specify the company's blog-wide standards that hold across variants. Examples:
- Length bands (e.g., 800-1,500 words standard; 1,500-2,500 anchor; 600-900 short-form)
- H1 handling (set by frontmatter vs. in body)
- Image cadence (e.g., one image per ~400 words)
- Quote attribution rules
- Sign-off / author byline conventions
- Voice and tone notes specific to blog (vs. other formats)]

[Tips:
- Be specific about word counts; vague guidance leads to inconsistent output
- Note any platform-specific quirks (e.g., HubSpot character limits, WordPress excerpt fields)
- Variant-specific length adjustments belong in the variant's Structure section, not here]

## Frontmatter requirements

[Instructions:
Document the required and optional frontmatter fields for the publishing destination. Be explicit about format and constraints. Common additions to the default content-keys above:
- `published_date` (ISO 8601)
- `updated_date` (ISO 8601)
- `canonical_url` (for syndication)
- `meta_robots` (index/noindex)

Note any controlled vocabularies (e.g., a fixed list of allowed categories).]

## Variants

Catalog of variants this asset supports. The `default-variant` frontmatter field marks the variant the writer uses when a brief's asset manifest doesn't specify one. Files live in `variants/[slug].md`.

| Variant | File | Default | Description |
|---|---|---|---|
| [Instructions: Populated by `/design asset --add-variant [name]`. One row per variant; ✓ in Default for the default; description matches the variant's `When to use` section.] | | | |
