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

## Baseline Source 门禁

- 先读取 `../using-cpython-optimize/references/baseline-source-contract.md`。
- baseline slot 必须绑定 `baseline_source_verified`：口径 baseline、提交 baseline、source path、commit/ref、`git status --short`、`patchlevel.h`、`SOABI` 和容器 bind mount 都已确认。
- 远程环境、容器线或 tmux pane 可用不等于 baseline 源码可信；不能把远程 workspace 当前源码直接当 baseline。
- 若 baseline ref 不明、dirty 状态未解释、bind mount 指向不明或混入 candidate editable install，返回 `baseline_source_untrusted`，不分配正式 A/B slot。

## 并行前检查

- verifier 已确认环境可复用或已 bootstrap。
- verifier 已确认 baseline source verified；只有执行环境 reusable 不够。
- baseline/candidate 只在目标变量上不同。
- 先读取 `../using-cpython-optimize/references/pyperformance-affinity-guidance.md`，确认 `--affinity` / `taskset` 使用当前可用 CPU，而不是逐字照抄用户命令里的不可用高核号。
- 绑核策略写清，例如 `--affinity=0-7` 与 `--affinity=8-15`，或 `taskset -c 0-7` 与 `taskset -c 8-15`。
- 分配前查 `nproc`、`lscpu`、`taskset -pc $$` 和容器 cpuset；baseline/candidate 的 CPU set 数量尽量一致且不重叠。
- 可用 CPU 不足以并行隔离时，改为串行执行，并让 baseline/candidate 复用同一实际 affinity。
- `cinderx-test` 与 `cpython-baseline` 使用场景明确。

## 反问 Gate

- baseline/candidate 的唯一差异轴不明确时，询问要比较的变量。
- baseline source 不是 `baseline_source_verified` 时，询问用户指定 baseline、创建干净 worktree 或重建 `cpython-baseline`。
- CPU set、tmux pane、结果目录或容器线无法安全分离时，询问串行执行还是重新分配资源。
- 用户给出的真实命令 affinity 在当前环境不可用，且无法自动映射出可比 CPU set 时，询问是否接受重映射或换环境。
- 用户要求并行但环境 verifier 未确认可并行时，询问是否先做环境审计。

## 输出

返回两个 run slot、baseline source 状态、原始/实际 affinity、可用 CPU 证据和是否允许并行。无法保证 baseline 可信或资源隔离时，要求修复 baseline 或串行执行。
