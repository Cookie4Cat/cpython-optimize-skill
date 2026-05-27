---
name: workflow-pyperformance-regression
description: Use when 需要 L3/L4 正式 pyperformance、CPython/CinderX A/B 对比、提交前后性能回归、speedup.json 或报告级性能确认。
---

# pyperformance Regression Workflow

## 定位

Supporting Workflow：正式性能验证分支。由主 Workflow 在 L3/L4 阶段调用。

## Agent 分派

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境确认 | `cinderx-environment-verifier` | `cinderx-env-validate` |
| A/B slot | `cinderx-orchestrator` | `cinderx-ab-run-slot` |
| baseline | `pyperformance-baseline-runner` | `pyperformance-suite-run` |
| candidate | `pyperformance-candidate-runner` | `pyperformance-suite-run` |
| 分析 | `pyperformance-benchmark-analyst` | `pyperformance-result-compare` |
| 报告 | `pyperformance-benchmark-analyst` | `cinderx-optimization-report` |

## Gate

baseline/candidate 必须说明口径 baseline 和提交 baseline。并行前 CPU set、绑核、结果目录、容器线不冲突。
