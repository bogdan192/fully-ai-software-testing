"""Bounded agent loop, sandbox tools, and an independent evidence evaluator.

No external application, real account, or payment system is connected.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Protocol


TOOLS = {
    "create_user": "Create the single synthetic demo user.",
    "login": "Attempt login; records whether access was granted.",
    "create_order": "Place one synthetic order for 100 cents; requires a session.",
    "refund_order": "Refund the order; a second request must not refund twice.",
    "disable_user": "Disable the synthetic user and revoke its existing session.",
    "probe_session": "Test access with the existing session after disabling the user.",
}
GOAL = (
    "Create a user, log in, place an order, refund it, try refunding it again, "
    "disable the user, test the old session, and try a fresh login. "
    "Gather observations; do not decide whether the application passes."
)


@dataclass(frozen=True)
class Decision:
    action: str
    reason: str = ""


class Planner(Protocol):
    def decide(self, observation: dict, history: list[dict]) -> Decision: ...


@dataclass
class Sandbox:
    """In-memory application model; faults are deliberately injectable."""
    fault: str = "none"
    user_exists: bool = False
    disabled: bool = False
    session: bool = False
    order: bool = False
    refund_count: int = 0
    login_results: list[bool] = field(default_factory=list)
    probe_results: list[bool] = field(default_factory=list)

    def __post_init__(self):
        if self.fault not in {"none", "duplicate-refund", "stale-session"}:
            raise ValueError("Unknown fault")

    def snapshot(self) -> dict:
        return deepcopy({
            "user_exists": self.user_exists, "disabled": self.disabled,
            "session": self.session, "order": self.order,
            "refund_count": self.refund_count,
            "login_results": self.login_results, "probe_results": self.probe_results,
        })

    def execute(self, action: str) -> dict:
        # The adapter is the authority boundary. It has no shell or arbitrary URL tool.
        if action not in TOOLS:
            raise ValueError("Action is outside the tool allowlist")
        if action == "create_user":
            if self.user_exists:
                return {"status": "already_exists"}
            self.user_exists = True
        elif action == "login":
            allowed = self.user_exists and not self.disabled
            self.login_results.append(allowed)
            self.session = allowed
            return {"status": "allowed" if allowed else "denied"}
        elif action == "create_order":
            if not self.session or self.disabled:
                return {"status": "denied"}
            if self.order:
                return {"status": "already_exists"}
            self.order = True
        elif action == "refund_order":
            if not self.session or self.disabled or not self.order:
                return {"status": "denied"}
            if self.refund_count and self.fault != "duplicate-refund":
                return {"status": "already_refunded"}
            self.refund_count += 1
        elif action == "disable_user":
            if not self.user_exists:
                return {"status": "missing_user"}
            self.disabled = True
            if self.fault != "stale-session":
                self.session = False
        elif action == "probe_session":
            self.probe_results.append(self.session)
            return {"status": "allowed" if self.session else "denied"}
        return {"status": "ok"}


class ReplayPlanner:
    """A scripted fixture, deliberately NOT described as AI."""
    actions = (
        "create_user", "login", "create_order", "refund_order", "refund_order",
        "disable_user", "probe_session", "login", "finish",
    )

    def decide(self, observation: dict, history: list[dict]) -> Decision:
        return Decision(self.actions[min(len(history), len(self.actions) - 1)], "offline fixture")


def evaluate(history: list[dict]) -> dict:
    """Use actual tool outcomes and state transitions, never an agent's verdict."""
    checks: dict[str, str] = {
        key: "NOT_OBSERVED" for key in
        ("user_created", "login_allowed", "order_created", "refund_once",
         "duplicate_refund_blocked", "user_disabled", "old_session_denied", "new_login_denied")
    }

    def record(key: str, ok: bool):
        # A later success must never erase an earlier observed failure.
        if checks[key] != "FAIL":
            checks[key] = "PASS" if ok else "FAIL"

    for event in history:
        action, before, after, result = (event[k] for k in ("action", "before", "after", "result"))
        status = result["status"]
        if action == "create_user" and not before["user_exists"]:
            record("user_created", after["user_exists"] and status == "ok")
        elif action == "login" and before["user_exists"]:
            if before["disabled"]:
                record("new_login_denied", status == "denied" and not after["session"])
            else:
                record("login_allowed", status == "allowed" and after["session"])
        elif action == "create_order" and before["session"] and not before["disabled"] and not before["order"]:
            record("order_created", after["order"] and status == "ok")
        elif action == "refund_order" and before["order"] and before["session"] and not before["disabled"]:
            if before["refund_count"] == 0:
                record("refund_once", after["refund_count"] == 1 and status == "ok")
            else:
                record("duplicate_refund_blocked", after["refund_count"] == 1 and status == "already_refunded")
        elif action == "disable_user" and before["user_exists"]:
            record("user_disabled", after["disabled"] and status == "ok")
        elif action == "probe_session" and before["disabled"]:
            # A probe must occur after disable and before another login overwrites the session.
            previous = [e["action"] for e in history[:event["step"] - 1]]
            last_disable = max((i for i, a in enumerate(previous) if a == "disable_user"), default=-1)
            had_session = any(e["action"] == "disable_user" and e["before"]["session"]
                              for e in history[:event["step"] - 1])
            if had_session and "login" not in previous[last_disable + 1:]:
                record("old_session_denied", status == "denied")
    status = "FAIL" if "FAIL" in checks.values() else (
        "PASS" if all(v == "PASS" for v in checks.values()) else "INCONCLUSIVE"
    )
    return {"status": status, "checks": checks}


def run(planner: Planner, sandbox: Sandbox | None = None, max_steps: int = 12) -> dict[str, Any]:
    if type(max_steps) is not int or not 1 <= max_steps <= 100:
        raise ValueError("max_steps must be an integer from 1 to 100")
    sandbox = sandbox or Sandbox()
    history: list[dict] = []
    stop = "step_budget"
    for _ in range(max_steps):
        try:
            decision = planner.decide(sandbox.snapshot(), deepcopy(history))
            if not isinstance(decision, Decision):
                raise ValueError("Planner must return Decision")
            if decision.action == "finish":
                stop = "agent_finished"
                break
            if decision.action not in TOOLS:
                stop = "policy_blocked"
                break
            before = sandbox.snapshot()
            result = sandbox.execute(decision.action)
            history.append({"step": len(history) + 1, "action": decision.action,
                            "before": before, "result": result, "after": sandbox.snapshot()})
        except Exception as exc:
            # Do not write exception messages: provider errors may contain request details.
            stop = "planner_or_adapter_error:" + type(exc).__name__
            break
    evaluation = evaluate(history)
    if stop != "agent_finished" and evaluation["status"] != "FAIL":
        evaluation["status"] = "INCONCLUSIVE"
    return {"schema_version": 1, "stop_reason": stop, **evaluation, "events": history}
