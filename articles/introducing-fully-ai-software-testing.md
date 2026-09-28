# Beyond Scripted Automation: Introducing Fully AI Software Testing

By **Bogdan Stefan Plesa**


A login test can click the right buttons and still tell us very little about the product. It may confirm that a familiar journey works while missing the changed redirect, the stale session, or the account that should no longer have access. Writing that script with an LLM changes how we produce the script. It does not automatically change how we investigate the application.

FaST, my proposal for Fully AI Software Testing, starts with a different unit of work: the testing objective. An agent receives a goal, observes the application, chooses an action, examines the result, and decides what to try next. The intended output is evidence that helps us understand the product.

“Fully AI” describes the operational delegation I want to explore. It does not mean that accountability disappears. People still choose the purpose of the investigation, the environment, the permissions, and the evidence needed for a release decision. An agent completing a task is not the same as a product being safe to ship.

Consider a simple objective: create a user, log in, place an order, refund it, and disable the account. A scripted path can perform those actions. A useful investigation also asks whether the refund can happen twice and whether an old session remains usable after the account is disabled.

Those questions change the architecture. The agent needs observations from the system, tools it can use, and permission boundaries it cannot rewrite. It also needs a way to distinguish a failed action from a defect. A network timeout does not prove that the application rejected a disabled account. A success message does not prove that money moved exactly once.

That is why the FaST reference project separates action selection from result evaluation. The planner chooses what to do. The execution layer performs the permitted action. An evaluator examines what actually happened. An unfinished investigation stays inconclusive; the model cannot turn it green by describing it optimistically.

The first release is intentionally small. It contains a synthetic account-and-order model, a deterministic offline walkthrough, and an optional LangChain adapter that asks a model to choose the next action. The offline walkthrough is a fixture, not AI. The project does not yet implement a general browser agent or claim broad autonomous defect discovery.

You can inspect the architecture without setting up a model account:

```sh
python -m fast_demo
python -m fast_demo --fault duplicate-refund
python -m fast_demo --fault stale-session
```

The two fault examples should fail. They are there to make the evidence boundary visible: a demonstration that can only succeed is difficult to learn from.

The next question is experimental. Does adaptive action selection find useful problems that a fixed path misses, and at what cost? Answering that requires repeated runs, realistic applications, and comparisons against existing approaches. This release creates a place to do that work; it does not pretend the work is already finished.

**FaST: Fully AI Software Testing — Concept and Paradigm, created by Bogdan Stefan Plesa.** Read the proposal and run the architectural reference at [the public repository](https://github.com/bogdan192/fully-ai-software-testing).

---

Part 1 of [the FaST article series](README.md). [About Bogdan Stefan Plesa](../AUTHOR.md). Prepared with AI assistance; technical scope and provenance are documented in [source notes](../docs/sources.md).

