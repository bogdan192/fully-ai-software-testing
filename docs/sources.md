# Sources and provenance

Prepared for the FaST proposal by **Bogdan Stefan Plesa**. Links checked during preparation on 2026-09-28. Source dates can differ from search-engine timestamps; consult the original page.

## Testing and prior work

- James Bach, [Seriously Testing LLMs](https://www.satisfice.com/blog/archives/487957): repeated trials, careful observation, and retrieval-consistency experiments. Cited as critical testing guidance.
- James Bach, [Serious Data From Testing LLMs](https://www.satisfice.com/blog/archives/487962): a concrete multi-condition LLM experiment. We do not reuse its dataset or claim to reproduce it.
- James Bach, [WAIT #2 Peer Conference Report](https://www.satisfice.com/blog/archives/487671): earlier community investigation of testing AI and AI-assisted testing. This is one reason the repository does not assert invention of the entire field.

## Agent tooling

- LangChain, [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output): schema-constrained model responses. Valid structure is not proof of a correct decision.
- LangSmith, [Evaluation types](https://docs.langchain.com/langsmith/evaluation-types): offline and online evaluation settings. The repository implements local evaluation and optional tracing, not all capabilities of this service.

## Certification mapping

- Anthropic, [Claude Partner Network announcement](https://www.anthropic.com/news/claude-partner-network): confirms the Claude Certified Architect, Foundations certification and its architecture focus.
- [Externally hosted exam-guide copy](https://nehasharma.dev/images/content/claude-exam-guide.pdf), pages 2–3: source for the five domain labels. This is a mirror, not an issuer-controlled URL, and its currentness/authenticity has not been independently certified. Only high-level domain labels are used; no exam questions or answers are reproduced.

The README's mapping from those areas to testing is this project's interpretation. Verify the latest issuer-provided blueprint before relying on it for certification study. There is no affiliation with Anthropic, LangChain, LangSmith, James Bach, or their organizations.

## Authorship boundaries

Bogdan Stefan Plesa commissioned this repository and supplied its concept, attribution, intended topics, and example flows. This initial documentation and reference implementation were prepared with AI assistance. The detailed architecture is an initial formulation for review and refinement, not a transcription of a previously supplied specification.

No independent source establishing historical priority for FaST was supplied for this release. Future provenance additions should link actual dated publications or archived artifacts; repository creation is not evidence of an earlier invention date.
