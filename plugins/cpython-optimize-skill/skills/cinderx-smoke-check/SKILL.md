---
name: cinderx-smoke-check
description: Use when 需要确认 CinderX 安装和最小 JIT 可用，包括 import cinderx、_cinderx、is_initialized、get_import_error、最小 JIT 和 HIR 输出。
---

# CinderX Smoke Check

给 verifier、bootstrap 和 runners 使用。它是进入测试或 benchmark 前的 L1 门禁。

## 必查

- `import cinderx`
- `cinderx.__file__`
- `_cinderx` 是否可加载
- `cinderx.is_initialized()`
- `cinderx.get_import_error()`
- 最小 JIT 函数能否触发
- HIR / `PYTHONJITDUMPFINALHIR` 是否可输出

## 输出

返回 smoke 是否通过、失败项、解释器路径、CinderX 路径、JIT flags 和 HIR 产物路径。

smoke 不通过时，不进入 pyperformance 正式跑分。
