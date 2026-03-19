Build a multi-asset content campaign or orchestrate a product launch.

Build type: $1 (campaign or launch)

Campaign mode:
  /build campaign [type] [topic]
  /build campaign --continue [folder]
  /build campaign --continue [folder] --asset [id]

  Campaign types: digital, event, outbound, play, abm.
  If no type specified, the skill will ask.

Launch mode:
  /build launch [name]

  The launch name becomes the directory slug for input materials and output assets.

Read and follow the instructions in the corresponding skill:
- campaign → `.claude/skills/workflows/campaign/SKILL.md`
- launch → `.claude/skills/workflows/launch/SKILL.md`

Pass all remaining arguments to the skill.
