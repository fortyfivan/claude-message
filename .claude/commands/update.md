Update produced assets — detect messaging drift, propose changes, get approval, refresh or version the result.

Arguments: $ARGUMENTS

Usage:
  /update                                    — Show drift status across all produced assets
  /update [slug]                             — Update a living artifact
  /update campaign [folder]                  — Refresh drifted assets in a campaign
  /update campaign [folder] [asset-id]       — Refresh a single campaign asset
  /update launch [name]                      — Refresh drifted assets in a launch
  /update launch [name] [asset-id]           — Refresh a single launch asset
  /update asset [filename]                   — Refresh a standalone asset

Examples:
  /update first-call-deck
  /update campaign q2-digital-03-17-26
  /update campaign q2-digital-03-17-26 asset-03-ciso-email
  /update launch acme-v3
  /update launch acme-v3 asset-02-sales-enablement
  /update asset ciso-outbound-sequence
  /update

Read and follow the instructions in `.claude/skills/workflows/update/SKILL.md`. Pass all arguments.
