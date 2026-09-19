# Using IBM Bob on this project

IBM Bob is an AI development partner. In this project it is a **build-time** tool
(planning, coding, testing, documentation, review). The AI that end users talk to
is retrieval over a cited knowledge base at **run time**, with IBM Granite as an optional
answer writer that turns it into full RAG. A human reviews everything Bob produces.

> **Add your own evidence.** The internship asks you to show where Bob was used.
> Run the prompts below in your own Bob session, then paste screenshots or short
> summaries into the *Session log* at the bottom of this file. Keep only what
> you actually did.

## Access and cost

Bob is **not needed to run or deploy** EcoSort. It is only the build-time tool.
IBM offers a 30-day free trial with a limited Bobcoin allowance (see <https://bob.ibm.com/trial>);
paid plans follow. Check with your internship coordinator whether access is provided.
Because the allowance is small, run a few focused sessions (one per prompt below) rather than
open-ended chats, and screenshot each session as evidence.

## Prompts to try in Bob

**Plan**
> Read README.md and docs/architecture.md. Suggest three improvements to the retrieval pipeline for a campus waste-segregation assistant and list the files each would touch.

**Build**
> Add an embedding-based retriever in ecosort/retriever.py with the same `search(query, k)` signature. Keep the TF-IDF retriever as a fallback and add tests.

**Test**
> Read eval/test_items.csv and ecosort/pipeline.py. Write 50 more realistic test items (including misspellings and Hinglish item names) and find cases where the assistant is confidently wrong.

**Document**
> Generate docstrings for every public function in ecosort/ and a short user guide for campus housekeeping staff.

**Review**
> Review the repository for hard-coded secrets, personal-data storage, and prompt-injection risks in the user input path. List findings by severity.

## Session log

| Date | Stage | Prompt used | What Bob produced | What I changed / rejected |
|---|---|---|---|---|
| 2026-09 | Plan (`/init`) | `/init` | `AGENTS.md` plus three mode files (`.bob/rules-agent`, `.bob/rules-ask`, `.bob/rules-plan`), covering the `EcoSort.ask()`-only entry point, the stream guardrail at `pipeline.py:137`, the frozen `Settings`, and the JS/Python dual-implementation trap in `site/engine.js`. | Kept as generated. Notes-only write (no code touched), approved directly. |
| 2026-09 | Review | "Review this repository for hard-coded secrets, personal-data storage, and prompt-injection risks in the user input path. List findings by severity and save them to `docs/bob_review.md`. Do not modify any existing files." | `docs/bob_review.md`: 3 medium, 4 low, 3 informational findings, each with file:line references — notably the exception-leak at `pipeline.py:83`→`app.py:81`, the unredacted `Settings` repr, the unbounded `_cache` dict, and narrow PII stripping in `privacy.py`. | Kept the file as Bob wrote it — reviewed but did not let Bob touch `app.py` or `ecosort/` in this session (edits to existing files were declined per the prompt's own instruction). |
| 2026-09 | Fix (from review) | Triaged the review findings and asked Bob to patch the three "worth fixing" items: redact secrets from `Settings.__repr__`, stop surfacing raw exception text in the UI, bound the reply cache. | `ecosort/config.py` — `watsonx_api_key`/`watsonx_project_id` marked `field(repr=False)`. `ecosort/pipeline.py` — startup/init failures now set a fixed user-facing note ("AI model unavailable; using the offline knowledge base.") and log the real exception server-side via `logging.getLogger(__name__).warning(...)`; `_cache` capped at 256 entries. | Deferred: `us-south` hard-coded watsonx region (low priority, config flexibility not security) and the two names/Aadhaar/PAN-style PII patterns beyond email/phone — left as future work, not blocking. |
| 2026-09 | Test | Asked Bob to add tests proving the three fixes actually work (and to check them against the pre-fix code). | `tests/test_security.py` — `test_settings_repr_hides_secrets`, `test_startup_failure_note_hides_exception_detail`, `test_cache_never_exceeds_256_entries`. Bob confirmed by hand (pytest wasn't installed in that session) that all three fail on the original code and pass on the patched code. | Left one harmless unused import (`from ecosort.pipeline import Answer`) in the test file rather than editing it. |
| 2026-09 | Build | "Read `eval/test_items.csv` and `ecosort/pipeline.py`. Write 20 more realistic test items, including misspellings, in a new file `eval/bob_extra_items.csv` with the same columns (item,expected). Do not edit existing files." | `eval/bob_extra_items.csv` — 20 new rows, same schema as `eval/test_items.csv`. | Kept as a new file; did not let Bob touch `eval/test_items.csv` or `run_eval.py`. |
| 2026-09 | Document | "Write a one-page user guide for campus housekeeping staff explaining how to use EcoSort Campus, and save it as `docs/user_guide.md`. Do not edit existing files." | `docs/user_guide.md`. | Kept as a new file. |
