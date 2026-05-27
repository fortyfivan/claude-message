---
slug: email
status: active
last-reviewed: ""
content-keys:
  - subject
  - preheader
  - body
  - cta_label
  - cta_url
  - sender_name
  - sender_title
  - segment
array-keys: []
publishing: ""
default-variant: ""
production-targets:
  - email
---

# Email

[Instructions:
Email asset — nurture sequences, cold outbound, promotional sends, lifecycle messages. Default for the `email` content type in MESSAGE.md `## Assets`.

Common variants: nurture, outbound, promo, lifecycle, transactional-companion.

This envelope carries only the company conventions that hold across every email variant — subject-line policy, sender identity, deliverability discipline, sequence-position-implicit rule. Structure and CTA conventions live in each variant under `variants/` since they vary significantly by editorial intent (an outbound email has earned no attention; a nurture email has; a promo email expects scanning over reading).]

## Conventions

[Instructions:
Specify the company's email-wide standards that hold across variants:
- Subject line policy (e.g., ≤8 words for nurture, ≤6 words for outbound, no sales clichés like "circling back" / "touching base" / "just following up")
- Preheader rule (extends subject; treats as second headline; never repeats subject)
- Plain-text vs. lightly-styled HTML default (avoid heavy graphics that hurt deliverability)
- Sender identity (named human vs. generic "team@"; signature conventions)
- Sequence-position-implicit rule (don't write "Email 3 of 5" in body)
- One asset reference per email (multiple links dilute conversion)
- Merge-token / personalization syntax for the sales engagement or marketing automation platform]

## Frontmatter requirements

[Instructions:
Document fields the marketing-automation or sales-engagement platform expects. Common patterns:
- Marketo / Pardot: `program`, `step_number`, `program_token`
- HubSpot: `workflow_id`, `subscription_type`
- Outreach / Salesloft / Apollo: liquid/handlebars merge tokens in `subject` and `body` strings; `cta_url` carries tracking params per platform
- `segment` is a routing hint; replace or remove based on the platform
- `sender_name`/`sender_title` may be platform-resolved (omit if so)]

## Variants

Catalog of variants this asset supports. The `default-variant` frontmatter field marks the variant the writer uses when a brief's asset manifest doesn't specify one. Files live in `variants/[slug].md`.

| Variant | File | Default | Description |
|---|---|---|---|
| [Instructions: Populated by `/design asset --add-variant [name]`. One row per variant; ✓ in Default for the default; description matches the variant's `When to use` section.] | | | |
