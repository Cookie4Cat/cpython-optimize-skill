---
name: pyperformance-result-compare
description: Use when 已有 pyperformance run.json 或 speedup.json，需要比较 baseline/candidate、方差、噪声、提交 baseline、收益范围或回归可信度。
---

# pyperformance Result Compare

负责解释结果，不负责跑 benchmark。

## 输入

- baseline `run.json`
- candidate `run.json`
- `speedup.json`
- 提交 baseline / candidate commit
- 口径 baseline：CPython JIT、CinderX JIT、解释执行等

## 判断

- 命令口径是否一致
- 按 `../using-cpython-optimize/references/baseline-source-contract.md` 核对 baseline source 是否 `baseline_source_verified`，包括口径 baseline、提交 baseline、source path、commit/ref、dirty 状态、`patchlevel.h`、`SOABI` 和容器 bind mount。
- 按 `../using-cpython-optimize/references/pyperformance-affinity-guidance.md` 核对 baseline/candidate 的原始/实际 `--affinity`、可用 CPU 映射和并行/串行口径是否一致。
- 先按 `../using-cpython-optimize/references/pyperformance-env-contract.md` 核对 baseline/candidate 的 `--inherit-environ`、driver/worker env 和唯一差异轴。
- CinderX JIT 口径必须核对 worker 内证据：`.pth`、`pyvenv.cfg` / `include-system-site-packages`、`import cinderx` / `_cinderx`、`cinderx.__file__`、`cinderx.get_import_error()`、`cinderx.is_initialized()`。
- baseline/candidate 是否只在目标变量上不同
- 方差、噪声和异常值
- 收益范围、无收益范围、未验证范围
- 需要回到 `pyperformance-worker-run` 的异常用例
- 如果 baseline source、affinity 口径、环境契约、worker JIT 证据缺失或 baseline/candidate 不一致，先降级结论，不把 `run.json` 写成可信性能收益。

## 反问 Gate

- baseline/candidate `run.json`、`speedup.json` 或口径 baseline 缺失且无法从路径/文件推断时，询问用户。
- baseline source 缺少 commit/ref、dirty 状态、source path 或用户指定事实源时，询问用户补充 baseline 事实源。
- 方差或异常值使结论不稳定，需要补跑、扩大样本或降级结论时，询问。
- 用户要求收益外推到全量，但当前只覆盖单 benchmark 或小集合时，询问是否晋级验证。

输出可信收益、可信回归、baseline source 状态、噪声项、补测建议和不能外推的范围。
