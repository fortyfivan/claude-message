Query the messaging house for content matching a natural-language intent. Returns structured results with citations to source files.

Usage:
  /search [query]
  /search [query] --scope pillars
  /search [query] --scope collections
  /search [query] --scope assets

Examples:
  /search "what's our position on AI surveillance?"
  /search "proof points relevant to CISO conversations" --scope collections
  /search "competitive battlecards against ServiceNow"

The search skill lives at `.claude/skills/system/search/SKILL.md`. It knows the messaging-house architecture, loads only the files relevant to the query, and returns synthesized results with citations.

Read and follow the instructions in `.claude/skills/system/search/SKILL.md`. Pass the query and optional scope as arguments.
