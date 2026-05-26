---
name: workflow-pyperformance-regression
description: 需要正式运行 pyperformance、对比 CPython/CinderX 或提交前后性能回归时使用；串联环境隔离、构建、benchmark、结果对比和报告沉淀
---

# pyperformance Regression Workflow

## 目标

生成可复核的性能对比结果，避免混用解释器口径、JIT 口径和提交基线。

## 调用技能

| 阶段 | 技能 | 产出 |
|------|------|------|
| 环境接入 | `remote-environment` | 独立远程目录和 tmux 会话 |
| 运行时隔离 | `docker-runtime` | `cpython-baseline` 或 `cinderx-test` 容器线 |
| 构建安装 | `cpython-build` | baseline/candidate 解释器与 CinderX 安装确认 |
| 基准测试 | `pyperformance-test` | `baseline/run.json`、`candidate/run.json` |
| 异常分析 | `cinderx-analysis` | 对异常用例补充 HIR/LIR 或热点归因 |
| 报告沉淀 | `experiment-documentation` | `speedup.json`、`report.md` |

## 推荐 Agent

- `agents/pyperformance-env-auditor.md`：正式跑分前审计环境和命令口径。
- `agents/cinderx-performance-reviewer.md`：审查 speedup 可信度、噪声和异常用例。

## 基线声明

开始前必须明确两个 baseline：

| baseline | 必填内容 |
|----------|----------|
| 口径基线 | `CPython 解释执行`、`CPython JIT`、`CinderX 解释执行` 或 `CinderX JIT` |
| 提交基线 | baseline commit/branch 和 candidate commit/branch |

## Workflow Gates

### Gate 1: 口径对齐

正式比较前必须确认：

- Python 版本
- 编译器版本
- pyperformance 版本
- JIT 开关和关键环境变量
- baseline/candidate 命令只在目标变量上不同

### Gate 2: 禁止 debug 干扰

正式性能数据必须关闭会显著影响性能的 dump 或 log。需要 HIR/JIT 证据时，另跑 debug 命令，不把 debug 数据当正式跑分。

### Gate 3: 异常用例复核

如果某个 benchmark 出现显著回归、崩溃或方差异常，先用 `pyperformance-test` 单用例复现，再按需调用 `cinderx-analysis`。

## 完成条件

最小交付集合：

- `baseline/run.json`
- `candidate/run.json`
- `speedup.json`
- `report.md`

报告中必须说明性能口径、提交基线、关键环境变量、异常用例处理方式和残余风险。
