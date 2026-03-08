Scaffold the messaging workspace — directories, templates, seed files, and project context.

Safe to run on fresh or existing projects. Creates missing structure without overwriting.

Run the onboard script. Determine the plugin root by finding where this command file lives (the plugin's `scripts/` directory is a sibling of `commands/`).

```bash
bash [plugin-root]/scripts/onboard.sh [plugin-root] [project-root]
```

Review the output. If any `WARNING:` lines appear, explain each to the user and help resolve them. If no warnings, summarize what was created.
