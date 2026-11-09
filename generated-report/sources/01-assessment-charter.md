# Assessment charter • baseline, 2 November 2026

> SYNTHETIC CASE STUDY — not vendor guidance or production measurements.

## Decision context
Atlas is a fictional 28-module Java estate. The assessment compares retaining the present stack, staged modernization, and a replacement. The target is an illustrative Spring 7 / current-generation application-server candidate; this document asserts no real support matrix.

## Scope and measurement contract
The six dimensions have business-defined weights totalling 100. An investigation counts as examined only after a documented preliminary result (or an inconclusive outcome), never merely because an agent started it. Planned scope weights are explicit. Coverage is not confidence or feasibility.

## Assumptions and exclusions
- No code has been migrated as a deliverable of this study.
- Sample counts, timings, costs and findings below are fabricated to test the module.
- Benefits, enterprise licensing, and restore readiness still lack defensible measurements.

## Review protocol
Weekly reports contain the complete current understanding plus structured deltas. An authorized human approves each snapshot; a favorable technical observation alone cannot authorize migration.

```assessment
program:
  id: ATLAS
  title: Atlas modernization assessment
  subtitle: Feasibility, effort & migration worthiness
  owner: Architecture & Technology Strategy
  scope: Evaluate whether a legacy Java estate should be modernized. No implementation
    progress is represented.
  exampleData: true
  currentRecommendationId: REC-ATLAS
executiveSummary:
- The compatibility investigation has identified a plausible adaptation route, but
  no migration decision is justified yet.
- Dependency and security findings remain preliminary. Economics and operational recovery
  are materially underexamined.
- Management should fund targeted validation experiments rather than approve implementation
  on current evidence.
dimensions:
- id: D-COMPAT
  title: Framework compatibility
  description: Planned assessment dimension for the Atlas modernization study.
  scope: API, namespace, serialization and transaction semantics
  weight: 25
  coverageStatus: investigating
  evidenceMaturity: low
- id: D-DEPS
  title: Dependency viability
  description: Planned assessment dimension for the Atlas modernization study.
  scope: Direct and transitive dependency maintenance and licensing
  weight: 20
  coverageStatus: investigating
  evidenceMaturity: low
- id: D-PLATFORM
  title: Runtime & platform
  description: Planned assessment dimension for the Atlas modernization study.
  scope: Representative application-server, JDK and operational fit
  weight: 15
  coverageStatus: investigating
  evidenceMaturity: low
- id: D-SEC
  title: Security & compliance
  description: Planned assessment dimension for the Atlas modernization study.
  scope: Security controls, support lifecycle and access boundaries
  weight: 15
  coverageStatus: investigating
  evidenceMaturity: low
- id: D-ECON
  title: Effort & worthiness
  description: Planned assessment dimension for the Atlas modernization study.
  scope: Uncertainty-bounded effort, costs, benefits and alternatives
  weight: 20
  coverageStatus: investigating
  evidenceMaturity: low
- id: D-OPS
  title: Operational impact
  description: Planned assessment dimension for the Atlas modernization study.
  scope: Recovery, observability, on-call and data-handling readiness
  weight: 5
  coverageStatus: not-examined
  evidenceMaturity: unknown
investigations:
- id: I-API
  dimensionId: D-COMPAT
  question: Are API and namespace adaptations bounded?
  status: preliminary
  owner: Research team
  scopeWeight: 2
  nextStep: Validate a representative transaction slice.
- id: I-SERIAL
  dimensionId: D-COMPAT
  question: Can stored serialized sessions be read?
  status: not-examined
  owner: Research team
  scopeWeight: 1
  nextStep: Capture legacy session fixtures.
- id: I-DEPS
  dimensionId: D-DEPS
  question: Do maintained replacement libraries exist?
  status: preliminary
  owner: Research team
  scopeWeight: 2
  nextStep: Reconcile the full transitive inventory.
- id: I-LICENSE
  dimensionId: D-DEPS
  question: Are replacement licenses acceptable?
  status: investigating
  owner: Research team
  scopeWeight: 1
  nextStep: Request legal review of candidate licenses.
- id: I-RUNTIME
  dimensionId: D-PLATFORM
  question: Does the target runtime host representative workloads?
  status: investigating
  owner: Research team
  scopeWeight: 1
  nextStep: Run a transaction and recovery experiment.
- id: I-CAPACITY
  dimensionId: D-PLATFORM
  question: Is performance acceptable at peak load?
  status: not-examined
  owner: Research team
  scopeWeight: 1
  nextStep: Design a replay dataset without customer data.
- id: I-AUTH
  dimensionId: D-SEC
  question: Are authorization semantics equivalent?
  status: preliminary
  owner: Research team
  scopeWeight: 1
  nextStep: Exercise denied and cross-tenant requests.
- id: I-SUPPORT
  dimensionId: D-SEC
  question: Is the support lifecycle adequate?
  status: not-examined
  owner: Research team
  scopeWeight: 1
  nextStep: Obtain written support assumptions.
- id: I-EFFORT
  dimensionId: D-ECON
  question: What effort range is defensible?
  status: preliminary
  owner: Research team
  scopeWeight: 1
  nextStep: Model remediation sensitivity.
- id: I-ROI
  dimensionId: D-ECON
  question: Are benefits and avoided costs worth the effort?
  status: not-examined
  owner: Research team
  scopeWeight: 2
  nextStep: Validate the counterfactual and benefit horizon.
- id: I-RECOVERY
  dimensionId: D-OPS
  question: Can operations sustain the candidate platform?
  status: not-examined
  owner: Research team
  scopeWeight: 1
  nextStep: Interview operations and test restore assumptions.
recommendations:
- id: REC-ATLAS
  conclusion: Recommendation pending; continue targeted assessment.
  rationale: Compatibility evidence is promising but economics and recovery remain
    unexplored.
  supportingFindings:
  - F-API
  - F-DEPS
  limitations:
  - Sampled modules only
  - No validated benefit model
  decisionStatus: pending
  stance: pending
```
