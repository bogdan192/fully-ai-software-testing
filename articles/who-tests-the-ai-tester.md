# Who Tests the AI Tester? Evidence Before Autonomy

By **Bogdan Stefan Plesa**


An AI testing agent has two opportunities to fail. It can fail to perform a useful experiment, and it can misinterpret the experiment it did perform. Watching it finish a login journey tells us little about either risk.

FaST, my Fully AI Software Testing proposal, explores agent-led testing workflows. That makes the testing agent itself part of the system we need to investigate. Before making a reliability claim, we need to know how it behaves across repeated trials, changed conditions, and deliberately faulty applications.

James Bach's [Seriously Testing LLMs](https://www.satisfice.com/blog/archives/487957) challenges confidence based on isolated demonstrations. His later [Serious Data From Testing LLMs](https://www.satisfice.com/blog/archives/487962) presents evidence from a retrieval experiment under multiple conditions. These are useful challenges to FaST, not endorsements of it.

The first practical question is what counts as a result. Suppose an agent disables an account and says that access is revoked. We need an observation that supports that statement: can the old session still reach a protected resource? If that probe never happened, the honest result is “not observed.” An explanation from the agent is not a substitute for the probe.

The next question is whether the testing system can detect a known failure. The FaST architectural demo includes two deliberate faults: a duplicate refund and a session that survives account disabling. Its independent checks are designed to catch those effects. A healthy fixture gives us a useful comparison.

That does not establish that the agent will discover unfamiliar faults. The fixture exposes state directly and the objective explicitly asks for the relevant probes. It is a controlled architectural exercise. A realistic evaluation must add less obvious defects, browser and API uncertainty, and cases where the correct next step is unclear.

I would record at least four separate outcomes: a faulty application incorrectly passed, a healthy application incorrectly failed, an inconclusive investigation, and an observed policy violation. Collapsing them into one “accuracy” score can hide the most consequential failure. An agent that refuses every task may appear cautious while delivering no useful testing.

For an initial experiment, run multiple fresh trials for each condition, preserve every trace, and record the exact model and prompt version. Repeat with modest variations of the objective. Report denominators and costs. Twenty-five runs may reveal variation; it does not establish a universal reliability guarantee.

A second model can offer criticism, but it can share the first model's assumptions. Where possible, use independently specified business rules and application evidence. A refund ledger, a protected-resource response, and a known fixture state provide a different kind of support from another fluent explanation.

The first [FaST release](https://github.com/bogdan192/fully-ai-software-testing) provides the harness and the questions. Its deterministic tests validate a small implementation; they do not demonstrate live-model performance. The useful next contribution is a reproducible experiment, including the cases where the agent gets it wrong.

**Concept and Paradigm, created by Bogdan Stefan Plesa.** FaST's progress should be judged by the quality of the evidence it produces and the limitations it makes visible.

---

Part 3 of [the FaST article series](README.md). [About Bogdan Stefan Plesa](../AUTHOR.md). Prepared with AI assistance; technical scope and provenance are documented in [source notes](../docs/sources.md).

