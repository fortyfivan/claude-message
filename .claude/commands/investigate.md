Messaging intelligence, feedback processing, system health, and insight management.

Usage:
  /investigate                              — Broad scan across all domains
  /investigate [type] [name]                — Targeted investigation (e.g., competitor acme-corp)
  /investigate feedback [input]             — Process real-world feedback into messaging changes
  /investigate feedback --log [input]       — Log observation without proposing changes
  /investigate health                       — Run all 7 health checks
  /investigate health --fix [check]         — Health checks + propose fixes
  /investigate health --report              — Full health report to output/
  /investigate review                       — Tracker dashboard + health summary
  /investigate acknowledge [ID]             — Acknowledge an insight
  /investigate defer [ID]                   — Defer an insight
  /investigate resolve [ID]                 — Resolve an insight

Read and follow the instructions in `.claude/skills/workflows/investigate/SKILL.md`.

Mode routing:
- No args or [type] [name]  → scan or target mode
- feedback                  → feedback mode
- health                    → fix / report / review mode
- review                    → review mode
- acknowledge/defer/resolve → state management

Pass all arguments to the skill.
