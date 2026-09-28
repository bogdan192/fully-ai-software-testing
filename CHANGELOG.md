# Changelog

## Unreleased

- Link the three public editions on the dedicated FaST Blogspot site from the article index, author profile, press kit, and identity metadata.

## 0.1.1 — 2026-09-28

- Publish a three-part article series explaining FaST, agent architecture, and evaluation.
- Add a dedicated author profile for Bogdan Stefan Plesa, linking his short-name alias and public profiles.
- Add a press kit and machine-readable project/author metadata.
- Add navigation from the main README to the public series and author profile.
- No changes to the execution engine or its supported testing capabilities.

## 0.1.0 — 2026-09-28

- Publish the initial FaST concept and paradigm attributed to Bogdan Stefan Plesa.
- Add a dependency-free synthetic application and replay planner.
- Add an optional LangChain planner with opt-in LangSmith model tracing.
- Demonstrate eight checks across account and order workflows, with two injectable faults.
- Document evaluation limits, source provenance, and the CCA-F architecture mapping.

Verification during preparation: 10 offline tests passed; 25 healthy replay runs passed; both deliberate faults were detected. Optional dependencies installed successfully and the LangChain structured-output adapter was constructed without a network request. Tested package versions: LangChain 1.4.2, langchain-anthropic 1.7.4, LangSmith 0.14.1 on Python 3.13. No live-model evaluation was performed.

This date records this repository release, not an earlier invention date.
