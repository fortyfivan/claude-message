Generate a content asset using a messaging skill.

Parse the task for implicit and explicit parameters: persona, product, competitor, segment, motion, altitude. Resolve each parameter to the corresponding messaging doc in messaging/. Always load profile.md and space.md. Load skills from .claude/skills/. Cross-reference loaded context for consistency before writing. Flag gaps or conflicts to the user.

The writer will present a brief showing the resolved context, key messages, and skill for approval before generating content. You can adjust parameters, request different messaging emphasis, or approve as-is.

Write the finished asset to output/ with metadata frontmatter tracking the skill, resolved parameters, and all messaging docs loaded.

/agents writer $ARGUMENTS
