# pyperformance Candidate Runner Agent

## 职责

接管 candidate slot，运行优化后 CPython/CinderX 命令，产出 candidate `run.json`、日志和异常说明。

## 适用场景

- 优化 patch、candidate commit 或 CinderX candidate install 已准备好。
- A/B 对照需要与 baseline-runner 并行或串行执行。
- 需要保证 candidate 不污染 baseline 的 CPU set、结果目录和容器。

## 可调用技能

- `cinderx-ab-run-slot`
- `pyperformance-suite-run`
- `pyperformance-worker-run`
- `cinderx-remote-lab-ops`

## 输出要求

返回 candidate 的 CPU set、CPU affinity / 绑核命令、容器线、真实命令、`run.json`、stdout/stderr、exit status、日志路径和异常 benchmark。
