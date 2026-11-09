# Week 2 • revised effort and pending business case

> SYNTHETIC CASE STUDY — not vendor guidance or production measurements.

## Revised effort model
The session adapter introduces an additional effort driver. The synthetic technical adaptation range increases from 60–100 to 95–155 person-days. This is a model revision, not implementation slippage. The external-cost range stays unchanged because procurement has supplied no updated quote.

## What remains unknown
Finance cannot yet validate an avoided-support-cost counterfactual or benefit horizon. Recurring benefits remain unknown. A high research-coverage score would not close this gap.

## Current worthiness view
Defer the migration commitment while authorizing the next assessment slice. The staged option remains the leading research candidate, not an approved migration plan. Recovery assessment and a defensible economic model are mandatory decision gates.

## Next management conversation
Agree the counterfactual, sponsor the recovery experiment, and obtain a license position. Research funding is approved; migration implementation is not.

```assessment
executiveSummary:
- 'The week changed our understanding: namespace-only session compatibility was contradicted;
  an explicit adapter is now evidenced on synthetic fixtures.'
- Representative transaction evidence strengthened, and dependency alternatives partially
  matured. Technical adaptation effort rises to 95–155 person-days.
- 'Defer migration commitment: benefits remain unknown and operational recovery is
  insufficiently assessed. Next priorities are the economic counterfactual, recovery
  experiment and license position.'
evidence:
- id: E-MODEL2
  description: Revised synthetic effort model incorporating session adapter work.
  kind: financial-model
  verificationStatus: reviewed
  capturedAt: '2026-11-09'
  reviewedBy: Analysis lead
  limitations: Benefits, recovery and rollout remain uncalibrated; estimates are not
    commitments.
  sourceRefs:
  - path: '@self'
    startLine: 5
    endLine: 15
estimates:
- id: EST-EFFORT
  title: Technical adaptation effort
  category: effort
  low: 95
  high: 155
  unit: person-days
  confidence: medium
  assumptions:
  - Explicit serialization adapter now required
  - Includes wrapper isolation uncertainty
  - Excludes rollout and unassessed recovery effort
  evidenceRefs:
  - E-MODEL2
  - E-SERIAL
recommendations:
- id: REC-ATLAS
  conclusion: Defer migration commitment; continue focused assessment.
  rationale: Technical feasibility is increasingly evidenced, but worthiness is not
    established without the economic counterfactual and recovery assessment.
  supportingFindings:
  - F-API
  - F-ADAPTER
  - F-DEPS
  limitations:
  - Unknown benefits
  - No recovery evidence
  - License exception unresolved
  decisionStatus: recommended
  stance: defer
gates:
- id: G-OPS
  title: Operational recovery assessment
  status: unmet
  critical: true
  rationale: Investigation started, but no restore/replay evidence is available.
  evidenceRefs: []
decisions:
- id: DEC-EXPERIMENT
  title: Authorize two assessment experiments
  status: approved
  owner: Architecture sponsor
  dueOn: '2026-11-06'
  rationale: Assessment experiment funding approved. This does not approve migration
    execution.
  evidenceRefs:
  - E-TX
  - E-SERIAL
- id: DEC-COUNTERFACTUAL
  title: Agree an economic counterfactual and horizon
  status: proposed
  owner: Finance sponsor
  dueOn: '2026-11-16'
  rationale: Worthiness cannot be evaluated without a baseline and horizon.
  evidenceRefs:
  - E-MODEL2
```
