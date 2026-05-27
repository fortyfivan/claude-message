---
name: design-asset
description: Full lifecycle (create, update, remove) for asset definitions and their variants. Variants live inside the asset folder (`messaging/assets/[slug]/variants/[variant].md`); the relationship is structural, not declared. Maintains MESSAGE.md `## Assets` routing on every operation.
---

# Design Asset

Full lifecycle for asset definitions plus their optional variants. Variants live inside the asset folder — no bidirectional refs to maintain; the relationship is structural by directory.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, ICP, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona") and follows the file path conventions in CLAUDE.md. If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

Invoked via `/design asset [slug]`. Branches on file existence, `--remove`, `--add-variant`, and `--remove-variant`.

## Modes

| Invocation | Behavior |
|---|---|
| `/design asset [slug]` (folder doesn't exist) | **Create flow.** Two-phase interview (identity + envelope) → optional variant phase → generate atomically. |
| `/design asset [slug]` (folder exists) | **Update flow.** Load asset + existing variants → focused interview → regenerate. |
| `/design asset [slug] --add-variant [name]` | **Add variant flow.** Asset must exist. Interview variant specifics → generate `variants/[name].md` → optionally set as default. |
| `/design asset [slug] --remove` | **Remove asset flow.** Enumerate impact (routing row, variant files) → preview → "confirm" → atomic deletion → audit log. |
| `/design asset [slug] --remove-variant [name]` | **Remove variant flow.** Variant must exist. Preview → "confirm" → delete the single variant file. If it was the default, prompt for replacement. |
| `/design asset [slug] --research` | Adds web-search-driven calibration to any flow. |

## Asset folder shape

```
messaging/assets/[slug]/
├── asset.md              # deliverable envelope (structure, conventions, frontmatter, CTA)
└── variants/             # optional; only for assets with meaningful editorial variation
    ├── use-case.md       # variant: when to use, voice notes, structure pattern, examples
    ├── thought-leadership.md
    └── product-announcement.md
```

Asset frontmatter declares `default-variant: "use-case"` when variants exist; empty string when the asset is atomic (e.g., outbound-email, press-release, social-post-linkedin).

## Create flow

### Step 1: Detect

Folder `messaging/assets/[slug]/` does not exist → proceed.

### Step 2: Two-phase interview (asset envelope)

**Phase A — Identity:**
- Brief description? (One-line summary of the asset.)
- Content type for routing? (E.g., `blog`, `landing-page`, `outbound-email`. Determines the row in MESSAGE.md `## Assets`. Either matches an existing content type or introduces a new one.)
- Is this a default for the content type, or an alternative? (Affects how it lands in the routing table.)
- Does this asset have meaningful editorial variants (use-case vs. thought-leadership for blogs, mini vs. anchor for stories), or is it atomic (one shape)? Determines whether to run Phase C.

**Phase B — Deliverable envelope (company conventions for this asset type):**
- What's the publishing destination? (HubSpot, WordPress, custom CMS — populates `publishing` field.)
- What frontmatter fields does it require? (Populates `content-keys` array; flag which serialize as JSON arrays into `array-keys`.)
- What are the company-wide conventions for this asset type — length norms, image cadence, sign-off style, platform quirks? (Populates Conventions section.)
- For **atomic** assets only (Phase A signaled no variants): Structural section sequence + CTA conventions. (Populates `## Structure` and `## CTA conventions` in asset.md.)

For variant-likely assets, Phase B asks only Conventions + Frontmatter requirements. Structure and CTA conventions move to Phase C (per-variant) — these vary by editorial intent.

Cap each phase at 4-5 questions. If `--research` was passed, dispatch the researcher subagent first (task_type `generic`) to scrape the user's CMS public docs for required fields and conventions, then narrow the interview to fill gaps.

### Step 3: Optional Phase C — Default variant

Only if Phase A signaled variants. Single round of questions for the default variant — these populate `messaging/assets/[slug]/variants/[variant].md`:

- Variant name (slug)? (E.g., `use-case`, `default`.)
- When does this variant apply vs. siblings? (Populates `## When to use` section.)
- What's the voice register specific to this variant? (Populates `## Voice notes` — variant-specific shifts on top of MESSAGE.md Brand Guardrails + profile.md voice.)
- Full structural section sequence for this variant? (Populates `## Structure` — variants own this; the envelope doesn't.)
- CTA placement, destination, and button text patterns for this variant? (Populates `## CTA conventions` — variants own this too; CTAs vary by editorial intent.)
- Reference examples? (Populates `## Examples` section.)

Sets `default-variant: [slug]` in asset frontmatter. Adds a row to asset.md's `## Variants` table with `✓` in the Default column and a one-line description derived from the variant's When to use.

For atomic assets (Phase A signaled no variants), skip Phase C entirely. `default-variant: ""` in frontmatter; the asset stands alone with Structure + CTA conventions in asset.md (populated in Phase B).

### Step 4: Read templates

- Asset envelope: `templates/assets/[slug]-template/asset.md` if a matching template exists; otherwise use the closest-fit template (e.g., for a new blog variant, use `blog-post-template`) as the structural scaffold.
- Variant (if Phase C ran): `templates/assets/[slug]-template/variants/variant-template.md` if the matching template has a variants/ subdirectory; otherwise use `blog-post-template/variants/variant-template.md` as the generic fallback.

### Step 5: Generate

Files generated atomically:

1. **Asset file** at `messaging/assets/[slug]/asset.md` — frontmatter populated including `default-variant`; body populated from Phase B answers. For variant-likely assets, body has `## Conventions`, `## Frontmatter requirements`, `## Variants` (with the default variant row). For atomic assets, body adds `## Structure` and `## CTA conventions`.
2. **Variant file** (if Phase C ran) at `messaging/assets/[slug]/variants/[variant].md` — populated from Phase C answers (When to use, Voice notes, Structure, CTA conventions, Examples).
3. **MESSAGE.md `## Assets` row** — add a row mapping the content type to this slug (default or alternative per Phase A). Row columns: `Content type | Asset | Default variant | Available variants`. For atomic assets, Default variant is `—` and Available variants is `—`.

### Step 6: Diff + approve

Show the changes side by side. User approves, edits, or cancels.

### Step 7: Write atomically

All writes succeed or none do. If any individual write fails, roll back the partial state.

## Update flow

### Step 1: Detect

Folder exists, no `--remove` / `--add-variant` / `--remove-variant` → proceed.

### Step 2: Load current

Read the asset file + every file in `variants/`. Show the user what's currently there.

### Step 3: Focused interview

"What do you want to change?" Probe specific sections. Common updates: new CMS fields (extend `content-keys`), tone refinement (Conventions section), structural shift, changing the default variant.

### Step 4: Regenerate

Apply changes. If new variants need adding, the user can chain into `--add-variant` after this flow.

### Step 5: Diff + approve

Show all changes — asset file, any variants modified, MESSAGE.md if updated.

### Step 6: Write

Write atomically. Update `last-reviewed` in asset frontmatter.

## Add variant flow

### Step 1: Detect

Folder exists, `--add-variant [name]` flag → proceed. The variant name becomes the slug; must be kebab-case and unique within the asset's `variants/` directory.

### Step 2: Variant interview

Same questions as Create flow Phase C — when to use, voice notes, structure, CTA conventions, examples, plus: should this become the new default?

If adding a variant to an atomic asset (one that previously had no variants/ directory), this operation **converts** the asset: it moves `## Structure` and `## CTA conventions` from asset.md into the new variant file (preserving whatever was there), creates the `variants/` directory, and adds a `## Variants` section to asset.md. Surface this conversion to the user before proceeding.

### Step 3: Read variant template

From `templates/assets/[slug]-template/variants/variant-template.md` (per-asset template), or the generic fallback if not present.

### Step 4: Generate

1. **Variant file** at `messaging/assets/[slug]/variants/[name].md` — populated with When to use, Voice notes, Structure, CTA conventions, Examples.
2. **Asset.md update** — append a row to `## Variants` table with the new variant (one-line description from When to use; `✓` in Default if user chose to make it the new default — and clear any prior `✓`).
3. **Asset frontmatter update** if user chose to make this the new default: update `default-variant`.
4. **MESSAGE.md `## Assets` row update** — append `[name]` to Available variants column; update Default variant if changed.
5. **(Atomic→variant conversion only)** Strip `## Structure` and `## CTA conventions` from asset.md (their content has been migrated into the new variant); add `## Variants` table to asset.md.

### Step 5: Diff + approve

### Step 6: Write atomically

## Remove asset flow

### Step 1: Detect

Folder exists, `--remove` flag → proceed.

### Step 2: Enumerate impact

- **MESSAGE.md routing row** — will be removed (if this is the only asset for that content type) OR the row's Default updated (if alternatives exist).
- **Asset folder** — entire `messaging/assets/[slug]/` directory will be deleted (asset.md + all variants).
- **Historical workflow asset manifests in `output/`** — flagged but NOT modified.

### Step 3: Preview

```
Removing messaging/assets/[slug]/

Files to delete:
  - messaging/assets/[slug]/asset.md
  - messaging/assets/[slug]/variants/use-case.md
  - messaging/assets/[slug]/variants/thought-leadership.md

Files to modify:
  - MESSAGE.md: remove row for content type "blog" → "[slug]" (or update Default if alternative)

Historical references (flagged, not modified):
  - output/campaigns/example/01-blog.md
```

### Step 4: Forced approval

Require literal "confirm" text input. No bypass.

### Step 5: Execute atomically

Delete asset folder (recursive). Update MESSAGE.md routing. Write audit log.

### Step 6: Audit log

Write to `.design/removals/YYYY-MM-DD-HHMMSS.md`:

```yaml
---
artifact: messaging/assets/[slug]/
removed_at: 2026-05-22T15:30:00Z
removed_by: design-asset
---

# Removal of messaging/assets/[slug]/

## Files deleted

- messaging/assets/[slug]/asset.md
- messaging/assets/[slug]/variants/use-case.md
- messaging/assets/[slug]/variants/thought-leadership.md

## Files modified

- MESSAGE.md (removed routing row for content type "blog")

## Historical references flagged (not modified)

- output/campaigns/example/01-blog.md
```

## Remove variant flow

### Step 1: Detect

Folder exists, variant file exists, `--remove-variant [name]` → proceed.

### Step 2: Check default

If the variant being removed is currently the asset's `default-variant`, prompt the user to choose a replacement default from remaining variants (or accept `""` if no variants remain — asset becomes atomic).

### Step 3: Preview

```
Removing messaging/assets/[slug]/variants/[name].md

Files to delete:
  - messaging/assets/[slug]/variants/[name].md

Files to modify:
  - messaging/assets/[slug]/asset.md: default-variant changes from "[name]" to "[replacement]"
  - MESSAGE.md: drop "[name]" from Available variants for content type "[type]"
```

### Step 4: Forced approval

Require literal "confirm" text input.

### Step 5: Execute + audit log

Delete the variant file. Update asset.md frontmatter if default changed. Update MESSAGE.md. Write audit log at `.design/removals/`.

## Refused operations

If the asset doesn't exist and `--remove` (or `--remove-variant`) is passed:

> Cannot remove asset `[slug]` — it doesn't exist. Run `/design asset [slug]` (without `--remove`) to create it.

If `--add-variant` is passed on a non-existent asset:

> Cannot add variant to asset `[slug]` — it doesn't exist. Run `/design asset [slug]` to create the asset first.

## Tool Scoping

- **Read** — `MESSAGE.md`, `messaging/`, `templates/assets/`, `output/` (historical refs), `input/`
- **Write, Edit** — `messaging/assets/[slug]/` (user approval), `MESSAGE.md` (routing table maintenance, user approval), `.design/removals/` (autonomous on remove)
- **Agent(researcher)** — Dispatched when `--research` flag is passed
- **Glob, Grep** — Full access (impact analysis)
- **AskUserQuestion** — Interactive interview + approval gates
