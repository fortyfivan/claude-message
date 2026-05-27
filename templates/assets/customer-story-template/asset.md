---
slug: customer-story
status: active
last-reviewed: ""
content-keys:
  - title
  - slug
  - customer_name
  - customer_logo_url
  - industry
  - region
  - products_used
  - challenge
  - solution
  - outcome
  - quote
  - quote_attribution
  - metrics
  - seo_title
  - seo_description
array-keys:
  - products_used
  - metrics
publishing: ""
default-variant: ""
production-targets:
  - web
  - print
---

# Customer Story

[Instructions:
Long-form customer narrative for the website's customers section, sales enablement, and proof-led marketing. Default for the `customer-story` content type. Source narratives from `messaging/collections/stories/[slug].md` — this format is the deliverable shape; the collection file is the source of truth.

This envelope carries only the company conventions that hold across every customer-story variant — length bands, sourcing rules, approval workflow, metrics provenance. Structure and CTA conventions live in each variant under `variants/` since they vary by editorial intent (anchor case study vs. mini-story vs. video transcript companion).]

## Conventions

[Instructions:
Specify the company's customer-story standards that hold across variants:
- Length bands (e.g., 600-1,200 words anchor; 200-400 words mini)
- Outcome metrics must trace to the source story in `messaging/collections/stories/` — never invent numbers
- Pull quote must be marked "approved" in the source story file
- Customer logo + photo permissions confirmed before publish
- Industry / region labeling conventions]

## Frontmatter requirements

[Instructions:
Document CMS expectations. `metrics` is typically an array of objects (`{label, value, context}`) or flat strings. Some CMSs require `customer_logo_alt` for accessibility — add as needed. Note any controlled vocabularies (industries, regions).]

## Variants

Catalog of variants this asset supports. The `default-variant` frontmatter field marks the variant the writer uses when a brief's asset manifest doesn't specify one. Files live in `variants/[slug].md`.

| Variant | File | Default | Description |
|---|---|---|---|
| [Instructions: Populated by `/design asset --add-variant [name]`. One row per variant; ✓ in Default for the default; description matches the variant's `When to use` section.] | | | |
