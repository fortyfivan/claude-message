Generate production-ready HTML from existing writer output using the producer subagent.

Usage:
  /produce [output-file-path] --target web|email|print

Examples:
  /produce output/single-assets/cisos-perspective.md --target web
  /produce output/campaigns/q1-launch/a01-cisos-perspective.md --target web
  /produce output/campaigns/q1-launch/a02-onboarding-email.md --target email
  /produce output/whitepapers/zero-trust-guide.md --target print

Argument resolution:
- `[output-file-path]` — path to the writer's `.md` output file. The command resolves the sibling `.json` automatically.
- `--target` (required) — `web`, `email`, or `print`. Determines which production task skill the producer loads.

Output destinations:
- `--target web` → `[base].html`
- `--target email` → `[base].email.html`
- `--target print` → `[base].print.html`

The producer reads `brand/DESIGN.md`, applies tokens per the target's task skill, and writes HTML co-located with the writer output. Operates outside the messaging system (no MESSAGE.md or pillars loaded). Refuses to operate if `brand/DESIGN.md` is missing or non-conformant — see [`docs/brand-system.md`](../../docs/brand-system.md) for setup.

Read and follow the instructions in `.claude/agents/producer.md`. Pass all remaining arguments to the producer.
