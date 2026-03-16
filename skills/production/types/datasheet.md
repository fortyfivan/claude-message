# Datasheet Production

Produces a designed, print-ready datasheet from content following the `datasheet` schema.

## Asset Template

`templates/assets/datasheet.html`

## Schema

`templates/content-schemas/datasheet.md`

## Schema-to-Template Mapping

| Schema Field | Template Zone | Element |
|-------------|--------------|---------|
| Tagline | `.zone-header` | `h1` |
| Problem | `.zone-value` | `p` |
| Capabilities | `.zone-capabilities` | `.capabilities-grid` — one `.capability` card per entry |
| Differentiation | `.zone-differentiation` | `.diff-item` per entry |
| Proof.Quote | `.zone-proof` | `blockquote` |
| Proof.Attribution | `.zone-proof` | `.attribution` |
| Proof.Metric | `.zone-proof` | `.metric` |
| CTA.Action | `.zone-footer` | `.cta-button` text |
| CTA.URL | `.zone-footer` | `.cta-button` href and `.cta-url` text |

## Design Conventions

- **Layout:** Single page, letter size (8.5 x 11in), portrait orientation
- **Visual hierarchy:** Header with logo and tagline at top, challenge statement, capabilities grid (2 columns), differentiation points, proof pull-quote, CTA footer
- **Capabilities grid:** 2-column layout. Lead with unique capabilities. Each card has a type badge, name, and one-sentence description
- **Differentiation:** Each point uses an "Unlike / We" contrast pattern. Keep to 2-3 points max
- **Proof zone:** Full-width gradient background (primary to secondary color). Contains a quote, attribution, and metric. If no proof exists in the content, omit this zone entirely — do not fabricate
- **Footer:** CTA button (primary color) on the left, URL in light text on the right
- **Typography:** Section labels are 13px uppercase with accent color. Body text is 14px. Capability descriptions are 12.5px
- **Spacing:** 0.3in between zones. 0.6in top/bottom padding, 0.75in side padding

## Format Rules

- **Primary output:** Self-contained HTML file with all styles inline
- **PDF conversion:** If a PDF platform skill is available, follow its conversion instructions. Otherwise, instruct the user to open the HTML file in a browser and print to PDF (File > Print > Save as PDF)
- **Brand tokens:** Inject via CSS custom properties in the `:root` block. Replace `{{colors.primary}}` etc. with values from `brand.yml`
- **Content tokens:** Replace `{{field}}` placeholders with parsed content. For repeating sections (capabilities, differentiation), generate the HTML for each entry
- **Logo:** Replace `{{logo.primary}}` with the path from `brand.yml`. If the logo file doesn't exist, omit the `<img>` tag

## Quality Checks

Before presenting the deliverable:

1. All required schema fields are present in the output
2. No `{{placeholder}}` tokens remain in the HTML
3. Brand colors render correctly (check for empty values that would break CSS)
4. Capabilities grid has at least 2 entries
5. If proof zone is included, both quote and attribution are populated
