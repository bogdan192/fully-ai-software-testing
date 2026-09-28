# Changelog

## 0.1.0 — 2026-09-28

- Publish the initial FaST concept and paradigm attributed to Bogdan Stefan Plesa.
- Add a dependency-free synthetic application and replay planner.
- Add an optional LangChain planner with opt-in LangSmith model tracing.
- Demonstrate eight checks across account and order workflows, with two injectable faults.
- Document evaluation limits, source provenance, and the CCA-F architecture mapping.

Verification during preparation: 10 offline tests passed; 25 healthy replay runs passed; both deliberate faults were detected. Optional dependencies installed successfully and the LangChain structured-output adapter was constructed without a network request. Tested package versions: LangChain 1.4.2, langchain-anthropic 1.7.4, LangSmith 0.14.1 on Python 3.13. No live-model evaluation was performed.

This date records this repository release, not an earlier invention date.
