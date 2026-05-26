---
name: workflow-cinderx-crash-triage
description: 需要端到端复现、定位并记录 CinderX/pyperformance crash 时使用；串联远程环境、Docker、构建、单 benchmark 复现、JIT/HIR 证据采集和实验文档
---

# CinderX Crash Triage Workflow

## 目标

把 crash 从现象推进到可复现证据、根因假设、修复或规避方案，并沉淀为后续 Agent 可直接消费的文档。

## 调用技能

按需调用以下技能：

| 阶段 | 技能 | 产出 |
|------|------|------|
| 环境接入 | `remote-environment` | 远程 host、独立宿主机目录、tmux 会话 |
| 运行时隔离 | `docker-runtime` | `cinderx-test` 调试线容器 |
| 构建安装 | `cpython-build` | 当前解释器、CinderX 安装路径、commit/branch |
| crash 复现 | `pyperformance-test` | 单 benchmark worker 命令、crash 日志 |
| 根因分析 | `cinderx-analysis` | `gdb bt`、jit.log、HIR/LIR、问题片段 |
| 结果沉淀 | `experiment-documentation` | `docs/guides/YYYY-MM-DD-<topic>.md` |

## 推荐 Agent

- `agents/cinderx-crash-triager.md`：crash 复现、core dump、JIT 证据链。
- `agents/pyperformance-env-auditor.md`：worker 环境变量、路径和依赖一致性。

## Workflow Gates

### Gate 1: 环境可复现

进入 crash 判断前必须记录：

- 远程 host 和宿主机工作目录
- 容器线，默认 `cinderx-test`
- Python 路径
- CinderX commit / branch
- benchmark 名称和完整 worker 命令

### Gate 2: crash 证据

没有以下证据时，不进入根因结论：

- crash log 或退出信号
- 真实 worker 命令
- `gdb bt` 或 core dump 摘要
- JIT 相关问题必须包含 `jit.log`、HIR 或说明为何无法采集

### Gate 3: 根因输出

结论至少包含：

- crash 触发条件
- 失败路径
- 最小复现命令
- 修复方案、规避方案或下一步验证点

## 完成条件

调用 `experiment-documentation` 写入报告。报告必须包含真实命令、证据链、根因判断和回归结果；如果仍未定位根因，明确列出下一步验证假设。
