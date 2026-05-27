# Landing Page Template — Author Guidance

Calibrates `asset.md` for `landing-page` to the company's CMS, conversion architecture, and brand standards. Covers every conversion-page surface — campaign destinations, product pages, gated assets, webinar registrations, event pages, partner co-marketing pages. The cross-page invariants (one-goal rule, word count caps, form integration) live in the envelope; variant-specific structure (webinar speakers + agenda; gated-asset form field count; product-page feature grid) lives in variants.

## Ownership rule

The asset envelope (`asset.md`) carries only the **company conventions** for landing pages — one-goal rule, word count caps, hero headline derivation, CMS section structure. Variants do the editorial heavy lifting (Structure, CTA conventions, Voice notes, Examples).

| Lives in `asset.md` | Lives in `variants/[name].md` |
|---|---|
| Frontmatter (slug, content-keys, array-keys, publishing, default-variant) | When to use |
| Conventions (one-goal rule, word count caps, lead-with stance, hero derivation) | Voice notes |
| Frontmatter requirements (CMS field details, form integration) | Structure (section sequence — campaign destination vs. product page differ) |
| Variants table | CTA conventions (form vs. calendar vs. external link; placement) |
|  | Examples |

## Common variants

Typical variants for this asset: `campaign-destination`, `product-page`, `gated-asset`, `webinar`, `event`, `partner-co-marketing`. Webinar/event variants typically add `event_date`, `event_time`, `speakers`, `agenda` to frontmatter; gated-asset adds `asset_download_url` + `gated_form_id`. Add via `/design asset landing-page --add-variant [name]`.

## When this template is generated

- `/bootstrap` Phase 8 with "landing-page" selected.
- `/design asset landing-page` directly.
- `/design asset landing-page --add-variant [name]` to add a variant.

## What makes a good asset spec

- **Single goal discipline.** The asset envelope should reinforce one CTA per page. If the company has high-converting pages with two CTAs, document the exception explicitly.
- **Form integration.** If gated pages route through Marketo/Pardot/HubSpot Forms, the envelope should include the form-id field name the CMS expects.
- **Section structure as an array.** Most modern CMSs render landing pages as section arrays. The `sections` content-key carries this; specify the block schema the CMS accepts.

## Common pitfalls

- Allowing multiple primary CTAs. Erodes conversion. The convention should make this difficult.
- Omitting `og_image_url`. Landing pages get shared on social; missing OG images hurt CTR.
- Conflating landing page with product page. They have different Structure and CTA conventions — handle as separate variants (or separate assets if scope diverges further).

## What stays in the template

- All standard frontmatter fields.
- The three section headers: `## Conventions`, `## Frontmatter requirements`, `## Variants`.
- `[Instructions: ...]` blocks (replaced on generation).
- The `variants/` subdirectory and `variant-template.md` scaffold.
