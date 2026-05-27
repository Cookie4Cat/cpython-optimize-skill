---
name: cinderx-ab-run-slot
description: Use when CPython/CinderX A/B 性能验证需要分配 baseline/candidate 的容器、工作目录、CPU affinity、绑核、结果目录，并确认可并行运行。
---

# CinderX A/B Run Slot

给 orchestrator 和 pyperformance runners 使用。它只负责 A/B 资源切分，不解释性能结果。

## Slot 内容

- baseline slot：commit、容器线、Python、CPU affinity、结果目录、日志路径。
- candidate slot：commit、容器线、Python、CPU affinity、结果目录、日志路径。
- 互斥资源：CPU set 不重叠，tmux pane 不共享，build dir 不共享，`run.json` 输出不覆盖。

## 并行前检查

- verifier 已确认环境可复用或已 bootstrap。
- baseline/candidate 只在目标变量上不同。
- 绑核策略写清，例如 `taskset -c 0-15` 与 `taskset -c 16-31`。
- `cinderx-test` 与 `cpython-baseline` 使用场景明确。

## 输出

返回两个 run slot 和是否允许并行。无法保证隔离时，要求串行执行。
