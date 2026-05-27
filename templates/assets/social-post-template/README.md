# Social Post Template — Author Guidance

Calibrates `asset.md` for `social-post` to the company's social conventions and publishing paths across platforms (LinkedIn, Twitter/X, Reddit, Threads, Bluesky).

## Ownership rule

The asset envelope (`asset.md`) carries only the **company conventions** for social posts — hashtag policy, link discipline, mention policy, image-alt rule. Variants do the editorial heavy lifting per platform (Structure, CTA conventions, Voice notes, Examples).

| Lives in `asset.md` | Lives in `variants/[name].md` |
|---|---|
| Frontmatter (slug, content-keys, array-keys, publishing, default-variant) | When to use |
| Conventions (hashtag cap, one-link rule, mention policy, alt-text rule) | Voice notes (platform-native register) |
| Frontmatter requirements (platform-specific handle formats, media schema) | Structure (LinkedIn's "see more" truncation vs. Twitter's 280-char limit vs. Reddit's title-body split) |
| Variants table | CTA conventions (LinkedIn questions vs. Twitter no-CTA vs. Reddit's discussion-prompts) |
|  | Examples |

## Common variants

Typical variants for this asset: `linkedin`, `twitter-x-post`, `twitter-x-thread`, `reddit`, `threads-bsky`. Add via `/design asset social-post --add-variant [name]`.

## When this template is generated

- `/bootstrap` Phase 8 with "social-post" selected.
- `/design asset social-post` directly.
- `/design asset social-post --add-variant [name]` to add a platform-specific variant.

## What makes a good asset spec

- **Cross-platform invariants only in the envelope.** Hashtag cap, one-link rule, mention policy, alt-text — these hold across every platform. Platform-specific Structure and CTAs live in variants.
- **Hook discipline (variant-specific).** Line 1 of LinkedIn determines whether anyone reads past truncation; the opener tweet of a thread carries the whole argument. Variant guidance should enforce strong openings per platform.
- **One link maximum per post.** Multi-link posts dilute engagement on every platform. This stays at the envelope level.

## Common pitfalls

- Hashtag spam. >3 hashtags reads like a 2015 marketing playbook. Cap explicitly in Conventions.
- Generic CTAs ("Learn more"). Variant guidance should require specific asks.
- Mention spam. Mass mentions hurt reach on every platform. Reserve for relevant individuals.
- Treating LinkedIn voice as universal social voice. LinkedIn ≠ Twitter ≠ Reddit. Each gets its own variant with its own voice register.

## What stays in the template (do not delete during generation)

- The `slug`, `status`, `content-keys`, `array-keys`, `publishing`, and `default-variant` frontmatter fields.
- The three section headers: `## Conventions`, `## Frontmatter requirements`, `## Variants`.
- The `[Instructions: ...]` blocks.
- The `variants/` subdirectory and `variant-template.md` scaffold.
