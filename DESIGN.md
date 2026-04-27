---
version: alpha
name: ""
description: ""
colors:
  primary: ""
  secondary: ""
  tertiary: ""
  neutral: ""
typography:
  headline-lg:
    fontFamily: ""
    fontSize: ""
    fontWeight: 600
    lineHeight: 1.1
  headline-md:
    fontFamily: ""
    fontSize: ""
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: ""
    fontSize: ""
    fontWeight: 400
    lineHeight: 1.5
  label-sm:
    fontFamily: ""
    fontSize: ""
    fontWeight: 500
    lineHeight: 1.2
---

# DESIGN.md — The Visual Identity

This file is the visual identity of the brand. It pairs with `/MESSAGE.md` (which carries voice, narrative, and positioning) and is consumed by downstream rendering tools (e.g., Claude Design, Claude Artifacts) when producing finished deliverables. Keep tokens above as the canonical source; use the prose below to explain how to apply them.

The schema follows the Stitch DESIGN.md spec. Bootstrap and `/investigate fix design` are the only writers.

## Overview

[Instructions: Describe the brand's visual personality in 2-4 sentences. What feeling should collateral evoke? Confident, approachable, technical, premium? What do you want a CISO or VP to think when they see a one-pager? This sets the tone for every design decision below.]

## Colors

[Instructions: Define each color in the palette with its semantic role and one sentence on when to use it. Match the prose to the YAML tokens in frontmatter.]

- **Primary:** [purpose — e.g., headlines, primary CTAs, brand signature]
- **Secondary:** [purpose — e.g., supporting elements, dividers]
- **Tertiary:** [purpose — e.g., accents, highlights, callouts]
- **Neutral:** [purpose — e.g., background, body text]

## Typography

[Instructions: Describe the type system. Which font carries headlines, which carries body, which carries data/labels. Match prose to typography tokens above.]

- **Headlines:** [font + intent]
- **Body:** [font + intent]
- **Labels:** [font + intent — for metadata, captions, and data tables in collateral]

## Logo

Asset paths live alongside this file. PMM deliverables select the variant based on background.

- `messaging/brand/logo-primary.svg` — full lockup on light backgrounds
- `messaging/brand/logo-icon.svg` — icon-only mark for thumbnails and avatars
- `messaging/brand/logo-white.svg` — full lockup on dark or photographic backgrounds

[Instructions: Add placement rules — minimum size, clear-space, what not to do (recolor, distort, place on busy imagery). 3-4 bullets max.]

## Do's and Don'ts

[Instructions: 4-6 practical rules that prevent the most common mistakes when producing collateral. Keep them concrete and testable.]

- Do [practical rule]
- Don't [practical rule]
- Do [practical rule]
- Don't [practical rule]
