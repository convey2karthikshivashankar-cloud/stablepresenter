# Week 2 • runtime experiments change the conclusion

> SYNTHETIC CASE STUDY — not vendor guidance or production measurements.

## Reproducible experimental design
Synthetic run ID LAB-ATLAS-2026-11-09-A used 32 session fixtures and 18 transaction cases on an isolated candidate stack. The control used the legacy serialization descriptors. Results were reviewed by a second analyst; all numbers are fictional test inputs.

| Experiment | Passed | Failed | Consequence |
| --- | ---: | ---: | --- |
| Legacy session deserialization without adapter | 23 | 9 | Namespace-only hypothesis contradicted |
| Session deserialization with explicit version adapter | 32 | 0 | Candidate mitigation demonstrated on sample |
| Representative transaction rollback | 18 | 0 | Bounded transaction path validated |

## Revised interpretation
The prior F-SERIAL conclusion is contradicted by nine failing fixtures. It remains in the record and in the earlier snapshot. New finding F-ADAPTER supersedes it for planning: explicit serialization version adaptation is necessary. Passing sampled fixtures does not establish full production behavior.

## Residual uncertainties
- Distributed recovery and restart behavior are still outside this experiment.
- Capacity and long-lived session diversity are unassessed.
- A namespace scan cannot demonstrate semantic equivalence.

## Next research
Prioritize a restore-and-replay experiment, including partial transaction failure and aged session fixtures.

```assessment
investigations:
- id: I-API
  dimensionId: D-COMPAT
  question: Are API and namespace adaptations bounded?
  status: validated
  owner: Research team
  scopeWeight: 2
  nextStep: Validate a representative transaction slice.
- id: I-SERIAL
  dimensionId: D-COMPAT
  question: Can stored serialized sessions be read?
  status: corroborated
  owner: Research team
  scopeWeight: 1
  nextStep: Capture legacy session fixtures.
- id: I-DEPS
  dimensionId: D-DEPS
  question: Do maintained replacement libraries exist?
  status: corroborated
  owner: Research team
  scopeWeight: 2
  nextStep: Reconcile the full transitive inventory.
- id: I-LICENSE
  dimensionId: D-DEPS
  question: Are replacement licenses acceptable?
  status: preliminary
  owner: Research team
  scopeWeight: 1
  nextStep: Request legal review of candidate licenses.
- id: I-RUNTIME
  dimensionId: D-PLATFORM
  question: Does the target runtime host representative workloads?
  status: preliminary
  owner: Research team
  scopeWeight: 1
  nextStep: Run a transaction and recovery experiment.
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
  status: inconclusive
  owner: Research team
  scopeWeight: 1
  nextStep: Obtain written support assumptions.
- id: I-ROI
  dimensionId: D-ECON
  question: Are benefits and avoided costs worth the effort?
  status: investigating
  owner: Research team
  scopeWeight: 2
  nextStep: Validate the counterfactual and benefit horizon.
- id: I-RECOVERY
  dimensionId: D-OPS
  question: Can operations sustain the candidate platform?
  status: investigating
  owner: Research team
  scopeWeight: 1
  nextStep: Interview operations and test restore assumptions.
evidence:
- id: E-TX
  description: 'Synthetic transaction rollback experiment: 18/18 passed on a representative
    slice.'
  kind: experiment
  verificationStatus: validated
  capturedAt: '2026-11-09'
  reviewedBy: Independent reviewer
  limitations: Sampled cases only; distributed recovery excluded.
  sourceRefs:
  - path: '@self'
    startLine: 5
    endLine: 23
- id: E-SERIAL
  description: 'Synthetic legacy fixture experiment: 9/32 fail without adapter; 32/32
    pass with adapter.'
  kind: experiment
  verificationStatus: validated
  capturedAt: '2026-11-09'
  reviewedBy: Independent reviewer
  limitations: Synthetic fixture set; production diversity unmeasured.
  sourceRefs:
  - path: '@self'
    startLine: 5
    endLine: 23
findings:
- id: F-API
  investigationId: I-API
  title: Representative API adaptation validated
  conclusion: The representative transaction slice passes all 18 rollback cases with
    the adapter layer.
  status: validated
  confidence: high
  evidenceRefs:
  - E-TX
  implications: This informs feasibility and estimated research needs; it is not implementation
    completion.
  uncertainties:
  - Distributed recovery excluded
  nextInvestigation: Test failure recovery under restart.
  severity: high
  impact: favorable
  supersedes: []
- id: F-SERIAL
  investigationId: I-SERIAL
  title: Namespace-only session hypothesis contradicted
  conclusion: Nine of 32 synthetic legacy fixtures fail without an explicit serialization
    adapter. The prior assumption is contradicted.
  status: contradicted
  confidence: low
  evidenceRefs:
  - E-SERIAL
  implications: This informs feasibility and estimated research needs; it is not implementation
    completion.
  uncertainties:
  - Legacy session diversity unknown
  nextInvestigation: Use F-ADAPTER for subsequent evaluation.
  severity: critical
  impact: adverse
  supersedes: []
- id: F-ADAPTER
  investigationId: I-SERIAL
  title: Explicit session adapter required
  conclusion: An explicit serialization version adapter is required; it passes all
    sampled fixtures.
  status: corroborated
  confidence: medium
  evidenceRefs:
  - E-SERIAL
  implications: This informs feasibility and estimated research needs; it is not implementation
    completion.
  uncertainties:
  - Production fixture diversity unmeasured
  nextInvestigation: Expand fixture diversity before accepting broad compatibility.
  severity: critical
  impact: mixed
  supersedes:
  - F-SERIAL
questions:
- id: Q-SERIAL
  dimensionId: D-COMPAT
  question: Will legacy session fixtures deserialize safely?
  status: answered
  owner: Runtime research lead
  nextStep: Expand production-representative fixture diversity.
  blocking: true
  evidenceRefs:
  - E-SERIAL
risks:
- id: R-SESSION
  description: Stored session incompatibility raises adaptation effort and backward-compatibility
    uncertainty.
  likelihood: high
  impact: critical
  evidenceRefs:
  - E-SERIAL
  mitigationOptions:
  - Explicit version adapters
  - Investigate session invalidation trade-offs
  status: open
  owner: Runtime research lead
gates:
- id: G-COMPAT
  title: Representative compatibility evidence
  status: met
  critical: true
  rationale: Sampled API and serialization behavior is evidenced; this gate is limited
    to representative evidence.
  evidenceRefs:
  - E-TX
  - E-SERIAL
activities:
- id: ACT-RESEARCH
  title: Serialization and transaction research experiments
  status: completed
  owner: Research agents + reviewer
  nextStep: Investigate operational recovery and broaden fixtures.
  evidenceRefs:
  - E-TX
  - E-SERIAL
```
