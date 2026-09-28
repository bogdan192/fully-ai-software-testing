# FaST architecture and extension contract

Concept and paradigm: **Bogdan Stefan Plesa**.

The implementation deliberately keeps the planner, execution boundary, and evaluator separate. It is an architectural experiment, not a production testing service.

## Implemented components

| Component | File | Responsibility |
| --- | --- | --- |
| Planner protocol | `fast_demo/core.py` | Return one `Decision`; cannot mutate the executor's copied state or evidence |
| Replay planner | `fast_demo/core.py` | Supply a deterministic fixture to exercise the architecture without AI |
| LLM planner | `fast_demo/agents.py` | Request an allowed action through LangChain structured output |
| Sandbox tools | `fast_demo/core.py` | Model account and order transitions in memory |
| Evaluator | `fast_demo/core.py` | Derive eight check outcomes from observed transitions |
| CLI/report writer | `fast_demo/__main__.py` | Run fresh experiments and write separate JSON artifacts |

The agent sees state and events, not the injected fault label. It has no method for editing the evaluator, changing its own budget, or declaring a pass. A stop caused by a budget or an exception is inconclusive unless an observed violation already warrants failure.

## Evidence contract

An event contains a sequential step number, an allowed action name, pre-action state, tool result, and post-action state. The report includes planner mode, model identifier, deliberate fault configuration, stop reason, individual check outcomes, and the event list. These observations are trustworthy only relative to the test harness; they are not tamper-proof audit records.

For example, a disabled account's old session must be probed before another login changes session state. Otherwise the harness reports that check as NOT_OBSERVED. This prevents a failed new login from hiding a still-valid old session.

The in-memory app omits password hashing, authorization roles, asynchronous payments, eventual consistency, networking, browser behavior, and persistence. Its refund counter is a teaching stand-in for a ledger. A real adapter must bring those concerns back rather than assume the simulation covers them.

## Browser/API adapter design

1. Start a disposable environment with synthetic fixtures and record its build identifier.
2. Give the planner observed UI/API state and a bounded set of domain tools.
3. Validate each tool call, arguments, target environment, account scope, and resource limits in executable code.
4. Execute with test-only credentials; return a normalized result plus evidence references.
5. Evaluate effects using a separate read-only application interface where possible.
6. Preserve failures and cleanup results; dispose of the environment after evidence capture.

Login and user creation can run in a local fixture. For orders and refunds, use a payment provider's sandbox and enforce a fixed test-account allowlist. User disabling must target only the run's synthetic identity. Do not give an LLM unrestricted administrative credentials.

MCP can expose this tool contract but does not itself establish that a tool is authorized or truthful. LangGraph could manage durable state and handoffs; neither is implemented in v0.1.0. Additional planner, explorer, and critic roles should be introduced only when experiments show a benefit. Role separation alone does not make agents' mistakes independent.

## Optional integration scope

LangChain structured output is implemented as a small provider adapter. The bundled optional dependencies support Anthropic models. Other providers require their own integration packages and validation. Provider configuration is explicit; no current model is hardcoded.

LangSmith tracing captures model calls when enabled. It does not replace the local evidence ledger or provide a preconfigured evaluation dashboard. A future LangSmith dataset should contain the scenario objective, fixture identity, expected invariants, and reference observations. Score task completion, fault detection, unsupported passes, tool violations, latency, and cost separately.

The current loop limits decisions, not total currency spend. Its full-history context grows with the step count. Keep the default bound for initial experiments; token accounting, context compaction, dollar limits, and transport-level cancellation are future work.
