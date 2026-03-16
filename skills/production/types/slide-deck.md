# Slide Deck Production

Produces an interactive HTML slide deck from content following the `slide-deck` schema.

## Asset Templates

- **Pitch deck:** `templates/assets/pitch-deck.html`
- **Sales deck:** `templates/assets/sales-deck.html`

Select the template based on the `deck_type` field in the content schema.

## Schema

`templates/content-schemas/slide-deck.md`

## Slide Type Mapping

Each slide's `type` field maps to a CSS class and structural pattern in the template:

| Slide Type | CSS Class | Structure |
|-----------|-----------|-----------|
| title | `.slide-title` | Logo, headline (h1), subtitle |
| narrative | `.slide-narrative` | Headline (h2), body (paragraphs or bullet list) |
| two-column | `.slide-two-column` | Headline (h2), two `.column` divs with h3 + content |
| proof | `.slide-proof` | Blockquote, attribution, metric + metric label |
| section-divider | `.slide-section-divider` | Headline (h2), subtitle — full primary-color background |
| closing | `.slide-closing` | Headline (h2), body — gradient background |
| challenge | `.slide-challenge` | Headline (h2), body — red-tinted background (sales deck) |
| solution | `.slide-solution` | Headline (h2), body — primary-color headline (sales deck) |
| demo | `.slide-demo` | Headline (h2), body, demo placeholder area (sales deck) |
| competitive | `.slide-competitive` | Headline (h2), comparison table (sales deck) |
| pricing | `.slide-pricing` | Headline (h2), body (sales deck) |

## Design Conventions

- **Format:** Self-contained HTML file. Zero external dependencies. All CSS and JS inline. Works offline, opens in any browser
- **Navigation:** Arrow keys (left/right/up/down), spacebar (next), escape (first slide), click (left half = prev, right half = next)
- **Speaker notes:** Each slide has a hidden `.speaker-notes` div. Press `N` to toggle the speaker notes panel at the bottom
- **Progress:** Thin progress bar at the bottom. Slide counter (current/total) at bottom-right
- **Transitions:** Opacity fade (0.4s ease) between slides
- **Scaling:** Viewport-based units (vw/vh) for responsive sizing. Works on any screen resolution
- **Title/closing slides:** Gradient background (primary to secondary), white text, centered
- **Section dividers:** Solid primary-color background, white text, centered
- **Content slides:** White background, primary-color headlines, standard text color

### Pitch Deck Conventions

- 8-15 slides
- Narrative arc: Status quo is broken -> Here's why -> Here's a better way -> Proof -> What to do
- Slide types: title, narrative, two-column, proof, section-divider, closing
- Focus on the story, not the product

### Sales Deck Conventions

- 10-20 slides
- Structured conversation: Title -> Challenge -> Solution -> Proof -> Demo -> Competitive -> Pricing -> Closing
- Includes sales-specific slide types: challenge (red accent), solution, demo (placeholder), competitive (comparison table), pricing
- Demo slide includes a placeholder area for live demo or screenshot insertion

## Building Slides

For each slide in the content's `slides` array:

1. Determine the slide type from the `type` field
2. Create a `<section class="slide slide-[type]" data-slide="[n]">` element
3. Populate the headline from `headline`
4. Populate the body based on slide type:
   - **narrative/challenge/solution/demo/pricing:** Body text or bullet list
   - **two-column:** Split `left_title`/`left_body` and `right_title`/`right_body` into `.column` divs
   - **proof:** Map `quote`, `attribution`, `metric`, `metric_label`
   - **competitive:** Build a `<table>` from comparison rows
5. Add speaker notes in a hidden `.speaker-notes` div
6. The first slide gets the `.active` class

## Format Rules

- **Primary output:** Self-contained HTML file
- **PPTX conversion:** If a PPTX/frontend-slides/revealjs platform skill is available, follow its instructions to convert or re-render. Map brand tokens to theme colors and slide master styles
- **PDF export:** The template includes `@media print` rules for landscape, one slide per page. User can print to PDF from the browser
- **Speaker notes:** Hidden in presentation and print mode. Toggled with `N` key. Content comes from the `speaker_notes` field per slide
- **Appendix slides:** If present, add after the closing slide. These are not part of the main narrative — the presenter pulls them up on demand

## Quality Checks

1. All slides from the content schema are present in the output
2. First slide is `.active`, all others start hidden
3. Navigation JS works (arrow keys, spacebar, click, escape)
4. Speaker notes panel toggles with `N`
5. No `{{placeholder}}` tokens remain
6. Slide count matches the content schema
7. Progress bar reflects accurate slide count
8. Print layout renders one slide per page in landscape
