# Email Template — Author Guidance

Calibrates `asset.md` for `email` to the company's marketing-automation or sales-engagement platform and broader email conventions.

## Ownership rule

The asset envelope (`asset.md`) carries only the **company conventions** for email — subject-line policy, sender identity, deliverability discipline, sequence-position-implicit rule. Variants do the editorial heavy lifting per intent (Structure, CTA conventions, Voice notes, Examples).

| Lives in `asset.md` | Lives in `variants/[name].md` |
|---|---|
| Frontmatter (slug, content-keys, array-keys, publishing, default-variant) | When to use |
| Conventions (subject policy, plain-text default, sender identity, sequence-position rule, one-asset-reference rule) | Voice notes (nurture's earned-attention vs. outbound's cold-hook) |
| Frontmatter requirements (MA/SEP platform fields, merge tokens) | Structure (nurture vs. outbound vs. promo have very different shapes) |
| Variants table | CTA conventions (calendar-link policy by touch / funnel stage; question-form vs. imperative) |
|  | Examples |

## Common variants

Typical variants for this asset: `nurture`, `outbound`, `promo`, `lifecycle`, `transactional-companion`. Add via `/design asset email --add-variant [name]`.

## When this template is generated

- `/bootstrap` Phase 8 with "email" selected.
- `/design asset email` directly.
- `/design asset email --add-variant [name]` to add a variant.

## What makes a good asset spec

- **Cross-variant invariants only in the envelope.** Subject-line policy, plain-text default, sequence-position-implicit, one-asset-reference — these hold across every email type. Per-intent Structure and CTAs live in variants.
- **Subject discipline.** No clichés — "circling back," "touching base," "just following up." Enforce in Conventions; specific banned phrases give the writer a clear gate.
- **Personalization depth tied to data.** Outbound requires role + trigger event; nurture references the recipient's last action. Document the depth policy in Conventions; specific personalization patterns live in variants.

## Common pitfalls

- Treating outbound like nurture. Different relationship; different voice. Variant guidance should make the distinction sharp.
- Calendar links on first-touch outbound. Burns reply rate. Variant guidance should reserve for touch 2+.
- Heavy HTML graphics. Hurts deliverability. Default plain-text or lightly styled in Conventions; per-variant exceptions (promo) live in the variant file.
- Forgetting merge tokens. Document the platform's token syntax in Frontmatter requirements so writers don't hard-code names.
- Conflating promo with nurture. Promo is time-bound and offer-led; nurture is sequence-aware and education-led. Separate variants.

## What stays in the template (do not delete during generation)

- The `slug`, `status`, `content-keys`, `array-keys`, `publishing`, and `default-variant` frontmatter fields.
- The three section headers: `## Conventions`, `## Frontmatter requirements`, `## Variants`.
- The `[Instructions: ...]` blocks.
- The `variants/` subdirectory and `variant-template.md` scaffold.
