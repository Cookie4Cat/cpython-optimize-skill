---
name: workflow-platform-differential-discovery
description: Use when 需要系统分析 CPython/CinderX 代码、Kunpeng/x86 ISA 与微架构差异，发现候选优化点并评估收益范围。
---

# Platform Differential Discovery Workflow

## Agent 分派

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境确认 | `cinderx-environment-verifier` | `cinderx-env-validate` |
| 平台建模 | `cinderx-platform-analyst` | `cinderx-isa-microarch-compare` |
| 覆盖数据 | `pyperformance-benchmark-analyst` | `pyperformance-result-compare` |
| JIT 细节 | `cinderx-jit-analyst` | `cinderx-jit-entry-check`、`cinderx-hir-lir-analyze` |
| 报告 | `cinderx-platform-analyst` | `cinderx-optimization-report` |

## Gate

先建立 ISA、微架构、perf、benchmark 覆盖矩阵，再进入具体 HIR/LIR。不要默认跑三小时全量。
