#!/usr/bin/env python3
"""Regression tests for the runtime hook router."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "hooks" / "runtime-skill-router"


def run_router(
    command: str,
    *,
    stdout: str = "",
    stderr: str = "",
    duration_ms: int = 10,
) -> str:
    payload = {
        "hook_event_name": "PostToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "tool_response": {
            "stdout": stdout,
            "stderr": stderr,
        },
        "duration_ms": duration_ms,
    }
    result = subprocess.run(
        [str(ROUTER)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    history_output = """
commit 1234567
Author: example

    mention SIGSEGV / exit 139 / core dump in an old investigation note
"""
    require(
        run_router("git show --stat HEAD", stdout=history_output) == "",
        "git history inspection must not trigger crash triage",
    )
    require(
        run_router("git log -p -- hooks/runtime-skill-router", stdout=history_output) == "",
        "git log patch inspection must not trigger crash triage",
    )
    require(
        run_router("git -C /tmp/repo show HEAD", stdout=history_output) == "",
        "git -C history inspection must not trigger crash triage",
    )
    require(
        run_router("git --no-pager diff HEAD~1", stdout=history_output) == "",
        "git --no-pager diff inspection must not trigger crash triage",
    )
    require(
        run_router("rg -n 'SIGSEGV|timeout' plugins/cpython-optimize-skill", stdout=history_output) == "",
        "text search inspection must not trigger runtime guards",
    )

    crash_context = run_router(
        "python -m test test_cinderx",
        stderr="Segmentation fault (core dumped)",
    )
    require(
        "workflow-cinderx-crash-triage" in crash_context
        and "cinderx-gdb-core-triage" in crash_context,
        "real crash output must trigger crash triage",
    )

    remote_context = run_router(
        "python -m pip install -r requirements.txt",
        stderr="Read timed out while connecting to pypi.org",
    )
    require(
        "cinderx-remote-lab-ops" in remote_context,
        "real network timeout must trigger remote lab ops",
    )

    empty_long_context = run_router(
        "ssh kunpeng 'python -m pyperformance run'",
        duration_ms=130000,
    )
    require(
        "stdout/stderr" in empty_long_context,
        "long empty command must trigger observability reminder",
    )

    print("runtime hook router validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
