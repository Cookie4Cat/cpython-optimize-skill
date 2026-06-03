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

运行前必须引用 `skills/using-cpython-optimize/references/pyperformance-affinity-guidance.md` 和 `skills/using-cpython-optimize/references/pyperformance-env-contract.md`，输出 candidate 的原始/实际 `--affinity`、可用 CPU 证据、`--inherit-environ`、driver/worker env、helper 变量、CinderX `.pth`、worker `pyvenv.cfg` 和 `cinderx.is_initialized()` 证据，并和 baseline 对齐。

## 反问 Gate

- candidate patch、commit、editable install 或 CinderX flags 有多个候选时，询问选择。
- candidate 的 CPU set、结果目录、tmux pane 或容器线会与 baseline 冲突且无法自动隔离时，询问串行或重分配。
- candidate smoke 失败、crash 或异常慢时，询问是否转入 crash/JIT 分支还是中止性能验证。

## 输出要求

返回 candidate 的 CPU set、CPU affinity / 绑核命令、原始/实际 `--affinity`、可用 CPU 证据、容器线、真实命令、`run.json`、`--inherit-environ`、driver/worker 环境差异、`.pth` / venv / worker JIT 证据、stdout/stderr、exit status、日志路径和异常 benchmark。
