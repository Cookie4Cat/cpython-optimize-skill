---
name: workflow-feature-driven-optimization
description: Use when 已知 CPython/CinderX 特性或实现路径预计能提升性能，需要修改代码、补功能/集成测试并验证 pyperformance 收益。
---

# Feature Driven Optimization Workflow

## Agent 分派

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境确认 | `cinderx-environment-verifier` | `cinderx-env-validate` |
| 功能/集成测试 | `cinderx-jit-analyst` / orchestrator | `cpython-runtime-test-run`、`cinderx-smoke-check` |
| JIT/路径分析 | `cinderx-jit-analyst` | `cinderx-jit-entry-check`、`cinderx-hir-lir-analyze` |
| 性能验证 | `pyperformance-candidate-runner` | `pyperformance-worker-run` / `pyperformance-suite-run` |
| 结果分析 | `pyperformance-benchmark-analyst` | `pyperformance-result-compare` |
| 报告 | `pyperformance-benchmark-analyst` | `cinderx-optimization-report` |

## Gate

先功能后性能。L1 功能/集成测试未通过时，不讨论性能收益；目标 benchmark 无收益时，先解释假设失败原因。
