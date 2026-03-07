# Product Datasheet

Provide technical details, specifications, and integration information for evaluators comparing solutions.

## Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| Overview | Brief positioning statement | 2-3 sentences on what the product does and for whom |
| Key Capabilities | Core functionality summary | 4-6 capabilities with brief descriptions |
| Technical Specifications | Detailed specs | Deployment options, architecture, performance |
| Integrations | Ecosystem connectivity | Categories of integrations with examples |
| Requirements | What's needed to deploy | System requirements, prerequisites |
| Pricing/Licensing | Model overview (if public) | Or "Contact sales for pricing" |

## Tone & Style

- **Voice:** Technical, precise, scannable
- **Length:** 1-2 pages (400-800 words)
- **Altitude:** Technical evaluators and architects

Be accurate and complete. This document will be used in technical comparisons. Errors or omissions damage credibility.

## Formatting Guidance

- **Tables:** Use for specs, integrations, requirements
- **Bullet lists:** Use for capabilities
- **No marketing fluff:** Technical readers will skip it anyway
- **Version/date:** Include document currency

## Example

**Input:** Create a product datasheet for the asset management platform

**Output:**
```markdown
# Axonius Cybersecurity Asset Management Platform

**Datasheet | v2024.1**

## Overview

Axonius provides a comprehensive cybersecurity asset management platform that aggregates, correlates, and normalizes data from existing security and IT tools to deliver a unified, continuously updated inventory of all assets.

## Key Capabilities

- **Universal Asset Discovery:** Identifies devices, users, cloud instances, and software across hybrid environments
- **Multi-Source Correlation:** Reconciles data from 700+ integrations into deduplicated asset records
- **Coverage Gap Analysis:** Identifies assets missing required security controls
- **Query & Reporting:** Flexible query language for custom asset searches and automated reports
- **Automated Response:** Triggers actions based on asset state via integrations or custom scripts
- **Vulnerability Enrichment:** Correlates vulnerability data with asset context for prioritization

## Technical Specifications

| Specification | Details |
|---------------|---------|
| Deployment | SaaS (primary), On-premises, Hybrid |
| Architecture | Microservices-based, horizontally scalable |
| Data Refresh | Continuous (configurable intervals per adapter) |
| Query Performance | Sub-second for most queries across 1M+ assets |
| Data Retention | Configurable (default: 90 days historical) |
| High Availability | Active-active deployment supported |
| Encryption | TLS 1.3 in transit, AES-256 at rest |

## Integrations

| Category | Examples |
|----------|----------|
| Endpoint Security | CrowdStrike, Microsoft Defender, SentinelOne, Carbon Black |
| Vulnerability Management | Tenable, Qualys, Rapid7, Microsoft Defender VM |
| Cloud Providers | AWS, Azure, GCP, Oracle Cloud |
| Identity | Okta, Azure AD, Ping, CyberArk |
| ITSM/CMDB | ServiceNow, Jira, BMC |
| Network | Cisco, Palo Alto, Fortinet, Zscaler |

**Total Integrations:** 700+ with new adapters released monthly

## System Requirements

**SaaS Deployment:**
- Outbound HTTPS connectivity to Axonius cloud
- Service account credentials for connected data sources

**On-Premises Deployment:**
- VMware vSphere 6.7+ or equivalent virtualization
- 16 vCPU, 64GB RAM, 500GB storage (minimum)
- RHEL 8.x or Ubuntu 20.04 LTS

## Certifications & Compliance

- SOC 2 Type II
- ISO 27001
- FedRAMP (in process)
- GDPR compliant

## Contact

For pricing, custom requirements, or technical questions:
**sales@axonius.com** | **axonius.com/demo**
```

## Evaluation Criteria

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Technical Accuracy | All specs verifiable and current | Outdated versions, incorrect details |
| Completeness | Covers what evaluators need to compare | Missing key categories (integrations, requirements) |
| Scannability | Information findable in seconds | Dense paragraphs, buried details |
| Objectivity | Facts without marketing spin | Superlatives, vague claims |
| Currency | Document date and version visible | No indication of when updated |
