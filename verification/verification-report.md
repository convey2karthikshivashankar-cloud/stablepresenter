# End-to-end verification report

Verification date: 9 November 2026 (Asia/Kolkata). Input contract: supplied SRS v1.0. Result: **30 automated tests passed**, including real Chromium workflows and a visual-regression negative control. No test was skipped. The normal final run did not update visual baselines.

## Environment and commands

- Python 3.12.14; Quarto 1.11.9 (official portable Linux distribution).
- Chromium 156.0.8078.79, Debian GNU/Linux 13; Playwright 1.55.0.
- PyYAML 6.0.3; jsonschema 4.25.1; pytest 8.4.2; Pillow 11.3.0.
- Viewports: 1440×1080 desktop, 1024×900, 768×900 and 390×900 mobile.
- Runtime/test dependencies are recorded in `requirements-lock.txt`.

Executed from the source root:

```sh
python -m pytest -q --junitxml=test-results/results.xml
python -m build
assess --store data validate
assess --store data build --out generated-report
```

An isolated wheel installation was also used to execute the documented two-period demo from a fresh, empty store. The report's original inputs are included; Python/Quarto/browser binaries and virtual environments are excluded from the downloadable source archive.

## Samples and expected results

Six substantial Markdown source files contain **852 lines**, including narrative summaries, observation tables, experimental design, exclusions, assumptions, a deliberately hostile script string, scoped effort ranges and structured assessment blocks. They describe **49 current entities** across two periods:

| Check | Baseline (2026-W45) | Current (2026-W46) |
| --- | --- | --- |
| Assessment date | 2026-11-02 | 2026-11-09 |
| Sources retained | 3 | 6 |
| Namespace-only session hypothesis | Preliminary, explicitly unverified assumption | Contradicted by synthetic fixture results |
| Representative transaction conclusion | Preliminary, medium confidence | Validated, high confidence |
| Technical adaptation estimate | 60–100 person-days | 95–155 person-days |
| Recurring economic benefit | Unknown | Unknown |
| Recommendation | Pending | Defer migration commitment |

Current coverage is **74.2%** of weighted planned research scope; validated evidence is **2/8 (25%)**; **3 questions** remain open; **2/4 decision gates (50%)** are met. Critical economic and recovery gates still block a proceed recommendation. These are independent measures. None measures migration implementation.

## Acceptance mapping

| Criterion | Verification evidence | Result |
| --- | --- | --- |
| AC-01: Stable report layout on repeated builds | `test_repeated_quarto_build_semantically_identical`: HTML, fixed data composition, style and build manifest byte comparisons; visual baseline | Pass |
| AC-02: One finding update affects its record/dependents | `test_patch_only_affected_entity_and_assets_unchanged`: only F-API appears in structured diff; unrelated records equal | Pass |
| AC-03: Agent updates do not edit presentation | Same test hashes every UI asset before/after; CLI and context utility accept records/patches only | Pass |
| AC-04: Published weekly snapshots preserved | `test_immutable_approval_and_draft_separation`, plus historical archive checks | Pass |
| AC-05: Cumulative and differential reports from one KB | `test_incremental_cumulative_and_evolution` and complete management browser workflow | Pass |
| AC-06: Evolving conclusions traceable | Contradicted, strengthened, weakened, revised and resolved changes checked, with before/after fields and revision numbers | Pass |
| AC-07: Source references and verification states | Browser executive → finding → evidence → original line range → Markdown download; hash/locator unit checks | Pass |
| AC-08: Missing evidence and uncertain estimates explicit | Empty denominators return Unknown; economics shows Not yet measurable; unverified source evidence visible | Pass |
| AC-09: Invalid/conflicting changes reject atomically | 13 parameterized invalid patch cases; stale hash; writer lock; corruption check; YAML/path checks; current/revision counts unchanged on rejection | Pass |
| AC-10: Visual regression detection | Golden PNG comparison plus deliberate 66px layout shift rejected by the same comparator | Pass |
| AC-11: Local operation without paid service | Local temporary HTTP service, then offline-rendered generated HTML with all external requests aborted; no remote HTTP requests | Pass |
| AC-12: Documented fresh build | Two-period fixtures build from empty stores; sdist and wheel build; isolated wheel demo reproduces the source state hashes | Pass |

## Additional checks and artifacts

All nine persistent sections render. Findings filter and search work. Earlier snapshot selection restores the earlier conclusion and excludes later findings. Standalone early archives contain no future-period data. Data and original Markdown downloads are checked. Dark theme, keyboard activation, modal closure and print visibility are exercised. All nine sections are printable. A PDF was generated from the final report. Mobile/tablet sections have no document-wide horizontal overflow; wide tables scroll inside their containers.

The literal `<script>window.__sourceExecuted = true</script>` appears as source text, with no execution. Raw research HTML is never inserted as trusted markup. Traversal paths, symlinks, YAML object constructors, aliases, stale evidence hashes, unknown record references and attempts to patch presentation/version/revision metadata are rejected.

The source bundle includes `verification/results.xml`, screenshots, visual-difference evidence, sample status JSON and this report. `tests/visual/overview.png` is the reviewed regression baseline. The negative-control mutated screenshot is deliberately broken and is labeled `layout-mutation.png`; it is not the delivered UI.

## Verification limits

These are synthetic cases; the checks establish module behavior, not factual correctness of real migration analysis. Human/agent assertions of confidence and verification need domain review. Application-level snapshots are not an authenticated or tamper-proof ledger. Browser workflow checks use the installed Chromium; other browsers and complete accessibility conformance are not certified. Direct `file://` navigation is blocked by the managed browser's enterprise policy, so self-contained offline behavior was verified by loading the generated HTML bytes with network disabled; ordinary static serving was verified separately.
