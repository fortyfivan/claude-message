# Input Directory

User-provided source materials that inform messaging, content, and campaign builds. Place files in the appropriate subdirectory so agents can prioritize context correctly.

## Subdirectories

| Directory | What goes here | Examples |
|---|---|---|
| `messaging/` | Brand guides, positioning decks, messaging frameworks, voice docs | `brand-guide-2026.pdf`, `deck-positioning.pptx` |
| `docs/` | PRDs, release notes, specs, pricing sheets, NPI procedures | `prd-acme-v3.pdf`, `release-notes-q1.md` |
| `research/` | Market research, analyst reports, competitive intel | `research-gartner-mq.pdf`, `battlecard-competitor-x.docx` |
| `transcripts/` | Sales call recordings, customer interviews, feedback logs | `interview-ciso-acme.md`, `call-discovery-enterprise.pdf` |
| `examples/` | Content references, competitor samples, inspiration pieces | `example-competitor-blog.md`, `reference-email-series.pdf` |

Files in the `input/` root still work for backward compatibility. Prefix determines effective category.

**Note:** `input/research/` holds user-provided research materials. The top-level `research/` directory holds agent-generated research reports.

## Priority Hierarchy

Skills scan subdirectories in this order, with earlier directories carrying higher weight:

1. **`messaging/`** — Voice, positioning, narrative structure (highest weight)
2. **`docs/`** — Product detail, capabilities, factual grounding
3. **`research/`** — External perspectives, competitive intel
4. **`transcripts/`** — Real-world language, persona signals, objections
5. **`examples/`** — Reference context (lowest weight)
6. **Root `input/`** — Backward compat; prefix determines effective category

## File Naming

### Prefix Convention

Tag filenames with a prefix so agents know what the file contains:

- `deck-` — Pitch decks or one-pagers
- `brand-guide-` — Brand or messaging guides
- `battlecard-` — Competitive intel or battlecards
- `case-study-` — Customer stories or case studies
- `prd-` or `release-notes-` — Product docs or release notes
- `research-` — Market or audience research
- `npi-` — NPI or launch procedure docs
- `pricing-` — Pricing or packaging sheets
- `brief-` — Existing positioning drafts

### Builder Tagging

Associate a file with a specific builder using a double-dash suffix:

```
[name]--[builder-type]-[slug].ext
```

Examples:
- `prd-acme-v3--launch-acme-v3.pdf` — PRD tagged for the acme-v3 launch
- `research-trends--campaign-q2-digital.pdf` — Research tagged for Q2 digital campaign
- `brand-guide--launch-rebrand.pptx` — Brand guide tagged for the rebrand launch

Builder types: `launch`, `campaign`, or any custom builder identifier.

This works for all file types (PDF, PPTX, DOCX, MD). No manifest or sidecar files needed — the tag is in the filename itself.
