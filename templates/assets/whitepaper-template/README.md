# Whitepaper Template — Author Guidance

Calibrates `asset.md` for `whitepaper` to the company's research / point-of-view / topic-paper conventions, gating strategy, and publishing pipeline. Covers any long-form analytical asset that earns authority through depth — research studies, topic deep-dives, market benchmarks, point-of-view papers, analyst-style briefs, technical or regulatory guides.

## Ownership rule

The asset envelope (`asset.md`) carries only the **company conventions** for whitepapers — citation discipline, attribution requirements, methodology rule, gating model. Variants do the editorial heavy lifting (Structure, CTA conventions, Voice notes, Examples).

| Lives in `asset.md` | Lives in `variants/[name].md` |
|---|---|
| Frontmatter (slug, content-keys, array-keys, publishing, default-variant) | When to use |
| Conventions (citation style, attribution rule, length bands, methodology requirement) | Voice notes (research's detached voice vs. point-of-view's opinionated voice) |
| Frontmatter requirements (CMS field details, gating fields) | Structure (research opens with methodology; topic opens with thesis; benchmark opens with data) |
| Variants table | CTA conventions (gated download, author briefing, related papers, peer-network call) |
|  | Examples |

## Common variants

Typical variants for this asset: `research`, `topic`, `benchmark`, `point-of-view`, `analyst-brief`, `technical-guide`, `regulatory`. Add via `/design asset whitepaper --add-variant [name]`. Research variants typically add `survey_n` / `survey_date` to frontmatter; benchmarks add `peer_set`.

## When this template is generated

- `/bootstrap` Phase 8 with "whitepaper" selected.
- `/design asset whitepaper` directly.
- `/design asset whitepaper --add-variant [name]` to add a variant.

## What makes a good asset spec

- **Methodology transparency** (research variant). Research papers carry authority only if methodology is documented. The convention should require it for any variant that claims primary data.
- **Citation discipline.** Every stat carries a source on the same page. No orphan numbers. Holds across every variant.
- **Gating intentional.** Gated papers convert; ungated papers earn authority. Document the company's choice — and which variants override the default (e.g., benchmark might be ungated; research might be gated).

## Common pitfalls

- Quantitative claims without sources. Convention should reject this on review.
- Marketing fluff in the executive summary. Variants own this — but most variants frame ES as facts + implications, not narrative.
- Forgetting the author bio. Whitepapers carry author credibility; the bio belongs in the asset's content-keys.
- Conflating research with point-of-view. Research is detached and data-led; point-of-view is opinionated and argument-led. Variants make the distinction; the envelope shouldn't collapse them.
- Putting variant-specific structure in asset.md. Research vs. analyst-brief vs. point-of-view open very differently — Structure lives in variants/.

## What stays in the template (do not delete during generation)

- The `slug`, `status`, `content-keys`, `array-keys`, `publishing`, and `default-variant` frontmatter fields.
- The three section headers: `## Conventions`, `## Frontmatter requirements`, `## Variants`.
- The `[Instructions: ...]` blocks.
- The `variants/` subdirectory and `variant-template.md` scaffold.
