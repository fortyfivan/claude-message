# Executive Brief Production

Produces a designed executive brief from content following the `executive-brief` schema.

## Asset Template

`templates/assets/executive-brief.html`

## Schema

`templates/content-schemas/executive-brief.md`

## Schema-to-Template Mapping

| Schema Field | Template Zone | Element |
|-------------|--------------|---------|
| Title | `.zone-header` | `h1` |
| Situation | `.zone-situation` | `p` |
| Risk of Inaction | `.zone-risk` | `p` |
| Approach | `.zone-approach` | `p` |
| Outcomes | `.zone-outcomes` | `.outcome` per entry (marker + name + description) |
| Proof.Quote | `.zone-proof` | `blockquote` |
| Proof.Attribution | `.zone-proof` | `.attribution` |
| Proof.Result | `.zone-proof` | `.result` |
| Next Steps.Immediate | `.zone-next-steps` | First `.step` |
| Next Steps.Short-term | `.zone-next-steps` | Second `.step` |
| Next Steps.Evaluation | `.zone-next-steps` | Third `.step` |

## Design Conventions

- **Layout:** Single page, letter size (8.5 x 11in), portrait orientation with wider margins (0.85in sides)
- **Visual hierarchy:** Logo + "Executive Brief" label + title at top. Situation > Risk (alert styling) > Approach > Outcomes > Proof > Next Steps
- **Altitude:** This is executive-level content. Design should feel boardroom-ready — clean, authoritative, restrained
- **Risk zone:** Distinctive visual treatment — red-tinted background with red left border. This is the urgency signal. If no risk_of_inaction in content, omit this zone
- **Section headings:** 16px with a 2px primary-color underline. Provides clear structure without crowding
- **Outcomes:** Each outcome uses a primary-color dot marker, bold name, and light-colored description
- **Next steps:** Three-column grid with primary-color top border on each card. Labels: Immediate, Short-term, Evaluation
- **Proof zone:** Full-width gradient. Executive-level proof should reference business outcomes, not features
- **Typography:** Title at 28px. Section headings at 16px. Body at 14px. Next-step cards at 12.5px

## Format Rules

- **Primary output:** Self-contained HTML file
- **PDF conversion:** If a PDF platform skill is available, follow its instructions. Otherwise, browser print to PDF
- **Brand tokens:** Inject via CSS custom properties in `:root`
- **Content tokens:** Replace placeholders. For outcomes, generate one `.outcome` div per entry
- **Optional zones:** Risk of Inaction and Proof are optional — omit gracefully if missing

## Quality Checks

1. All required fields (title, situation, approach, outcomes, next_steps) present
2. No `{{placeholder}}` tokens remain
3. Outcomes have 3-4 entries
4. Next steps has all three stages (immediate, short-term, evaluation)
5. Title is 10 words or fewer
6. Tone is executive — no product jargon in section headings
