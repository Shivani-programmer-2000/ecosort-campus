# Responsible AI considerations

| Principle | What the project does | Where in the code |
|---|---|---|
| **Fairness** | Plain language; no login; free to use. The sample knowledge base should be extended with items from many regions and households. Test on your own campus's items before a pilot. | `data/knowledge_base.json`, `eval/` |
| **Transparency** | Every answer shows stream, reason and source. An expander shows the retrieved passages and the retrieval score. When unsure it says so. | `ecosort/pipeline.py`, `app.py` |
| **Ethics** | Advisory only. No monitoring or penalising of individuals. Ambiguous or hazardous cases are referred to a person. No medical advice. | `ecosort/prompts.py`, ambiguity list |
| **Privacy** | No accounts or names. E-mail addresses and phone numbers typed by mistake are stripped. Photos are processed in memory and never written to disk. Feedback is three integer counters. | `ecosort/privacy.py`, `ecosort/feedback.py`, `ecosort/vision.py` |

## Known limitations

* The knowledge base is a small **sample**. It covers common campus items only and must be checked against your local municipal rules and bin colours.
* Retrieval is keyword-based (TF-IDF). Misspellings, slang and non-English names are not handled yet.
* The built-in evaluation set is small and was written by the author while building the system, so its results are optimistic. Collect real questions from a pilot before drawing conclusions.
* Photo mode is experimental and depends on a local vision model.
* Not legal or compliance advice.
