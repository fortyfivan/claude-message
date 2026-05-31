# Brand system

`claude-message` separates verbal identity (messaging) from visual identity (brand). Each lives in its own foundation directory at the repo root:

| Foundation | Directory | Always-on file | Loaded by |
|---|---|---|---|
| Verbal | `messaging/` | `MESSAGE.md` | Main session (orchestrator, every skill) |
| Visual | `brand/` | `brand/DESIGN.md` | Producer subagent only, at dispatch time |

The producer never loads `MESSAGE.md`; the orchestrator never loads `brand/DESIGN.md`. Context stays in the surface that needs it.

## Why a separate foundation

Three pressures shaped the design:

1. **Brand application should be canonical.** Without a single source of truth for "this is how we look," brand tokens get baked into individual CMS templates, individual email service configurations, individual print layouts. Updates to brand identity require touching every endpoint. A canonical DESIGN.md eliminates that fragmentation.
2. **Writer output isn't immediately usable.** The writer produces `.md` + `.json` — downstream consumers each handle HTML conversion their own way. Centralizing production in a subagent removes that ad-hoc step.
3. **Context economics.** Brand assets (woff2 fonts can be hundreds of KB each) and target-specific patterns (email HTML conventions, print CSS rules) shouldn't accumulate in the orchestrator's context. Isolating in a subagent with its own foundation keeps the orchestrator lean.

## Spec conformance

DESIGN.md follows the [Google Labs DESIGN.md format specification](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md). The spec defines:

- **YAML frontmatter** for machine-readable design tokens (`colors`, `typography`, `spacing`, `rounded`, `components`)
- **Markdown body sections** for human-readable design rationale (`## Overview`, `## Colors`, `## Typography`, `## Layout`, `## Elevation & Depth`, `## Shapes`, `## Components`, `## Do's and Don'ts`)
- **Token reference syntax** `{path.to.token}` for cross-referencing values within frontmatter
- **Section order convention** and **unknown-content preservation rules**

By conforming to the spec, our DESIGN.md is consumable by any spec-compliant tooling — Figma variable importers, Tailwind theme generators, design-system documentation tools. Conversely, a DESIGN.md authored against the spec by another company can be consumed by our producer, modulo the Assets extension below.

## The Assets extension

The Google Labs spec doesn't address brand asset file references — logos, fonts, favicons, OG images. We extend the spec with two additions:

1. **`assets:` block in frontmatter** — paths to logo SVGs, woff2 fonts, image files (relative to repo root):

    ```yaml
    assets:
      logos:
        primary: "brand/logos/primary.svg"
        icon: "brand/logos/icon.svg"
      fonts:
        primary-regular: "brand/fonts/primary-regular.woff2"
        primary-bold: "brand/fonts/primary-bold.woff2"
      images:
        favicon: "brand/images/favicon.ico"
        og-default: "brand/images/og-default.png"
    ```

2. **`## Assets` markdown section** — human-readable usage rationale (logo minimum sizes, clearspace, font-loading strategy by target).

Per the spec's unknown-content preservation rules, spec-compliant parsers leave the `assets:` key intact. Our producer reads it to resolve file paths during HTML generation.

## Setup

The repo ships with `brand/` empty (matching the empty-after-clone discipline of `messaging/`). To enable HTML production:

1. **Copy the template:**

    ```bash
    cp templates/DESIGN-template.md brand/DESIGN.md
    ```

2. **Customize the tokens.** Open `brand/DESIGN.md` and replace bracketed `[Instructions: ...]` blocks with your brand values — colors, type scale, spacing, components.

3. **Drop in asset files.** Place logo SVGs in `brand/logos/`, woff2 fonts in `brand/fonts/`, favicon + OG image in `brand/images/`.

4. **Populate the `assets:` frontmatter.** Reference the files you dropped in. Leave entries empty (or omit them) if you don't have a particular asset yet — the producer falls back gracefully (system fonts when web fonts absent, no favicon link when favicon absent).

5. **Verify with CI:**

    ```bash
    python scripts/validate.py
    ```

    CI checks: DESIGN.md spec conformance, asset file resolution, token reference resolution. Failures surface specific spec violations.

## Producer behavior

The producer subagent (`.claude/agents/producer.md`):

- Loads `brand/DESIGN.md` fresh on every dispatch (it's the always-on foundation for the producer's context, parallel to MESSAGE.md for the main session).
- Resolves the target (`web`, `email`, or `print`) → loads the corresponding production task skill at `.claude/skills/tasks/produce-{target}/SKILL.md`.
- Reads writer output (`.md` body + `.json` structured fields).
- Generates HTML applying DESIGN.md tokens per the task skill's conventions.
- Writes HTML to a destination co-located with the writer output.

Producer is invoked:

- **Automatically** by builders (`/build campaign`, `/build launch`, `/build play`) for assets that declare a `production:` field in the brief.
- **Manually** via `/produce path/to/asset.md --target web` for one-off generation or regeneration after brand-token changes.

## Tooling interoperability

By conforming to the Google Labs spec, DESIGN.md becomes consumable by:

- Spec-compliant DESIGN.md parsers (any tool built against the format)
- Figma variable importers (the spec is designed for easy conversion)
- Tailwind theme generators (token format maps cleanly)
- Design system documentation tools

This is intentional — the brand foundation is not locked into claude-message's runtime; it's a portable artifact.

## Custom production targets

Web, email, and print are the standard targets. To add a custom target (PDF, slide deck HTML, OG image generation, mobile app wrapper), create a new task skill:

```
.claude/skills/tasks/produce-pdf/SKILL.md
```

The skill describes how to apply DESIGN.md tokens to the new target's syntax. The producer dispatches to whichever target a brief declares or `/produce --target` specifies — adding a custom target is the same pattern as adding any task skill.

## Spec version

We pin to the Google Labs DESIGN.md spec as of its `alpha` version. The spec is at https://github.com/google-labs-code/design.md/blob/main/docs/spec.md — periodic review (annual) keeps our template aligned with upstream changes.
