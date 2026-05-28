---
slug: press-release
status: active
last-reviewed: ""
content-keys:
  - title
  - subtitle
  - dateline
  - body
  - executive_quote
  - executive_quote_attribution
  - partner_quote
  - partner_quote_attribution
  - boilerplate
  - media_contact_name
  - media_contact_email
array-keys: []
publishing: ""
default-variant: ""
production-targets:
  - web
---

# Press Release

[Instructions:
Standard wire-format release for company news — product launches, funding announcements, customer wins, partnerships, executive appointments. Default for the `press-release` content type.]

## Structure

[Instructions:
Describe the wire-format structure:
- Headline — declarative, factual, ≤12 words
- Subhead — secondary line clarifying scope or significance
- Dateline — `CITY — Month Day, Year —` followed by lede paragraph
- Lede (1 paragraph) — who, what, why now in plain language
- Detail (2-3 paragraphs) — substantive context, capability description, market frame
- Executive quote — attributed quote from a company leader
- Partner/customer quote (optional) — second perspective
- Boilerplate — pull from `messaging/pillars/profile.md` boilerplate field
- Media contact — name and email]

## Conventions

[Instructions:
Specify standards:
- Word count target (e.g., 400-700 words)
- Style guide (e.g., AP style: numerals 10+, lowercase company verbs)
- One quote per stakeholder; quotes approved by the named speaker
- Banned superlatives in the lede ("revolutionary," "best-in-class," "next-generation")]

## Frontmatter requirements

[Instructions:
Document fields the distribution platform requires. PR Newswire/Business Wire may need `category`, `industry_codes`. For self-distributed releases, document the company newsroom CMS fields.]

## CTA conventions

[Instructions:
Press releases don't carry marketing CTAs. The "next step" is media contact info. Hyperlinks in the body point to source materials (product page, customer story, analyst report) rather than conversion endpoints. Document any exceptions.]

## Writing checks

[Instructions:
Testable, asset-specific checks the writer must satisfy at generation time — a first writing gate on top of the global voice gate. Atomic assets have no variant file, so the checks live here. Capture format-specific tells the global voice gate doesn't already catch; don't restate global banned phrases or Brand Guardrails. Each check must be observable, not vague.

Examples (press release):
- No hype adjectives anywhere ("revolutionary", "groundbreaking", "best-in-class"), not just the lede
- No "is proud / thrilled / excited to announce" filler — open on the news
- Quotes sound like a named human said them, not like marketing copy
- Every significance claim is attributed or backed by a fact, not asserted
- Boilerplate matches profile.md verbatim; not paraphrased
]

[Format: testable bullet rules. Omit this section if the asset has no tells beyond the global voice gate.]
