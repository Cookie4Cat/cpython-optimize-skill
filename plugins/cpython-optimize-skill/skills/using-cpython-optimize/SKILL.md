---
name: using-cpython-optimize
description: Use when 开始 CPython/CinderX 优化、环境审计、A/B 跑分、pyperformance、Runtime 测试、crash、JIT 或 Kunpeng/x86 平台差异任务。
---

# CPython/CinderX Optimize Router

薄 router：Orchestrator 选 Workflow，Workflow 分派 Agent，Agent 调专业 Skill。

## 层级

| 层 | 职责 |
|----|------|
| Orchestrator | 运行时主 Agent，理解目标、选 Workflow、分派 Agent、合并结果 |
| Workflow | 端到端剧本和 gate |
| Agent | 阶段负责人，接管环境、跑分、crash、JIT 或平台分析 |
| Skill | CPython/CinderX 专业动作 |

## Agent 路由

| Agent | 触发 |
|-------|------|
| `cinderx-orchestrator` | 任意入口和任务分发 |
| `cinderx-environment-verifier` / environment-verifier | 环境审计、三态判断 |
| `pyperformance-baseline-runner` / baseline-runner | baseline slot 跑分 |
| `pyperformance-candidate-runner` / candidate-runner | candidate slot 跑分 |
| `pyperformance-benchmark-analyst` | `run.json` / `speedup.json` 结果解读 |
| `cinderx-crash-triager` / crash-triager | `SIGSEGV`、`exit 139`、core dump |
| `cinderx-jit-analyst` | CinderX JIT、HIR/LIR、机器码优化点 |
| `cinderx-platform-analyst` | Kunpeng/x86、ISA、微架构差异 |

## Environment Verifier 三态

| 状态 | 下一步 |
|------|--------|
| 可复用 / `reusable` | 返回环境句柄 |
| 新环境 / `needs_bootstrap` | 调 `cinderx-env-bootstrap` |
| 被破坏 / `needs_clean_bootstrap` | 调 `cinderx-env-clean` 再 bootstrap |

## 专业 Skill

`cinderx-env-validate`、`cinderx-env-clean`、`cinderx-env-bootstrap`、`cinderx-remote-lab-ops`、`cinderx-ab-run-slot`、`cpython-runtime-test-run`、`cinderx-smoke-check`、`pyperformance-worker-run`、`pyperformance-suite-run`、`pyperformance-result-compare`、`cinderx-gdb-core-triage`、`cinderx-hir-dump`、`cinderx-jit-entry-check`、`cinderx-hir-lir-analyze`、`cinderx-isa-microarch-compare`、`cinderx-optimization-report`、`validation-strategy`。

## Workflow 路由

- 双平台性能差距：`workflow-cross-platform-delta-triage`
- 已知特性优化：`workflow-feature-driven-optimization`
- 系统找平台优化点：`workflow-platform-differential-discovery`
- 环境准备：`workflow-remote-cinderx-lab-setup`
- crash：`workflow-cinderx-crash-triage`
- 正式回归：`workflow-pyperformance-regression`
- 单 benchmark JIT：`workflow-jit-optimization-analysis`

## 不变原则

- 先让 `cinderx-environment-verifier` 审计环境，再跑昂贵任务。
- A/B 并行前用 `cinderx-ab-run-slot` 确认 CPU 绑核和结果目录不冲突。
- `SIGSEGV` / core dump 走 `cinderx-gdb-core-triage`，日志不能替代 `gdb bt full`。
- 远程命令输出契约用 `cinderx-remote-lab-ops`，异常耗时要诊断并询问用户。
- 验证阶梯和成本预算用 `validation-strategy`。
