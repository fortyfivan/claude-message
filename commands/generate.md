Generate a content asset using a messaging skill.

Parse the task for implicit and explicit parameters: persona, product, competitor, segment, motion, altitude. Resolve each parameter to the corresponding messaging doc in messaging/. Always load profile.md and space.md. Load tuned skills from .claude/skills/, falling back to templates/skills/ if no tuned version exists. Cross-reference loaded context for consistency before writing. Flag gaps or conflicts to the user.

Write the finished asset to output/ with metadata frontmatter tracking the skill, resolved parameters, and all messaging docs loaded.

/agents writer $ARGUMENTS
