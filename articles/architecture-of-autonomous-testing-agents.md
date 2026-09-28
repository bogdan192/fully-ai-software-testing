# The Architecture of Autonomous Agents in Software Testing

By **Bogdan Stefan Plesa**, creator of the FaST concept and paradigm.


An autonomous testing agent needs more than a browser and a prompt. It needs an objective, observations, a restricted set of actions, and a defensible way to report what it learned. In FaST, my Fully AI Software Testing proposal, those responsibilities form an explicit architecture.

The [reference repository](https://github.com/bogdan192/fully-ai-software-testing) implements a compact version in Python. Its application is an in-memory model, so there are no real users, orders, or payments. The purpose is to make the boundary between an agent's choices and the evidence for its conclusions easy to inspect.

## One decision at a time

The planner receives the current application snapshot and the history of observed actions. It returns one action. The runner validates that action against an allowlist before executing it. The resulting state becomes input to the next decision.

In offline mode, the planner is a fixed sequence. In model mode, LangChain requests a structured response from a configured LLM. Structured output narrows the format of the response; it does not prove that the chosen action makes sense. The runner therefore enforces the tool boundary independently.

The minimal interface is small:

```python
class Planner:
    def decide(self, observation, history):
        # Return one Decision with an allowed action name.
        ...
```

This separation makes it possible to compare different planners against the same application and evaluator. It also exposes an uncomfortable possibility: a more elaborate agent may perform worse than the replay fixture on a routine task.

## Evaluate the consequence

A refund action is not successful merely because a tool returned a friendly message. The evaluator must check the state change. The demonstration uses a refund counter; a real application would need an appropriate transaction record or ledger.

The stale-session example is equally important. After disabling a user, probe the existing session before attempting another login. A new login could overwrite the old session state and hide the defect. The demo treats the wrong observation order as missing evidence, not a pass.

Every report includes the individual checks, observed transitions, and stop reason. If the agent stops early or exhausts its step budget, the result is inconclusive unless a failure was already observed. Evidence of failure remains visible even if later actions succeed.

## Run and inspect

```sh
python -m unittest discover -s tests -v
python -m fast_demo
python -m fast_demo --fault stale-session
```

Inspect the JSON files under `artifacts/`. Compare the healthy and faulty runs. Then, if you have configured a model provider, try the optional LangChain planner described in the README. Live calls may incur charges; the default replay makes none.

LangSmith can trace the optional model calls when explicitly enabled. It helps inspect decisions, but it does not replace the evaluator. LangGraph and MCP are possible extensions for durable orchestration and tool interfaces; neither is implemented in this first release. See [LangChain's structured-output documentation](https://docs.langchain.com/oss/python/langchain/structured-output) and [LangSmith's evaluation documentation](https://docs.langchain.com/langsmith/evaluation-types).

The architectural test is straightforward: can the system expose an agent's mistake clearly enough for a tester to investigate it? If it cannot, adding more autonomy will make the demonstration more impressive while making the evidence harder to trust.

---

Part 2 of [the FaST article series](README.md). [About Bogdan Stefan Plesa](../AUTHOR.md). Prepared with AI assistance; technical scope and provenance are documented in [source notes](../docs/sources.md).

