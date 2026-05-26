---
name: workflow-jit-optimization-analysis
description: 需要针对单个 CinderX JIT 用例定位性能瓶颈、分析 HIR/LIR、提出优化点时使用；串联单 benchmark、热点归因、JIT 证据和优化报告
---

# JIT Optimization Analysis Workflow

## 目标

针对一个 benchmark 或最小用例，确认是否进入 CinderX JIT，定位热点，读取 HIR/LIR 证据，并输出可实施的优化点。

## 调用技能

| 阶段 | 技能 | 产出 |
|------|------|------|
| 环境准备 | `remote-environment`、`docker-runtime` | 远程和容器上下文 |
| 构建安装 | `cpython-build` | 当前 CinderX 安装确认 |
| 单用例运行 | `pyperformance-test` | 真实 worker 命令、debug 环境变量 |
| JIT 分析 | `cinderx-analysis` | 热点归因、HIR/LIR、问题片段 |
| 结果沉淀 | `experiment-documentation` | 优化分析报告 |

## 推荐 Agent

- `agents/cinderx-performance-reviewer.md`：判断优化点是否被证据支持。
- `agents/pyperformance-env-auditor.md`：确认 benchmark 命令和环境没有漂移。

## Workflow Gates

### Gate 1: 确认进入 JIT

不满足以下条件时，不进入 HIR 优化结论：

- 真实 benchmark 本体进入 CinderX JIT
- 有 jit.log、HIR dump 或等价证据
- 明确当前口径是 `CinderX JIT`

### Gate 2: 先热点再 HIR

必须先做热点归因，再解释 HIR/LIR。禁止只凭 HIR 形态直接下性能结论。

### Gate 3: 优化点完整性

每个优化点至少包含：

- 热点归因
- 具体 HIR/LIR/机器码片段
- 问题说明
- 修改方案

## 完成条件

输出一份分析报告，列出已证实的优化点、未证实假设、需要补充的实验，以及能复现分析结果的真实命令。
