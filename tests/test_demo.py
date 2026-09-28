import unittest

from fast_demo.core import Decision, ReplayPlanner, Sandbox, run


class Sequence:
    def __init__(self, actions):
        self.actions = iter(actions)

    def decide(self, observation, history):
        return Decision(next(self.actions, "finish"))


class DemoTests(unittest.TestCase):
    def test_normal_journey(self):
        report = run(ReplayPlanner())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(len(report["checks"]), 8)

    def test_duplicate_refund_is_caught(self):
        report = run(ReplayPlanner(), Sandbox(fault="duplicate-refund"))
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["checks"]["duplicate_refund_blocked"], "FAIL")

    def test_stale_session_is_caught_even_after_login_clears_it(self):
        report = run(ReplayPlanner(), Sandbox(fault="stale-session"))
        self.assertEqual(report["checks"]["old_session_denied"], "FAIL")

    def test_unobserved_work_cannot_pass(self):
        self.assertEqual(run(Sequence(["finish"]))["status"], "INCONCLUSIVE")

    def test_budget_is_not_a_pass(self):
        report = run(ReplayPlanner(), max_steps=2)
        self.assertEqual(report["stop_reason"], "step_budget")
        self.assertEqual(report["status"], "INCONCLUSIVE")

    def test_unknown_tool_blocked_before_mutation(self):
        sandbox = Sandbox()
        report = run(Sequence(["delete_database"]), sandbox)
        self.assertEqual(report["stop_reason"], "policy_blocked")
        self.assertFalse(sandbox.user_exists)

    def test_wrong_probe_order_cannot_hide_stale_session(self):
        report = run(Sequence(["create_user", "login", "create_order", "refund_order",
                               "refund_order", "disable_user", "login", "probe_session"]),
                     Sandbox(fault="stale-session"))
        self.assertEqual(report["checks"]["old_session_denied"], "NOT_OBSERVED")
        self.assertEqual(report["status"], "INCONCLUSIVE")

    def test_planner_does_not_receive_mutable_evidence(self):
        class Mutator:
            def decide(self, observation, history):
                observation["user_exists"] = True
                history.clear()
                return Decision("finish")
        sandbox = Sandbox()
        self.assertEqual(run(Mutator(), sandbox)["status"], "INCONCLUSIVE")
        self.assertFalse(sandbox.user_exists)

    def test_provider_failure_is_inconclusive_and_redacted(self):
        class Broken:
            def decide(self, observation, history):
                raise RuntimeError("secret-provider-request")
        report = run(Broken())
        self.assertEqual(report["status"], "INCONCLUSIVE")
        self.assertNotIn("secret-provider-request", str(report))

    def test_bad_budget_rejected(self):
        with self.assertRaises(ValueError):
            run(ReplayPlanner(), max_steps=0)


if __name__ == "__main__":
    unittest.main()
