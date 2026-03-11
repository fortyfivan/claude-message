Scaffold the messaging workspace — directories, templates, seed files, and project context.

Safe to run on fresh or existing projects. Creates missing structure without overwriting.

Run the onboard script. Determine the plugin root using this resolution order:

1. **Fast path:** Read `.claude/.plugin-root` in the project root. If it exists, its contents are the plugin root path. Use it.
2. **First-run path:** Read `~/.claude/plugins/installed_plugins.json`. Find the entry whose key starts with `claude-message@`. Use the `installPath` value as the plugin root.

```bash
bash [plugin-root]/scripts/onboard.sh [plugin-root] [project-root]
```

Review the output. If any `WARNING:` lines appear, explain each to the user and help resolve them. If no warnings, summarize what was created.
