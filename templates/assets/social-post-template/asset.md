---
slug: social-post
status: active
last-reviewed: ""
content-keys:
  - body
  - cta_url
  - media_url
  - media_alt
  - hashtags
  - mentions
array-keys:
  - hashtags
  - mentions
publishing: ""
default-variant: ""
production-targets: []
---

# Social Post

[Instructions:
Short-form social post for any platform — LinkedIn, Twitter/X, Reddit, threads. Used for brand voice, thought leadership, campaign distribution, executive amplification. Default for the `social-post` content type in MESSAGE.md `## Assets`.

Common variants: linkedin, twitter-x-post, twitter-x-thread, reddit, threads-bsky.

This envelope carries only the company conventions that hold across every social-post variant — hashtag policy, link discipline, mention policy, image/alt conventions. Structure and CTA conventions live in each variant under `variants/` since each platform has its own form constraints (LinkedIn's "see more" truncation, Twitter's char limit, Reddit's title vs. body, thread sequencing).]

## Conventions

[Instructions:
Specify the company's social-wide standards that hold across variants:
- Hashtag cap (e.g., ≤3 — >3 reads like a 2015 marketing playbook)
- One link maximum per post; tracking-param convention
- Mention policy: reserved for relevant individuals; no mass-tag spam
- Image-alt rule: every `media_url` requires `media_alt` (accessibility + algorithmic boost)
- Quote-share rule: 1-2 sentences of original framing before the share
- Attribution policy when reposting customer or analyst content]

## Frontmatter requirements

[Instructions:
`mentions` is an array of platform-prefixed handle strings (e.g., LinkedIn `["company/axonius", "in/jdoe"]`; Twitter/X `["@axonius"]`; Reddit `["u/jdoe"]`). `media_url` supports a single image or video; for multi-image carousels or threads, extend the schema (`media_urls`, `thread_sequence`) per variant requirements. Document any publishing automation (Buffer, Hootsuite, native LinkedIn API, Twitter API).]

## Variants

Catalog of variants this asset supports. The `default-variant` frontmatter field marks the variant the writer uses when a brief's asset manifest doesn't specify one. Files live in `variants/[slug].md`.

| Variant | File | Default | Description |
|---|---|---|---|
| [Instructions: Populated by `/design asset --add-variant [name]`. One row per variant; ✓ in Default for the default; description matches the variant's `When to use` section.] | | | |
