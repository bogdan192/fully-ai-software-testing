# Evaluating the FaST testing agent

Author: **Bogdan Stefan Plesa**.

A tool that tests software also needs testing. Evaluate the application and the agent as separate systems. A single successful walkthrough is an illustration, not a reliability estimate.

## Reproducible offline checks

```sh
python -m unittest discover -s tests -v
python -m fast_demo --repeat 25
python -m fast_demo --fault duplicate-refund
python -m fast_demo --fault stale-session
```

Expected results: the healthy replay passes; the two injected faults fail their relevant independent checks. Fault commands intentionally return exit code 1. The test suite also covers premature completion, exhausted budgets, disallowed actions, planner exceptions, evidence isolation, and incorrect session-probe ordering.

Repeating replay runs demonstrates deterministic behavior only. It must not be presented as 25 successful AI tests.

## Model experiment protocol

Run this after configuring a provider and agreeing a cost budget. No live-model experiment is claimed in this release.

1. Choose a fixed model identifier, dependency versions, prompt version, and application fixture.
2. Run at least 25 fresh trials per condition as an initial exploratory sample. This is not a universal statistical sufficiency threshold.
3. Compare healthy, duplicate-refund, and stale-session conditions. Randomize condition order in a larger study.
4. Include objective paraphrases and contradictory application text when extending the fixture. The bundled fixture does not simulate prompt injection.
5. Retain all runs, including timeouts and inconclusive outcomes. Never retry until green and discard previous attempts.
6. Have a tester examine event traces and compare the evaluator against an independently specified oracle.

Record exact counts, denominator, and uncertainty. Measure false PASS on faulty fixtures, false FAIL on healthy fixtures, inconclusive rate, policy-block rate, useful observations, latency, and provider-reported tokens/cost. The current CLI records verdict counts but does not compute statistical confidence intervals or cost.

Do not collapse these into a single “AI accuracy” percentage. A model that refuses every action may avoid unsafe actions while accomplishing no testing. A model that completes every journey may still miss every defect.

## Interpretation limits

The demo exposes application state directly to simplify architectural inspection. Success on this fixture does not establish successful browser navigation, useful exploratory testing, general fault discovery, or reduced team costs. Add realistic adapters, seeded defects not revealed to the planner, and comparisons against established testing approaches before making those claims.

Related reading: James Bach's [Seriously Testing LLMs](https://www.satisfice.com/blog/archives/487957) and [Serious Data From Testing LLMs](https://www.satisfice.com/blog/archives/487962). Their critical perspective informs this evaluation approach; no endorsement is implied.
