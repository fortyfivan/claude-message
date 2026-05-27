System operations — health check and investigation. Verb-noun router; the subcommand selects the underlying system skill.

Usage:
  /run health                              — Full structural + calibration health check
  /run health --calibration                — Calibration drift only
  /run investigation                       — Broad scan across enabled signal domains
  /run investigation [type] [name]         — Targeted investigation (e.g., `competitor acme-corp`)
  /run investigation feedback [input]      — Process real-world feedback into messaging changes
  /run investigation review                — Insight tracker dashboard + health summary
  /run investigation fix [check]           — Health-check-driven fix proposal
  /run investigation report                — Full health report to output/
  /run investigation acknowledge [ID]      — Move insight to acknowledged
  /run investigation defer [ID]            — Move insight to deferred
  /run investigation resolve [ID]          — Move insight to resolved

Subcommand → skill routing:
- `health` → `.claude/skills/system/run-health/SKILL.md`
- `investigation` → `.claude/skills/system/run-investigation/SKILL.md`

Read and follow the instructions in the matching skill. Pass all remaining arguments to the skill.
