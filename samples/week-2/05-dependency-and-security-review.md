# Week 2 • dependencies, licensing and security unknowns

> SYNTHETIC CASE STUDY — not vendor guidance or production measurements.

## Dependency reconciliation
The fictional inventory now reconciles all 187 direct dependencies. Two maintained replacement candidates pass interface smoke checks; one wrapper still needs an isolation experiment. A license exception has been requested but not approved.

## Security investigation
A negative-case walkthrough exposes two ambiguous authorization paths. Without an approved policy oracle these results are inconclusive. The support-policy investigation could not reconcile conflicting draft vendor terms, so it is explicitly inconclusive rather than favorable evidence.

## Cross-agent interpretation
The inventory agent and security agent worked on separate records. Review retained original evidence IDs and added new evidence rather than relabeling old assumptions as validated.

## Open research
Obtain authoritative license and support terms. Validate denied, cross-tenant and delegated-access cases. Test the third wrapper in isolation.

```assessment
evidence:
- id: E-DEPS2
  description: Complete synthetic direct inventory with two interface smoke checks.
  kind: analysis
  verificationStatus: reviewed
  capturedAt: '2026-11-09'
  reviewedBy: Analysis lead
  limitations: License exception unresolved; third wrapper experiment pending.
  sourceRefs:
  - path: '@self'
    startLine: 5
    endLine: 15
findings:
- id: F-DEPS
  investigationId: I-DEPS
  title: Dependency path partially corroborated
  conclusion: Two maintained replacement candidates pass smoke checks; one wrapper
    and license exception remain unresolved.
  status: corroborated
  confidence: medium
  evidenceRefs:
  - E-DEPS
  - E-DEPS2
  implications: This informs feasibility and estimated research needs; it is not implementation
    completion.
  uncertainties:
  - License exception not approved
  - Third wrapper untested
  nextInvestigation: Resolve license and isolation questions.
  severity: high
  impact: mixed
  supersedes: []
gates:
- id: G-DEPS
  title: Maintained dependency path demonstrated
  status: met
  critical: false
  rationale: A representative maintained replacement path is documented; complete
    legal clearance is tracked separately.
  evidenceRefs:
  - E-DEPS2
questions:
- id: Q-SUPPORT
  dimensionId: D-SEC
  question: Which support terms and security policy oracle are authoritative?
  status: open
  owner: Security & procurement
  nextStep: Obtain written terms and an approved deny-policy oracle.
  blocking: true
  evidenceRefs:
  - E-DEPS2
```
