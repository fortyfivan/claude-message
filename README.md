```
 _____ _                 _       ___  ___
/  __ \ |               | |      |  \/  |
| /  \/ | __ _ _   _  __| | ___  | .  . | ___  ___ ___  __ _  __ _  ___
| |   | |/ _` | | | |/ _` |/ _ \ | |\/| |/ _ \/ __/ __|/ _` |/ _` |/ _ \
| \__/\ | (_| | |_| | (_| |  __/ | |  | |  __/\__ \__ \ (_| | (_| |  __/
 \____/_|\__,_|\__,_|\__,_|\___| \_|  |_/\___||___/___/\__,_|\__, |\___|
                                                              __/ |
                                                             |___/
```

Claude Message is a dynamic messaging system for Claude Code. It combines a structured messaging house with agents, skills, and commands to help teams build, maintain, and operationalize their messaging across the GTM lifecycle.

Built for Product Marketers, Founders, and anyone who cares about messaging quality and taste.

## Getting Started

Fork or clone the repository:

```bash
git clone https://github.com/fortyfivan/claude-message.git my-company-messaging
cd my-company-messaging
```

Open in Claude Code and build your messaging system:

```
> /bootstrap
```

The bootstrap command guides you through an interactive workflow to build your complete messaging system. It can start from scratch or from existing materials placed in the `input/` directory — organized by type into `messaging/`, `docs/`, `research/`, `transcripts/`, and `examples/` subdirectories. See `input/README.md` for details.

## How It Works

Three files anchor the system:

- `MESSAGE.md` — the messaging design system. Architecture, frontmatter contracts, progressive loading rules, and your writing profile.
- `DESIGN.md` — the visual identity. Brand tokens (colors, typography, logos) consumed by downstream rendering tools.
- `messaging/` — the messaging house. Eight pillar files plus collection profiles for personas, competitors, products, stories, and more.

### Messaging House

The Messaging House is a structured model of your messaging. Eight pillars cover every strategic dimension (the 8P system):

| # | Pillar      | Purpose                                   |
|---|-------------|-------------------------------------------|
| 1 | Profile     | Identity, voice, marketplace statement    |
| 2 | Pitch       | Strategic narrative                       |
| 3 | Position    | Category and competitive landscape        |
| 4 | People      | ICP, personas, segments                   |
| 5 | Portfolio   | Products and solutions                    |
| 6 | Proposition | UVPs, differentiators, value claims       |
| 7 | Proof       | Customer evidence and external validation |
| 8 | Play        | GTM motion, plays, signals                |

Each pillar uses YAML frontmatter for structured metadata and markdown body for narrative content. Collection subdirectories hold detailed profiles:

- `categories/` — Market categories the company aligns with or competes in
- `competitors/` — Alternatives buyers evaluate (vendor, DIY, status quo)
- `personas/` — Buyer or user roles with altitude and pain points
- `plays/` — GTM motion narratives for buyer situations
- `products/` — Products, modules, platforms in the portfolio
- `reports/` — Third-party research, analyst reports, surveys, benchmarks
- `segments/` — Industry, size, region, or maturity slices
- `signals/` — Compelling events that trigger one or more plays
- `solutions/` — Use-case bundles composed of one or more products
- `stories/` — Customer evidence — outcome, quote, and proof

Two operational files round out the house:

- `glossary.md` — Custom terminology used in messaging. Once defined, terms override all other word-choice guidance.
- `journal.md` — Longitudinal log of learnings, decisions, and process notes.

### Agents

Three subagents handle execution — dispatched by workflow skills and the user.

| Agent | Purpose |
|-------|---------|
| **writer** | Context-resolution content engine. Resolves the exact messaging docs a task requires, loads the appropriate skill, generates content grounded in the messaging house, and self-evaluates. |
| **researcher** | Research execution agent. Searches external sources and evaluates findings against the messaging system. Dispatched standalone or by the investigate workflow. |
| **reader** | Content review specialist. Adopts the target persona's perspective and scores generated content against quality criteria. |

### Commands

Commands are the stable invocation layer. Each routes to a skill or agent.

| Command | Purpose |
|---------|---------|
| `/bootstrap` | Build messaging system from scratch |
| `/build campaign [type] [topic]` | Build a multi-asset content campaign |
| `/build launch [name]` | Orchestrate a product launch |
| `/compose [type] [name]` | Compose or update a messaging document |
| `/investigate` | Broad scan across all domains |
| `/investigate [type] [name]` | Targeted investigation of a specific entity |
| `/investigate feedback [input]` | Process feedback into messaging changes |
| `/investigate health` | Validate messaging system health |
| `/investigate review` | Tracker dashboard + health summary |
| `/generate [skill] [topic]` | Generate content using a skill |
| `/update` | Detect drift across artifacts, campaigns, launches, and standalone assets |
| `/update [slug]` | Refresh and version a specific living artifact |
| `/review [file]` | Review a content asset |
| `/tune` | Calibrate skills to the messaging house |

**Task skills** (content generation by category):

| Category | Types |
|----------|-------|
| Assessment | Business value assessment, risk assessment, tech assessment |
| Blog Copywriting | Thought leadership, use case deep dive, threat research, data study, product announcement, press release, event recap, predictions |
| Brief Copywriting | Solution brief, industry vertical, persona brief, product datasheet, use case overview, company overview, event companion, session abstract, partner better together |
| Email Copywriting | Single outbound, outbound sequence, inbound sequence, event promotion, product newsletter |
| Enablement | Competitive battlecard, discovery guide, playbook walkthrough, partner joint solution |
| Paper Copywriting | Topic deep-dive, research study, industry trend, data findings |
| Social Copywriting | LinkedIn post, LinkedIn article, X post, X thread |
| Story | Customer story, partner story |
| Web Copywriting | Product page, solution page, comparison page, topic page |

**Voice Gate** — Writing rules loaded for every content task. Eliminates AI writing patterns, enforces clean prose rules.

### Living Artifacts

Artifacts are versioned, continuously maintained content sources (decks, collateral, roadmaps) that stay current with the messaging house. Each artifact lives in `artifacts/[slug]/` with three files:

- `manifest.md` — Dependencies on the messaging house, trigger conditions, and section-to-source mapping
- `current.md` — The canonical content
- `changelog.md` — Version history

Run `/update [slug]` to detect drift, review proposed changes, and version the result. Run `/update` with no arguments for a unified drift overview across all artifacts and produced content.

### Production Handoff

Claude Message authors messaging-grounded markdown content. Schemas in `templates/schemas/` define structure for each deliverable type (datasheet, one-pager, battlecard, executive brief, slide deck) so writers compose consistently.

Rendering happens externally — open content alongside `/DESIGN.md` in Claude Design or Claude Artifacts to produce finished decks, PDFs, and web pages. The repo's job is content + structure; downstream tools handle pixels.

### Insights System

The `/investigate` workflow unifies external research, field feedback, and system health into a single tracker. Insights follow a lifecycle:

```
open -> acknowledged -> resolved
         |
       deferred
```

Configure investigation cadence and focus areas in `insights/config.md`.

## Your Writing Profile

Bootstrap generates a writing profile in `MESSAGE.md` based on your messaging house. The profile is the always-loaded context for every messaging or content task — voice, identity, market position, stage. It calibrates tone, claims, and proof to where the company actually sits in the market.

To update the profile after changes to your messaging house, re-run `/bootstrap` or edit the profile block in `MESSAGE.md` directly.

## Pulling Upstream Updates

To pull in new agents, skills, or templates from the upstream repo:

```bash
git remote add upstream https://github.com/fortyfivan/claude-message.git
git fetch upstream
git merge upstream/main
```

Resolve any conflicts — your `messaging/`, `output/`, and tuned `.claude/skills/` are yours. Upstream changes typically land in `templates/`, base skills, and agent definitions.

## FAQ

**Why did you build this?**
I have to use Gemini at work. It's... messy. This is a lot more structured, a lot more focused, and a lot more fun to build.

**Isn't this overkill?**
Yes, probably for most. But when your company has multiple products serving multiple audiences across multiple segments, your regional teams are out there running wild, and your global sales reps are running even wilder, messaging gets real squirrely, real fast.

**Is Claude Code the right tool for this?**
No, probably not. But it has potential to get you into a messaging flow state that no other tool has been able to accomplish (yet).

## Contributing

I primarily encourage you to take this as-is and make it yours. But I do welcome PRs for the agents, commands, and skills.

## History

Version 0.5 (2026-03-16) - fork mode, workspace ships complete, no plugin layer
Version 0.4 (2026-03-06) - all-in on plugin mode, workspace scaffolding
Version 0.3 (2026-03-03) - plugin architecture, 6-pillar consolidation, agent-driven system
Version 0.2 (2026-02-06) - system bootstrap
Version 0.1 (2026-01-16) - initial drop

## Credits

Ivan Dwyer (@fortyfivan)

## License

The MIT License (MIT)

Copyright (c) 2015 Chris Kibble

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
