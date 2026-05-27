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

**`claude-message`** is a Claude-native messaging system built around the MESSAGE.md spec. Run this system for consistent and targeted content generation across campaigns, launches, events, and plays. 

The contents of this repository are a fully contained system that works in both Claude Code and Cowork. Slash commands work natively in Claude Code. In Cowork, `CLAUDE.md` includes an intent table that routes natural language to the right workflow — "build me a campaign about CISO buyers" routes to `/build campaign` automatically. Same skills, same outputs, same messaging house.

## Why MESSAGE.md?

Markets are dynamic, your messaging must be too. Context is king in the AI era, but if your messaging is stuck in static documents or if agents are running wild with no guardrails, the slop will continue. 

Product Marketers, this is your time to shine. Be the durable context layer for your entire GTM. 

## Get started

​```bash
git clone https://github.com/fortyfivan/claude-message.git my-company-messaging
cd my-company-messaging
​```

Then open the folder in **Claude Code** (`claude`) or **Claude Cowork** (Customize → Add folder). Both tools discover the skills, agents, and commands in `.claude/` automatically.

In a Claude Code session, run `/bootstrap` to populate the messaging system. The workshop runs an interactive discovery session to lock in your messaging — it takes about 30-90 minutes depending on how much source material you bring in `input/`. When it finishes, you have a complete messaging house ready for content production.

To configure the system for HTML production (web, email, print), add your brand design system at: [`docs/brand-system.md`](docs/brand-system.md).

## System design principles

**Messaging is shaped.** `messaging/` holds six pillars (Profile, Pitch, Position, People, Portfolio, Proof), eight collection types (personas, products, competitors, segments, solutions, stories, categories, reports), and asset definitions (blog-post, customer-story, etc.). `MESSAGE.md` at the repo root holds company-level attributes, ICP, glossary, brand guardrails, and the catalog of everything below. Empty after clone; `/bootstrap` populates it.

**Loading is progressive.** `MESSAGE.md` loads on every session — it's the altitude-setter for everything else. Pillars and collections load on-demand per the task. A campaign targeting CISO buyers loads People, Position, and collections/personas/ciso.md — not the whole system. Sessions stay lean even as the messaging system grows.

**Workflows are the builders.** `/build campaign`, `/build launch`, `/build play` are where multi-asset content gets produced. Each workflow runs a structured interview, assembles a brief, then orchestrates the work across subagents. The user describes intent; the workflow handles inference, dispatch, and assembly.

**Subagents do the focused work.** Workflows orchestrate; subagents execute in isolated context windows. The writer generates from a dispatch payload, the reader evaluates without bias from generation, the researcher's web content stays out of the main thread, the producer reads brand tokens without polluting messaging context. Each gets the minimum it needs.

**Production is coded.** Writer output is markdown and JSON — clean for review, ready for downstream tooling. For HTML deliverables, `brand/DESIGN.md` (per the Google Labs `DESIGN.md` spec) holds design tokens and asset references. The producer subagent reads brand context at dispatch time to generate web, email, or print HTML. Production is opt-in — repos without brand/ operate as content-only systems.

## The messaging house

The system is backed by a Messaging House, a structured document model representing a company's complete positioning and messaging narrative. The Messaging House consists of four elements, each with a distinct role. MESSAGE.md sets the altitude, pillars define the narrative, collections hold instance details, and assets define how content is produced. 

### MESSAGE.md

The always-on foundation. Loaded on every session as the altitude-setter for everything else. Contains:

- **Attributes** — company stage, type, market position, regions
- **Facts** — basics like founded date, HQ, size, funding
- **ICP** — characteristics, behaviors, and environmental context of the ideal buyer
- **Glossary** — cross-cutting terms with usage rules (company name capitalization, industry abbreviations, prohibited terms)
- **Brand Guardrails** — absolute, testable constraints that bind every output
- **Scenarios** — dimensional vocabulary for runtime context assembly (compelling event, market moment, strategic shape, content lens, topic maturity)
- **Index** — the pillars, collections, and assets in the messaging house

### Pillars

Six pillars in `messaging/pillars/`, each a narrative anchor for its respective domain:

| Pillar        | Purpose                                                   |
|---------------|-----------------------------------------------------------|
| **Profile**   | Identity, voice, lexicon, marketplace statement           |
| **Pitch**     | Strategic narrative, UVPs, differentiators                |
| **Position**  | Category claim and competitive landscape                  |
| **People**    | Audience framing, persona altitude, buying considerations |
| **Portfolio** | Product ecosystem and capability map                      |
| **Proof**     | Customer evidence and external validation                 |

Pillars are stable. They change when strategy changes, not when individual personas or competitors update.

### Collections

Eight collection types in `messaging/collections/`, each holding the specific instances a pillar references:

| Pillar    | Collections             |
|-----------|-------------------------|
| Position  | categories, competitors |
| People    | personas, segments      |
| Portfolio | products, solutions     |
| Proof     | stories, reports        |

A pillar's Collection Tables list what exists; the collection files carry the detail. A persona file describes one persona — their role, behaviors, messaging guidance, what proof resonates with them. A competitor file profiles one competitor — their positioning, differentiation against them, where they're vulnerable.

Collections are where the messaging house gets specific. They're also where it grows — adding a persona, a customer story, or a competitor doesn't require touching pillars.

### Assets

Asset definitions in `messaging/assets/` describe the structural envelope for deliverables — blog posts, customer stories, outbound emails, landing pages, one-pagers, whitepapers. Each asset declares:

- **Conventions** — structural patterns specific to this asset type (length targets, section conventions, CTA placement)
- **Frontmatter requirements** — fields needed for CMS or downstream tooling
- **Variants** — editorial calibrations for assets with meaningful variation (a blog post might have thought-leadership and use-case variants; a customer story might have anchor, mini, and video-companion)

Assets define structure; pillars and collections provide voice and content. When a workflow generates a blog post, the asset says how the content is shaped; the pillars and collections say what the content is.

## How to use this system

Three types of actions cover most of what you'll do with this system:

- **`design`** — shape the messaging (narrative, market, audience, portfolio, proof)
- **`build`** — produce content (campaigns, launches, plays, events)
- **`run`** — operate the system (health checks, research, investigations)

### Design

​```
/design pillar profile
/design persona ciso
/design competitor servicenow --research
/design message glossary

​```

Design commands edit the messaging house. `/design pillar` updates voice, narrative, positioning, or any pillar content. `/design [collection-type] [slug]` creates or updates a collection item (personas, products, competitors, segments, solutions, stories, categories, reports). `/design asset [slug]` defines a new asset type and its variants. `/design message [section]` edits a MESSAGE.md section directly. Append `--research` to dispatch the researcher subagent for external research before the interview; append `--remove` to delete with forced approval.

Each command runs a focused interview for what's changing, shows a diff, and writes atomically. Cross-reference maintenance happens automatically — removing a persona cleans up its references in pillar Collection Tables; renaming a competitor updates everywhere it's mentioned. The messaging house stays consistent without manual reconciliation.

### Build

​```
/build campaign "AI readiness for CISOs"
/build launch "container security feature"
/build play "ServiceNow displacement"
/build event "RSA 2026"
/generate blog-post "what AI buyers actually evaluate"

​```

Build commands produce content. `/build campaign` orchestrates a multi-asset campaign around a topic or theme. `/build launch` builds a release-driven launch program. `/build play` builds a competitive or account-targeted sales play. `/build event` builds a phase-distinct event program (brief + pre-event + on-site + post-event waves). `/generate` produces a single asset.

Each `/build` command runs a brief interview, then orchestrates the work: the writer subagent generates each asset in an isolated context window, the reader subagent evaluates high-stakes assets, and the producer subagent generates HTML for assets that need it. The orchestrator loads only what's needed — a campaign about CISO buyers loads People, Position, and the CISO persona, not the entire messaging house.

Each asset emerges as both `.md` (for review) and `.json` (for downstream tooling). HTML is opt-in per asset, declared in the brief.

### Run

​```
/run health
/run investigation "ServiceNow positioning shift"
/review output/campaigns/q1-launch/cisos-perspective.md

​```

Run commands operate on the system. `/run health` checks structural integrity, cross-references, and calibration of the messaging house. `/run investigation` dispatches the researcher subagent for deep external research on a topic — useful when you need market intelligence before a campaign or want to scan for competitive shifts. `/review` runs the reader subagent against a draft for messaging-alignment evaluation, independent of any build workflow.

## Skill structure

Skills cluster into four categories based on type:

- **System** — lifecycle operations on the messaging house itself (`/bootstrap`, `/run health`, `/run investigation`)
- **Workflows** — multi-step orchestrations with human-in-the-loop approval gates (`/build campaign`, `/design pillar`, etc.)
- **Tasks** — one-off operations that subagents dispatch (research-market, research-competitor, research-company)
- **Craft** — reusable patterns workflows and tasks both lean on (voice gate, review, SEO/GEO)

The distinctive thing about claude-message skills is that every skill is calibrated to the messaging system architecture, not copy-pasted from a generic skill library. Workflows know how to compose dispatch payloads for subagents working in isolated contexts. Tasks know how to load the right researcher patterns for the right kind of inquiry. Craft skills reference MESSAGE.md's brand guardrails and glossary as their source of truth, not their own internal copies.

Skills that operate against the messaging system carry a **Messaging System Reference** blurb asserting conformance, sourced from `templates/messaging-system-reference.md`. Adding a custom skill is a matter of dropping it into the right category folder, including the blurb if it operates against the messaging house, and letting natural-language routing pick it up. 

What the skill surface deliberately doesn't include: generic writing skills. The model already knows how to structure a blog post or write an email. Editorial calibration that's specific to an asset variant (a thought-leadership blog vs. a use-case blog) lives inside the asset folder at `messaging/assets/[slug]/variants/[variant].md`, not in a skill file. The result is a leaner skill surface that focuses on what's genuinely operational rather than what the model already does well.


## Inputs and outputs

### Inputs

Drop materials into `input/` and the system uses them as primary source material. 

​```
input/
├── messaging/          # existing brand guides, positioning decks, messaging frameworks
├── docs/               # PRDs, release notes, specs, pricing
├── research/           # market research, analyst reports, competitive intel
├── transcripts/        # sales calls, customer interviews, feedback
└── examples/           # content references, competitor samples

​```

Inputs are used when bootstrapping the system, but you can also directly reference during any session as additional context.

### Outputs

​```
output/
├── campaigns/[name]/
│   ├── brief.md            ← the Bill of Messaging
│   ├── 01-asset.md         ← markdown deliverable
│   ├── 01-asset.json       ← structured JSON deliverable
│   ├── 01-asset.html       ← HTML deliverable (when production is enabled)
│   └── _meta/01-asset.md   ← audit trail
├── launches/[name]/        # organized by wave
├── plays/[name]/           # organized by motion
└── single-assets/          # one-off generations

​```

Every asset emerges in multiple shapes for multiple consumers:

- **Markdown** for human review, source-of-truth audit, and copy-into-CMS workflows
- **JSON** for programmatic consumers — CMS APIs, marketing automation platforms, MCP-driven workflows
- **HTML** for direct delivery when the brand system is enabled and the asset is configured for production
- **`_meta/`** for traceability — brief spec, outline, design notes, messaging references the writer drew from, reader evaluation scores

## Built for scale

A single asset is easy. Twelve assets across a campaign without the system collapsing under its own weight is the design constraint claude-message was built around.

claude-message stays lean at multi-asset scale because the architecture takes context discipline seriously from the start:

- **Subagents work in isolated windows.** A campaign producing twelve assets dispatches twelve writer subagents, each with the minimum context needed for its specific asset. The orchestrator stays clean.
- **The messaging house loads progressively.** A CISO-focused campaign loads People and Position, not Portfolio or Proof. A product launch loads Portfolio. The system fetches what's relevant, ignores what isn't.
- **Shared context gets extracted once.** Positioning, key messages, voice anchors, and proof passages get extracted during brief assembly and inlined into every writer dispatch. No re-reading the same pillars twelve times.
- **Models match the task.** Generation runs on Sonnet because writing benefits from depth. Review, research, and production run on Haiku because focused tasks don't need it. Per-asset reader mode is configurable — light review for derivatives, full subagent dispatch for high-stakes work.

The result: a twelve-asset campaign costs closer to two single-asset generations than twelve. Latency stays predictable. Iteration stays affordable. Weekly cadence is real.

## CI

`scripts/validate.py` runs on every PR via `.github/workflows/validate.yml` to check taxonomy, no removed-command references, frontmatter linting, skill anatomy, cross-reference validity, type-file conventions, assets integrity, pillar section structure, and duplicate detection. The same script runs locally: `python scripts/validate.py`.

## Credits

Created and maintained by [Ivan Dwyer](https://github.com/fortyfivan).

## License

The MIT License (MIT)

Copyright (c) 2016 Ivan Dwyer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
