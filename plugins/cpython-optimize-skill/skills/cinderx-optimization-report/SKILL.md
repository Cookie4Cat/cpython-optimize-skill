---
name: cinderx-optimization-report
description: Use when CPython/CinderX 优化、crash、pyperformance 回归或平台差异分析需要沉淀环境指纹、证据链、根因、patch 和回归结果。
---

# CinderX Optimization Report

报告必须让下一位 Agent 能直接复现实验。

## 必填章节

- 背景
- 复现命令
- 环境指纹：Python、SOABI、CinderX commit、容器线、平台、JIT flags
- 证据链：run.json、speedup.json、gdb/core、HIR/LIR、perf
- 根因
- patch / 修复方法
- 回归结果
- 残余风险和下一步

## 产物

- `baseline/run.json`
- `candidate/run.json`
- `speedup.json`
- `report.md`
- crash 时补 `gdb bt full`、core 摘要、jit.log、HIR dump

参考 schema：`references/report_schema.example.json`。
