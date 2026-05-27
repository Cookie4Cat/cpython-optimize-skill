---
name: workflow-jit-optimization-analysis
description: Use when 单个 CinderX JIT 用例需要 L2 热点归因、HIR/LIR/机器码证据、JIT 优化点判断，或主流程需要单 benchmark 证据分支。
---

# JIT Optimization Analysis Workflow

## 定位

Supporting Workflow：单 benchmark JIT 证据分支。端到端任务中由主 Workflow 在 L2 阶段调用。

## Agent 分派

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境确认 | `cinderx-environment-verifier` | `cinderx-smoke-check` |
| worker 运行 | `cinderx-jit-analyst` | `pyperformance-worker-run` |
| 进入 JIT | `cinderx-jit-analyst` | `cinderx-jit-entry-check` |
| HIR/LIR | `cinderx-jit-analyst` | `cinderx-hir-dump`、`cinderx-hir-lir-analyze` |
| 报告 | `cinderx-jit-analyst` | `cinderx-optimization-report` |

## Gate

未证明 benchmark 本体进入 CinderX JIT，不进入 HIR/LIR 优化结论。必须先热点归因，再解释 IR。
