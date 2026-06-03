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

## TDD 要求

修改代码前先做测试缺口判断：

- 检查是否需要补充或修改 RuntimeTests 功能用例；不需要时写明理由。
- 检查是否需要补充或修改 test_cinderx/lib test 集成用例；不需要时写明理由。
- 新增或修改的功能用例必须使用 Python `unittest` 框架，不能改成 pytest 风格或只写脚本式断言。
- 功能用例和集成用例先于性能验证；没有对应行为覆盖时，不能只靠 pyperformance 收益证明特性正确。

## Gate

先功能后性能。L1 功能/集成测试未通过时，不讨论性能收益；目标 benchmark 无收益时，先解释假设失败原因。
