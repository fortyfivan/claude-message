# One-Pager Production

Produces a designed, single-page overview from content following the `one-pager` schema.

## Asset Template

`templates/assets/one-pager.html`

## Schema

`templates/schemas/one-pager.md`

## Schema-to-Template Mapping

| Schema Field | Template Zone | Element |
|-------------|--------------|---------|
| Headline | `.zone-header` | `h1` |
| Subheadline | `.zone-header` | `.subheadline` |
| Challenge | `.zone-challenge` | `p` |
| Solution | `.zone-solution` | `p` |
| Key Benefits | `.zone-benefits` | `.benefits-list` — one `li` per entry |
| Proof.Quote | `.zone-proof` | `blockquote` |
| Proof.Attribution | `.zone-proof` | `.attribution` |
| Proof.Metric | `.zone-proof` | `.metric` |
| CTA.Action | `.zone-cta` | `.cta-button` text |
| CTA.URL | `.zone-cta` | `.cta-button` href |
| CTA.Supporting | `.zone-cta` | `.cta-supporting` text |

## Design Conventions

- **Layout:** Single page, letter size (8.5 x 11in), portrait orientation
- **Visual hierarchy:** Centered header with logo, headline, and subheadline. Left-aligned body sections. Challenge > Solution (highlighted) > Benefits > Proof > CTA
- **Header:** Centered, with a 3px primary-color border at the bottom. Headline in primary color, subheadline in light text color
- **Solution zone:** Highlighted with a light background and primary-color left border (4px) to visually distinguish from the challenge
- **Benefits:** Simple list with primary-color bold labels. 3 benefits max. Each benefit is one sentence
- **Proof zone:** Full-width gradient background (primary to secondary). If no proof in content, omit entirely
- **CTA:** Primary action button on the left, optional supporting text on the right
- **Typography:** Section labels are 13px uppercase with accent color. Body text is 14px. Headline is 26px
- **Spacing:** 0.35in between zones

## Format Rules

- **Primary output:** Self-contained HTML file with all styles inline
- **PDF conversion:** If a PDF platform skill is available, follow its conversion instructions. Otherwise, open in browser and print to PDF
- **Brand tokens:** Inject via CSS custom properties in the `:root` block
- **Content tokens:** Replace `{{field}}` placeholders. For key benefits, generate one `<li>` per entry
- **Logo:** Replace `{{logo.primary}}` with the path from `brand.yml`. Omit if missing

## Quality Checks

1. All required fields (headline, challenge, solution, CTA) present
2. No `{{placeholder}}` tokens remain
3. Key benefits have 3 or fewer entries
4. Headline is under 12 words
5. Content fits on a single printed page
