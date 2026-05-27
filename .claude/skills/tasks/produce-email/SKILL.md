---
name: produce-email
description: Email-safe HTML production from writer output and brand/DESIGN.md tokens. Generates table-based HTML with inline CSS for compatibility across email clients (Gmail, Outlook, Apple Mail, Yahoo).
---

The email target produces HTML for delivery via email service providers. Email rendering is fragmented — Outlook desktop uses the Word rendering engine; Gmail strips `<head>`; some clients block external resources. Output uses table-based layouts, inline CSS, and system font fallbacks to survive across the major clients.

## Output shape

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="x-apple-disable-message-reformatting">
  <title>[from asset_metadata.title]</title>
  <style type="text/css">
    /* Media queries only — most rules go inline on elements */
    @media (prefers-color-scheme: dark) { /* dark mode overrides */ }
    @media only screen and (max-width: 600px) { /* mobile overrides */ }
  </style>
  <!--[if mso]>
    <style>/* Outlook-specific overrides */</style>
  <![endif]-->
</head>
<body style="margin: 0; padding: 0; background-color: [colors.neutral];">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px;">
          <!-- header, body, CTA, footer rows -->
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

XHTML 1.0 Transitional doctype for max compatibility. Single nested-table layout (no Flexbox, no CSS Grid). Inline `style=""` attributes everywhere except media queries.

## DESIGN.md token application

Tokens resolved at generation time and inlined as `style=""` attribute values:

```html
<!-- Wrong (won't work in Outlook) -->
<div class="text-primary">...</div>

<!-- Right -->
<td style="color: #0A2540; font-family: 'Inter', system-ui, sans-serif; font-size: 16px; line-height: 1.6;">...</td>
```

No CSS custom properties — Outlook (and several other clients) don't support them. The producer resolves `{colors.primary}` to its hex literal at generation time.

## Email client constraints

| Client | Considerations |
|---|---|
| **Gmail (web/mobile)** | Strips `<head>` tags except in some configurations; supports media queries inline; rewrites class names. Build with inline styles assuming `<head>` may be discarded. |
| **Outlook (desktop)** | Uses Word's rendering engine. No CSS Grid, no Flexbox, no `padding` on `<div>` (use `<td>` padding). Use MSO conditional comments for VML rendering of buttons. |
| **Apple Mail (macOS/iOS)** | Full CSS3 support; dark mode aware. The most forgiving client; not a baseline. |
| **Yahoo Mail** | Limited CSS support; verify with [Litmus](https://www.litmus.com/) or [Email on Acid](https://www.emailonacid.com/) before final delivery. |

## Fonts

Web fonts don't load reliably in email clients. Use system font fallback chains from the typography token's `fontFamily`:

```html
<td style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; font-size: 16px;">
```

Default chain order: brand font → -apple-system (iOS/macOS Safari) → BlinkMacSystemFont (Chrome) → Segoe UI (Windows) → system-ui → sans-serif.

Do NOT emit `@font-face` declarations for email. Don't preload fonts. Don't reference brand woff2 files.

## Dark mode

Apple Mail, iOS Mail, and modern Outlook support `prefers-color-scheme: dark`:

```html
<style type="text/css">
  @media (prefers-color-scheme: dark) {
    .dark-bg { background-color: #1A1A1A !important; }
    .dark-text { color: #FFFFFF !important; }
  }
</style>

<td class="dark-bg dark-text" style="background-color: [colors.background]; color: [colors.text];">
```

Apply classes that media queries target; rely on `!important` to override inline styles in dark mode. Test the inversion — light-on-light or dark-on-dark failures are the most common email rendering bugs.

## Images

- **Absolute URLs only.** Email clients don't resolve relative paths. Producer fails when image references aren't absolute or resolvable to a hosted URL.
- **Alt text required.** Many clients block images by default — alt text is what the recipient sees first.
- **Fallback background colors.** `<td bgcolor="[colors.neutral]" style="background-color: [colors.neutral];">` ensures a colored block renders even when the image is blocked.
- **Logo sizing.** Use `width` attribute on `<img>` for Outlook + inline `style="width: ..."` for everything else. Specify both to avoid blowout in Outlook.

## Width constraints

- **Body width:** 600px max (the de facto standard). Wider breaks on mobile and in narrow preview panes.
- **Outer wrapper:** 100% width with `align="center"` and a 600px inner table — works around Outlook's quirks.
- **Viewport meta:** `<meta name="viewport" content="width=device-width, initial-scale=1">` for mobile.

## CTA buttons

Bulletproof button technique — VML for Outlook, table for everything else:

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td align="center" bgcolor="[colors.primary]" style="background-color: [colors.primary]; border-radius: [rounded.md];">
      <!--[if mso]>
        <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="[cta_url]" style="height:44px;v-text-anchor:middle;width:200px;" arcsize="20%" fillcolor="[colors.primary]">
          <w:anchorlock/>
          <center style="color:#FFFFFF;font-family:sans-serif;font-size:16px;">[cta_label]</center>
        </v:roundrect>
      <![endif]-->
      <!--[if !mso]><!-- -->
        <a href="[cta_url]" style="display: inline-block; padding: 12px 24px; color: #FFFFFF; text-decoration: none; font-family: sans-serif; font-size: 16px; font-weight: 600;">[cta_label]</a>
      <!--<![endif]-->
    </td>
  </tr>
</table>
```

Minimum tap target: 44x44px (Apple Human Interface Guidelines).

## Pitfalls

- **No `<style>` blocks outside `<head>`.** Most clients strip them. Use inline styles for visual properties; reserve `<style>` only for media queries and pseudo-class hover states.
- **No `background-image` for primary visual.** Poor support across clients; always provide a `bgcolor` fallback.
- **No CSS Grid, no Flexbox.** Tables for layout. This is non-negotiable for Outlook compatibility.
- **No JavaScript.** Email clients strip it; no exceptions.
- **Test before declaring done.** Email rendering varies enough that without testing, "looks fine in Gmail" is meaningless. Litmus / Email on Acid catch the differences.
- **Don't use `<button>` element.** Use anchor tags styled as buttons (with the bulletproof technique above). `<button>` behaves inconsistently across clients.
- **Encode entities.** Use HTML entities (`&amp;`, `&copy;`) instead of literal characters where the encoding matters — some clients re-encode and double-escape.
