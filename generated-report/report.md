# Atlas modernization assessment


Reporting period: 2026-W46 · As of 2026-11-09 · Approved by Demonstration reviewer


**Synthetic demonstration data**


## Executive summary

- The week changed our understanding: namespace-only session compatibility was contradicted; an explicit adapter is now evidenced on synthetic fixtures.

- Representative transaction evidence strengthened, and dependency alternatives partially matured. Technical adaptation effort rises to 95–155 person-days.

- Defer migration commitment: benefits remain unknown and operational recovery is insufficiently assessed. Next priorities are the economic counterfactual, recovery experiment and license position.


## Current assessment

Defer migration commitment; continue focused assessment.

Technical feasibility is increasingly evidenced, but worthiness is not established without the economic counterfactual and recovery assessment.


Analysis coverage: 74.2%. Validated evidence: 2/8. Decision gates met: 2/4.


## Coverage

- Framework compatibility: 100.0%; examined scope 3/3.

- Dependency viability: 100.0%; examined scope 3/3.

- Effort & worthiness: 33.3%; examined scope 1/3.

- Operational impact: 0.0%; examined scope 0/1.

- Runtime & platform: 50.0%; examined scope 1/2.

- Security & compliance: 100.0%; examined scope 2/2.


## Findings and evidence


### F-ADAPTER · Explicit session adapter required

Status: corroborated

An explicit serialization version adapter is required; it passes all sampled fixtures.

This informs feasibility and estimated research needs; it is not implementation completion.

Confidence: medium; uncertainties: Production fixture diversity unmeasured

- Evidence E-SERIAL (validated): Synthetic legacy fixture experiment: 9/32 fail without adapter; 32/32 pass with adapter.

  - 04-runtime-validation.md:L5–L23 · SHA-256 4836c587a0824ecc17a347f223e3f609fc084dcc121f138f2d97a03c3f6e9ee3


### F-API · Representative API adaptation validated

Status: validated

The representative transaction slice passes all 18 rollback cases with the adapter layer.

This informs feasibility and estimated research needs; it is not implementation completion.

Confidence: high; uncertainties: Distributed recovery excluded

- Evidence E-TX (validated): Synthetic transaction rollback experiment: 18/18 passed on a representative slice.

  - 04-runtime-validation.md:L5–L23 · SHA-256 4836c587a0824ecc17a347f223e3f609fc084dcc121f138f2d97a03c3f6e9ee3


### F-DEPS · Dependency path partially corroborated

Status: corroborated

Two maintained replacement candidates pass smoke checks; one wrapper and license exception remain unresolved.

This informs feasibility and estimated research needs; it is not implementation completion.

Confidence: medium; uncertainties: License exception not approved; Third wrapper untested

- Evidence E-DEPS (reviewed): Synthetic dependency inventory and candidate maintenance scan.

  - 02-technical-analysis.md:L5–L23 · SHA-256 90f89252abc6b201fdf5cb158bdd4d6d1b1b94744af1303238b5a68ea199b193

- Evidence E-DEPS2 (reviewed): Complete synthetic direct inventory with two interface smoke checks.

  - 05-dependency-and-security-review.md:L5–L15 · SHA-256 fa36424386f9d6d082e9c380ab5db9f61feb31ca0c2d1ba499759061c32228d9


### F-SERIAL · Namespace-only session hypothesis contradicted

Status: contradicted

Nine of 32 synthetic legacy fixtures fail without an explicit serialization adapter. The prior assumption is contradicted.

This informs feasibility and estimated research needs; it is not implementation completion.

Confidence: low; uncertainties: Legacy session diversity unknown

- Evidence E-SERIAL (validated): Synthetic legacy fixture experiment: 9/32 fail without adapter; 32/32 pass with adapter.

  - 04-runtime-validation.md:L5–L23 · SHA-256 4836c587a0824ecc17a347f223e3f609fc084dcc121f138f2d97a03c3f6e9ee3


## Risks


### R-SESSION · Stored session incompatibility raises adaptation effort and backward-compatibility uncertainty.

Status: open

- Evidence E-SERIAL (validated): Synthetic legacy fixture experiment: 9/32 fail without adapter; 32/32 pass with adapter.

  - 04-runtime-validation.md:L5–L23 · SHA-256 4836c587a0824ecc17a347f223e3f609fc084dcc121f138f2d97a03c3f6e9ee3


### R-WRAPPERS · Unmaintained wrappers may require custom replacement and increase effort.

Status: open

- Evidence E-DEPS (reviewed): Synthetic dependency inventory and candidate maintenance scan.

  - 02-technical-analysis.md:L5–L23 · SHA-256 90f89252abc6b201fdf5cb158bdd4d6d1b1b94744af1303238b5a68ea199b193


## Open questions


### Q-LEGAL · Are candidate replacement licenses acceptable?

Status: open

Request a documented license position.

- Evidence E-DEPS (reviewed): Synthetic dependency inventory and candidate maintenance scan.

  - 02-technical-analysis.md:L5–L23 · SHA-256 90f89252abc6b201fdf5cb158bdd4d6d1b1b94744af1303238b5a68ea199b193


### Q-ROI · What counterfactual cost and benefit horizon should management use?

Status: open

Validate avoided-cost assumptions.


### Q-SERIAL · Will legacy session fixtures deserialize safely?

Status: answered

Expand production-representative fixture diversity.

- Evidence E-SERIAL (validated): Synthetic legacy fixture experiment: 9/32 fail without adapter; 32/32 pass with adapter.

  - 04-runtime-validation.md:L5–L23 · SHA-256 4836c587a0824ecc17a347f223e3f609fc084dcc121f138f2d97a03c3f6e9ee3


### Q-SUPPORT · Which support terms and security policy oracle are authoritative?

Status: open

Obtain written terms and an approved deny-policy oracle.

- Evidence E-DEPS2 (reviewed): Complete synthetic direct inventory with two interface smoke checks.

  - 05-dependency-and-security-review.md:L5–L15 · SHA-256 fa36424386f9d6d082e9c380ab5db9f61feb31ca0c2d1ba499759061c32228d9


## Alternatives and trade-offs


### ALT-REPLACE · Replace with a new service implementation

Status: unassessed

Not yet measurable

Benefits: Potential simplification
Drawbacks: Functional parity and data migration unassessed


### ALT-RETAIN · Retain the current platform

Status: viable

Unknown; support stabilization not estimated

Benefits: No immediate conversion expenditure
Drawbacks: Unquantified support and opportunity costs

- Evidence E-MODEL (reviewed): Synthetic effort scenario model with explicitly incomplete benefits.

  - 03-economics-and-decisions.md:L5–L23 · SHA-256 d4ebea1d341c46b82d7406d7ca3b7ac0ca0d71a13ab79f0f1e5daf4fafcf92e9


### ALT-STAGED · Assess a staged modernization

Status: preferred

See EST-EFFORT; not a delivery commitment

Benefits: Limits exposure while testing critical hypotheses
Drawbacks: Parallel-platform overhead remains unknown

- Evidence E-SCAN (reviewed): Synthetic static namespace/API inventory across six modules.

  - 02-technical-analysis.md:L5–L23 · SHA-256 90f89252abc6b201fdf5cb158bdd4d6d1b1b94744af1303238b5a68ea199b193

- Evidence E-MODEL (reviewed): Synthetic effort scenario model with explicitly incomplete benefits.

  - 03-economics-and-decisions.md:L5–L23 · SHA-256 d4ebea1d341c46b82d7406d7ca3b7ac0ca0d71a13ab79f0f1e5daf4fafcf92e9


## Effort, cost and benefit


### EST-BENEFIT · Recurring economic benefit

Status: unknown

Range: None–None USD/year (Unknown when null). Assumptions: Benefit horizon and counterfactual not yet agreed


### EST-COST · One-time external assessment of transition costs

Status: low

Range: 35000–65000 USD (Unknown when null). Assumptions: Synthetic quotes; Licensing renegotiation excluded

- Evidence E-MODEL (reviewed): Synthetic effort scenario model with explicitly incomplete benefits.

  - 03-economics-and-decisions.md:L5–L23 · SHA-256 d4ebea1d341c46b82d7406d7ca3b7ac0ca0d71a13ab79f0f1e5daf4fafcf92e9


### EST-EFFORT · Technical adaptation effort

Status: medium

Range: 95–155 person-days (Unknown when null). Assumptions: Explicit serialization adapter now required; Includes wrapper isolation uncertainty; Excludes rollout and unassessed recovery effort

- Evidence E-MODEL2 (reviewed): Revised synthetic effort model incorporating session adapter work.

  - 06-worthiness-reassessment.md:L5–L15 · SHA-256 d0f46f3e79fa31fe4ee5194d66b7f4e3ca71dbcad6649bc4696080cecf27c3c0

- Evidence E-SERIAL (validated): Synthetic legacy fixture experiment: 9/32 fail without adapter; 32/32 pass with adapter.

  - 04-runtime-validation.md:L5–L23 · SHA-256 4836c587a0824ecc17a347f223e3f609fc084dcc121f138f2d97a03c3f6e9ee3


## Management decisions


### DEC-COUNTERFACTUAL · Agree an economic counterfactual and horizon

Status: proposed

Worthiness cannot be evaluated without a baseline and horizon.

- Evidence E-MODEL2 (reviewed): Revised synthetic effort model incorporating session adapter work.

  - 06-worthiness-reassessment.md:L5–L15 · SHA-256 d0f46f3e79fa31fe4ee5194d66b7f4e3ca71dbcad6649bc4696080cecf27c3c0


### DEC-EXPERIMENT · Authorize two assessment experiments

Status: approved

Assessment experiment funding approved. This does not approve migration execution.

- Evidence E-TX (validated): Synthetic transaction rollback experiment: 18/18 passed on a representative slice.

  - 04-runtime-validation.md:L5–L23 · SHA-256 4836c587a0824ecc17a347f223e3f609fc084dcc121f138f2d97a03c3f6e9ee3

- Evidence E-SERIAL (validated): Synthetic legacy fixture experiment: 9/32 fail without adapter; 32/32 pass with adapter.

  - 04-runtime-validation.md:L5–L23 · SHA-256 4836c587a0824ecc17a347f223e3f609fc084dcc121f138f2d97a03c3f6e9ee3


## Decision readiness


### G-COMPAT · Representative compatibility evidence

Status: met

Sampled API and serialization behavior is evidenced; this gate is limited to representative evidence.

- Evidence E-TX (validated): Synthetic transaction rollback experiment: 18/18 passed on a representative slice.

  - 04-runtime-validation.md:L5–L23 · SHA-256 4836c587a0824ecc17a347f223e3f609fc084dcc121f138f2d97a03c3f6e9ee3

- Evidence E-SERIAL (validated): Synthetic legacy fixture experiment: 9/32 fail without adapter; 32/32 pass with adapter.

  - 04-runtime-validation.md:L5–L23 · SHA-256 4836c587a0824ecc17a347f223e3f609fc084dcc121f138f2d97a03c3f6e9ee3


### G-DEPS · Maintained dependency path demonstrated

Status: met

A representative maintained replacement path is documented; complete legal clearance is tracked separately.

- Evidence E-DEPS2 (reviewed): Complete synthetic direct inventory with two interface smoke checks.

  - 05-dependency-and-security-review.md:L5–L15 · SHA-256 fa36424386f9d6d082e9c380ab5db9f61feb31ca0c2d1ba499759061c32228d9


### G-ECON · Defensible worthiness model

Status: unknown

Benefit model and counterfactual missing.

- Evidence E-MODEL (reviewed): Synthetic effort scenario model with explicitly incomplete benefits.

  - 03-economics-and-decisions.md:L5–L23 · SHA-256 d4ebea1d341c46b82d7406d7ca3b7ac0ca0d71a13ab79f0f1e5daf4fafcf92e9


### G-OPS · Operational recovery assessment

Status: unmet

Investigation started, but no restore/replay evidence is available.


## Next research priorities


### I-API · Are API and namespace adaptations bounded?

Status: validated

Validate a representative transaction slice.


### I-AUTH · Are authorization semantics equivalent?

Status: preliminary

Exercise denied and cross-tenant requests.


### I-CAPACITY · Is performance acceptable at peak load?

Status: not-examined

Design a replay dataset without customer data.


### I-DEPS · Do maintained replacement libraries exist?

Status: corroborated

Reconcile the full transitive inventory.


### I-EFFORT · What effort range is defensible?

Status: preliminary

Model remediation sensitivity.


### I-LICENSE · Are replacement licenses acceptable?

Status: preliminary

Request legal review of candidate licenses.


### I-RECOVERY · Can operations sustain the candidate platform?

Status: investigating

Interview operations and test restore assumptions.


### I-ROI · Are benefits and avoided costs worth the effort?

Status: investigating

Validate the counterfactual and benefit horizon.


### I-RUNTIME · Does the target runtime host representative workloads?

Status: preliminary

Run a transaction and recovery experiment.


### I-SERIAL · Can stored serialized sessions be read?

Status: corroborated

Capture legacy session fixtures.


### I-SUPPORT · Is the support lifecycle adequate?

Status: inconclusive

Obtain written support assumptions.


## Weekly evolution

- REVISED: I-API · Are API and namespace adaptations bounded?

- REVISED: I-DEPS · Do maintained replacement libraries exist?

- REVISED: I-LICENSE · Are replacement licenses acceptable?

- REVISED: I-RECOVERY · Can operations sustain the candidate platform?

- REVISED: I-ROI · Are benefits and avoided costs worth the effort?

- REVISED: I-RUNTIME · Does the target runtime host representative workloads?

- REVISED: I-SERIAL · Can stored serialized sessions be read?

- REVISED: I-SUPPORT · Is the support lifecycle adequate?

- ADDED: F-ADAPTER · Explicit session adapter required

- STRENGTHENED: F-API · Representative API adaptation validated

- STRENGTHENED: F-DEPS · Dependency path partially corroborated

- CONTRADICTED: F-SERIAL · Namespace-only session hypothesis contradicted

- ADDED: E-DEPS2 · Complete synthetic direct inventory with two interface smoke checks.

- ADDED: E-MODEL2 · Revised synthetic effort model incorporating session adapter work.

- ADDED: E-SERIAL · Synthetic legacy fixture experiment: 9/32 fail without adapter; 32/32 pass with adapter.

- ADDED: E-TX · Synthetic transaction rollback experiment: 18/18 passed on a representative slice.

- ADDED: R-SESSION · Stored session incompatibility raises adaptation effort and backward-compatibility uncertainty.

- RESOLVED: Q-SERIAL · Will legacy session fixtures deserialize safely?

- ADDED: Q-SUPPORT · Which support terms and security policy oracle are authoritative?

- REVISED: EST-EFFORT · Technical adaptation effort

- REVISED: G-COMPAT · Representative compatibility evidence

- REVISED: G-DEPS · Maintained dependency path demonstrated

- REVISED: G-OPS · Operational recovery assessment

- ADDED: DEC-COUNTERFACTUAL · Agree an economic counterfactual and horizon

- REVISED: DEC-EXPERIMENT · Authorize two assessment experiments

- REVISED: REC-ATLAS · Defer migration commitment; continue focused assessment.

- REVISED: ACT-RESEARCH · Serialization and transaction research experiments

- REVISED: summary · Executive synthesis updated


## Measurement methodology

Coverage = weighted mean of dimension examined-scope / planned-scope ratios. Examined statuses: preliminary, corroborated, validated, inconclusive, contradicted, superseded. Investigating and not-examined count as zero; missing planned scope yields Unknown.

Evidence validation = validated evidence count / all evidence records, including assumptions and rejected evidence. Evidence maturity also exposes corroborated-or-validated findings / all findings.

Decision readiness = met gates / all gates. Any unmet or unknown critical gate blocks a proceed recommendation. No metric measures migration implementation or implies feasibility.
