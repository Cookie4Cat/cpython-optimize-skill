# pyperformance Affinity 指南

`--affinity` 是 pyperf/pyperformance 的 CPU 绑核参数，用来限制 benchmark worker 进程运行在哪些 CPU 上，降低调度噪声。它不是 benchmark 选择器、不是 JIT 开关，也不是必须逐字照抄的语义参数。

## 使用原则

- 真实命令里的 `--affinity` 表示“绑到一组稳定 CPU 上”的测试口径；当前环境没有相同核号时，应保持口径而不是照抄不可用核号。
- `--affinity=<cpu>`、`--affinity=<cpu-list>`、`--affinity=<range>` 等形式要以当前 pyperf/pyperformance 支持为准；先用 `python -m pyperformance run --help` 或 `python -m pyperf --help` 确认。
- 实际 affinity 必须落在当前进程可用 CPU 集合内。先查 `nproc`、`lscpu`、`taskset -pc $$`、容器 `cpuset` / `cpuset.cpus.effective`，必要时查 `docker inspect`。
- 如果用户给的高核号在当前环境不可用，不要停止，也不要声称命令必须完全一致；不能逐字照抄不可用核号，应重分配到可用 CPU，并记录原始 affinity -> 实际 affinity 的映射。
- A/B 对比时，baseline/candidate 要使用相同数量、同类位置、互不冲突的 CPU set。当前 CPU 不足以并行隔离时，改为串行执行并让两边复用同一 affinity。
- 如果使用 `taskset` 包裹命令，`taskset` 的 CPU set 必须覆盖 `--affinity` 指定的 CPU；两者冲突时优先修正为一致。

## 映射规则

| 场景 | 处理 |
|------|------|
| 单 run，原始 CPU 可用 | 保留原始 `--affinity` |
| 单 run，原始 CPU 不可用 | 选择当前可用且较空闲的 CPU 或 CPU set，记录映射理由 |
| A/B 并行，可用 CPU 充足 | baseline/candidate 分配不重叠 CPU set，数量尽量一致 |
| A/B 并行，可用 CPU 不足 | 降级为串行，两边使用同一 CPU set |
| 原命令跨 NUMA/socket | 当前环境有 NUMA 时尽量保持同类拓扑；没有时记录无法保持 |
| 用户要求复现实测命令 | 复现命令结构和测试口径，但 affinity 可按当前可用 CPU 变通 |

## 输出要求

报告中写明：
- 当前可用 CPU 证据：`nproc`、`lscpu`、`taskset -pc $$`、容器 cpuset。
- 原始 `--affinity` 和实际 `--affinity`。
- baseline/candidate 是否并行，CPU set 是否互不冲突。
- 变通理由：核号不可用、CPU 数不足、容器 cpuset 限制、NUMA 不一致等。
- 对结论的影响：正式可比、只能做趋势观察、或需要更大机器复跑。
