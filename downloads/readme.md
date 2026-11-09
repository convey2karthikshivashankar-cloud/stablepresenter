# Assessment Intelligence

A working, local-first assessment and executive reporting module. It tracks the maturity of modernization **research**, the evidence supporting it, uncertainty, effort ranges and migration worthiness. It does not track migration implementation.

AI agents interpret research and submit data. JSON Schema, revision control and fixed Quarto components own validation, history and presentation. No API key, account, backend service, Node.js or cloud subscription is required.

## Open the supplied reports

The source bundle includes `generated-report/index.html`, `generated-report/weekly-delta.html`, historical reports, raw snapshots and original Markdown. Open the HTML in a browser; every HTML file embeds its assets and data. A separate report ZIP contains the same reports. `generated-report/report.md` is a readable text export. All sample observations, compatibility claims, costs and measurements are **synthetic**.

If your workstation blocks file URLs, serve the directory:

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory generated-report
```

Visit http://127.0.0.1:8000. The report never sends data to a remote server.

## Install

Requirements: Python 3.11+, Quarto CLI (verified with 1.11.9), and a modern browser. Install Quarto from https://quarto.org/docs/get-started/ . The module calls its executable directly; `QUARTO_BIN` or `--quarto /absolute/path/to/quarto` can select a portable installation.

From the extracted source root on Linux/macOS:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e . --no-deps
```

On Windows PowerShell, use `py -3 -m venv .venv` and `.venv\Scripts\Activate.ps1`, then the same pip commands. To install only runtime dependencies instead of the complete verified test environment, use `python -m pip install -e .`.

## One-command sample build

After installation, from the source root:

```sh
assess --store demo-data demo --samples samples --out site
```

This ingests six substantial Markdown files across two periods, approves two sample snapshots, and renders the cumulative, differential and historical Quarto HTML reports. It requires a new/empty store; choose a different `--store` on a repeat demo. To rebuild an existing store:

```sh
assess --store demo-data validate
assess --store demo-data build --out site
```

Open `site/index.html` or serve `site` with the standard-library HTTP server above. `site/weekly-delta.html` opens directly on Weekly Evolution. `site/history/2026-W45/index.html` contains only information known in that period. The current report's selector can browse every approved snapshot.

## Research ingestion and review

Ordinary Markdown prose is retained verbatim. The module imports only fenced `assessment` blocks containing structured YAML or JSON. It **does not pretend to perform natural-language analysis**: your preferred AI agent or a human authors those records after interpreting the research. A prose-only file is accepted as source material and is visible in the technical appendix; it creates no inferred facts. See the six supplied source files for the complete format.

```sh
assess --store my-data ingest --sources samples/week-1 --as-of 2026-11-02 --actor analyst-a
assess --store my-data status
```

Inspect the resulting `my-data/current.json` and the source/evidence references. Then approve a report:

```sh
assess --store my-data approve --period 2026-W45 --reviewer "Assessment lead" --base-hash HASH_FROM_STATUS
assess --store my-data build --out my-report
```

For subsequent sources, provide the current hash. Omitted entities remain present. Only new or hash-modified Markdown documents are parsed. Changed files must carry updated locators for every record whose source changed; stale references are rejected, never silently rebound.

```sh
assess --store my-data ingest --sources samples/week-2 --as-of 2026-11-09 --actor analyst-b --base-hash HASH_FROM_STATUS
assess --store my-data approve --period 2026-W46 --reviewer "Assessment lead" --base-hash NEW_HASH_FROM_STATUS
assess --store my-data build --out my-report
```

`--store` is a global option and belongs **before** the subcommand. Dates and periods are explicit inputs. Period labels are configurable, e.g. `2026-W46`, `board-2026-11-09`, or `2026-W46-revised`. Reusing an approved period fails.

## Agent updates without HTML access

Produce a small relevant context package, with no HTML:

```sh
python scripts/agent_context.py --store demo-data --collection findings --id F-API > agent-context.json
```

Ask the agent to output a patch conforming to `schemas/patch.schema.json`. The included example reduces confidence and adds an uncertainty:

```sh
assess --store demo-data patch --file examples/confidence-update.patch.json --as-of 2026-11-10 --actor agent-review --base-hash HASH_FROM_STATUS
```

`add`, `replace`, `remove` and `test` JSON Patch operations are supported, including array indexing and JSON Pointer escaping. `move` and `copy` are deliberately unsupported. Identity, schema, presentation, timestamps and revision counters are protected. Every patch is applied to an isolated copy, then the **whole resulting state** is schema-validated and checked for referential integrity. Any failure rejects the complete transaction.

For full-entity updates, `assess records --file records.json ...` accepts `{ "findings": [COMPLETE_FINDING_RECORD] }` with the same hash check. Preserve source references from the context package; timestamps and revisions are managed by the store. New records need supporting source references or explicit evidence; unsupported findings are marked unverified in the UI.

Every successful content change creates an immutable `revisions/HASH.json` plus an atomic working `current.json`. A draft is **not** published by `build`: only explicit approved snapshots are rendered. Approval here is a local review operation, not an authenticated identity or a migration authorization.

## History, rollback and scheduling

```sh
assess --store demo-data history
assess --store demo-data diff demo-data/snapshots/2026-W45.json demo-data/snapshots/2026-W46.json
assess --store demo-data rollback --revision OLD_HASH --as-of 2026-11-11 --actor reviewer --base-hash CURRENT_HASH
```

Rollback creates a new draft revision; it does not rewrite snapshots. Review it and approve a new period if you want to publish it. Missing entity references, invalid estimates and proceed recommendations with unknown/unmet critical gates are rejected.

A workstation cron job / Task Scheduler can run:

```sh
python scripts/weekly_report.py --store demo-data --out site
```

This rebuilds approved reports. Explicit `--approve --reviewer "Review automation"` also snapshots the current draft using the ISO week of the **assessment as-of date**, with the period format in `config/reporting.json`. Use this only in a workflow where the draft has already been reviewed. A duplicate period fails safely. The timezone in that config documents your scheduler setting; the module does not install a scheduler or infer reporting dates from the host clock.

For Git-backed recovery in your own repository:

```sh
git add my-data/current.json my-data/revisions my-data/snapshots
git commit -m "Approve weekly assessment report"
```

## Verify

The full test suite needs Quarto and Chromium. Install a Playwright Chromium build if a system Chromium is unavailable:

```sh
python -m playwright install chromium
python -m pytest -q --junitxml=test-results/results.xml
```

`CHROMIUM_BIN=/absolute/path/to/chromium` selects a system installation. Unit tests alone: `python -m pytest tests/test_domain.py -q`. Browser tests use a temporary localhost server, then separately render with network access disabled. No paid service is contacted.

The suite exercises ingestion, unchanged-input skipping, cumulative preservation, evidence hashes/locators, lifecycle revisions, schema violations, stale writers, atomic rejection, rollback, immutable approval, repeated Quarto build equivalence, real UI navigation, source/JSON downloads, contradiction history, unknown estimates, dark theme, keyboard use, print rendering, responsive layouts, XSS text handling and a visual regression negative control.

The approved visual baseline is `tests/visual/overview.png` at 1440×1080, Linux Chromium (recorded in `docs/verification.md`). The comparator tolerates 0.5% changed pixels with a 24/255 per-pixel channel threshold. Different OS fonts or browser versions can require a reviewed platform baseline. First inspect `test-results/overview.png` and `visual-difference.png`; only after intentionally accepting a visual change, regenerate with:

```sh
UPDATE_VISUALS=1 python -m pytest tests/test_reports.py::test_visual_baseline_and_negative_control -q
```

PowerShell: set `$env:UPDATE_VISUALS="1"` before the command. Normal verification never updates baselines. A deliberately shifted layout is tested to ensure the comparator rejects it.

## Build a distributable Python module

```sh
python -m build
python -m pip install dist/assessment_intelligence-1.0.0-py3-none-any.whl
```

The wheel includes schemas and fixed report assets. The source bundle additionally contains samples, tests, scripts, documentation and generated example data/reports. To rerender the supplied Quarto composition directly: change into `generated-report` and run `quarto render report.qmd`.

## Data model and measurement

The strict versioned schema is `schemas/assessment.schema.json`; the runtime ships the identical schema. Stable IDs key normalized collections: dimensions, investigations, findings, evidence, risks, questions, alternatives, estimates, gates, decisions, recommendations and research activities. Each entity has `createdAt`, `updatedAt`, an application-controlled `revision`, and source references. Evidence stores original path, line range and SHA-256 in `sourceRefs`; original Markdown is embedded in the state and frozen snapshots.

Coverage = weighted mean of examined planned investigation scope within each dimension. Examined statuses are preliminary, corroborated, validated, inconclusive, contradicted and superseded. Investigating/not-examined contribute zero. A dimension without a planned denominator makes overall coverage Unknown. Coverage is not a percentage of feasibility.

Evidence validation = validated evidence records / all evidence records, including assumptions and rejected evidence. Finding maturity separately shows corroborated-or-validated findings / all findings. Decision readiness = met gates / all gates; an unknown/unmet critical gate blocks proceed. Missing evidence or gates yields Unknown. Open uncertainties count questions marked open; deferred questions remain visible. No guessed stage percentages, ROI, currency conversions or mixed-unit totals are introduced.

See [architecture](docs/architecture.md), [agent contract](docs/agent-contract.md), [verification and acceptance mapping](docs/verification.md), and [scope and limitations](docs/limitations.md). Source is MIT licensed. Quarto, JSON Schema, PyYAML, Playwright and their dependencies retain their respective licenses and are not bundled as executables.
