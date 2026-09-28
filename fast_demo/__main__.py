import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from uuid import uuid4

from .core import ReplayPlanner, Sandbox, run


def main():
    parser = argparse.ArgumentParser(description="FaST sandbox architectural demo")
    parser.add_argument("--planner", choices=["replay", "langchain"], default="replay")
    parser.add_argument("--model", help="Provider-prefixed model ID, e.g. anthropic:<available-model-id>")
    parser.add_argument("--fault", choices=["none", "duplicate-refund", "stale-session"], default="none")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--max-steps", type=int, default=12)
    parser.add_argument("--trace", action="store_true", help="Opt in to LangSmith uploads for the LLM planner")
    parser.add_argument("--output", default="artifacts")
    args = parser.parse_args()
    if not 1 <= args.repeat <= 100 or not 1 <= args.max_steps <= 100:
        parser.error("repeat and max-steps must be between 1 and 100")
    if args.planner == "langchain" and not args.model:
        parser.error("--model is required for the LangChain planner")
    if args.trace and args.planner != "langchain":
        parser.error("--trace requires --planner langchain")
    output = Path(args.output) / str(uuid4())
    output.mkdir(parents=True, exist_ok=False)
    counts = Counter()
    for number in range(args.repeat):
        if args.planner == "langchain":
            from .agents import LangChainPlanner
            planner = LangChainPlanner(args.model, tracing=args.trace)
        else:
            planner = ReplayPlanner()
        report = run(planner, Sandbox(fault=args.fault), args.max_steps)
        report.update(planner=args.planner, model=args.model, injected_fault=args.fault)
        (output / f"run-{number + 1:03}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        counts[report["status"]] += 1
    print(json.dumps({"runs": args.repeat, "results": dict(counts), "artifacts": str(output)}))
    return 1 if counts["FAIL"] else 2 if counts["INCONCLUSIVE"] else 0


if __name__ == "__main__":
    sys.exit(main())
