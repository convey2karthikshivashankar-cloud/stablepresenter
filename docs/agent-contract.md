# Agent input and update contract

The platform is model/vendor independent. It does not invoke an LLM. Agents receive relevant Markdown excerpts, the target entity's schema, its current record and base hash. They output JSON records or a restricted JSON Patch. Existing plain prose is preserved; facts are created only by explicit authored records.

Suggested instruction to an analysis agent:

> Evaluate only the supplied research question. Preserve IDs. Distinguish observations, assumptions and interpretation. Cite source paths and one-based inclusive line ranges. State limitations, confidence, unresolved questions and the next experiment. Output JSON matching the supplied record schema or restricted patch operations. Do not output HTML, CSS, JavaScript or layout instructions. Do not claim validation unless reviewed evidence demonstrates it. Never equate research coverage with migration feasibility. Preserve contradicted conclusions and add a successor finding instead of deleting the historical understanding.

Source files use one or more `assessment` fences. Top-level fields may be `program`, `executiveSummary`, or a normalized collection name containing a list of records. New entities receive dates/revision counters automatically. `@self` in source references means the containing Markdown file; the application attaches its SHA-256. Without explicit references, a record points to the narrative preceding its structured block. Evidence always requires a source locator. Cross-file references should use the source-root-relative POSIX path and correct source hash; all targets are checked before commit.

Updates require the expected current hash. If another agent writes first, the application rejects the stale proposal; reload the affected records and regenerate the proposal. Do not automatically overwrite the newer state. Unknown keys/statuses/references fail before head mutation. Full-entity updates replace only named entity IDs; omitted entities survive.

Agent safety is an application API contract, not OS isolation. For stronger filesystem enforcement, grant agents write access only to a staging directory and have a separate reviewer process invoke the CLI. The module does not sandbox an arbitrary external agent that already has filesystem access.
