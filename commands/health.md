Validate the messaging system for completeness, consistency, and health.

Runs six checks: gap (missing content), relationship (broken links), schema (template compliance), freshness (stale docs), glossary(terminology health), and profile (identity sync).

Use --fix to propose and execute remediations. Use --report to write a full report to output/health-report.md. Specify individual checks by name: gap, relationship, schema, freshness, glossary, profile.

/agents health $ARGUMENTS
