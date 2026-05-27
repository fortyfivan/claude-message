---
name: produce-web
description: Web HTML production from writer output and brand/DESIGN.md tokens. Generates standards-compliant HTML5 with embedded CSS, semantic markup, and responsive design.
---

The web target produces standards-compliant HTML5 for publication via CMS or direct hosting. Design tokens become CSS custom properties; the markup uses semantic elements; responsive design is mobile-first.

## Output shape

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>[from asset_metadata.title]</title>
  <meta name="description" content="[from asset_metadata.excerpt]">
  <link rel="icon" href="[from assets.images.favicon]">
  <!-- OG tags, Twitter Card, font preloads -->
  <style>
    :root { /* design tokens as custom properties */ }
    @font-face { /* from assets.fonts */ }
    /* component classes */
  </style>
</head>
<body>
  <header>...</header>
  <main>
    <article>
      <!-- body content from writer .md -->
    </article>
  </main>
  <footer>...</footer>
</body>
</html>
```

Single file, no external CSS or JavaScript dependencies, no build step required.

## DESIGN.md token application

| Spec section | CSS application |
|---|---|
| `colors.*` | CSS custom properties (`--color-primary`, `--color-text`) + utility classes (`.text-primary`, `.bg-neutral`) |
| `typography.*` | CSS classes (`.headline-lg`, `.body-md`) with `font-family`, `font-size`, `font-weight`, `line-height`; `@font-face` declarations from `assets.fonts` |
| `spacing.*` | CSS custom properties (`--space-xs` through `--space-xl`) |
| `rounded.*` | CSS custom properties (`--rounded-sm` through `--rounded-full`) |
| `components.*` | CSS classes (`.button-primary`, `.card`) with `{path.to.token}` references resolved to literal values |

Apply tokens as both custom properties (for cascade-aware overrides) AND utility classes (for direct application in markup). The producer emits both — markup uses the class; the class definition uses the custom property.

## Web fonts

For every entry in `assets.fonts.*`:

```css
@font-face {
  font-family: '[primary-regular]';
  src: url('[brand/fonts/primary-regular.woff2]') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

Preload critical fonts (regular + bold) in `<head>`:

```html
<link rel="preload" href="[brand/fonts/primary-regular.woff2]" as="font" type="font/woff2" crossorigin>
```

`font-display: swap` ensures text renders immediately with the fallback while the custom font loads. Fallback chain comes from the typography token's `fontFamily` value.

## Accessibility

Target: WCAG 2.1 AA.

- **Semantic markup.** Use `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>` per content role. One `<h1>` per page (the title); `<h2>` for sections; `<h3>` for subsections. Don't skip heading levels.
- **Alt text.** Every `<img>` has descriptive `alt`. Decorative images use `alt=""` (empty, not omitted).
- **Focus styles.** Interactive elements (links, buttons) carry visible focus outlines. Don't suppress with `outline: none` without a replacement.
- **Color contrast.** Verify body text on background meets 4.5:1; large text and UI components meet 3:1. The producer surfaces a warning when a token combination falls below threshold.
- **ARIA.** Use sparingly — semantic HTML covers most cases. Add `aria-label` for icon-only buttons; `aria-current` for active navigation.

## Meta tags

```html
<title>[asset_metadata.title]</title>
<meta name="description" content="[asset_metadata.excerpt]">

<!-- Open Graph -->
<meta property="og:title" content="[asset_metadata.title]">
<meta property="og:description" content="[asset_metadata.excerpt]">
<meta property="og:image" content="[from .json: og_image, OR assets.images.og-default]">
<meta property="og:type" content="article">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[asset_metadata.title]">
<meta name="twitter:description" content="[asset_metadata.excerpt]">
<meta name="twitter:image" content="[from .json: og_image, OR assets.images.og-default]">

<!-- Favicon -->
<link rel="icon" href="[assets.images.favicon]">
<link rel="apple-touch-icon" href="[assets.images.apple-touch-icon]">
```

When the writer `.json` includes asset-specific OG fields (e.g., custom hero image), those override `assets.images.og-default`.

## Responsive design

Mobile-first breakpoints:

| Breakpoint | Width | Use case |
|---|---|---|
| Mobile | `<768px` | Default styles (no media query) |
| Tablet | `768px–1024px` | `@media (min-width: 768px)` |
| Desktop | `>1024px` | `@media (min-width: 1024px)` |

Use CSS Grid for page-level layout (`grid-template-columns`, `gap` with `--space-*` tokens); Flexbox for component internals (header nav, button rows). Avoid float-based layouts.

Container width: max 1200px for marketing content; max 720px for long-form reading.

## Pitfalls

- **No external CSS frameworks.** Tailwind, Bootstrap, etc. introduce runtime dependencies and override design tokens. Embed all CSS in `<style>`.
- **No JavaScript.** Producer emits static HTML. Interactive features come from CMS/downstream integration, not producer output.
- **Image paths.** Use absolute URLs or repo-relative paths only. Never use `file://` paths or paths assuming a specific working directory.
- **Token resolution.** Verify every `{path.to.token}` resolves before output. Unresolved references in CSS render as literal text and break visual fidelity silently.
- **Font loading races.** Preload critical fonts; use `font-display: swap` for body fonts. Don't preload every weight — bandwidth waste.
- **Inline style attributes.** Avoid in `<body>` markup. Apply via component classes for maintainability; the producer can update one class definition vs. every inline occurrence.
