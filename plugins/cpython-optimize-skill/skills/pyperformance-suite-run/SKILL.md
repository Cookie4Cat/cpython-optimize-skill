---
name: pyperformance-suite-run
description: Use when 需要正式运行 python -m pyperformance run，生成 subset/full 的 run.json，配置 warmup、loops、affinity 或 L3/L4 性能验证。
---

# pyperformance Suite Run

负责正式 pyperformance 运行。单 benchmark 调试先用 `pyperformance-worker-run`。

## 三类测试边界

- RuntimeTests 是功能测试。
- test_cinderx/lib test 是集成测试。
- pyperformance 是性能测试；正式性能测试前必须说明功能测试和集成测试是否已通过、跳过或仍待验证。

## 使用场景

- L3 相关子集
- L4 full 全量性能验证
- baseline/candidate 正式对照
- 生成 `run.json`

## 规则

- 用 `python -m pyperformance run`。
- 运行前必须读取 `../using-cpython-optimize/references/pyperformance-env-contract.md`，先列出 driver env、`--inherit-environ`、worker env 和 baseline/candidate 差异轴。
- 使用 `--affinity` 前必须读取 `../using-cpython-optimize/references/pyperformance-affinity-guidance.md`，说明它是 CPU 绑核参数；先检查当前可用 CPU，再把用户真实命令中的 affinity 映射到当前环境，不要逐字照抄不可用核号。
- CinderX JIT 口径必须证明真实 worker 启用 JIT：检查 CinderX `.pth`、worker `pyvenv.cfg` / `include-system-site-packages` 或等价 `PYTHONPATH`、worker 内 `import cinderx` / `_cinderx`、`cinderx.__file__`、`cinderx.get_import_error()` 和 `cinderx.is_initialized()`。
- 正式非 debug 命令形态必须包含 `--affinity`、`--warmup`、`-b <benchmark-selector>`（subset 时）、`-o <result.json>` 和 `--inherit-environ`。
- `--affinity` 必须落在当前 `nproc` / `lscpu` / `taskset -pc $$` / 容器 cpuset 显示的可用 CPU 内；高核号不可用时，重分配可用 CPU 并记录原始 affinity -> 实际 affinity。
- `--inherit-environ` 至少覆盖代理、`LD_LIBRARY_PATH`、`PYTHONPATH`、插件开关和 JIT 关键变量。
- 若 `validation-skill-router` deny 了 pyperformance 命令，不要把它当测试失败；先补齐 `pyperformance-env-contract.md` 要求的 worker venv / `.pth` / `--inherit-environ` / JIT 初始化证据，再用 `CPYTHON_OPTIMIZE_HOOK_ACK=1` 前缀重试同一条正式命令。
- 不能在未完成前置证据时提前加 `CPYTHON_OPTIMIZE_HOOK_ACK=1` 绕过 hook；ACK 只表示已经完成环境契约检查。
- 记录 warmup、loops、CPU affinity、容器线、Python、CinderX commit。
- 正式数据关闭 HIR/JIT dump、`--debug-single-value` 和临时诊断变量；这些只用于 L2 调试，不进入正式性能结论。
- subset/full 选择必须来自 `validation-strategy` 的晋级理由。
- 文档和报告只写 `<benchmark-selector>`、`<result.json>`、`<baseline.json>`、`<candidate.json>` 等占位，不硬编码具体 pyperformance 用例名或文件名。

## 命令形态

目标集合正式性能测试：

```bash
<env-vars> <python> -m pyperformance run \
  --affinity=<cpu-list-or-set> \
  --warmup <n> \
  -b <benchmark-selector> \
  --inherit-environ <comma-separated-env-list> \
  -o <result.json>
```

全量性能测试：去掉 `-b <benchmark-selector>`，但必须先经过 `validation-strategy` 授权 L4。

性能对比：

```bash
<python> -m pyperf compare_to <baseline.json> <candidate.json> --table -G
```

## 故障排查 Checklist

- `run.json` 缺失或损坏：先查 stdout/stderr、exit status、输出目录和 pyperformance worker 日志，不要立即重跑全量。
- `--affinity` 核号不存在或被容器 cpuset 限制：按 `pyperformance-affinity-guidance.md` 重映射到可用 CPU；A/B CPU 不足时改串行或询问降级口径。
- 环境变量不生效：先按 `pyperformance-env-contract.md` 检查变量是否只到 driver、未进 `--inherit-environ`，或在 worker/bench_command 子进程中丢失。
- worker 导入 CinderX 或 JIT 初始化失败：回到 `pyperformance-worker-run` 检查 `.pth`、系统 site-packages、`pyvenv.cfg`、`PYTHONPATH`、`--inherit-environ` 和 worker 内 `cinderx.is_initialized()`。
- 结果波动大：检查 CPU 绑核、governor、后台任务、容器资源隔离、warmup/loops 和 baseline/candidate 唯一差异轴。
- 正式运行中发现 debug 变量：丢弃该结果，重新用非 debug 命令运行。

## 反问 Gate

- 用户未明确授权 L4 full 或预计接近三小时的全量 pyperformance 时，询问是否降级到目标 benchmark/相关子集。
- benchmark subset、warmup、loops、CPU affinity 或正式/调试口径缺失时，询问。
- 可用 CPU 不足以满足用户要求的并行 A/B 隔离或正式口径时，询问串行执行、降低验证等级或更换环境。
- 当前环境仍有 HIR/JIT dump 等调试变量，且用户目标是正式性能数据时，询问是否切换口径。

输出 `run.json` 路径、命令、原始/实际 `--affinity`、可用 CPU 证据、`--inherit-environ` 列表、driver/worker 环境差异、`.pth` / venv / worker JIT 证据、环境指纹和异常 benchmark 列表。
