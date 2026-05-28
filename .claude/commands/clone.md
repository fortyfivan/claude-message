Build the brand/ folder from a company URL — extract design tokens into brand/DESIGN.md and download SVG logos, woff2 fonts, and images. The automated cousin of /bootstrap, scoped to visual identity.

Usage:
  /clone <url>

Example:
  /clone https://stripe.com

The skill fetches the site, extracts a design-token proposal and an asset manifest, presents both for review, and writes brand/DESIGN.md plus downloaded assets to brand/ on approval. Operates outside the messaging system (no MESSAGE.md or pillars loaded). If brand/DESIGN.md already exists, it confirms before overwriting. See `docs/brand-system.md` for the brand system and DESIGN.md spec.

Read and follow the instructions in `.claude/skills/system/clone/SKILL.md`. Pass all remaining arguments to the skill.
