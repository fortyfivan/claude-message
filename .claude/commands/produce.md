Produce finished deliverables from content files.

Usage:
  /produce                            — Discover producible assets in output/
  /produce [type] [file]              — Produce a single deliverable
  /produce --campaign [name]          — Produce all campaign deliverables
  /produce --launch [name]            — Produce all launch deliverables

**Discovery mode** (no arguments): Scan `output/` for content files (markdown with frontmatter). Scan order: `output/assets/`, `output/campaigns/*/`, `output/launches/*/`. Present a numbered list with title, type, source path, and produced status (check for `.manifest.md` sibling). Let the user select which to produce.

**Direct mode** (`[type] [file]`): Produce a single deliverable from the specified content file.

**Campaign mode** (`--campaign [name]`): Produce all deliverables for a campaign.

**Launch mode** (`--launch [name]`): Produce all deliverables for a launch.

/agents producer $ARGUMENTS
