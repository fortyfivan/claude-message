# Campaign Skill

Plan multi-asset content campaigns using the Claude Message system. Assemble a bill of materials, write a structured messaging brief for human approval, then dispatch writer subagents to produce each asset with precisely scoped context.

Invoked via `/campaign [type] [topic]`.

You do not directly write content — you plan what to write, get approval, then delegate to the writer agent.

## How You Work

Four phases, with a hard approval gate between planning and production.

```
Pre-flight → Intake (interactive) → Brief (human-in-the-loop) → Production (subagent orchestration)
                                                  ↑
                                            user approval gate
```

---

## Step 0: Pre-flight

Resolve campaign type and detect resume/regeneration scenarios before entering intake.

**Campaign type resolution.** If the user provided a campaign type argument, use it. If no type specified, ask the user to choose from: digital, event, outbound, play, abm.

**Resume detection (`--continue`).** If `--continue` is passed with a campaign folder name:
1. Read the brief at `output/campaigns/[folder]/brief.md`.
2. Check asset statuses in the brief frontmatter.
3. Generate pending assets, re-generate needs-revision assets, or resume draft approval.
4. Skip directly to Production (Phase 3).

**Single asset regeneration (`--asset`).** If `--continue` is passed with a specific `--asset` flag:
1. Re-read the brief and load the asset spec.
2. Spawn a fresh writer subagent with the same context for just that asset.
3. Update the asset status in the brief.

If neither resume flag is present, proceed to Phase 1: Intake.

---

## Messaging Context Resolution

Load the full messaging house during intake to plan the brief — positioning, audience, portfolio scope, proof, and motion context. During production, writer subagents load docs per-asset for content generation.

### Core Pillars

Load all six pillars (`profile.md`, `space.md`, `audience.md`, `portfolio.md`, `proof.md`, `motion.md`) and `glossary.md` at the start of every campaign intake. Campaign planning requires the full messaging house for positioning, audience context, portfolio scope, proof matching, and motion alignment.

### Profile Table Routing

Pillar tables are the routing layer — they tell you what collection profiles exist without loading them. During intake, use these tables to present options to the user. Load full profiles only after the user confirms selections or when the campaign type requires specific profile context.

| Pillar Table | Collection Directory | Key Columns | When to Load Full Profiles |
|---|---|---|---|
| Personas table (`audience.md`) | `messaging/personas/` | Name, Description, Role | After user selects target persona(s). Always load at least one — persona is the only required profile. |
| Segments table (`audience.md`) | `messaging/segments/` | Name, Description | After user specifies a segment, or when campaign type implies segment targeting (ABM, industry-specific). Skip if campaign is segment-agnostic. |
| Products table (`portfolio.md`) | `messaging/products/` | Name, Description | After user specifies a product. Load for value props, capabilities, and use cases. |
| Solutions table (`portfolio.md`) | `messaging/solutions/` | Name, Description, Products | When campaign spans multiple products or the user references a solution rather than a single product. |
| Categories table (`space.md`) | `messaging/categories/` | Name, Description | When campaign needs category-level framing — positioning within or across market categories. |
| Competitive Landscape (`space.md`) | `messaging/competitors/` | Name, Description | When campaign is competitive (play type) or user names a competitor. Load each named competitor's profile. |
| Stories table (`proof.md`) | `messaging/stories/` | Name, Description, Products, Personas, Segments | After profile selections are confirmed. Match stories by the campaign's product-persona-segment intersection. |
| Plays table (`motion.md`) | `messaging/plays/` | Name, Description | When campaign supports a specific GTM play. Load the named play's profile. |

When tables have many rows, read frontmatter of candidate profiles to enrich intake options — adding `type`, `status`, `priority`, and `description` to help the user select before loading full profiles.

### Using Messaging Across Campaign Phases

**Intake** — Load all pillars. Present pillar tables for profile selection using AskUserQuestion. Route through tables before loading any collection profiles.

**Brief writing** — Derive the positioning statement from `profile.md` (identity) + `space.md` (positioning) + the selected product/solution doc (value prop). Extract key messages from loaded docs, each citing its source. Match proof to key messages via the Stories table cross-references (Products, Personas, Segments columns). Check glossary for term consistency across the narrative and asset specs.

**Asset manifest** — Each asset entry specifies its context resolution: shared campaign context (inherited by all assets) plus per-asset additions (extra profiles this specific asset needs). Writer subagents load these docs during production — the campaign skill resolves what to load, not the content itself.

---

## Phase 1: Intake

Intake is a structured conversation that resolves three things: campaign type, profile selections, and asset selections. Use AskUserQuestion to present options from pillar tables and the asset catalog.

### Check Input Materials

Read `input/` for files relevant to this campaign — files tagged with the campaign topic or type (e.g., `brief-q2-campaign.md`, `research-market-trends.pdf`). If relevant files exist, note them in the intake context. These supplement the messaging house during brief writing — they don't replace the intake conversation.

### Campaign Types

Each type carries a default bill of materials. Defaults are a starting point — the user customizes in asset selection.

| Type | Description | Default Assets |
|---|---|---|
| **digital** | Inbound content engine | Thought leadership blog (anchor), white paper or research report (alternative anchor), use case blog series (2-3 posts), nurture email sequence (3-5 emails), social post series, product page copy |
| **event** | Conference, webinar, or field event | Event promotion email (pre-event), event companion, session abstract, post-event follow-up email, event recap blog, social post series (pre/during/post) |
| **outbound** | Sales-driven prospecting | Cold email sequence (3-5 emails), LinkedIn message sequence, sales one-pager, competitive battlecard |
| **play** | Competitive or strategic play | Competitive battlecard, competitive blog post, objection handling guide, sales email templates, internal cheat sheet |
| **abm** | Account-based targeting | Account brief, personalized email sequence, solution page copy, sales talking points, executive summary |

If the user doesn't specify a type, ask. If they provide a description that implies a type, confirm: "This sounds like a [type] campaign. I'd suggest these assets: [default list]. Want to adjust?"

### Scenario Resolution

Each campaign type carries scenario attributes that shape the brief and asset content. Extract these from the user's input. If any are missing, use AskUserQuestion to close the gaps before proceeding to profile selection.

| Type | Attributes |
|---|---|
| **digital** | Content theme or angle? Target funnel stage (awareness, consideration, decision)? Content cadence or timeline? Anchor asset preference? |
| **event** | Event name and format (conference, webinar, field event, hosted)? Date and location? Company presence (booth, session, sponsor, keynote)? Event audience profile? |
| **outbound** | Prospecting trigger (why now)? Target account profile? Value hypothesis for this outreach? Outbound channel preference (email, LinkedIn, multi-channel)? |
| **play** | Play objective? Competitive trigger or market shift? Target win scenario? Displacement or greenfield? |
| **abm** | Target account(s)? Known stakeholders? Deal stage? Account intelligence (recent news, initiatives, tech stack)? |

Present resolved attributes back to the user for confirmation before moving to profile selection: "Here's what I understand about this campaign: [attributes]. Anything to add or correct?"

### Asset Catalog

Every asset the campaign skill can dispatch, mapped to its skill. Use this catalog when presenting the BOM to users and when resolving skill mappings during asset selection.

| Asset | Skill Category | Skill Type | Notes |
|---|---|---|---|
| Announcement blog | copywriting/blog | product-announcement | |
| Thought leadership blog | copywriting/blog | thought-leadership | Also used as anchor asset for digital campaigns |
| Use case blog | copywriting/blog | use-case-deep-dive | |
| Data study blog | copywriting/blog | data-study | Requires data/metrics from proof or input |
| Threat research blog | copywriting/blog | threat-research | Security-specific vertical content |
| Competitive blog post | copywriting/blog | thought-leadership | Competitive angle — load competitor profile |
| Press release | copywriting/blog | press-release | Dateline, quotes, boilerplate, media contact. Formal tone. |
| Cold email sequence | copywriting/email | outbound-sequence | 3-5 emails, progressive value |
| Nurture email sequence | copywriting/email | inbound-sequence | Content-led follow-up series |
| Event promotion email | copywriting/email | event-promotion | Pre-event, post-event, or multi-touch variant |
| Post-event follow-up email | copywriting/email | event-promotion | Follow-up variant of event promotion |
| Customer email | copywriting/email | product-newsletter | Existing customer announcement |
| Sales email templates | copywriting/email | single-outbound | Individual prospecting emails |
| Personalized email sequence | copywriting/email | outbound-sequence | ABM variant — higher personalization |
| LinkedIn message sequence | copywriting/email | outbound-sequence | Shorter messages, personal tone, InMail constraints (~1900 chars). 3-4 touches. |
| Solution brief | copywriting/brief | solution-brief | |
| Product datasheet | copywriting/brief | product-datasheet | |
| Sales one-pager | copywriting/brief | product-datasheet | Condensed single-page variant |
| Account brief | copywriting/brief | persona-brief | ABM account-level targeting |
| Executive summary | copywriting/brief | company-overview | |
| Use case overview | copywriting/brief | use-case-overview | |
| Industry brief | copywriting/brief | industry-vertical | |
| Event companion | copywriting/brief | event-companion | Leave-behind or session handout |
| Session abstract | copywriting/brief | session-abstract | 150-word abstract: problem framing, session scope, attendee takeaways. |
| LinkedIn post | copywriting/social | linkedin-post | |
| LinkedIn article | copywriting/social | linkedin-article | Long-form LinkedIn content |
| X post | copywriting/social | x-post | |
| X thread | copywriting/social | x-thread | Multi-post narrative |
| Social post series | copywriting/social | linkedin-post, x-post | Multi-platform bundle — generates one of each |
| Competitive battlecard | copywriting/enablement | competitive-battlecard | |
| Discovery guide | copywriting/enablement | discovery-guide | |
| Playbook walkthrough | copywriting/enablement | playbook-walkthrough | |
| Sales talking points | copywriting/enablement | discovery-guide | Scannable reference: situation trigger, core message, proof point, pivot to next step. |
| Objection handling guide | copywriting/enablement | competitive-battlecard | Objection-response pairs: objection, why it comes up, response framework, proof to cite. |
| Internal cheat sheet | copywriting/enablement | competitive-battlecard | One-page internal reference: differentiators, landmine questions, competitive traps, talk track. |
| White paper | copywriting/paper | topic-deep-dive | Long-form authority content |
| Research report | copywriting/paper | research-study | Original research with data and analysis |
| Industry report | copywriting/paper | industry-trend | Market landscape or trend analysis |
| Data findings report | copywriting/paper | data-findings | Data-driven insights and benchmarks |
| Product page copy | copywriting/web | product-page | Product-focused web/landing page |
| Solution page copy | copywriting/web | solution-page | Solution-focused web page |
| Comparison page | copywriting/web | comparison-page | Bottom-funnel competitive page |
| Topic page | copywriting/web | topic-page | Long-form SEO pillar page |
| Event recap blog | copywriting/blog | event-recap | Post-event content, SEO fuel |
| Predictions blog | copywriting/blog | predictions | Forward-looking thought leadership |
| Partner better together brief | copywriting/brief | partner-better-together | External joint value proposition for co-sell |
| Partner joint solution guide | copywriting/enablement | partner-joint-solution | Internal partner business case |
| Business value assessment | copywriting/assessment | business-value | ROI/value case framework |
| Risk assessment | copywriting/assessment | risk | Risk evaluation framework |
| Tech assessment | copywriting/assessment | tech | Technical readiness assessment |
| Customer story | copywriting/story | customer | Published case study |
| Partner story | copywriting/story | partner | Joint proof asset |

### Profile Selection

Resolve the messaging context that applies to the campaign as a whole. These become the **shared context** that every asset inherits. Use the pillar table routing from the Messaging Context Resolution section to discover and present options.

| Parameter | Question to resolve | Multi-select? |
|---|---|---|
| **Persona(s)** | Who is this campaign targeting? | Yes — different assets may target different personas. **Required.** |
| **Product/Solution** | What offering is being campaigned? | Usually one, sometimes multiple for portfolio campaigns |
| **Category** | What market category frames this campaign? | Usually one |
| **Competitor** | Is this competitive? Against whom? | Yes — a play campaign might address multiple competitors |
| **Segment** | Is this segment-specific? | Usually one |
| **Play** | Is this supporting a specific GTM play? | Usually one |

All parameters are optional except Persona. Resolve what the task implies — don't force every parameter for every campaign.

For each parameter, load the relevant pillar and present the collection reference table with Descriptions for user selection rather than asking open-ended questions. Example: "I found 4 personas in the messaging house: [table rows with Descriptions]. Which should this campaign target?"

If the user names a specific entity, match against the table. If the user gives a descriptive reference, match against the Description column. If no match exists, flag it: "There's no CISO persona in the messaging house. Want me to create one first with the compose command, or proceed using the audience-level context from `audience.md`?"

Some campaigns target multiple personas across different assets. A launch campaign might have a CISO email, a DevOps blog post, and an executive press quote. Each asset gets its own persona assignment — this is resolved in the asset manifest, not at the campaign level. But the campaign-level persona list defines the universe of personas this campaign addresses.

### Asset Selection

Present the default BOM for the resolved campaign type as a numbered checklist with skill mappings visible. Use AskUserQuestion to walk through the list interactively.

```
Default assets for [type] campaign:

 1. Announcement blog          → copywriting/blog / product-announcement
 2. Press release              → copywriting/blog / product-announcement
 3. Customer email             → copywriting/email / product-newsletter
 4. Social post series         → copywriting/social / linkedin-post, x-post
 5. Sales talking points       → copywriting/enablement / discovery-guide
 6. Product page copy          → copywriting/web / product-page

Options: Add / Remove / Modify / Reassign / Custom
```

The user can:

- **Add** — Select from the asset catalog or describe a custom asset.
- **Remove** — Drop assets they don't need.
- **Modify** — Scope changes. "Make the blog series 4 posts instead of 2."
- **Reassign** — Per-asset persona targeting. "The email sequence should target CISOs but the blog posts should target DevOps leads."
- **Custom** — Assets not in the catalog. Work with the user to identify the closest skill mapping and add it to the manifest with adaptation notes.

For each asset, verify the skill exists in `.claude/skills/tasks/`. If missing, flag it: "There's no skill for 'copywriting/blog/thought-leadership' in `.claude/skills/tasks/`."

Confirm the final asset list before proceeding to the brief.

### Intake Output

By the end of intake, you have:

- Campaign type and name
- Campaign objective (one sentence)
- Shared profile selections (personas, products, competitors, segments)
- Final asset list with per-asset persona assignments and skill mappings
- Flagged gaps (missing personas, missing skills, thin messaging context)

---

## Phase 2: Messaging Brief

The brief is the plan. Generate the folder name from a kebab-case topic slug + current date (mm-dd-yy) — e.g., `product-launch-03-17-26`. Write it to `output/campaigns/[topic-mm-dd-yy]/brief.md`. The user must approve it before production begins.

### Brief Frontmatter

Write YAML frontmatter with:

- `campaign_name` — Semantic kebab-case identifier (e.g., `product-launch-q1`)
- `campaign_folder` — Actual directory name: kebab-case topic slug + date (e.g., `product-launch-03-17-26`)
- `campaign_type` — One of: digital, event, outbound, play, abm (or "custom")
- `objective` — One-sentence campaign goal
- `created` — Date string
- `status` — "draft" initially, "approved" after gate, "in-progress" during production, "complete" when done
- `shared_context` — Personas, products, competitors, segments, and `messaging_docs_loaded` list
- `assets` — Array of asset entries, each with: id, type, skill, title, persona, altitude, depends_on, status

### Brief Body

#### Campaign Narrative

The through-line that unifies every asset. Derive from the messaging house using the Messaging Context Resolution section.

**Positioning statement** — 2-3 sentences. The core argument. Derived from `profile.md` (identity) + `space.md` (positioning and differentiation) + the relevant product/solution doc (value prop). This is not invented — it is assembled from existing messaging components.

**Key messages** — 3-5 specific claims the campaign makes. Not taglines — grounded assertions. Each key message follows this structure:

1. **State the claim** — A specific, defensible assertion.
2. **Cite the source** — The messaging doc(s) it derives from.
3. **Note supporting proof** — Matching stories from `proof.md` via the Stories table cross-references, or flag "No proof available — consider adding a customer story."
4. **Indicate asset emphasis** — Which assets in the manifest emphasize this message.

Load `messaging/glossary.md` when writing the campaign narrative. Key terms used in the narrative should align with glossary definitions. If the campaign introduces terms not in the glossary, note them for the user — the glossary may need updating after the campaign is produced.

```markdown
## Campaign Narrative

**Positioning:**
[Core argument derived from profile.md, space.md, and product doc]

**Key Messages:**

1. **[Capability claim]** — [Specific capability claim].
   _Source: [messaging doc path(s)]_
   _Proof: [story name] or "No proof available"_
   _Assets: [asset IDs that emphasize this message]_

2. **[Differentiation claim]** — [Unique method/approach claim].
   _Source: [messaging doc path(s)]_
   _Proof: [story name] or "No proof available"_
   _Assets: [asset IDs that emphasize this message]_

3. **[Outcome claim]** — [Customer outcome/metric claim].
   _Source: [messaging doc path(s)]_
   _Proof: [story name] or "No proof available"_
   _Assets: [asset IDs that emphasize this message]_
```

#### What to Know

A shareable internal primer that synthesizes the campaign for anyone who needs to understand or support it — sales reps, field marketers, executives, partner teams. Derived from the loaded messaging context, not invented.

**Campaign context** — Why this campaign, why now. The market trigger, customer signal, or business event driving the campaign. 2-3 sentences.

**Who we're talking to** — Target persona(s) in plain language. What they care about, what's keeping them up at night, where they are in the buying process. Drawn from the selected persona profile(s).

**What we're saying** — The 3-5 key messages distilled into conversational language. Not taglines — what you'd say in a meeting. Each grounded in the messaging house.

**How we're different** — The competitive angle in 2-3 sentences. What alternatives the audience is considering and why our approach wins. Drawn from `space.md` and competitor profiles if loaded.

**Proof we can point to** — The matched customer stories, metrics, and evidence. What to reference when asked "who else does this?" Drawn from `proof.md` and loaded stories.

**Common objections** — 2-4 likely pushbacks and how to address them. Drawn from persona pain points, competitive positioning, and product messaging.

#### Asset Manifest

For each asset, specify:

- **Skill** — Category/type mapping from the asset catalog
- **Persona** — Target audience for this asset
- **Altitude** — Depth calibration (executive, practitioner, technical, consultative)
- **Dependencies** — Asset IDs that must be generated first
- **Context Resolution** — Which messaging docs this asset loads beyond shared campaign context
- **Narrative Thread** — Which key messages this asset emphasizes and what angle it takes
- **Notes** — Anything the writer needs to know (anchor asset designation, cross-references, format guidance, adaptation instructions)

#### Generation Sequence

Order assets by dependency graph into waves. Assets with no dependencies go in Wave 1 and can be generated in parallel. Subsequent waves wait for their dependencies to complete.

### Approval Flow

After writing the brief, present a summary:

```
Campaign: [Name]
Type: [type]
Objective: [one sentence]

Shared Context:
  Personas: [list]
  Products: [list]
  Competitors: [list]
  Messaging docs: [count] pillar/collection docs loaded

Assets ([count]):
  1. [title] ([persona], [altitude]) → [skill category/type]
  2. [title] ([persona], [altitude]) → [skill category/type] → depends on #N
  ...

Generation: [N] waves
Flagged issues: [count or "None"]

Ready to generate? You can also edit the brief directly at
output/campaigns/[folder]/brief.md and tell me when you're done.
```

The user can:

- **Approve** — Production begins.
- **Edit** — Modify the brief through conversation or by editing the file directly and telling you to re-read it.
- **Cancel** — Brief stays as a draft. Resume later with the campaign command using `--continue [folder]`.

---

## Phase 3: Composition

After approval, update the brief status to `in-progress` and generate assets by wave.

### Writer Subagent Dispatch

For each asset, spawn a writer subagent with five pieces of context:

| Context | Source | Purpose |
|---|---|---|
| Campaign narrative | Brief body, narrative section | Shared through-line every asset inherits |
| Asset spec | Brief body, asset manifest entry | Per-asset context resolution, narrative thread, altitude, notes |
| Shared messaging docs | Resolved from brief frontmatter `shared_context.messaging_docs_loaded` | Baseline messaging context |
| Asset-specific messaging docs | Resolved from asset manifest context resolution | Per-asset messaging additions |
| Dependency assets | File content from previously generated assets in `output/campaigns/[folder]/` | Narrative continuity |

The writer agent runs in campaign mode — using the campaign brief as its primary input rather than resolving context from scratch. It derives its asset brief from the campaign narrative and asset spec, loads the skill, cross-references for consistency, generates the draft, validates against the voice gate (max 2 voice passes), writes to disk, dispatches the reader for formal review, and iterates on reader feedback autonomously (max 1 post-reader revision). Only "Major rework" verdicts are surfaced to the campaign orchestrator. The writer skips user approval on the asset brief since the campaign brief was already approved. If the writer flags critical gaps or conflicts, it surfaces them rather than blocking.

Do not override the writer's quality checks. If a writer flags an issue, surface it to the user.

### Dependency Handling

When an asset has dependencies, pass the generated content from dependency assets as reference context. The writer uses this for narrative continuity — referencing rather than duplicating.

For large campaigns (10+ assets), pass dependency content as summaries rather than full files. Extract key arguments, positioning statements, and CTAs from each dependency asset.

### Output Structure

```
output/campaigns/
  [topic-mm-dd-yy]/
    brief.md
    asset-01-[slug].md
    asset-02-[slug].md
    ...
    assets/              <- produced deliverables (if any)
```

Each asset file includes metadata frontmatter linking back to the campaign (campaign_name, campaign_folder, asset_id, type, skill, persona, altitude, key_messages, messaging_docs_loaded, dependency_assets, generated date, status).

### Progress Tracking

As each wave completes:

1. Update each asset's status in the brief frontmatter (`pending` → `complete` or `needs-revision`). An asset arrives as `complete` when the writer resolved the reader's feedback internally (including "Needs revision" verdicts handled via post-reader revision). An asset arrives as `needs-revision` only when the reader returned "Major rework" and the writer escalated.
2. Check for writer-flagged issues. If any exist, surface them to the user between waves.
3. Proceed to the next wave.

After all waves complete:

1. Update brief status to `complete`.
2. Present a completion summary with per-asset status, flagged issues, total messaging docs loaded, and the campaign directory path.

### Post-Campaign Learning

After all assets are generated and the campaign is marked complete, review the execution for process learnings. Append a journal entry to `messaging/journal.md` with type "process." Create the file from `templates/messaging/journal.md` if it doesn't exist.

### Production Offer

After all assets are generated and marked complete, offer to produce finished deliverables:

1. Present the list of completed assets via AskUserQuestion: "Would you like to produce finished deliverables for any of these assets? Select which ones, or skip to finish."
2. For each selected asset, invoke the producer agent with the asset file path.
3. Produced files go to `output/campaigns/[folder]/assets/`.
4. If the user skips, note that they can run `/produce --campaign [folder]` later to produce deliverables at any time.

---

## Iteration

### Single Asset Regeneration

Re-dispatch a specific asset by running the campaign command with `--continue [folder] --asset [asset-id]`. Re-read the brief, load the asset spec, and spawn a fresh writer subagent with the same context.

### Adding Assets

Edit the brief to add new asset entries, then run the campaign command with `--continue [folder]`. Detect assets with `status: pending` and generate only those, treating existing complete assets as available dependencies.

### Brief Revision

If the campaign narrative shifts, the user edits the brief and re-runs production. Re-generate all assets whose context was affected by the change. Assets unaffected keep their `complete` status.

---

## Edge Cases

**Skill not found for an asset.** During brief generation, check that every asset's specified skill exists in `.claude/skills/`. If missing, flag it and suggest alternatives.

**Persona not in messaging house.** Flag during intake. Suggest running the compose command first. If the user wants to proceed, fall back to pillar-level audience context from `audience.md` and note the limitation in the brief.

**Context window pressure.** Large campaigns (10+ assets) may strain the context window. Track assets by file path rather than holding full content in memory. When dispatching a writer with dependencies, extract key arguments and CTAs from dependency assets rather than passing full content.

**Partial production failure.** If a writer subagent fails, produces poor output, or the reader flags it as "Major rework," mark that asset as `needs-revision` in the brief and continue with the next wave. Assets in later waves that depend on the failed asset receive a note that their dependency is flagged.

**Asset not in catalog.** Work with the user to identify the closest skill mapping and add it to the asset manifest with adaptation notes.

**Campaign type not listed.** Propose a custom BOM using the asset catalog. Present the full catalog and build the manifest from the user's selections.