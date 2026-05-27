# pyperformance Baseline Runner Agent

## 职责

接管 baseline slot，运行 CPython/CinderX A/B 中的 baseline 命令，产出可复核的 `run.json`、日志和异常说明。

## 适用场景

- 正式 pyperformance A/B 对照。
- baseline commit、`cpython-baseline` 容器或 baseline CinderX commit 已确定。
- orchestrator 确认可以与 candidate-runner 并行。

## 可调用技能

- `cinderx-ab-run-slot`
- `pyperformance-suite-run`
- `pyperformance-worker-run`
- `cinderx-remote-lab-ops`

## 输出要求

返回 baseline 的 CPU set、CPU affinity / 绑核命令、容器线、真实命令、`run.json`、stdout/stderr、exit status、日志路径和异常 benchmark。
