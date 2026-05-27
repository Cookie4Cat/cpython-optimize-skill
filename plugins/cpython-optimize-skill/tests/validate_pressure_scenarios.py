#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(text: str, needle: str, context: str) -> None:
    if needle not in text:
        raise AssertionError(f"{context} 缺少关键信号: {needle}")


def main() -> int:
    pyperf = read(ROOT / "skills" / "pyperformance-test" / "SKILL.md")
    docker = read(ROOT / "skills" / "docker-runtime" / "SKILL.md")
    docs = read(ROOT / "skills" / "experiment-documentation" / "SKILL.md")
    case = read(ROOT / "skills" / "cinderx-analysis" / "SKILL.md")
    triage = read(
        ROOT
        / "skills"
        / "pyperformance-test"
        / "references"
        / "pyperformance-crash-triage.md"
    )
    entry = read(ROOT / "skills" / "using-cpython-optimize" / "SKILL.md")
    remote = read(ROOT / "skills" / "remote-environment" / "SKILL.md")
    build = read(ROOT / "skills" / "cpython-build" / "SKILL.md")
    scenarios = read(ROOT / "tests" / "pressure-scenarios.md")

    require(scenarios, "场景 1", "pressure scenarios")
    require(scenarios, "场景 6", "pressure scenarios")
    require(scenarios, "场景 7", "pressure scenarios")
    require(scenarios, "场景 8", "pressure scenarios")
    require(scenarios, "场景 9", "pressure scenarios")
    require(scenarios, "场景 10", "pressure scenarios")
    require(scenarios, "场景 11", "pressure scenarios")
    require(scenarios, "场景 12", "pressure scenarios")
    require(scenarios, "场景 13", "pressure scenarios")
    require(scenarios, "场景 14", "pressure scenarios")
    require(scenarios, "场景 15", "pressure scenarios")
    require(scenarios, "场景 16", "pressure scenarios")
    require(scenarios, "场景 17", "pressure scenarios")
    require(scenarios, "场景 18", "pressure scenarios")

    for needle in [
        "run_benchmark.py",
        "HIR dump",
        "worker",
        "bench_command",
        "sitecustomize",
        "真实命令",
        "性能口径",
        "baseline 的定义",
        "跨平台口径",
    ]:
        require(pyperf, needle, "pyperformance workflow")

    for needle in [
        "双线结构",
        "cpython-baseline",
        "cinderx-test",
        "长连接交互终端",
        "docker exec",
        "独立宿主机目录",
        "bind mount",
        "PIP_INDEX_URL",
    ]:
        require(docker, needle, "docker skill")

    for needle in [
        "run_benchmark.py",
        "python -m pyperformance run",
        "cpython-baseline",
        "cinderx-test",
        "HIR dump",
        "只看功能",
        "正式对照",
        "宿主机独立目录",
        "性能口径",
        "baseline",
        "API/ABI",
        "输出契约",
        "SIGSEGV",
        "异常耗时",
    ]:
        require(entry, needle, "entry skill")

    for needle in [
        "SSH",
        "tmux",
        "裸机",
        "独立宿主机目录",
        "rsync",
        "Docker",
        "输出契约",
        "exit status",
        "无输出",
        "timeout",
        "网络卡顿",
        "询问用户",
    ]:
        require(remote, needle, "remote skill")

    for needle in [
        "API/ABI 版本门禁",
        "Python 3.14.3",
        "3.14.5",
        "patchlevel.h",
        "SOABI",
        "目标解释器",
    ]:
        require(build, needle, "build skill")

    review = read(ROOT / "tests" / "dynamic-pressure-review.md")
    for needle in [
        "双线区分",
        "长连接交互终端",
        "正式对照",
        "宿主机目录",
    ]:
        require(review, needle, "dynamic pressure review")

    for needle in [
        "背景",
        "复现命令",
        "证据链",
        "根因",
        "修复方法",
        "回归结果",
    ]:
        require(docs, needle, "documentation workflow")

    for needle in [
        "HIR",
        "LIR",
        "uop",
        "机器码",
        "确认是否真的进入 CinderX JIT",
        "热点归因",
        "优化点输出格式",
        "修改方案",
    ]:
        require(case, needle, "case analysis workflow")

    for needle in [
        "LD_LIBRARY_PATH",
        "compile storm",
        "SIGSEGV",
        "gdb",
        "bt full",
        "core dump",
        "日志不能替代",
    ]:
        require(triage, needle, "crash triage reference")

    print("pressure scenario validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
