Generate a single content asset using the writer subagent in standalone mode (no orchestrator, no campaign brief).

Usage:
  /generate [asset-slug] "[topic]"
  /generate [asset-slug] "[topic]" --variant [name]
  /generate [asset-slug] "[topic]" --persona [slug] --variant [name]
  /generate [asset-slug] "[topic]" --produce [target]

Examples:
  /generate blog-post "Why AI readiness starts with data governance"
  /generate email "Wiz displacement outreach" --persona ciso --variant outbound
  /generate one-pager "Acme partner overview" --variant partner
  /generate blog-post "AI readiness" --produce web

Argument resolution:
- `[asset-slug]` — resolves to the asset envelope via MESSAGE.md `## Assets`
- `--variant` (optional) — picks one of the asset's variants; falls back to the asset's `default-variant`
- `--persona`, `--product`, `--competitor`, `--segment`, `--altitude` (optional) — narrow context resolution
- `--produce` (optional) — `web`, `email`, or `print`. After the writer (and reader) complete, dispatches the producer subagent to generate HTML. Requires `brand/DESIGN.md` (see `docs/brand-system.md` for setup). Target must be in the asset's `production-targets` frontmatter array.

The writer infers scenario, builds an asset brief, presents for approval, generates, runs voice validation, dispatches the reader, and writes outputs to `output/single-assets/[slug]/`. With `--produce`, also dispatches the producer to write a sibling `.html` file.

Read and follow the instructions in `.claude/agents/writer.md`. Pass all remaining arguments to the writer.
