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

Claude Message is a dynamic messaging system for Claude Code. It combines a structured messaging house with agents, skills, and commands to help teams build, maintain, and operationalize their positioning and messaging across the GTM lifecycle.

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

The bootstrap command guides you through an interactive workflow to build your complete messaging system. It can start from scratch or from existing materials (pitch decks, website content, brand guides) placed in the `input/` directory.

## How It Works

### Messaging House

The Messaging House is a structured model of your positioning and messaging. Six pillars cover every strategic dimension, built progressively:

| # | Pillar | Purpose | Absorbs |
|---|--------|---------|---------|
| 1 | Profile | Company identity, narrative, voice, mission | purpose, profile, pitch, preferences |
| 2 | Space | Market landscape, positioning, differentiation | position, proposition |
| 3 | Audience | ICP, buyer/user personas, market segments | people |
| 4 | Portfolio | Products, solutions, capabilities | portfolio |
| 5 | Proof | Social proof, case studies, evidence | proof |
| 6 | Motion | GTM strategies, campaign playbooks | plays |

Each pillar uses YAML frontmatter for structured metadata and markdown body for narrative content. Collection subdirectories hold detailed profiles:

- `categories/` — Market category profiles
- `competitors/` — Competitor profiles
- `personas/` — Persona profiles
- `plays/` — GTM play profiles
- `products/` — Product detail docs
- `stories/` — Customer stories and proof narratives
- `segments/` — Market segment profiles
- `solutions/` — Solution briefs

### Agents

Four subagents handle execution — dispatched by workflow skills and the user.

| Agent | Purpose |
|-------|---------|
| **writer** | Context-resolution content engine. Resolves the exact messaging docs a task requires, loads the appropriate skill, generates content grounded in the messaging house, and self-evaluates. |
| **researcher** | Research execution agent. Searches external sources and evaluates findings against the messaging system. Dispatched standalone or by the insights workflow. |
| **reader** | Content review specialist. Adopts the target persona's perspective and scores generated content against quality criteria. |
| **producer** | Deliverable production agent. Creates finished files from approved content — applies brand tokens and asset templates. |

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
| `/produce [type] [file]` | Produce a finished deliverable |
| `/review [file]` | Review a content asset |
| `/tune` | Calibrate skills to the messaging house |

**Task skills** (content generation by category):

| Category | Types |
|----------|-------|
| Blog Copywriting | Thought leadership, use case deep dive, threat research, data study, product announcement, press release |
| Brief Copywriting | Solution brief, industry vertical, persona brief, product datasheet, use case overview, company overview, event companion, session abstract, booth messaging |
| Email Copywriting | Single outbound, outbound sequence, inbound sequence, event promotion, product newsletter |
| Enablement | Competitive battlecard, discovery guide, playbook walkthrough |
| Paper Copywriting | Topic deep-dive, research study, industry trend, data findings |
| Social Copywriting | LinkedIn post, LinkedIn article, X post, X thread |
| Web Copywriting | Product page, solution page |
| Production | Datasheet, one-pager, executive brief, slide deck, battlecard |

**Voice Gate** — Universal quality gate loaded for every content task. Eliminates AI writing patterns, scores across five dimensions.

### Insights System

The `/investigate` workflow unifies external research, field feedback, and system health into a single tracker. Insights follow a lifecycle:

```
open -> acknowledged -> resolved
         |
       deferred
```

Configure investigation cadence and focus areas in `insights/config.md`.

## Your Writing Profile

Bootstrap automatically generates a writing profile in CLAUDE.md based on the messaging house. The profile establishes your role, company identity, and market context so every interaction — not just content generation — is grounded in who you are and where you compete.

To update the profile after changes to your messaging house, re-run `/bootstrap` or edit the profile block in CLAUDE.md directly.

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
