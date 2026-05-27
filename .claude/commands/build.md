Multi-asset content production — campaigns, launches, competitive plays, and events. Verb-noun router; the subcommand selects the underlying workflow skill.

Usage:
  /build campaign [type] "[topic]"     — Multi-asset content campaign
  /build launch "[name]"               — Product or feature launch
  /build play [type] "[name]"          — Competitive/expansion/win-back/signal/partner play
  /build event "[event-name]"          — Four-phase event program (brief + pre/on-site/post waves)

Event scope flag:
  /build event "[event-name]" --brief-only  — produces the brief without dispatching production waves

Campaign types: digital, outbound, abm.
Play types: competitive, signal, expansion, win-back, partner, custom.
Event types: industry-conference, hosted-conference, partner-event, regional-event, hospitality-event (resolved inside the skill's Round 1 interview, not as a command arg).

Subcommand → skill routing:
- `campaign` → `.claude/skills/workflows/build-campaign/SKILL.md`
- `launch` → `.claude/skills/workflows/build-launch/SKILL.md`
- `play` → `.claude/skills/workflows/build-play/SKILL.md`
- `event` → `.claude/skills/workflows/build-event/SKILL.md`

Read and follow the instructions in the matching skill. Pass all remaining arguments to the skill.
