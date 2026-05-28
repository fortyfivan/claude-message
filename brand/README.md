# brand/

Visual identity foundation for `claude-message`. Parallel to `messaging/`: where the messaging house holds verbal identity, `brand/` holds visual identity.

## Contents

| Path | Holds |
|---|---|
| `DESIGN.md` | Canonical brand spec — design tokens (colors, typography, spacing, components) per the [Google Labs DESIGN.md spec](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md), plus an `assets:` extension for file references. |
| `logos/` | Wordmark + icon SVGs (primary, icon-only, wordmark-only, inverted). |
| `fonts/` | Web fonts (`.woff2`) for web HTML production. Email production uses system fallbacks. |
| `images/` | Favicon, Apple touch icon, OG default image. |
| `components/` | Optional HTML component snippets the producer can compose into. |

## Setup

**Fast path:** run `/clone <your-website-url>` to auto-populate `brand/DESIGN.md` and download logo/font/image assets from your site, then review before it commits. Or set up manually:

The repo ships with `brand/` empty. To enable HTML production:

1. Copy `templates/DESIGN-template.md` → `brand/DESIGN.md`.
2. Customize the design tokens (colors, typography, spacing, components) per the bracketed `[Instructions: ...]` blocks.
3. Drop logo SVGs into `brand/logos/` and woff2 fonts into `brand/fonts/`.
4. Populate the `assets:` frontmatter block in DESIGN.md with the file paths.

See [`docs/brand-system.md`](../docs/brand-system.md) for the full setup walkthrough and Assets extension reference.

## Producer requirements

The producer subagent (`/produce`, or auto-dispatched by build workflows for assets with `production:` declared) refuses to operate without a conformant DESIGN.md. CI validates spec conformance, asset file resolution, and token references; failures surface during `/run health` and `scripts/validate.py`.
