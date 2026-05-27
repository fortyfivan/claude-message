---
version: alpha
name: "[Company] Design System"
description: "Brand system for [Company]"

# [Instructions: Replace the placeholder palette with your brand colors.
# Primary = dominant brand color; secondary/tertiary = supporting; neutral = backgrounds.
# Use hex (#RRGGBB). The producer applies these as CSS custom properties (web) or
# inline style values (email/print).]
colors:
  primary: "#0A2540"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  background: "#FFFFFF"
  text: "#1A1A1A"

# [Instructions: Define your type scale. fontFamily lists primary then fallbacks.
# The producer loads woff2 files declared in assets.fonts via @font-face (web only);
# email production uses system fallbacks since web fonts don't load reliably in email clients.]
typography:
  headline-lg:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "48px"
    fontWeight: 600
    lineHeight: 1.1
  headline-md:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "32px"
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  caption:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.4

# [Instructions: Spacing scale in pixels. Used by the producer as CSS custom properties
# (--space-xs, --space-sm, etc.) and inline padding/margin values.]
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "32px"
  xl: "64px"

# [Instructions: Border-radius scale. `full` is for pills (avatars, fully-rounded buttons).]
rounded:
  sm: "4px"
  md: "8px"
  lg: "12px"
  full: "9999px"

# [Instructions: Components use {path.to.token} syntax to reference the tokens above.
# The producer resolves references at generation time. Add components your output
# actually uses; the producer falls back to defaults for unspecified components.]
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  button-secondary:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  card:
    backgroundColor: "{colors.background}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
    border: "1px solid {colors.neutral}"

# [Instructions: ASSETS EXTENSION — paths to brand asset files (relative to repo root).
# Spec-compliant parsers preserve this block per the Google Labs spec's unknown-content
# rules. The producer reads it to resolve logo paths, @font-face declarations, favicon
# links, and OG image references. Leave empty arrays/values until you drop the files in.]
assets:
  logos:
    primary: "brand/logos/primary.svg"
    icon: "brand/logos/icon.svg"
    wordmark: "brand/logos/wordmark.svg"
    inverted: "brand/logos/inverted.svg"
  fonts:
    primary-regular: "brand/fonts/primary-regular.woff2"
    primary-bold: "brand/fonts/primary-bold.woff2"
  images:
    favicon: "brand/images/favicon.ico"
    apple-touch-icon: "brand/images/apple-touch-icon.png"
    og-default: "brand/images/og-default.png"
---

## Overview

[Instructions: 2-4 sentences describing your design system's intent. What does the visual identity express? What posture (modern, classical, technical, warm)? What separates your brand visually from the category? This rationale informs the producer when ambiguous decisions arise.]

## Colors

[Instructions: Document how each color earns its place. Primary is the dominant brand color — used for CTAs, key accents, anchor surfaces. Secondary supports. Tertiary is accent-only (warnings, highlights). Neutral handles backgrounds and dividers.]

| Token | Use case |
|---|---|
| `colors.primary` | CTAs, primary buttons, headline accents, brand surfaces |
| `colors.secondary` | Supporting UI, secondary buttons, muted accents |
| `colors.tertiary` | Highlights, warnings, accent-only |
| `colors.neutral` | Backgrounds, card surfaces, dividers |
| `colors.background` | Page background |
| `colors.text` | Primary text color |

**Contrast:** Verify primary on background and text on background meet WCAG 2.1 AA (4.5:1 for body text, 3:1 for large text).

## Typography

[Instructions: Document your type scale's intent. Headline-lg for hero / cover; headline-md for section heads; body-md for body copy; body-sm for captions and metadata; caption for fine print. Note the fontFamily fallback chain — the producer's web target loads custom fonts via @font-face from assets.fonts; email and print fall back to the system fonts in the chain.]

| Level | Use case |
|---|---|
| `typography.headline-lg` | Hero headlines, document covers |
| `typography.headline-md` | Section headers, article titles |
| `typography.body-md` | Body copy, paragraphs |
| `typography.body-sm` | Captions, metadata, secondary text |
| `typography.caption` | Fine print, footnotes |

## Layout

[Instructions: Spacing system intent. The 4-8-16-32-64 progression doubles at each step — comfortable for human-readable rhythm. Use spacing tokens for padding, margin, gap. Avoid one-off pixel values that drift the system.]

**Grid:** [Instructions: 12-column for web layouts; single-column for email and print. Document any preferred max-width (e.g., 1200px for marketing pages, 600px for email body, 8.5in for letter-size print).]

## Elevation & Depth

[Instructions: Optional. Document shadow scale if your brand uses shadows. Many flat / minimalist brands skip this section entirely — the producer falls back to no-shadow when shadow tokens aren't defined.]

## Shapes

[Instructions: Border-radius conventions. `rounded.sm` for inputs, tags. `rounded.md` for buttons, cards. `rounded.lg` for hero surfaces. `rounded.full` for pills (avatars, badges).]

## Components

[Instructions: Patterns the producer composes into output. Document the intended use of each component above. Add custom components (badge, alert, etc.) as your output catalog grows.]

**Buttons:** `button-primary` for primary CTAs (Sign up, Get started, Schedule demo). `button-secondary` for supporting actions (Learn more, Cancel).

**Cards:** `card` wraps grouped content — feature blocks, testimonial quotes, pricing tiers.

## Assets

[Instructions: Document how each asset earns its place. Logo variants, font loading strategy, image conventions. The producer enforces these at generation time.]

### Logo usage

| Asset | Use case | Minimum size |
|---|---|---|
| `assets.logos.primary` | Default header use; horizontal layouts | ≥120px wide |
| `assets.logos.icon` | Square layouts (favicon, app icon) | ≥32px square |
| `assets.logos.wordmark` | When the icon would compete with other branding | ≥80px wide |
| `assets.logos.inverted` | Dark backgrounds only — never on light | ≥120px wide |

**Clearspace:** Reserve 0.5x logo height on all sides — no other graphic elements within that zone.

### Font loading

- **Web HTML:** producer emits `@font-face` declarations from `assets.fonts.*` with `font-display: swap` for performance. Preloads regular + bold weights.
- **Email HTML:** producer uses the system fallback chain in `fontFamily` (typically Inter → system-ui → -apple-system → BlinkMacSystemFont → sans-serif). Web fonts don't load reliably in email clients.
- **Print HTML:** producer uses web fonts if available (Chrome print-to-PDF embeds them); otherwise system fallbacks.

### Images

- **Favicon:** `assets.images.favicon` → `<link rel="icon">` in web output.
- **Apple touch icon:** `assets.images.apple-touch-icon` → `<link rel="apple-touch-icon">` for iOS bookmarks.
- **OG default:** `assets.images.og-default` → `<meta property="og:image">` fallback when an asset doesn't specify its own.

## Do's and Don'ts

[Instructions: Brand guardrails specific to visual identity. What to never do (e.g., "never stretch the logo," "never use brand colors at <60% opacity for text," "never combine more than two type weights in body copy"). These complement MESSAGE.md's `## Brand Guardrails` (which covers verbal identity).]

**Do:**
- Use design tokens — never hardcode colors, font sizes, or spacing values in producer output
- Reserve clearspace around the logo
- Verify color contrast meets WCAG 2.1 AA before publishing
- Use `headline-lg` for one hero element per page; avoid stacking multiple

**Don't:**
- Stretch, recolor, or rotate logos outside the declared variants
- Use brand primary at low opacity for body text (poor contrast)
- Mix typography from outside the declared scale
- Use external CDN-hosted fonts when self-hosted woff2 files are available
