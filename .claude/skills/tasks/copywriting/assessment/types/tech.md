# Tech Assessment

A structured evaluation framework that helps a prospect or customer assess their current technical environment, architecture maturity, or readiness for deployment — then maps those findings to specific capability gaps and solution requirements. Tech assessments are typically used in pre-sales technical discovery, proof of concept scoping, or post-sale implementation planning.

## When to Use

- Pre-POC scoping: understand the environment before committing to a deployment approach
- Technical discovery: help an SE or solutions architect gather structured input from a practitioner
- Architecture review: evaluate whether the current technical state is ready for a specific integration or deployment
- Implementation readiness: determine what prerequisites must be in place before deployment
- Self-serve technical qualification: help technically sophisticated buyers assess fit independently

## Primary Audience

Technical practitioners and evaluators — security engineers, architects, IT infrastructure leads, DevOps or platform engineers. The person completing a tech assessment is hands-on in the environment. They know what tools are deployed and how they're configured. Write for their vocabulary and level of specificity.

Tech assessments are rarely forwarded upward. They inform a technical recommendation that then gets translated into a business case. The output is typically: "Here's what we found. Here's what it means for implementation. Here's what we recommend."

## Tech Assessment vs. Risk and Business Value Assessments

| | Tech Assessment | Risk Assessment | Business Value |
|---|---|---|---|
| Primary audience | Practitioner / Architect | Practitioner → Executive | Champion → Budget owner |
| Funnel stage | Mid-cycle (technical evaluation) | Top / early discovery | Mid / late cycle |
| Output tone | Technical findings + recommendations | Risk exposure + urgency | ROI + payback |
| Output recipient | SE / Architect + Practitioner | CISO / Security leadership | CFO / Budget committee |
| Key output | Integration map, readiness gaps, deployment path | Risk profile by domain | Annual value + payback period |

## Structure

### 1. Introduction Block

Orient the practitioner:

- What this assessment evaluates (which technical dimensions)
- What expertise is needed to complete it accurately (e.g., "complete with access to your current tool inventory and network architecture documentation")
- What the output is (a technical readiness report, integration map, or deployment recommendation)
- How it will be used (self-serve, SE-facilitated, or shared with the vendor team)

### 2. Environment Inventory

Before evaluating maturity or gaps, establish the factual baseline of what's in place. This section is structured data gathering — not scored.

**Standard inventory dimensions:**

| Dimension | What to Capture |
|---|---|
| Endpoint tools | EDR/AV vendors, agent versions, coverage estimate |
| Cloud environments | Providers in use, account/subscription count, services type (IaaS, PaaS, SaaS) |
| Network infrastructure | On-prem vs. cloud-hosted, segmentation model, proxy/NAT topology |
| Identity systems | Directory services (AD, Entra ID, Okta), SSO coverage, service account inventory |
| Vulnerability management | Scanner vendors, scan frequency, coverage estimate |
| ITSM / CMDB | Existing asset tracking tools, data quality self-assessment |
| SIEM / SOAR | Platform in use, integration depth |

Inventory questions should be specific and answerable: "Which EDR vendor are you using?" not "Describe your endpoint security posture."

### 3. Technical Maturity Dimensions

Score the technical environment across the dimensions that determine fit, deployment complexity, and expected time-to-value. Dimensions should reflect the actual technical factors that differentiate deployments.

**Example maturity dimensions for an asset management context:**

| Dimension | What It Measures |
|---|---|
| Integration readiness | The breadth and health of existing security and IT data sources |
| Data quality | Accuracy, completeness, and freshness of existing asset data |
| Network accessibility | Whether the deployment model (cloud, on-prem, hybrid) presents connectivity constraints |
| Automation maturity | Whether the team has the infrastructure to act on enriched asset data programmatically |
| Change management readiness | Whether there are governance processes for adding new data sources or integrations |

**4-point maturity scale:**
- 4: Fully mature — defined, consistent, and well-maintained
- 3: Operational — in place and functional, with minor gaps
- 2: Developing — partially implemented or inconsistently maintained
- 1: Nascent — not yet in place or significant gaps

### 4. Integration Map

For solutions with multiple integrations or data source dependencies, an integration map documents which specific connectors are in scope, which are already available, and which have conditional requirements.

**Format per integration:**

| Integration | Status | Notes |
|---|---|---|
| [Tool/Source] | ✓ Available / ⚠ Conditional / ✗ Not applicable | Version requirements, authentication model, known constraints |

This section becomes a reference artifact for the POC scoping and implementation planning conversation.

### 5. Gap Analysis

Translate the maturity scores and integration map into a prioritized gap list:

- **Deployment blockers** — gaps that must be addressed before deployment begins
- **Recommended prerequisites** — gaps that aren't blockers but will limit initial value if not addressed
- **Post-deployment improvements** — gaps that can be addressed after initial deployment to increase coverage or performance

Format as a prioritized table so the practitioner and SE can use it directly in a planning conversation.

### 6. Deployment Path Recommendation

Based on the environment profile and gap analysis, recommend the most appropriate deployment path:

- **Standard deployment** — environment meets all prerequisites; full deployment recommended
- **Phased deployment** — some gaps present; recommend starting with [specific scope] and expanding
- **POC-first** — significant unknowns; recommend a scoped POC to validate fit before full deployment
- **Prerequisites first** — one or more blockers identified; address [specific gaps] before proceeding

The recommendation should name the specific gaps driving it and the estimated effort to close them.

### 7. Output Narrative

Write the output narrative for each deployment path recommendation. The narrative:

- Summarizes the key findings from the environment inventory and maturity scores
- Names the 1-3 factors that most significantly affect the deployment recommendation
- States the recommended path clearly
- Provides a concrete next step (POC scoping call, integration checklist review, technical workshop)

## Tone & Style

- **Voice:** Technical, precise, and peer-level. The SE or practitioner reading this should feel like it was written by someone who understood their environment.
- **Length:** Question section: 2-3 pages. Output report: 1-2 pages.
- **Altitude:** Practitioner and SE — specific, technical, with no simplification for executive consumption

## Delivery Modes

**SE-facilitated discovery:** The SE uses the framework as a structured discovery guide during a technical call. They complete the assessment in real time based on the practitioner's answers. Output becomes the technical discovery summary and POC scope.

**Self-serve pre-engagement:** Posted as a technical questionnaire that a prospect completes before their first technical call. Lets the SE arrive with context and focus the conversation on gaps and questions rather than basic inventory gathering.

**Technical workshop:** A half-day or full-day facilitated session where the team walks through the assessment together, using it as the structure for a deep technical discovery. Output is a formal technical findings report.

## Example

**Input:** Create a tech assessment for evaluating enterprise readiness to deploy a cybersecurity asset management platform, focused on integration depth and data source coverage.

**Output:**
```markdown
## Technical Readiness Assessment: Asset Management Deployment

This assessment evaluates your environment's readiness for an asset management deployment — specifically, your existing data source coverage, integration health, and the technical factors that affect deployment complexity and time-to-value. Complete with access to your current tool inventory and a working knowledge of your network topology.

_Designed for security engineers, IT architects, or the technical lead on your evaluation team. Estimated time: 20-30 minutes._

---

### Section 1: Environment Inventory

**1.1 Endpoint Management**

| Tool Category | Vendor | Estimated Coverage | Agent Version |
|---|---|---|---|
| EDR / Endpoint Security | | | |
| Mobile Device Management | | | |
| Patch Management | | | |

**1.2 Cloud Infrastructure**

Which cloud providers are in scope for this deployment?
_[ ] AWS  [ ] Azure  [ ] GCP  [ ] Private cloud  [ ] SaaS-only  [ ] Other: ___

Approximate number of cloud accounts/subscriptions: ___

**1.3 Identity & Directory**

Primary directory service: _[ ] Active Directory  [ ] Azure AD / Entra ID  [ ] Okta  [ ] Other: ___

Is SSO in place for all managed applications? _[ ] Yes  [ ] Partially  [ ] No_

**1.4 Existing Asset Tracking**

Do you currently maintain a CMDB or asset inventory?
_[ ] Yes, actively maintained  [ ] Yes, but stale/incomplete  [ ] Informal tracking only  [ ] No_

If yes, which tool: ___

---

### Section 2: Integration Readiness

Rate each of the following integrations in your environment:

| Integration | Status | Notes |
|---|---|---|
| [EDR vendor] | [ ] Available  [ ] Conditional  [ ] N/A | |
| Active Directory / LDAP | [ ] Available  [ ] Conditional  [ ] N/A | |
| Cloud provider APIs | [ ] Available  [ ] Conditional  [ ] N/A | |
| Vulnerability scanner | [ ] Available  [ ] Conditional  [ ] N/A | |
| Network infrastructure | [ ] Available  [ ] Conditional  [ ] N/A | |
| ITSM / ticketing | [ ] Available  [ ] Conditional  [ ] N/A | |
| SIEM | [ ] Available  [ ] Conditional  [ ] N/A | |

For integrations marked Conditional, note the constraint: ___

---

### Section 3: Technical Maturity

**3.1** How would you describe the accuracy of your current asset inventory?
_[ ] Comprehensive and actively maintained  [ ] Reasonably complete but with gaps  [ ] Significant gaps  [ ] Not maintained_

**3.2** Do you have a defined process for provisioning new assets into your security tooling?
_[ ] Yes, automated  [ ] Yes, manual but consistent  [ ] Informal  [ ] No defined process_

**3.3** Does your security team have the ability to query asset data programmatically via API?
_[ ] Yes, actively used  [ ] Available but not used  [ ] Not available  [ ] Unknown_

**3.4** How would you describe your network segmentation model relative to asset discovery?
_[ ] Flat network — no segmentation constraints  [ ] Segmented with defined discovery paths  [ ] Heavy segmentation — some zones inaccessible  [ ] Unknown_

---

### Your Technical Profile

**Integration Coverage:** [calculated from Section 2 — % of core integrations available]

**Environment Complexity:** [derived from network segmentation, cloud breadth, identity diversity]

**Deployment Recommendation:** [Standard / Phased / POC-first / Prerequisites first]

**Key Finding:** [1-2 sentence summary of the most significant finding]

**Priority Gaps:**
1. [Gap 1 — category, description, recommended action]
2. [Gap 2 — if applicable]

**Recommended Next Step:** [Specific action — scoping call, integration checklist review, or POC scope definition]
```

## Quality Signals

| Criterion | Target | Red Flags |
|-----------|--------|-----------|
| Inventory Specificity | Questions capture specific tools, versions, and coverage estimates | Vague questions about "security posture" or "tool maturity" |
| Integration Map Completeness | All core integrations relevant to the deployment are mapped | Integration map covers only the most common connectors |
| Gap Prioritization | Gaps classified as blockers, prerequisites, or post-deployment | All gaps treated as equal priority |
| Deployment Path Logic | Recommendation is deterministic from the inputs — practitioner understands why | Recommendation appears without explanation |
| SE Utility | Output is directly usable in a technical scoping conversation | Output requires significant interpretation before an SE can use it |
| Practitioner Altitude | Questions assume technical familiarity — no over-explanation of basic concepts | Questions over-simplified for the practitioner audience |