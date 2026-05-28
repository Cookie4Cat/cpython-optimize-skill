#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
AGENTS = ROOT / "agents"

PROFESSIONAL_SKILLS = [
    "cinderx-env-validate",
    "cinderx-env-clean",
    "cinderx-env-bootstrap",
    "cinderx-remote-lab-ops",
    "cinderx-ab-run-slot",
    "cpython-runtime-test-run",
    "cinderx-smoke-check",
    "pyperformance-worker-run",
    "pyperformance-suite-run",
    "pyperformance-result-compare",
    "cinderx-gdb-core-triage",
    "cinderx-hir-dump",
    "cinderx-jit-entry-check",
    "cinderx-hir-lir-analyze",
    "cinderx-isa-microarch-compare",
    "cinderx-optimization-report",
    "validation-strategy",
]

PROFESSIONAL_AGENTS = [
    "cinderx-orchestrator",
    "cinderx-environment-verifier",
    "pyperformance-baseline-runner",
    "pyperformance-candidate-runner",
    "pyperformance-benchmark-analyst",
    "cinderx-crash-triager",
    "cinderx-jit-analyst",
    "cinderx-platform-analyst",
]

GENERIC_OR_OLD_SKILLS = [
    "remote-environment",
    "remote-workspace",
    "command-observability",
    "docker-runtime",
    "docker-lab-runtime",
    "cpython-build",
    "cpython-build-install",
    "test-execution",
    "pyperformance-test",
    "pyperformance-benchmark",
    "benchmark-result-analysis",
    "native-crash-debugging",
    "cinderx-analysis",
    "cinderx-jit-analysis",
    "platform-differential-analysis",
    "experiment-documentation",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def skill(name: str) -> str:
    return read(SKILLS / name / "SKILL.md")


def agent(name: str) -> str:
    return read(AGENTS / f"{name}.md")


def require(text: str, needle: str, context: str) -> None:
    if needle not in text:
        raise AssertionError(f"{context} 缺少关键信号: {needle}")


def forbid(text: str, needle: str, context: str) -> None:
    if needle in text:
        raise AssertionError(f"{context} 仍包含泛化或旧边界信号: {needle}")


def require_all(text: str, needles: list[str], context: str) -> None:
    for needle in needles:
        require(text, needle, context)


def main() -> int:
    entry = skill("using-cpython-optimize")
    question_templates = read(SKILLS / "using-cpython-optimize" / "references" / "clarifying-question-templates.md")
    skill_texts = {name: skill(name) for name in PROFESSIONAL_SKILLS}
    agent_texts = {name: agent(name) for name in PROFESSIONAL_AGENTS}
    workflows = {
        "lab": skill("workflow-remote-cinderx-lab-setup"),
        "crash": skill("workflow-cinderx-crash-triage"),
        "regression": skill("workflow-pyperformance-regression"),
        "jit": skill("workflow-jit-optimization-analysis"),
        "cross_platform": skill("workflow-cross-platform-delta-triage"),
        "feature": skill("workflow-feature-driven-optimization"),
        "platform": skill("workflow-platform-differential-discovery"),
    }
    active_docs = "\n".join([entry, *workflows.values(), *agent_texts.values()])
    all_active_docs = "\n".join([entry, *workflows.values(), *agent_texts.values(), *skill_texts.values()])
    scenarios = read(ROOT / "tests" / "pressure-scenarios.md")
    review = read(ROOT / "tests" / "dynamic-pressure-review.md")
    runtime_router = read(ROOT / "hooks" / "runtime-skill-router")
    validation_router = read(ROOT / "hooks" / "validation-skill-router")

    for number in range(1, 36):
        require(scenarios, f"场景 {number}", "pressure scenarios")

    for name in PROFESSIONAL_SKILLS:
        require(entry, name, "entry skill professional routing")

    for name in PROFESSIONAL_AGENTS:
        require(entry, name, "entry skill agent routing")

    for old_name in GENERIC_OR_OLD_SKILLS:
        if (SKILLS / old_name).exists():
            raise AssertionError(f"泛化或旧 skill 目录未删除: {old_name}")
        forbid(active_docs, f"`{old_name}`", "active docs")

    forbid(all_active_docs, "3.14" + ".5", "active skill/agent/workflow docs")

    if len(entry.splitlines()) > 150:
        raise AssertionError("entry skill 应保持薄 router，当前行数超过 150")

    require_all(
        entry,
        [
            "Orchestrator",
            "Workflow",
            "Agent",
            "Skill",
            "environment-verifier",
            "baseline-runner",
            "candidate-runner",
            "crash-triager",
            "三态",
            "可复用",
            "新环境",
            "被破坏",
            "反问 Gate",
            "request_user_input",
            "AskUserQuestion",
            "clarifying-question-templates.md",
        ],
        "entry skill",
    )
    require_all(
        question_templates,
        [
            "question_id",
            "request_user_input",
            "AskUserQuestion",
            "文本降级",
            "workflow_route",
            "validation_level",
            "environment_target",
            "destructive_clean",
            "remote_stall",
            "ab_slot",
            "crash_evidence",
            "result_artifacts",
            "scope_budget",
        ],
        "clarifying question templates",
    )

    for name, text in agent_texts.items():
        require_all(text, ["## 职责", "## 适用场景", "## 可调用技能", "## 反问 Gate", "## 输出要求"], f"{name} agent")

    require_all(
        agent_texts["cinderx-environment-verifier"],
        ["reusable", "needs_bootstrap", "needs_clean_bootstrap", "cinderx-env-validate", "cinderx-env-clean", "cinderx-env-bootstrap"],
        "environment verifier",
    )
    require_all(
        agent_texts["pyperformance-baseline-runner"],
        ["baseline", "CPU set", "pyperformance-suite-run", "cinderx-ab-run-slot"],
        "baseline runner",
    )
    require_all(
        agent_texts["pyperformance-candidate-runner"],
        ["candidate", "CPU set", "pyperformance-suite-run", "cinderx-ab-run-slot"],
        "candidate runner",
    )

    require_all(
        runtime_router,
        [
            "cinderx-gdb-core-triage",
            "cinderx-remote-lab-ops",
            "workflow-cinderx-crash-triage",
            "gdb bt full",
            "validation-strategy",
            "extract_command",
            "extract_signal_text",
            "is_observation_command",
            "git\\ show",
            "git\\ log",
            "git\\ diff",
        ],
        "runtime hook router",
    )
    require_all(
        validation_router,
        [
            "PreToolUse",
            "permissionDecision",
            "additionalContext",
            "CPYTHON_OPTIMIZE_HOOK_ACK",
            "using-cpython-optimize",
            "validation-strategy",
            "cinderx-env-validate",
            "pyperformance",
            "pip install",
            "patchlevel.h",
        ],
        "validation hook router",
    )

    require_all(
        skill_texts["cinderx-env-validate"],
        ["目标 Python 版本固定为 `Python 3.14.3`", "SOABI", "patchlevel.h", "cinderx.__file__", "_cinderx", "pyperformance 1.14", "GCC", "openEuler", "reusable"],
        "cinderx-env-validate",
    )
    require_all(
        skill_texts["cinderx-env-clean"],
        ["editable install", "build 目录", "venv", "容器", "pyperformance env", "错版本头文件", "保留 cache", "反问 Gate"],
        "cinderx-env-clean",
    )
    require_all(
        skill_texts["cinderx-env-bootstrap"],
        ["cinderx-test", "cpython-baseline", "Docker 双线", "CinderX editable", "CPython baseline", "pip mirror", "pyperformance", "反问 Gate"],
        "cinderx-env-bootstrap",
    )
    require_all(
        skill_texts["cinderx-remote-lab-ops"],
        ["SSH", "tmux", "rsync", "docker compose", "stdout/stderr", "exit status", "timeout", "日志路径", "反问 Gate"],
        "cinderx-remote-lab-ops",
    )
    require_all(
        skill_texts["cinderx-ab-run-slot"],
        ["baseline", "candidate", "CPU affinity", "绑核", "结果目录", "不重叠", "并行", "反问 Gate"],
        "cinderx-ab-run-slot",
    )
    require_all(
        skill_texts["cpython-runtime-test-run"],
        ["CPython Runtime", "CinderX correctness", "L1 smoke", "L3", "L4", "近千条", "单元测试", "功能测试"],
        "cpython-runtime-test-run",
    )
    require_all(
        skill_texts["cinderx-smoke-check"],
        ["import cinderx", "is_initialized", "get_import_error", "最小 JIT", "HIR", "_cinderx"],
        "cinderx-smoke-check",
    )
    require_all(
        skill_texts["pyperformance-worker-run"],
        ["run_benchmark.py", "--worker", "bench_command", "sitecustomize", "LD_LIBRARY_PATH", "PYTHONPATH", "真实 worker"],
        "pyperformance-worker-run",
    )
    require_all(
        skill_texts["pyperformance-suite-run"],
        ["python -m pyperformance run", "warmup", "loops", "run.json", "subset", "full", "正式", "反问 Gate"],
        "pyperformance-suite-run",
    )
    require_all(
        skill_texts["pyperformance-result-compare"],
        ["run.json", "speedup.json", "baseline", "candidate", "方差", "噪声", "收益范围", "提交 baseline", "反问 Gate"],
        "pyperformance-result-compare",
    )
    require_all(
        skill_texts["cinderx-gdb-core-triage"],
        ["SIGSEGV", "exit 139", "core dump", "gdb", "bt full", "info registers", "同一真实命令", "日志不能替代", "反问 Gate"],
        "cinderx-gdb-core-triage",
    )
    require_all(
        skill_texts["cinderx-hir-dump"],
        ["PYTHONJITDUMPFINALHIR", "PYTHONJITLOGFILE", "真实 worker", "HIR dump", "jit.log", "不另造"],
        "cinderx-hir-dump",
    )
    require_all(
        skill_texts["cinderx-jit-entry-check"],
        ["benchmark 本体", "CinderX JIT", "启动期", "第三方包", "compile storm", "jit.log"],
        "cinderx-jit-entry-check",
    )
    require_all(
        skill_texts["cinderx-hir-lir-analyze"],
        ["HIR", "LIR", "uop", "机器码", "deopt", "frame layout", "调用约定", "修改方案"],
        "cinderx-hir-lir-analyze",
    )
    require_all(
        skill_texts["cinderx-isa-microarch-compare"],
        ["Kunpeng", "x86", "ISA", "cache", "分支预测", "SIMD", "barrier", "hugepages", "perf", "反问 Gate"],
        "cinderx-isa-microarch-compare",
    )
    require_all(
        skill_texts["cinderx-optimization-report"],
        ["背景", "复现命令", "环境指纹", "证据链", "根因", "patch", "回归结果"],
        "cinderx-optimization-report",
    )

    workflow_expectations = {
        "lab": ["cinderx-environment-verifier", "cinderx-env-validate", "cinderx-env-bootstrap", "cinderx-smoke-check"],
        "crash": ["cinderx-crash-triager", "cinderx-gdb-core-triage", "cinderx-hir-dump", "pyperformance-worker-run"],
        "regression": ["cinderx-environment-verifier", "pyperformance-baseline-runner", "pyperformance-candidate-runner", "pyperformance-benchmark-analyst"],
        "jit": ["cinderx-jit-analyst", "cinderx-jit-entry-check", "cinderx-hir-lir-analyze", "cinderx-hir-dump"],
        "cross_platform": ["cinderx-environment-verifier", "pyperformance-baseline-runner", "pyperformance-candidate-runner", "cinderx-platform-analyst"],
        "feature": ["cinderx-environment-verifier", "cinderx-jit-analyst", "cpython-runtime-test-run", "pyperformance-result-compare"],
        "platform": ["cinderx-platform-analyst", "cinderx-isa-microarch-compare", "cinderx-jit-analyst", "pyperformance-result-compare"],
    }
    for workflow_name, needles in workflow_expectations.items():
        require_all(workflows[workflow_name], needles, f"{workflow_name} workflow")

    require_all(
        scenarios,
        [
            "cinderx-env-validate",
            "cinderx-env-clean",
            "cinderx-env-bootstrap",
            "cinderx-ab-run-slot",
            "pyperformance-worker-run",
            "cinderx-gdb-core-triage",
            "cinderx-isa-microarch-compare",
            "request_user_input",
            "AskUserQuestion",
            "clarifying-question-templates.md",
            "validation-skill-router",
            "CPYTHON_OPTIMIZE_HOOK_ACK",
        ],
        "pressure scenarios",
    )
    require_all(
        review,
        ["专业 skill", "Agent 层", "cinderx-env-validate", "cinderx-ab-run-slot", "cinderx-gdb-core-triage", "PreToolUse"],
        "dynamic pressure review",
    )

    print("pressure scenario validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
