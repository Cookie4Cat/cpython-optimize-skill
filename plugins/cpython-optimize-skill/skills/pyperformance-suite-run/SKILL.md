---
name: pyperformance-suite-run
description: Use when 需要正式运行 python -m pyperformance run，生成 subset/full 的 run.json，配置 warmup、loops、affinity 或 L3/L4 性能验证。
---

# pyperformance Suite Run

负责正式 pyperformance 运行。单 benchmark 调试先用 `pyperformance-worker-run`。

## 使用场景

- L3 相关子集
- L4 full 全量性能验证
- baseline/candidate 正式对照
- 生成 `run.json`

## 规则

- 用 `python -m pyperformance run`。
- 记录 warmup、loops、CPU affinity、容器线、Python、CinderX commit。
- 正式数据关闭 HIR/JIT 大量 dump。
- subset/full 选择必须来自 `validation-strategy` 的晋级理由。

输出 `run.json` 路径、命令、环境指纹和异常 benchmark 列表。
