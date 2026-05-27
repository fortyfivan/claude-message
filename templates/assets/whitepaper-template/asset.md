---
slug: whitepaper
status: active
last-reviewed: ""
content-keys:
  - title
  - subtitle
  - executive_summary
  - body
  - methodology
  - data_appendix
  - author
  - author_bio
  - publication_date
  - seo_title
  - seo_description
  - download_cta_label
  - download_cta_url
array-keys: []
publishing: ""
default-variant: ""
production-targets:
  - web
  - print
---

# Whitepaper

[Instructions:
Long-form analytical content backed by primary data, methodology, citations, or strategic argument. Used for research studies, topic deep-dives, market benchmarks, point-of-view papers, analyst-style briefs, regulatory or technical guides — anything that earns authority through depth rather than brevity. Default for the `whitepaper` content type in MESSAGE.md `## Assets`.

Common variants: research, topic, benchmark, point-of-view, analyst-brief, technical-guide, regulatory.

This envelope carries only the company conventions that hold across every whitepaper variant — citation discipline, attribution requirements, gating model, author credibility convention. Structure and CTA conventions live in each variant under `variants/` since they vary by editorial intent (a research study leads with methodology; a topic paper leads with the thesis; a benchmark leads with the data; a point-of-view paper leads with the contrarian argument).]

## Conventions

[Instructions:
Specify the company's whitepaper-wide standards that hold across variants:
- Word count bands (e.g., 3,000-10,000 words depending on variant scope)
- Citation style (footnote on same page as claim; no orphan stats)
- Every quantitative claim attributes a source; every directional claim names its evidence basis
- Designed for gated download; supports both PDF and web rendering
- Author byline + contact conventions
- Methodology disclosure rule (when applicable to variant)]

## Frontmatter requirements

[Instructions:
Document gated-PDF + landing page schema. `download_cta_label`/`download_cta_url` for gated; drop for web-only. For HubSpot/Marketo gated content, add `form_id` and `landing_page_url`. Variant-specific frontmatter (a research variant's `survey_n` and `survey_date`; a benchmark's `peer_set`) added per-variant during `/design asset whitepaper --add-variant`.]

## Variants

Catalog of variants this asset supports. The `default-variant` frontmatter field marks the variant the writer uses when a brief's asset manifest doesn't specify one. Files live in `variants/[slug].md`.

| Variant | File | Default | Description |
|---|---|---|---|
| [Instructions: Populated by `/design asset --add-variant [name]`. One row per variant; ✓ in Default for the default; description matches the variant's `When to use` section.] | | | |
