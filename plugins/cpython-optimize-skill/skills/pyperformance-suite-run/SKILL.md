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
- 正式非 debug 命令形态必须包含 `--affinity`、`--warmup`、`-b <benchmark-selector>`（subset 时）、`-o <result.json>` 和 `--inherit-environ`。
- `--inherit-environ` 至少覆盖代理、`LD_LIBRARY_PATH`、`PYTHONPATH`、插件开关和 JIT 关键变量。
- 记录 warmup、loops、CPU affinity、容器线、Python、CinderX commit。
- 正式数据关闭 HIR/JIT dump、`--debug-single-value` 和临时诊断变量；这些只用于 L2 调试，不进入正式性能结论。
- subset/full 选择必须来自 `validation-strategy` 的晋级理由。
- 文档和报告只写 `<benchmark-selector>`、`<result.json>`、`<baseline.json>`、`<candidate.json>` 等占位，不硬编码具体 pyperformance 用例名或文件名。

## 命令形态

目标集合正式性能测试：

```bash
<env-vars> <python> -m pyperformance run \
  --affinity=<cpu-mask-or-set> \
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
- worker 导入 CinderX 失败：回到 `pyperformance-worker-run` 检查系统 site-packages、`PYTHONPATH` 和 `--inherit-environ`。
- 结果波动大：检查 CPU 绑核、governor、后台任务、容器资源隔离、warmup/loops 和 baseline/candidate 唯一差异轴。
- 正式运行中发现 debug 变量：丢弃该结果，重新用非 debug 命令运行。

## 反问 Gate

- 用户未明确授权 L4 full 或预计接近三小时的全量 pyperformance 时，询问是否降级到目标 benchmark/相关子集。
- benchmark subset、warmup、loops、CPU affinity 或正式/调试口径缺失时，询问。
- 当前环境仍有 HIR/JIT dump 等调试变量，且用户目标是正式性能数据时，询问是否切换口径。

输出 `run.json` 路径、命令、环境指纹和异常 benchmark 列表。
