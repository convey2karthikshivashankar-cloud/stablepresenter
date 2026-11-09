# Economic analysis • alternatives, ranges and decision gates

> SYNTHETIC CASE STUDY — not vendor guidance or production measurements.

## Estimation method
The sample estimate is an order-of-magnitude research output, not a delivery commitment. A low scenario assumes two reusable adapters; a high scenario assumes replacing three wrappers and retesting transaction behavior.

| Item | Low | High | Unit | Confidence |
| --- | ---: | ---: | --- | --- |
| Technical adaptation effort | 60 | 100 | person-days | Low |
| One-time external cost | 35000 | 65000 | USD | Low |
| Recurring benefit | Unknown | Unknown | USD/year | Unknown |

## Worthiness and sensitivity
No ROI is calculated: the benefit baseline and evaluation horizon are missing. Person-days are not added to dollars. The effort range excludes license renegotiation, enterprise rollout, parallel-run costs and contingency for operational recovery.

## Alternatives
Retain: avoids near-term change but leaves support exposure unquantified.
Staged modernization: offers a bounded experiment, with integration uncertainty.
Replace: might simplify the estate, but business-function parity is unassessed.

## Management ask
Approve two further assessment experiments and a finance workshop. Do not treat research funding as implementation authorization.

```assessment
evidence:
- id: E-MODEL
  description: Synthetic effort scenario model with explicitly incomplete benefits.
  kind: financial-model
  verificationStatus: reviewed
  capturedAt: '2026-11-02'
  reviewedBy: Analysis lead
  limitations: No calibrated productivity baseline, benefit horizon or operating-cost
    counterfactual.
  sourceRefs:
  - path: '@self'
    startLine: 5
    endLine: 23
estimates:
- id: EST-EFFORT
  title: Technical adaptation effort
  category: effort
  low: 60
  high: 100
  unit: person-days
  confidence: low
  assumptions:
  - Two reusable adapters in the low case
  - Three wrapper replacements in the high case
  - Excludes rollout and recovery
  evidenceRefs:
  - E-MODEL
- id: EST-COST
  title: One-time external assessment of transition costs
  category: cost
  low: 35000
  high: 65000
  unit: USD
  confidence: low
  assumptions:
  - Synthetic quotes
  - Licensing renegotiation excluded
  evidenceRefs:
  - E-MODEL
- id: EST-BENEFIT
  title: Recurring economic benefit
  category: benefit
  low: null
  high: null
  unit: USD/year
  confidence: unknown
  assumptions:
  - Benefit horizon and counterfactual not yet agreed
  evidenceRefs: []
alternatives:
- id: ALT-RETAIN
  description: Retain the current platform
  benefits:
  - No immediate conversion expenditure
  drawbacks:
  - Unquantified support and opportunity costs
  effortEstimate: Unknown; support stabilization not estimated
  assumptions:
  - Current support remains purchasable
  evidenceRefs:
  - E-MODEL
  verdict: viable
- id: ALT-STAGED
  description: Assess a staged modernization
  benefits:
  - Limits exposure while testing critical hypotheses
  drawbacks:
  - Parallel-platform overhead remains unknown
  effortEstimate: See EST-EFFORT; not a delivery commitment
  assumptions:
  - Representative slices predict key compatibility risks
  evidenceRefs:
  - E-SCAN
  - E-MODEL
  verdict: preferred
- id: ALT-REPLACE
  description: Replace with a new service implementation
  benefits:
  - Potential simplification
  drawbacks:
  - Functional parity and data migration unassessed
  effortEstimate: Not yet measurable
  assumptions:
  - Business processes can be re-specified
  evidenceRefs: []
  verdict: unassessed
gates:
- id: G-COMPAT
  title: Representative compatibility evidence
  status: unmet
  critical: true
  rationale: Runtime and serialization experiments missing.
  evidenceRefs:
  - E-SCAN
- id: G-DEPS
  title: Maintained dependency path demonstrated
  status: unknown
  critical: false
  rationale: Candidate replacements not yet tested.
  evidenceRefs:
  - E-DEPS
- id: G-ECON
  title: Defensible worthiness model
  status: unknown
  critical: true
  rationale: Benefit model and counterfactual missing.
  evidenceRefs:
  - E-MODEL
- id: G-OPS
  title: Operational recovery assessment
  status: unknown
  critical: true
  rationale: No recovery investigation completed.
  evidenceRefs: []
decisions:
- id: DEC-EXPERIMENT
  title: Authorize two assessment experiments
  status: proposed
  owner: Architecture sponsor
  dueOn: '2026-11-06'
  rationale: Resolve the most material compatibility uncertainties before a migration
    decision.
  evidenceRefs:
  - E-SCAN
activities:
- id: ACT-RESEARCH
  title: Serialization and transaction research experiments
  status: planned
  owner: Research agents + reviewer
  nextStep: Use synthetic fixtures and preserve raw observations.
  evidenceRefs:
  - E-ASSUME
```
