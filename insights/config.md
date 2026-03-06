# Scan Configuration

Configure the research agent's messaging intelligence scan behavior.

## Cadence

```
cadence: weekly
```

Options: daily, weekly, biweekly, monthly

## Focus Domains

Toggle scan domains on/off. All enabled by default.

| Domain | Enabled | Description |
|---|---|---|
| Competitive moves | yes | Product launches, pricing changes, funding, acquisitions |
| Market shifts | yes | Category redefinition, analyst reports, regulatory changes |
| Audience signals | yes | Role evolution, new pain points, buying process changes |
| Proof validation | yes | Customer churn signals, review sentiment, recognition cycles |
| Technology landscape | yes | New entrants, open source alternatives, platform shifts |

## Watchlists

Add extra keywords, competitors, or personas to monitor beyond what's in the messaging house.

### Competitors

<!-- Add competitor names or URLs to track beyond messaging/competitors/ -->

### Keywords

<!-- Add industry terms, emerging categories, or trend phrases to monitor -->

### Personas

<!-- Add roles or titles to watch for emerging buyer/user patterns -->

## MCP Sources

List configured MCP servers the scan should query. The agent discovers available tools at runtime and skips unavailable sources gracefully.

<!-- Add MCP source names here as they are configured in .claude/settings.json -->
