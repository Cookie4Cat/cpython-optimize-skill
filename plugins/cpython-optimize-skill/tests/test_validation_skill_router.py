#!/usr/bin/env python3
"""Regression tests for the pre-execution validation hook router."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "hooks" / "validation-skill-router"


def run_router(command: str, cwd: Path) -> str:
    payload = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {
            "command": command,
            "cwd": str(cwd),
        },
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


def make_cpython_repo(base: Path) -> Path:
    repo = base / "cpython"
    for rel in [
        "Include",
        "Python",
        "Objects",
        "Lib/test",
        "cinderx/Jit",
    ]:
        (repo / rel).mkdir(parents=True, exist_ok=True)
    (repo / "Include" / "patchlevel.h").write_text("#define PY_VERSION \"3.14.3\"\n")
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    return repo


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        repo = make_cpython_repo(base)
        outside = base / "plain-project"
        outside.mkdir()

        require(
            run_router("python -m pyperformance run", outside) == "",
            "validation commands outside CPython/CinderX repos must not trigger",
        )
        require(
            run_router("git show --stat HEAD", repo) == "",
            "read-only git inspection must not trigger validation routing",
        )

        low_cost_context = run_router("./python -m test test_dict", repo)
        require(
            "additionalContext" in low_cost_context
            and "using-cpython-optimize" in low_cost_context
            and "validation-strategy" in low_cost_context,
            "targeted runtime tests should inject skill context and continue",
        )

        full_perf_block = run_router("python -m pyperformance run", repo)
        require(
            '"permissionDecision": "deny"' in full_perf_block
            and "pyperformance" in full_perf_block
            and "CPYTHON_OPTIMIZE_HOOK_ACK=1" in full_perf_block,
            "full pyperformance runs should be blocked until validation planning is acknowledged",
        )

        local_editable_install = run_router(
            "python -m pip install --no-build-isolation --no-deps -e .",
            repo,
        )
        require(
            '"permissionDecision": "deny"' in local_editable_install
            and "cinderx-env-validate" in local_editable_install,
            "editable local project installs must route through environment validation",
        )

        local_plain_install = run_router("pip install --verbose .", repo)
        require(
            '"permissionDecision": "deny"' in local_plain_install
            and "pip install" in local_plain_install,
            "pip install [options] . must be matched broadly",
        )

        local_uv_install = run_router("uv pip install --no-deps .", repo)
        require(
            '"permissionDecision": "deny"' in local_uv_install
            and "pip install" in local_uv_install,
            "uv pip install [options] . must be matched broadly",
        )

        acknowledged = run_router(
            "CPYTHON_OPTIMIZE_HOOK_ACK=1 python -m pip install -e .",
            repo,
        )
        require(
            acknowledged == "",
            "acknowledged commands must be allowed to avoid deny loops",
        )

    print("validation hook router validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
