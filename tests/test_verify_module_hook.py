"""Tests for the Associate's SubagentStop gate (.claude/hooks/verify_module.py).

Each test builds a throwaway project with one module folder, pipes the hook the
JSON Claude Code would send, and checks the verdict: exit 0 lets the Associate
stop, exit 2 blocks it (stderr is the feedback it receives).
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_sniff_test import CLEAN

HOOK = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "verify_module.py"
MODULE = "engagements/acme/modules/us-pet-insurance"


class GateTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        self.module = self.project / MODULE
        self.module.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, content):
        if not isinstance(content, str):
            content = json.dumps(content)
        (self.module / name).write_text(content)

    def stop(self, message=f"Sizing done.\n\nMODULE: {MODULE}", agent_type="associate"):
        """Simulate the subagent stopping; return (exit code, stderr)."""
        hook_input = {
            "hook_event_name": "SubagentStop",
            "agent_type": agent_type,
            "cwd": str(self.project),
            "stop_hook_active": False,
            "last_assistant_message": message,
        }
        proc = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(hook_input), capture_output=True, text=True,
            env=dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project)),
        )
        return proc.returncode, proc.stderr

    def assertAllowed(self, result):
        code, stderr = result
        self.assertEqual(code, 0, stderr)

    def assertBlocked(self, result, fragment):
        code, stderr = result
        self.assertEqual(code, 2)
        self.assertIn(fragment, stderr)


class Allowed(GateTest):
    def test_clean_sizing_module(self):
        self.write("memo.md", "# US pet insurance is a $4.7B market")
        self.write("sizing.json", CLEAN)
        self.assertAllowed(self.stop())
        verdict = json.loads((self.module / "sniff_result.json").read_text())
        self.assertEqual(verdict["status"], "pass")

    def test_flags_do_not_block_but_are_saved(self):
        self.write("memo.md", "memo")
        self.write("sizing.json", dict(CLEAN, growth_rate_pct=25))
        self.assertAllowed(self.stop())
        verdict = json.loads((self.module / "sniff_result.json").read_text())
        self.assertEqual(verdict["status"], "flags_found")

    def test_non_sizing_module_needs_only_a_memo(self):
        self.write("memo.md", "memo")
        self.assertAllowed(self.stop())

    def test_escalation_is_the_escape_valve(self):
        self.write("sizing.json", dict(CLEAN, estimate=9e9))
        self.write("escalation.md", "Sources conflict; need EM call.")
        self.assertAllowed(self.stop())

    def test_other_agents_are_not_gated(self):
        self.assertAllowed(self.stop(message="no module line", agent_type="Explore"))

    def test_last_module_line_wins(self):
        self.write("memo.md", "memo")
        msg = f"Earlier I mentioned MODULE: engagements/x/modules/y\n\nMODULE: {MODULE}"
        self.assertAllowed(self.stop(message=msg))


class Blocked(GateTest):
    def test_sizing_errors_block_with_the_error_list(self):
        self.write("memo.md", "memo")
        self.write("sizing.json", dict(CLEAN, estimate=9e9))
        self.assertBlocked(self.stop(), "outside the method range")

    def test_block_message_offers_escalation(self):
        self.write("memo.md", "memo")
        self.write("sizing.json", dict(CLEAN, estimate=9e9))
        self.assertBlocked(self.stop(), "escalation.md")

    def test_unreadable_sizing_blocks(self):
        self.write("memo.md", "memo")
        self.write("sizing.json", "{not json")
        self.assertBlocked(self.stop(), "could not read sizing.json")

    def test_missing_memo_blocks(self):
        self.write("sizing.json", CLEAN)
        self.assertBlocked(self.stop(), "memo.md does not exist")

    def test_no_module_line_blocks(self):
        self.assertBlocked(self.stop(message="All done!"), "no module named")

    def test_nonexistent_module_blocks(self):
        msg = "MODULE: engagements/acme/modules/nope"
        self.assertBlocked(self.stop(message=msg), "not a module folder")

    def test_path_outside_engagements_blocks(self):
        # A folder that exists but is not a module: ../ must not escape the check.
        msg = f"MODULE: {MODULE}/../../../../"
        self.assertBlocked(self.stop(message=msg), "not a module folder")


if __name__ == "__main__":
    unittest.main()
