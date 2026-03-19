# Prompt

Before we move on, I really want to hone in on the right information architecture. There's a lot at play here, and I want to find the right use of agents and skills. 

For instance, I recently learned that skills can be invoked directly via slash, replacing the need for slash commands that invoke skills.

If I were to look at the entire product marketing function from it's core, the information architecture can be broken down as follows:

Context - messaging & positioning, CRM, research, sales & marketing tools, JIRA, etc.

Programs - content, compete, enablement, NPI, pricing & packaging, business value, etc.

Workflows - design (bootstrap), campaign, launch, etc.

Artifacts - roadmap, pitch, plays, etc.

Tasks - research, analyze, write, read, etc.

Assets - papers, web, briefs, blogs, email, social, videos, etc.

Delivery - documents, web, apps, automation, etc.

---

The question becomes what goes where in the Claude Code harness?

# Response

This is the right question to pause on. Let me map each layer to what Claude Code actually offers before we build more into the wrong containers.

**Claude Code primitives available:**
- CLAUDE.md — persistent project context
- Skills — executable, interactive (main session)
- Agents — executable, non-interactive (subagents)
- MCP servers — external tool connections
- Filesystem — state and content layer

---

**The mapping:**

| IA Layer | Claude Code Primitive | Notes |
|---|---|---|
| **Context** | CLAUDE.md + filesystem + MCP | Messaging house is filesystem. CRM, JIRA, tools are MCP. This layer is already well-handled. |
| **Programs** | Nothing native | Programs need persistence and scheduling. Neither exists in Claude Code without infra. This layer belongs in the hosted edition. |
| **Workflows** | Skills | Campaign, Launch, Assessment, Response. Interactive, stateful, gate-driven. |
| **Artifacts** | Filesystem + Workflow Skills | Artifacts are created by Workflows and live in the filesystem. A roadmap is an output of a Launch workflow, maintained by subsequent runs. |
| **Tasks** | Skills (task layer) + Agents | Task Skills define the craft. Writer agent executes them with scoped context. |
| **Assets** | Filesystem | The content output layer. Lives in `output/`. Produced by Task Skills via the writer agent. |
| **Delivery** | External to Claude Code | Documents (docx/pdf), web, apps, automation. This is the UI layer or downstream tooling — not a Claude Code concern in the open-source edition. |

---

**What this reveals:**

Three layers map cleanly — Context, Workflows, Tasks. These are where the Claude Code harness is strong and where you've been building correctly.

Two layers are filesystem outputs — Artifacts and Assets. They don't need their own primitive; they need consistent directory conventions and naming so Workflows can find and reference them.

Two layers are gaps — Programs and Delivery. Programs require infrastructure that violates the zero-infra constraint. Delivery is downstream of Claude Code entirely — it's the job of the web UI, the docx/pptx skills, or MCP integrations.

---

**The implication for what you've built:**

The skill architecture you have is correct for the Workflows and Tasks layers. The directory structure (`workflows/`, `tasks/`) reflects the real distinction. The writer agent is the right bridge between the two.

The gap is that Programs have been creeping into the design — CI, Win/Loss as recurring analysis, VOC — and none of those have a clean home in Claude Code today. Deferring them was the right call.

**Proposed harness, stated simply:**

```
CLAUDE.md          → project configuration + context pointers
messaging/         → context layer (filesystem)
research/          → context layer (filesystem)
.claude/skills/
  workflows/       → Campaign, Launch, etc.
  tasks/           → all copywriting skills
.claude/agents/
  writer.md        → single-task execution, no interactivity
output/            → assets and artifacts produced by workflows
input/             → user-provided materials per workflow run
```

MCP connections extend Context when available. The web UI is the Delivery layer. Programs wait for the hosted edition.

Does this framing hold against your IA, or do you see layers that still don't have a home?

# Prompt 2

Of our tasks, what do you think makes sense as a single-task execution? In my mind it's: 

* researcher: spawn a subagent to run a market, compete, other research exercise. Heavy use of web search and parsing files in research
* writer: spawn a subagent to generate the content asset based on the specific copywriting skill
* reader: spawn a subagent to assume a target persona and evaluate against set criteria
* producer: spawn a subagent to take a content asset to it's last-mile design and packaged artifact

I feel like anything analysis related is for the main agent. How does this sound?

# Response 2

The four subagents are well-reasoned and the instinct about analysis is exactly right. Here's how it maps:

**Subagents — no interactivity needed, single contained task:**

| Agent | Job | Key Tools |
|---|---|---|
| **researcher** | Gather and synthesize information from web and files into a structured research doc | WebSearch, WebFetch, Read, Write |
| **writer** | Generate a content asset from a scoped brief and copywriting skill | Read, Write |
| **reader** | Evaluate a draft against a persona and criteria set, return structured feedback | Read, Write |
| **producer** | Take a content asset to last-mile format — docx, pdf, pptx | Read, Write, Bash |

**Main agent — analysis stays interactive because it requires judgment and iteration:**

Things like win/loss trend synthesis, BVA calculation logic, competitive positioning analysis, pricing recommendations. These aren't single-task — they involve the agent forming an interpretation, presenting it, getting pushback, revising. That loop requires the main session.

**One thing to validate:** Reader and Producer are net-new agents you don't have yet. Reader in particular is interesting — it closes the quality loop inside a workflow without requiring human review of every asset. Writer produces, Reader evaluates against persona and criteria, flags issues back to the workflow skill, which surfaces only what needs human attention. That's a meaningful upgrade to the Campaign and Launch production phases.

Producer assumes the docx/pptx skill layer exists. Is that built yet, or is it still on the horizon?

# Prompt 3

Now for the Skills. Workflows and Tasks feel right, what about adding Lifts? This might be something like a design skill, or a slop filter skill - things that are subject matter experts within a specific task.

# Response 3

Lifts is the right name for the right concept. They're not workflows, they're not content generators — they're modular expertise that gets composed into other skills to raise the quality ceiling.

The distinction:

| Category | Job | Invoked by |
|---|---|---|
| **Workflows** | Orchestrate a multi-phase process | User via slash |
| **Tasks** | Generate a specific content asset | Writer subagent |
| **Lifts** | Apply specialized expertise to improve an output | Tasks, Workflows, or subagents |

Lifts don't produce standalone outputs — they augment what Tasks and Workflows produce. A slop filter doesn't write anything, it makes what was written better. A design lift doesn't create content, it makes an asset presentation-ready.

Candidates:

- **Slop filter** — strips clichés, passive constructions, AI-sounding language before an asset ships
- **Design** — layout and visual hierarchy guidance for Producer
- **SEO** — keyword and structure optimization applied to web copy tasks
- **Persona calibration** — sharpens voice and altitude for a specific reader, applied by Reader or Writer
- **Accessibility** — applied to any external asset before delivery
- **Readability** — Flesch-Kincaid or equivalent, applied to long-form assets

```
.claude/skills/
  workflows/
  tasks/
  lifts/
    slop-filter/
    design/
    seo/
    persona-calibration/
```

The slop filter in particular should probably run inside every writer subagent dispatch by default — not optional, just part of what Writer does before writing the file. Same way Reader is a quality gate, slop filter is a craft gate.

Does Lift feel like the right term, or do you want something that signals the SME angle more explicitly — something like **Craft** or **Lens**?

# Prompt 4

Ooh, I like Craft a lot!

# Response 4

.claude/skills/
  workflows/
    campaign/
    launch/
    assessment/
    response/
  tasks/
    blog-copywriting/
    email-copywriting/
    enablement-copywriting/
    paper-copywriting/
    social-copywriting/
    web-copywriting/
  craft/
    slop-filter/
    design/
    seo/
    persona-calibration/
    readability/
    accessibility/

# Prompt 5

I wonder if Tasks are too loaded with copywriting. What else fits here?

# Response 5

Good challenge. Tasks are any single-execution, bounded operation with a defined input and output — copywriting is just the most obvious example. Expanding the lens:

**Research tasks** — though these might live under the researcher subagent rather than as standalone skills. Worth clarifying the boundary.

**Analysis tasks** — summarize a document, extract themes from a set of files, score a draft against criteria, compare two positioning docs. These are bounded analytical operations, not full analysis workflows.

**Transformation tasks** — translate a long-form asset into a different format (blog → LinkedIn post, whitepaper → executive summary, transcript → structured notes). Different from writing from scratch — the source material is the input.

**Evaluation tasks** — the reader persona evaluation, a messaging consistency check, a terminology audit against the glossary. These could live under Craft but they're more operational than quality-raising.

**Extraction tasks** — pull structured data from unstructured inputs. Win/loss signals from a call transcript, product claims from a competitor's website, proof points from a customer story.

So Tasks might be better named by what they do rather than what they produce:

```
.claude/skills/
  workflows/
  tasks/
    write/          ← all copywriting types
    transform/      ← format and length transformations
    extract/        ← structured extraction from unstructured input
    evaluate/       ← scoring and assessment against criteria
  craft/
```

The question is whether `write/` is the right home for copywriting or whether copywriting is already well-named as its own category. My instinct is keep the copywriting naming — it's specific and searchable — and add the missing task types alongside it:

```
tasks/
  blog-copywriting/
  email-copywriting/
  enablement-copywriting/
  paper-copywriting/
  social-copywriting/
  web-copywriting/
  transform/
  extract/
  evaluate/
```

Does that feel like the right expansion, or do you want to normalize the naming so everything under tasks follows the same convention?

# Prompt 6

Good call - I actually already moved all the copywriting skills under a single folder. 

Where would production tasks go? Things like PPT or Web - assume under tasks?

# Response 6

Yes, tasks — but production is distinct enough from copywriting that it warrants its own folder rather than sitting alongside it.

```
tasks/
  copywriting/
    blog/
    email/
    enablement/
    paper/
    social/
    web/
  production/
    pptx/
    docx/
    pdf/
    web/
  transform/
  extract/
  evaluate/
```

The distinction between copywriting and production maps cleanly to the subagent boundary too. Writer invokes copywriting tasks to generate content. Producer invokes production tasks to package that content into its final format. Two different subagents, two different task categories, clean separation.

One naming collision to resolve: `tasks/copywriting/web/` and `tasks/production/web/` will feel ambiguous. Web copywriting is page copy — words. Web production is a rendered artifact — HTML, a landing page, an app. Worth being explicit:

```
tasks/
  copywriting/
    web-copy/       ← product page, solution page copy
  production/
    web-app/        ← rendered HTML artifacts
    pptx/
    docx/
    pdf/
```

The other thing production tasks share with copywriting tasks is that they're both invoked by subagents with scoped context — Writer for copy, Producer for format. So the skill structure inside each production type should follow the same pattern as copywriting: a SKILL.md with type-specific instructions, not a full workflow.

Does this match where you moved the copywriting skills, or does the folder consolidation change the routing logic?

# Prompt 7

This looks good. Are we missing anything?

# Response 7

Looking at the full picture a few things stand out:

**Bootstrap is unplaced.** It's a workflow skill but hasn't been added to `workflows/`. It's the most foundational workflow in the system — should be explicit.

**Maintenance workflows have no home.** The health and tune agents — glossary generation, messaging freshness checks, skill calibration — don't fit cleanly into workflows, tasks, or craft. They're system-level operations, not PMM-facing workflows. A `system/` or `maintenance/` folder under skills, or keeping them as agents, is worth deciding explicitly.

**Commands need a rethink.** If skills can now be invoked directly via slash, the commands layer is partially redundant. The remaining value of a command is pre-flight logic — input validation, resume handling, context setup — before the skill runs. Launch is the model: the command gates, the skill executes. Worth auditing which commands are just passthrough invocations (candidates for removal) versus which add genuine pre-flight value (keep).

**The writer agent has no routing map.** Writer receives a skill reference from the workflow brief and needs to resolve it to a file path in `tasks/copywriting/`. That routing logic should live somewhere explicit — either in the writer agent definition or a shared routing table — rather than being implied.

**MCP connections aren't represented.** The context layer is filesystem today, but MCP slots are where CRM, JIRA, and other tools will connect. Worth a placeholder in the structure even if the integrations aren't built yet.

```
.claude/
  agents/
    writer.md
    researcher.md
    reader.md
    producer.md
  skills/
    workflows/
      bootstrap/
      campaign/
      launch/
      assessment/
      response/
    tasks/
      copywriting/
      production/
      transform/
      extract/
      evaluate/
    craft/
      slop-filter/
      design/
      seo/
      persona-calibration/
      readability/
      accessibility/
    system/
      health/
      tune/
  settings.json     ← MCP server configuration
```

Does the system/ folder feel right for health and tune, or do those stay as agents?

# Prompt 8

System is a great call, that rounds it out. Bootstrap is a workflow, just not listed here.

# Response 8

.claude/
  agents/
    writer.md
    researcher.md
    reader.md
    producer.md
  skills/
    workflows/
      bootstrap/
      campaign/
      launch/ 
      assessment/ 
      response/ 
    tasks/
      copywriting/
        blog/
        email/
        enablement/
        paper/
        social/
        web-copy/
      production/
        pptx/
        docx/
        pdf/
        web-app/
      transform/
      extract/
      evaluate/
    craft/
      slop-filter/
      design/
      seo/
      persona-calibration/
      readability/
      accessibility/
    system/
      health/
      tune/
  commands/
    launch.md
    [others with genuine pre-flight value]
  settings.json

# Prompt 9

Here's another one - we currently have a feedback agent and an investigate agent. From our reflection here, I think these are workflow skills, but pasting here to see if you agree.

# Response 9

Both are workflow skills, but for different reasons — and one is a cleaner conversion than the other.

**Feedback** is straightforwardly a workflow skill. It's interactive by design — it parses input, proposes changes, and gates on user approval before executing. AskUserQuestion is central to the approval flow. Converting it to a skill is the same logic as Campaign and Launch.

**Investigate** is trickier. Look at what it actually does: it dispatches the researcher subagent, processes findings, manages tracker state, and presents a review dashboard. The Scan and Targeted modes are non-interactive — they could run as an agent or even headlessly. But Review mode uses AskUserQuestion for insight state transitions. So it has the same AskUserQuestion exposure as everything else.

The stronger argument for Investigate as a skill is consistency — if the rule is "anything with AskUserQuestion runs in the main session as a skill," Investigate qualifies. And the orchestration it does (dispatching researcher, managing tracker) is no different from how Campaign dispatches writer.

One nuance: Investigate has a scheduled execution section with a cron pattern. That's Program thinking — it assumes autonomous, non-interactive runs. That mode doesn't belong in a skill and probably doesn't belong in the open-source edition at all, for the same reasons Programs were deferred. Worth removing that section and treating Investigate as human-triggered only.

So: both become workflow skills, cron block removed from Investigate. They'd sit alongside Campaign and Launch:

```
workflows/
  bootstrap/
  campaign/
  launch/
  assessment/
  response/
  feedback/
  investigate/
```

Agreed?

# Prompt 10

This might be a larger conversation, but I do wonder about consolidating a few of the commands and agents that all do some form of messaging assessment - like a health check, a feedback inquiry, an investigation, etc. For simplicity sake, a single insights tracker is the way to go with many things feeding it. Table this or tackle now?

# Response 10

Tackle it at the architecture level now, build later. You have enough context in this session to make the decision cleanly — coming back to it cold means re-establishing all of this.

The consolidation case is strong. You currently have:

- **health** — messaging freshness and glossary checks
- **feedback** — field signal processing and proposed changes
- **investigate** — market and competitive research, tracker management
- **tune** — skill calibration against the messaging house

All four touch the messaging house, all four write to the insights tracker, all four produce journal entries. The user experience is fragmented — three different commands to get a picture of messaging health.

The consolidated model: **a single `insights` workflow skill** with modes.

```
/insights scan          → investigate: broad research run
/insights target [x]   → investigate: focused entity research  
/insights feedback      → feedback: process a field signal
/insights review        → health + tracker review dashboard
/insights tune          → calibrate skills to messaging house
```

Single entry point, single tracker, single journal convention. The subagent layer stays the same — researcher still does the research, the skill just routes to it. Feedback processing stays the same — it's just a mode now.

Tune is the one to think about. It's more of a system maintenance operation than an insights operation. Could stay separate under `system/` alongside health, or get pulled into insights as a mode. The question is whether a PMM thinks of tuning as part of their insights workflow or as a separate admin task.

My read: table the build, lock the decision. Insights becomes a single workflow skill with modes. Tune stays in system/. Health folds into the insights review mode. Does that framing hold?

# Prompt 11

I like that, but I would keep tune as a system agent as it's more focused on rewriting skill files than it is surfacing insights

# Response 11

.claude/
  agents/
    writer.md
    researcher.md
    reader.md
    producer.md
  skills/
    workflows/
      bootstrap/
      campaign/
      launch/
      assessment/
      response/
      insights/        ← consolidates investigate + feedback + health review
    tasks/
      copywriting/
      production/
      transform/
      extract/
      evaluate/
    craft/
      slop-filter/
      design/
      seo/
      persona-calibration/
      readability/
      accessibility/
    system/
      health/
      tune/
  settings.json



