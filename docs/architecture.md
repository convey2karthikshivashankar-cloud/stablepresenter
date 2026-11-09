# Architecture and extension points

The implementation follows the supplied SRS v1.0 and the shared discussion: https://chatgpt.com/share/6af1d7d4-311c-83e8-a07c-e42c4277de1f .

```text
Research Markdown + agent-authored structured blocks
  -> ingestion.py (safe YAML; file hashes; source locations)
  -> model.py (strict JSON Schema + cross-record integrity)
  -> store.py (optimistic concurrency; atomic writes; provenance)
  -> revisions + explicit approved snapshots
  -> diff.py (stable-ID field comparisons)
  -> reporting.py (fixed Quarto composition)
  -> self-contained cumulative / weekly / historical HTML
```

`assessment_intelligence/model.py` owns validation and measurements. `ingestion.py` reads only changed documents and treats prose as source evidence, never executable HTML. `store.py` owns revision metadata and single-writer transactions. `diff.py` classifies changes deterministically. `reporting.py` renders approved records with Quarto. `assets/shell.html`, `theme.css`, and `app.js` are the versioned presentation contract. Agent update methods have no path to those files.

The data store is JSON on disk. `current.json` is the draft head; `revisions/HASH.json` preserves every committed full state and provenance, with a parent content hash. `snapshots/PERIOD.json` freezes an explicitly reviewed report, its state hash, reviewer, approval timestamp and computed change summary. Application methods never overwrite an existing period. Hashes detect accidental state corruption; they are not signatures. Local writers use an exclusive create lock; current state advances using fsync and atomic replace. A power loss between revision creation and head replacement can leave a harmless orphan revision. Recovery can restore that revision. No distributed-lock assumptions are made.

Each snapshot embeds original source text and hashes, so subsequent file edits cannot alter historical evidence. Historical HTML contains only its own and earlier approved states. The cumulative HTML includes every approved state for on-demand browsing. Comparison is by stable entity ID, with exact field before/after values. Confidence enum increases/decreases are labeled strengthened/weakened; contradicted and superseded statuses are explicit. Text-only changes are revised, not guessed semantic strengthening.

Quarto supplies the publishing engine, HTML document, Bootstrap base and embedded resources. The app supplies the fixed domain-specific component catalog and content data; no agent chooses component hierarchy or generates CSS. The same approved data/template/Quarto version produces byte-identical HTML in the verified environment. Approval timestamps belong to versioned input. There is no build-time timestamp in report content. Theme behavior and search state are local browser UI preferences, not assessment facts.

Use Python `Store.ingest`, `Store.records`, `Store.patch`, `Store.approve`, `Store.rollback`, and `reporting.build` as an automation API; the CLI is the supported process API. A network API is not required for Phase 1.

To add an assessment dimension, create its structured record and planned investigations; no template edits are needed. To add entity fields, edit `scripts/generate_schema.py`, regenerate and version the schema, then update renderer/test contracts. A new component or an execution-tracking module requires a deliberate presentation version and a distinct domain model. Future authenticated collaboration, server storage, model adapters or Astro publishing can use the same validated snapshots without allowing models to edit templates.
