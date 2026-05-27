---
name: produce-print
description: Print-ready HTML production from writer output and brand/DESIGN.md tokens. Generates HTML with @page CSS rules, page break controls, and print-specific typography for browser print-to-PDF or direct print delivery.
---

The print target produces HTML designed for browser print-to-PDF (Chrome's print engine is best for PDF generation) or direct print delivery. No JavaScript, no interactive elements. Uses CSS Paged Media (`@page` rules), page break controls, and fixed dimensions for predictable pagination.

## Output shape

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[from asset_metadata.title]</title>
  <style>
    @page {
      size: Letter;
      margin: 0.75in;
      @top-center { content: "[asset_metadata.title]"; }
      @bottom-right { content: counter(page) " / " counter(pages); }
    }
    @page :first {
      @top-center { content: ""; }
    }
    body { /* tokens applied */ }
    .cover { page-break-after: always; }
    h1, h2 { page-break-after: avoid; }
    table, figure { page-break-inside: avoid; }
  </style>
</head>
<body>
  <section class="cover">
    <!-- title, subtitle, author, date, brand mark -->
  </section>
  <main>
    <!-- body content from writer .md -->
  </main>
</body>
</html>
```

Open in Chrome → File → Print → Save as PDF. Print preview is the source of truth — what you see in preview is what the PDF holds.

## DESIGN.md token application

Tokens in a `<style>` block with print-specific overrides:

```css
:root {
  --color-primary: [colors.primary];
  --color-text: [colors.text];
  --space-md: [spacing.md];
}

body {
  font-family: [typography.body-md.fontFamily];
  font-size: 12pt; /* points, not pixels — print-native unit */
  line-height: [typography.body-md.lineHeight];
  color: var(--color-text);
}

h1 { font-size: 28pt; }
h2 { font-size: 20pt; }
h3 { font-size: 14pt; }
```

Convert px → pt at generation: divide pixel value by 1.33 (96dpi → 72pt). The producer handles this automatically per the typography tokens. Spacing tokens stay in pixels (CSS resolves to inches/points at print time per `@page` margin context).

## Page setup

```css
@page {
  size: Letter;          /* or A4 — based on assets.publishing region */
  margin: 0.75in;         /* default; tighten to 0.5in for dense layouts */
  marks: none;            /* no crop marks for office printing */
}

@page :first {            /* cover page — no header */
  @top-center { content: ""; }
}

@page :left {             /* even pages — outer margin on left */
  margin-left: 1in;
  margin-right: 0.75in;
}

@page :right {            /* odd pages — outer margin on right */
  margin-left: 0.75in;
  margin-right: 1in;
}
```

Standard sizes: `Letter` (8.5×11 in, US), `A4` (210×297 mm, international), `Legal` (8.5×14 in, US legal). Default to `Letter` unless `asset_metadata.publishing` declares otherwise.

## Page breaks

```css
.cover { page-break-after: always; }       /* cover ends on its own page */

h1, h2 { page-break-after: avoid; }        /* don't orphan a heading at page bottom */
h1, h2, h3 { page-break-before: auto; }    /* allow break before, but don't force */

table, figure, blockquote {
  page-break-inside: avoid;                 /* keep these intact when possible */
}

img { page-break-inside: avoid; max-width: 100%; }
```

Avoid `page-break-before: always` except for true section starts (chapter headings, cover, back matter). Forcing breaks creates short pages.

## Typography

| Element | Size | Notes |
|---|---|---|
| Body | 12pt | `body-md.lineHeight` from tokens |
| H1 | 28pt | `headline-lg` scaled to print |
| H2 | 20pt | `headline-md` scaled to print |
| H3 | 14pt | Subsection headings |
| Caption | 9pt | `caption` scaled |

Line-height stays relative (e.g., `1.5`) — points × ratio gives the spacing. For body copy in print, 1.4–1.6 line-height is the readable range.

Serif fallbacks for body if the brand allows — serif typefaces read better at length on paper than sans-serif. Don't default-switch the brand font, but support a `print-body-font` token override if the brand authors one.

## Color handling

```css
body {
  -webkit-print-color-adjust: exact;    /* Chrome — preserve background colors */
  print-color-adjust: exact;             /* Standard — preserve background colors */
}
```

Without these, Chrome strips background colors during PDF generation. With them, the PDF matches screen colors.

Verify contrast remains AA in grayscale — if recipients print to monochrome, low-contrast color pairs become unreadable. The producer surfaces a warning when token combinations risk grayscale failure.

## Images

- **Embed as base64** when the producer has direct file access — eliminates external dependencies in the rendered PDF.
- **Or use absolute paths** when the print is happening from a server-rendered HTML page with hosted images.
- **Resolution ≥ 300dpi equivalent.** A 4×6in image renders at 1200×1800px minimum. Smaller images pixelate in print.
- **Vector when possible.** SVGs scale losslessly. Use SVG for logos, icons, illustrations — `assets.logos.*` are SVG-first.

## Headers & footers

CSS Paged Media `@top-*` and `@bottom-*` regions:

```css
@page {
  @top-left { content: "[asset_metadata.title]"; font-size: 9pt; color: [colors.secondary]; }
  @top-right { content: "[publication date]"; font-size: 9pt; color: [colors.secondary]; }
  @bottom-center { content: counter(page) " of " counter(pages); font-size: 9pt; }
}
```

Running heads automate across pages. The `:first` pseudo-selector suppresses the header on the cover page. Page counters (`counter(page)`, `counter(pages)`) work in Chrome's print engine.

## Pitfalls

- **No flexbox/grid for primary layout.** CSS Paged Media support for modern layout primitives is weak. Use block layout, floats (sparingly), and tables for tabular data. Save grid for screen-only content.
- **Test in Chrome print preview.** It's the best PDF generator. Firefox, Safari, and Edge produce reasonable but inconsistent output. Chrome is the baseline.
- **`@page` rules don't cascade like normal CSS.** Be explicit about every pseudo (`:first`, `:left`, `:right`) when you need them.
- **No JavaScript.** Print is one-shot; interactive elements have no meaning in PDF/paper.
- **Avoid web fonts in print** unless you've verified Chrome embeds them in the PDF. Many web font hosting setups don't allow PDF embedding due to licensing; system fallbacks are safer.
- **Long URLs break layouts.** Use `word-break: break-all` on `<a>` text or shorten with footnote-style references in body copy.
- **Image color profiles.** Embed sRGB; CMYK images need explicit handling for professional print (out of scope for this skill — flag with a warning).
