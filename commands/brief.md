Generate a creative brief for: $ARGUMENTS

Parse the topic for persona, product, segment, and motion parameters. Resolve each to messaging docs. Load profile.md for voice, audience.md for persona context, portfolio.md for product context, proof.md for supporting evidence.

The brief should include: objective, audience (resolved persona with link to messaging doc), key messages (derived from loaded pillars), tone and voice (from profile.md), supporting proof (filtered from proof.md), distribution channel, CTA, and success metrics.

Write to output/briefs/ with metadata frontmatter tracking resolved parameters.

/agents writer brief $ARGUMENTS
