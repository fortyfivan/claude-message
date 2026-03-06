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

Claude Message is a messaging intelligence system built for Claude Code. It combines a structured messaging house with agents, skills, and commands to help teams build, maintain, and operationalize their positioning and messaging.

Built for Product Marketers, Founders, and anyone who cares about messaging quality and taste. Primarily for B2B companies, but the principles may apply to others.

*I said who's house? Your house!*

## Getting Started

### Fork Mode (Primary)

Clone the repo and make it your messaging workspace:

```bash
git clone https://github.com/fortyfivan/claude-message.git my-company-messaging
cd my-company-messaging
claude
> /project:bootstrap
```

The bootstrap agent guides you through six interactive phases to build your complete messaging system. It can start from scratch or from existing materials (pitch decks, website content, brand guides).

### Plugin Mode

Install the agents, commands, and skills into an existing project:

```bash
claude plugin install https://github.com/fortyfivan/claude-message
```

Then run `/project:bootstrap` to create the messaging directories in your project.

## How It Works

### Messaging House

The Messaging House is a structured model of your positioning and messaging. Six pillars cover every strategic dimension, built progressively:

| # | Pillar | Purpose | Absorbs |
|---|--------|---------|---------|
| 1 | Profile | Company identity, narrative, voice, mission | purpose, profile, pitch, preferences |
| 2 | Portfolio | Products, solutions, capabilities | portfolio |
| 3 | Space | Market landscape, positioning, differentiation | position, proposition |
| 4 | Audience | ICP, buyer/user personas, market segments | people |
| 5 | Proof | Social proof, case studies, evidence | proof |
| 6 | Motions | GTM strategies, campaign playbooks | plays |

Each pillar uses YAML frontmatter for structured metadata and markdown body for narrative content. Collection subdirectories hold detailed profiles:

- `categories/` — Market category profiles
- `competitors/` — Competitor profiles
- `personas/` — Persona profiles
- `plays/` — GTM play profiles
- `products/` — Product detail docs
- `quotes/` — Customer quotes and proof fragments
- `segments/` — Market segment profiles
- `solutions/` — Solution briefs

### Agents

| Agent | Purpose |
|-------|---------|
| **bootstrap** | Interactive 6-phase system builder. Walks through Profile → Portfolio → Space → Audience → Proof → Motions with a discover → synthesize → validate → draft → write → bridge cycle at each phase. |
| **researcher** | Messaging intelligence. Runs automated scans to surface insights, handles deep-dive investigations, and performs ad-hoc research on competitors, personas, and topics. |
| **writer** | Context-resolution content engine. Resolves the exact messaging docs a task requires, loads the appropriate skill, generates content grounded in the messaging house, and self-evaluates. |
| **campaign** | Campaign orchestrator. Plans multi-asset campaigns through intake, writes a messaging brief for approval, then dispatches writer subagents by wave to produce each asset. |
| **tune** | Skill calibration agent. Reads the messaging house, builds a company profile across five dimensions, and writes tuned skills that encode company-specific guidance into the content generation instructions. |

### Commands

| Command | Purpose |
|---------|---------|
| `/project:bootstrap` | Build messaging system from scratch |
| `/project:scan` | Run messaging intelligence scan |
| `/project:investigate [topic]` | Deep-dive on an insight or topic |
| `/project:research [topic]` | Research a topic, write to research/ |
| `/project:competitor [name]` | Research and profile a competitor |
| `/project:persona [role]` | Draft or update a persona |
| `/project:audit` | Audit messaging for gaps and inconsistencies |
| `/project:generate [skill] [topic]` | Generate content using a skill |
| `/project:brief [topic]` | Generate a creative brief |
| `/project:campaign [type] [topic]` | Build a multi-asset content campaign |
| `/project:tune` | Calibrate skills to the messaging house |
| `/project:tune --check` | Detect tuning drift without changes |

### Skills

Skills are dynamically loaded instructions for content generation, organized by category/type:

| Category | Types |
|----------|-------|
| Blog Copywriting | Thought leadership, use case deep dive, threat research, data study, product announcement |
| Brief Copywriting | Solution brief, industry vertical, persona brief, product datasheet, use case overview, company overview, event companion |
| Email Copywriting | Single outbound, outbound sequence, inbound sequence, event promotion, product newsletter |
| Social Copywriting | LinkedIn post, LinkedIn article, X post, X thread |

### Insights System

The research agent runs scheduled scans that evaluate external signals against the messaging system. Insights follow a lifecycle:

```
open → acknowledged → resolved
         ↓
       deferred
```

Configure scan cadence and focus areas in `insights/config.md`. Run scans on a cron schedule:

```bash
0 6 * * 1 cd /path/to/repo && claude -p "/project:scan" --print
```

## Directory Structure

```
_templates/
  messaging/             → Canonical schemas for messaging docs (read-only)
  skills/                → Base generic skill templates (read-only)

.claude/
  CLAUDE.md              → Plugin context and user guide
  settings.json          → MCP server configuration
  skills/
    messaging/           → Tuned content generation skills

.claude-plugin/
  plugin.json            → Plugin manifest
  marketplace.json       → Marketplace manifest

agents/                  → Agent definitions
commands/                → Slash command definitions

messaging/
  profile.md             → Company identity, narrative, voice
  space.md               → Market landscape, positioning, differentiation
  motions.md             → GTM strategies, campaign playbooks
  audience.md            → ICP, personas, market segments
  portfolio.md           → Products, solutions, capabilities
  proof.md               → Social proof, case studies, evidence
  categories/            → Market category profiles
  competitors/           → Competitor profiles
  personas/              → Persona profiles
  quotes/                → Customer quotes and proof fragments
  plays/                 → GTM play profiles
  products/              → Product detail docs
  segments/              → Market segment profiles
  solutions/             → Solution briefs

research/                → Uploaded and agent-generated research
insights/                → Messaging intelligence
  tracker.md             → Rolling insight tracker
  config.md              → Scan configuration
  scans/                 → Scan digests
  investigations/        → Deep-dive reports
output/                  → Generated content (gitignored)
  campaigns/             → Campaign briefs and generated assets
```

## Your Writing Profile

Provide Claude Code with a writing profile in CLAUDE.md to guide its messaging style:

```
You are a {role} at {company}. {company} is a(n) {stage} {type} company in the {market} space.

You are responsible for generating consistent, clear, and compelling messaging based on user requests.

You must be well versed in the market, business, and technical landscape of {company} to be effective in this role.
```

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