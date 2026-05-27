---
name: pyperformance-worker-run
description: Use when 需要运行单个 pyperformance benchmark 的 run_benchmark.py --worker、bench_command、sitecustomize 或复现 worker 环境变量继承问题。
---

# pyperformance Worker Run

负责单 benchmark L2 复现，是 crash、HIR、JIT 分析的真实命令来源。

## 重点

- 使用真实 `run_benchmark.py --worker`，不要用交互式 import 替代。
- `bench_command()` 会生成 worker 子进程链。
- `sitecustomize`、`LD_LIBRARY_PATH`、`PYTHONPATH`、JIT flags 必须传到真实 worker。
- 分析阶段只增减 debug 变量，尽量保持同一真实 worker 命令。

## 参考资源

- `references/run-benchmark-worker-realenv.sh`
- `scripts/benchmark_harness.py`
- `scripts/test-benchmark.sh`

输出 benchmark、真实 worker 命令、环境变量、stdout/stderr、exit status 和产物路径。
