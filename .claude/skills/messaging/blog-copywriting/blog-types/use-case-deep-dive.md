# Use Case Deep Dive

Explain how to accomplish a specific task step-by-step, providing practical value that demonstrates expertise.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Problem Framing | Establish why this task matters | Connect to business pain, not just technical curiosity |
| Prerequisites | What you need before starting | Be explicit about tools, permissions, and baseline knowledge |
| Step-by-Step Guide | Clear numbered instructions | Each step should be atomic and verifiable |
| Variations | Alternative approaches or edge cases | Acknowledge real-world complexity without overwhelming |
| Outcome | What success looks like | Concrete result the reader can validate |

## Tone & Style

- **Voice:** Practical, instructional, accessible
- **Length:** 1,000-1,500 words
- **Altitude:** Practitioner-focused with executive context in the opener

Write like you're pairing with a colleague. Direct, helpful, without condescension. Assume competence but not omniscience.

## SEO/GEO Optimization

- Numbered steps with descriptive H3 headers (e.g., "Step 3: Configure the Query Filter")
- Code snippets or command examples in fenced blocks
- Summary checklist at the end for quick reference
- FAQ section addressing common blockers

## Example

**Input:** Write a use case guide on finding unmanaged cloud assets

**Output:**
```markdown
# How to Find Unmanaged Cloud Assets Before Your Auditor Does

Every organization has shadow IT. The question is whether you find it first—or your auditor does during a compliance review.

## Why This Matters

Unmanaged cloud assets represent blind spots in your security posture. They often lack proper configuration, miss patching cycles, and bypass your security controls entirely. This guide shows you how to surface them systematically.

## Prerequisites

Before starting, ensure you have:
- Read access to your cloud provider console (AWS, Azure, or GCP)
- An asset inventory baseline (even if incomplete)
- Network visibility into cloud traffic (optional but helpful)

## Step 1: Export Your Cloud Provider's Asset List

Start by pulling a complete inventory from your cloud provider...

[Continues with numbered steps through outcome]

## Quick Reference Checklist

- [ ] Exported cloud provider asset list
- [ ] Cross-referenced against known inventory
- [ ] Investigated orphaned resources
- [ ] Tagged newly discovered assets
- [ ] Updated inventory baseline
```

## Evaluation Criteria

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Actionability | Reader can complete task following the guide | Vague steps, missing prerequisites, assumed knowledge |
| Completeness | All necessary steps included | Gaps that require external research |
| Accuracy | Steps work as described | Outdated commands, wrong parameters |
| Accessibility | Appropriate for stated audience | Too advanced or too basic for target reader |
| Practical Value | Solves a real problem worth solving | Contrived scenario, edge case nobody faces |
