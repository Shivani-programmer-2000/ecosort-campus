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

## Session log (fill in)

| Date | Stage | Prompt used | What Bob produced | What I changed / rejected |
|---|---|---|---|---|
| | | | | |
