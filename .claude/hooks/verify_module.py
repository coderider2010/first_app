#!/usr/bin/env python3
"""SubagentStop gate for the Associate: a module cannot be submitted with broken numbers.

Registered in .claude/settings.json for agent_type "associate". Claude Code pipes
the hook input JSON on stdin. Exit 0 lets the Associate stop; exit 2 blocks the
stop and feeds stderr back to the Associate as instructions.

Protocol (see .claude/agents/associate.md):
  - The Associate ends its final message with `MODULE: engagements/<eng>/modules/<id>`.
  - That folder must contain memo.md.
  - If it contains sizing.json, sniff_test.py must not report errors_found.
    The verdict is saved to sniff_result.json so the EM can see any flags.
  - If it contains valuation.json, valuation_check.py must not report errors_found.
    The verdict is saved to valuation_result.json.
  - Escape valve: if the folder contains escalation.md, the Associate has handed
    the problem to the EM (per AGENTS.md) and may stop.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "agents" / "associate" / "skills"
# Module file -> (verifier script, where its verdict is saved).
VERIFIERS = {
    "sizing.json": (SKILLS / "market-sizing" / "scripts" / "sniff_test.py", "sniff_result.json"),
    "valuation.json": (
        SKILLS / "implied-expectations" / "scripts" / "valuation_check.py", "valuation_result.json"
    ),
}
MODULE_LINE = re.compile(r"^\s*MODULE:\s*(\S+)\s*$", re.MULTILINE)

SUBMIT_HELP = (
    "End your final message with a line `MODULE: engagements/<engagement>/modules/<module-id>` "
    "naming the module folder you are submitting."
)


def block(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)


def run_verifier(module, name, verifier, result_name):
    """Run one verifier on one module file; block the stop if it reports errors."""
    proc = subprocess.run(
        [sys.executable, str(verifier), str(module / name)], capture_output=True, text=True
    )
    (module / result_name).write_text(proc.stdout)
    if proc.returncode != 0:
        block(f"Submission blocked: {verifier.name} could not read {name}: {proc.stdout.strip()}")

    result = json.loads(proc.stdout)
    if result["status"] == "errors_found":
        errors = "\n".join(f"  - {e}" for e in result["errors"])
        block(
            f"Submission blocked: {verifier.name} reports errors in {name}. Fix them, update "
            f"memo.md to match, and submit again:\n{errors}\n"
            "If you cannot resolve them, write escalation.md in the module folder explaining "
            "why, per the AGENTS.md escalation rules."
        )


def main():
    hook = json.load(sys.stdin)
    if hook.get("agent_type") != "associate":
        sys.exit(0)

    matches = MODULE_LINE.findall(hook.get("last_assistant_message") or "")
    if not matches:
        block(f"Submission blocked: no module named. {SUBMIT_HELP}")

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or hook.get("cwd") or ".").resolve()
    engagements = project / "engagements"
    module = (project / matches[-1]).resolve()
    if not module.is_relative_to(engagements) or not module.is_dir():
        block(f"Submission blocked: {matches[-1]} is not a module folder under engagements/. {SUBMIT_HELP}")

    if (module / "escalation.md").exists():
        sys.exit(0)

    if not (module / "memo.md").exists():
        block(f"Submission blocked: {matches[-1]}/memo.md does not exist. Write the module memo first.")

    for name, (verifier, result_name) in VERIFIERS.items():
        if (module / name).exists():
            run_verifier(module, name, verifier, result_name)
    sys.exit(0)


if __name__ == "__main__":
    main()
