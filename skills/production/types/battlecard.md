# Battlecard Production

Produces an interactive HTML battlecard slide deck from content following the `battlecard` schema.

## Asset Template

`templates/assets/battlecard.html`

## Schema

`templates/content-schemas/battlecard.md`

## Schema-to-Template Mapping

| Schema Section | Slide | Template Elements |
|---------------|-------|-------------------|
| Competitor, Quick Read | Slide 1: Overview | `.slide-overview` — competitor name, quick read fields |
| Their Pitch, Strengths | Slide 2: Positioning | `.their-pitch` quote, `.strengths-table` rows |
| Objection Handling | Slide 3: Objections | `.objection-card` per objection (text + reframe) |
| Proof Ammunition | Slide 4: Proof | `.slide-proof-card` — quote, attribution, context |
| Head to Head | Slide 5: Competitive Matrix | `.matrix-table` rows with advantage styling |
| Talk Track, Killer Questions | Slide 6: Talk Track | `.talk-track-content` + `.question-list` |

## Design Conventions

- **Format:** Interactive HTML slide deck, same zero-dependency approach as other slide templates
- **Audience:** Sales reps mid-deal. Design for speed — a rep should find what they need in under 30 seconds per slide
- **Overview slide:** Gradient background (primary to secondary). Competitor name prominent. Quick Read in a semi-transparent card with key fields labeled
- **Positioning slide:** Their pitch in a styled blockquote (grey, italic). Strengths in a three-column table: Strength | Reality | Redirect
- **Objections slide:** Each objection in its own card. Objection text in bold, reframe in primary color with a left border. Verbatim-ready language the rep can use
- **Proof slide:** Centered, large quote with attribution and competitive context. One proof point per slide — keep it focused
- **Competitive matrix:** Table with Dimension | Us | Them | Edge columns. Edge column uses color-coded classes: `.advantage-us` (primary blue), `.advantage-them` (red), `.advantage-tie` (grey)
- **Talk track slide:** The 60-second verbal summary in a highlighted container with primary-color left border
- **Navigation:** Same as other slide templates — arrow keys, spacebar, click, `N` for notes, escape for first slide

### Handling Optional Sections

- **Head to Head:** If not in content, omit the competitive matrix slide entirely
- **Win/Loss Scenarios:** If present, add as an additional slide between Positioning and Objections
- **Killer Questions:** If present, add as a `.question-list` below the talk track on slide 6
- **Landmines:** If present, add as a final "Watch Out" slide with a red accent
- **Proof Ammunition:** If multiple proof points, show the strongest one on the proof slide. Others can go in speaker notes

## Format Rules

- **Primary output:** Self-contained HTML file
- **PDF export:** Print rules render one slide per page in landscape. Speaker notes hidden
- **Brand tokens:** Same CSS custom property injection as other templates
- **Content tokens:** Replace placeholders. For repeating sections (strengths, objections, head_to_head), generate the appropriate HTML elements for each entry
- **Advantage styling:** In the competitive matrix, use `advantage-us`, `advantage-them`, or `advantage-tie` CSS class based on the advantage value (case-insensitive match: "us"/"ours" -> us, "them"/"theirs" -> them, else tie)

## Quality Checks

1. All required fields (competitor, quick_read, their_pitch, strengths, weaknesses, objection_handling, killer_questions) present
2. No `{{placeholder}}` tokens remain
3. Quick Read has all four fields (who, their_angle, our_angle, remember)
4. Objections have both objection text and reframe
5. Navigation works correctly
6. Slide count reflects optional sections included/omitted
7. Competitive matrix advantage colors render correctly
