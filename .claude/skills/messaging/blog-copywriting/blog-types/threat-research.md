# Threat Research

Showcase technical findings and security insights that demonstrate deep expertise and provide actionable intelligence.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Executive Summary | Key findings upfront | Lead with impact, not methodology; 3-4 sentences max |
| Technical Background | Context for the threat | Enough to understand severity without exhaustive history |
| Analysis | What you discovered and how | Show your work; methodology matters for credibility |
| Impact | Risk assessment and implications | Who's affected, how badly, under what conditions |
| Mitigation | Recommendations or defenses | Actionable steps readers can take immediately |

## Tone & Style

- **Voice:** Authoritative, technical but accessible
- **Length:** 1,500-2,500 words
- **Altitude:** Technical practitioners as primary, security leaders as secondary

Write with precision. Avoid sensationalism—let the findings speak. Use technical terminology accurately but define it for broader audiences.

## SEO/GEO Optimization

- Technical terms with inline definitions (e.g., "lateral movement (attacker movement between systems)")
- Threat indicators as structured data (IOCs in tables or lists)
- Timeline of discovery and disclosure
- MITRE ATT&CK mapping where applicable

## Example

**Input:** Write a threat research post about misconfigured cloud storage exposures

**Output:**
```markdown
# Exposed: How Misconfigured Cloud Storage Became the New Data Breach Vector

## Executive Summary

Analysis of 10,000 cloud storage instances revealed 23% had permissions allowing public read access. Of these, 8% contained sensitive data including credentials, PII, and intellectual property. Organizations in healthcare and financial services showed the highest exposure rates.

## Technical Background

Cloud storage services like AWS S3, Azure Blob, and Google Cloud Storage default to private access. However, configuration drift, legacy migrations, and development shortcuts frequently result in overly permissive settings...

## Analysis Methodology

We conducted passive reconnaissance across public cloud ranges, identifying storage endpoints through DNS enumeration and certificate transparency logs...

[Continues with findings, impact assessment, and mitigations]

## Indicators of Compromise

| Indicator Type | Value | Context |
|----------------|-------|---------|
| Bucket naming pattern | *-backup, *-prod, *-staging | High-risk naming conventions |
| Permission configuration | AllUsers: READ | Public exposure indicator |

## Recommended Mitigations

1. **Immediate:** Audit all storage permissions using cloud-native tools
2. **Short-term:** Implement automated drift detection
3. **Long-term:** Establish infrastructure-as-code policies preventing public storage
```

## Evaluation Criteria

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Technical Accuracy | Findings are verifiable and precise | Vague claims, inaccurate technical details |
| Novelty | Adds to security community knowledge | Rehashing known threats without new insight |
| Actionability | Clear mitigation steps | Findings without remediation guidance |
| Responsible Disclosure | Appropriate handling of sensitive details | Exposing active vulnerabilities or victim data |
| Credibility Signals | Methodology transparency, data sources cited | "Trust us" assertions without evidence |
