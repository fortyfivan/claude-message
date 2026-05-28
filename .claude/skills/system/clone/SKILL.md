---
name: clone
description: Build the brand/ folder from a company URL — extract design tokens into brand/DESIGN.md and download SVG logos, woff2 fonts, and images. The automated cousin of /bootstrap, scoped to visual identity. Use when a user wants to set up brand/ from an existing website instead of authoring DESIGN.md by hand.
system-independent: true
---

# Clone Skill

Take a URL and populate `brand/` in one pass: fetch the site, extract design tokens, download accessible assets to a scratch area, present a proposed `brand/DESIGN.md` plus an asset manifest, and write to `brand/` only after the user approves. Clone is the automated cousin of `/bootstrap` — where bootstrap runs a multi-phase workshop to build the *messaging* house, clone does a mostly-automated first-pass extraction to build the *brand* folder.

Treat this as brand archaeology, not authorship. Extraction is heuristic: CSS rarely labels its colors by role, and the mapping of "which hue is the primary brand color" is a judgment call that the agent gets wrong often enough to always confirm. Propose and verify; never assert. The boundary is firm — clone builds visual identity only. Messaging stays with `/bootstrap` and the `/design` skills; clone never touches `messaging/` or `MESSAGE.md`.

## What clone produces

- `brand/DESIGN.md` — design tokens (colors, typography, spacing, radius, components) following the [Google Labs DESIGN.md spec](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md) (`version: alpha`) plus the repo's `assets:` extension.
- Downloaded files in `brand/logos/` (SVG only), `brand/fonts/` (woff2 only), and `brand/images/` (favicon, apple-touch-icon, OG image).

The output is consumed by the `producer` subagent (`.claude/agents/producer.md`) and validated by `scripts/validate.py` / `/run health`. Conformance is the bar to clear — see below.

## Brand System Reference

This skill operates against the brand system, not the messaging house — it is `system-independent` and loads no MESSAGE.md, pillars, or collections. The target spec:

- **Canonical shape:** `templates/DESIGN-template.md`. Populate its structure; strip the bracketed `[Instructions: ...]` blocks when writing real content (the same way bootstrap strips its disclaimer blocks).
- **Required frontmatter keys:** `version`, `name`, `colors`, `typography`. Missing any is a hard validation error.
- **Required body sections:** `## Overview`, `## Colors`, `## Typography`. Missing any is a hard validation error.
- **Resolvable references:** every `{path.to.token}` in `components` must resolve to a token that exists. An unresolved reference is a hard validation error.
- **Honest asset paths:** every `assets.*` path must point at a file that exists on disk, or the validator and the producer both warn.

The producer loads `brand/DESIGN.md` fresh on every dispatch and fails fast on non-conformance, so conformance is non-negotiable, not nice-to-have. Rationale and the assets-extension reference live in `docs/brand-system.md`.

The easiest way to keep `components` references resolvable is to retain the template's `button-primary` / `button-secondary` / `card` — they reference only tokens clone always emits (`colors.primary`, `colors.neutral`, `colors.background`, `rounded.md`, `spacing.md`, `spacing.lg`).

## Two phases

1. **Extract** — fetch the site, mine its CSS for tokens, detect and download assets to a scratch area, assemble a proposed DESIGN.md.
2. **Review & Commit** — present the proposal and the asset manifest, take corrections (the color-role mapping especially), then write `brand/DESIGN.md` and move the scratch assets into `brand/`.

The gate is between them: Phase 2 cannot write to `brand/` until the user approves. This is the single approval gate.

## Setup

Two checks before extraction:

**Capture the URL.** The URL is the one required input. If the user didn't supply one, ask for it. Normalize it — add `https://` if the scheme is missing.

**Detect existing brand content.** Check whether `brand/DESIGN.md` already exists and whether `brand/{logos,fonts,images}/` hold any non-`.gitkeep` files. If a DESIGN.md exists, do not silently overwrite it — surface it and offer, via AskUserQuestion:

- **Overwrite** — replace wholesale (best when the file is still the untouched template).
- **Merge** — keep hand-authored body sections and any `components` customizations; refresh only `colors`, `typography`, and `assets` from extraction (best when the file looks customized).
- **Abort** — stop and leave `brand/` untouched.

Default the recommendation to *merge* if the file looks customized, *overwrite* if it still matches the template.

## Phase 1: Extract

The heart of the skill. A heuristic procedure from URL to tokens + assets. Work in a scratch directory created with `mktemp -d` (a system temp dir, outside the repo — never write scratch into the tracked tree); move files into `brand/` only at commit.

### Step 1 — Fetch HTML and CSS

`curl -sL -A '<modern browser UA>' <url>` for the raw HTML. Use `-L` to follow redirects (apex → www, http → https) and a realistic User-Agent — many sites 403 the default curl agent. From the HTML, collect: external `<link rel="stylesheet">`, inline `<style>` blocks, `<link rel="icon">` / `apple-touch-icon`, `<meta property="og:image">`, `<meta name="theme-color">`, Google Fonts `<link>`/`@import`, header `<img>`, and inline `<svg>`. `curl` each external stylesheet (resolve relative hrefs against the *page* origin), and concatenate everything into one CSS corpus for token mining.

**Cap ingestion.** Don't slurp multi-MB framework bundles into context — `grep` them for the high-value patterns (`--color`, `@font-face`, `font-family`, `border-radius`) and sample rather than read whole.

**JS-heavy fallback.** If curl returns a near-empty SPA shell (a `<div id="root">` and a bundle script, no meaningful CSS), curl can't render it. Fall back to `WebFetch` on the URL for visible text and surfaced asset URLs, and try fetching obvious built CSS bundle URLs found in the HTML. Be explicit with the user that token confidence is lower, and lean harder on the review gate — never pass off low-confidence guesses as extracted facts.

**Gap-filling.** When the page is thin, or a vector logo / woff2 font isn't on the homepage, reach further: follow obvious `/brand`, `/press`, `/about`, or press-kit links on the site, and use `WebSearch` (e.g., `"<company> brand assets svg logo"`, `"<company> press kit"`) to locate higher-quality assets. Keep it bounded — this is asset hunting for one company, not open-ended research.

### Step 2 — Colors → six roles

Mine the CSS corpus for color signals, strongest first:

1. **CSS custom properties** — `--color-primary`, `--brand`, `--accent`, `--bg`, `--text`. The strongest signal, because the author named them; map by name where the name is semantically clear.
2. **`theme-color` meta** — often the truest brand primary.
3. **Raw hex / rgb / hsl values**, ranked by *prominence* over raw frequency: a color on the primary CTA, header background, or link outranks one used once in a footer border. Normalize all to hex; collapse near-identical shades (e.g., `#0A2540` ≈ `#0B2641`).

Then map to the six DESIGN.md roles (heuristic — confirm in Phase 2):

| Role | Heuristic |
|---|---|
| `primary` | Dominant brand / CTA / link color (highest-prominence non-neutral hue) |
| `secondary` | Next most-used supporting brand hue |
| `tertiary` | Sparse accent (warnings, highlights); if none, a tint/shade of primary — flag it |
| `neutral` | Dominant off-white / light-gray surface (cards, sections, dividers) |
| `background` | Page background (usually `#FFFFFF` or near-white from `body`) |
| `text` | Dominant body-text color (usually near-black from `body`/`p`) |

Note WCAG 2.1 AA contrast for `text` on `background` and `primary` on `background` (4.5:1 body, 3:1 large), as the template's `## Colors` section calls for.

### Step 3 — Typography → five tiers

Read `font-family` on `body` and `h1`–`h6` and the most-used text selectors; capture the full fallback chain as authored. Note `@font-face` rules (self-hosted) and Google Fonts references (hosted) for Step 4. The site won't expose exactly five tiers, so derive:

- `headline-lg` from the largest heading (hero / h1), `headline-md` from h2 / section heads.
- `body-md` from `body`/`p` (commonly 16px), `body-sm` one step down (~14px), `caption` smaller (~12px).
- `fontWeight` from the CSS weights (headings often 600–700, body 400); `lineHeight` from declared values, falling back to template ratios (1.1–1.2 headings, 1.5–1.6 body).

**Always emit a system fallback chain** in `fontFamily` even when a custom font is found — e.g., `"Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"`. Email and print production rely on it.

### Step 4 — Fonts (woff2 only)

From `@font-face src: url(...)` entries, prefer the `format("woff2")` URLs (resolve relative to the stylesheet origin). From Google Fonts `<link>`, fetch the Fonts CSS *with a browser UA* (Google serves woff2 to modern agents), then extract its woff2 `src` URLs. `curl` the regular (400) and bold (~700) faces of the primary family into scratch as `primary-regular.woff2` / `primary-bold.woff2`.

**Keep brand/ pure.** If only non-woff2 formats (woff / ttf / otf) are available, or the fonts are CDN-gated / return 403: do **not** commit them. Leave `assets.fonts` out, keep the system fallback chain in `fontFamily` so production still works, and list the font as a manual follow-up in the completion summary. A `.woff2` path pointing at a non-woff2 file would mislead the producer and the validator — don't.

### Step 5 — Logos (SVG only) and images

Detect, in rough priority: a header `<img>` whose `src`/`alt`/`class` contains "logo" or the brand name; an inline header/nav `<svg>` (capture the markup directly — it's already vector); `<link rel="icon">` and `apple-touch-icon`; `<meta property="og:image">`; any prominent `<img src="*.svg">`.

Map and download to scratch:

- **Logos (SVG):** main SVG → `assets.logos.primary`; square/mark-only SVG → `icon`; text-only SVG → `wordmark`; `inverted` only if a distinct dark-background SVG exists.
- **Keep brand/ pure:** raster-only logos (PNG/JPG, no SVG) are **not** committed to `brand/logos/`. List them as manual follow-ups — gap-filling search (Step 1) may still turn up an SVG.
- **Images** are raster by nature, so they *are* committed: favicon → `brand/images/favicon.{ico,png}` (match the real extension and point `assets.images.favicon` at it), apple-touch-icon → `brand/images/apple-touch-icon.png`, OG image → `brand/images/og-default.png`. The keep-pure rule applies to logos and fonts, not the images block.

### Step 6 — Assemble the proposed DESIGN.md

Populate the `templates/DESIGN-template.md` structure in the scratch area:

- **Frontmatter:** `version: alpha`; `name: "<Company> Design System"`; the six `colors`; the five `typography` tiers; `spacing` and `rounded` extracted from CSS (`--space-*`, `border-radius` values) or template defaults; the template's `components` (kept, so references stay resolvable); and `assets` populated **only with paths for files that were actually downloaded and verified** (omit the rest).
- **Body:** `## Overview` (2–4 sentences inferred from the site's visual posture), the `## Colors` and `## Typography` tables (required), and the remaining template sections (`## Layout`, `## Shapes`, `## Components`, `## Assets`, `## Do's and Don'ts`) filled from extraction or sensible defaults. Strip every `[Instructions: ...]` block.

Verify each downloaded file before listing it in `assets.*`: `file <path>` reports the expected type, size is non-zero, and the content isn't an HTML error page saved under a binary extension.

## Phase 2: Review & Commit

Single gate. Download to scratch first, commit on approval.

1. **Present the proposal:** the full proposed `brand/DESIGN.md`, and an asset manifest table — for each asset: source URL · target path · file type/size · status (downloaded / failed / skipped + why). Surface the heuristic **color-role mapping** prominently, since it's the most error-prone part.
2. **Take corrections** via AskUserQuestion — chiefly the color-role assignments (swap primary ↔ secondary, fix tertiary), plus "that's the wrong logo" rejections. Re-render the proposed DESIGN.md after corrections.
3. **Commit on approval:** write `brand/DESIGN.md` (via the chosen overwrite/merge path), then `mv` the verified scratch assets into `brand/logos|fonts|images/`. Moving (not re-downloading) means the only post-approval action is a local file move, which can't fail in surprising ways — so the user approves against what truly downloaded, not against optimism.
4. **Clean up** the scratch temp dir.

## Graceful degradation

The rule across every step: the emitted DESIGN.md must be valid, and the producer must never be misled. Concretely —

- Always emit the four required frontmatter keys and three required body sections (hard errors otherwise).
- Keep `components` references resolvable (hard error otherwise) — retaining the template components is the safe path.
- Point `assets.*` only at files that landed and verified on disk (warn-level noise + producer warnings otherwise).
- Always keep system-font fallback chains in `typography.*.fontFamily`.
- Summarize every gap to the user at completion — "no woff2 fonts found, using system fallbacks"; "logo is raster-only, no SVG committed"; "tertiary color guessed as a tint of primary."

## Completion

After writing:

**Self-check the written file.** Confirm the four required frontmatter keys and three required body sections are present, every `components` reference resolves, and every `assets.*` path points at a file now on disk.

**Summarize gaps and next steps.** List what was extracted vs. guessed vs. missing (raster-only logos, missing woff2, guessed tertiary). Recommend:

```
Recommended next steps:
  - Run /run health (or python scripts/validate.py) to validate DESIGN.md conformance
  - Test with /produce <some output asset> --target web to confirm the producer accepts it
  - Manual follow-ups: <e.g., source an SVG logo; convert the brand font to woff2>
```

**Journal entry.** Append to `output/journal.md` for parity with bootstrap — Source: Clone — initial brand build; Type: process; Learning: what was extracted with confidence vs. guessed vs. unavailable; Action: brand/ populated from `<url>`.

**License note.** Close with a one-line caution: downloaded logos, fonts, and images belong to the site's owner — confirm you have the right to use them (relevant when cloning a competitor's site rather than your own).

## Reference

### Handling ambiguity

- **Heuristic uncertain.** Propose a working value, flag it provisional, and confirm at the review gate. The color-role mapping is never written unconfirmed.
- **Asset unavailable.** Degrade gracefully (system fonts, no logo reference) and record the gap; never fabricate a path.
- **Site unreadable** (full 403 / anti-bot wall, no extractable CSS). Try the WebFetch and gap-filling fallbacks; if still blank, emit a valid template-defaults DESIGN.md and tell the user plainly that the site couldn't be read.

### Fetch budget

Clone is naturally bounded — one site, its stylesheets, and its assets. Gap-filling adds a few targeted searches/fetches when the page is thin; it is not open-ended research. Stop once the brand folder can be populated.

## Tool scoping

- **Read** — `templates/DESIGN-template.md`, `brand/`, `docs/brand-system.md`
- **Write** — `brand/DESIGN.md` and asset files under `brand/`; never `messaging/` or `MESSAGE.md`
- **Edit** — `brand/DESIGN.md` (the merge path against an existing file)
- **Glob, Grep** — `brand/` (existing-asset detection)
- **Bash** — `curl` (fetch HTML/CSS, download assets), `mktemp -d` (scratch), read-only file ops (`ls`, `file`), `mv`/`rm` within scratch and into `brand/`; no package installs
- **WebFetch** — page text and asset discovery on JS-heavy pages
- **WebSearch** — gap-filling: brand/press-kit pages and higher-quality logo/font assets when the homepage is thin
- **AskUserQuestion** — URL capture (if absent), color-role confirmation, overwrite/merge/abort choice, gap resolution
- **No Agent dispatch** — clone runs in the main session (the researcher subagent can't write to `brand/`, and a dedicated subagent wouldn't earn its keep)
