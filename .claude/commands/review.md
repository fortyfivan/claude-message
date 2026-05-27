Comprehensive messaging-alignment evaluation of a content asset — voice, terminology, pitch, positioning, audience appropriateness, persona alignment, proof support, and format conformance. Use to evaluate any draft: internal output, external content, partner deliverables, or sales drafts against the messaging house.

Usage:
  /review [file-path]

The evaluation framework lives in `.claude/skills/craft/review/SKILL.md`. The command dispatches the reader subagent (running on Haiku for cost efficiency) which loads that skill, adopts the target persona's perspective, scores each dimension, and returns a verdict with revision directives.

Read and follow the instructions in `.claude/skills/craft/review/SKILL.md`. Pass the file path as the argument.
