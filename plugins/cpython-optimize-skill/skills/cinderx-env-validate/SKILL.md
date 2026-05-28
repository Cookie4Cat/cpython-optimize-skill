---
name: cinderx-env-validate
description: Use when 需要判断 CPython/CinderX 实验环境是否可复用，尤其涉及 Python 3.14.3、SOABI、patchlevel.h、_cinderx、pyperformance、Docker 双线或 JIT flags。
---

# CinderX Env Validate

给 `cinderx-environment-verifier` 使用。结论只能是 `reusable`、`needs_bootstrap` 或 `needs_clean_bootstrap`。

## 版本事实源

目标 Python 版本固定为 `Python 3.14.3`。环境校验必须以目标解释器、容器内头文件和 `patchlevel.h` 为事实源，不能把更高 patchlevel 才有的 C API 当成可用能力。

## 必查项

- Python：目标解释器路径、`Python 3.14.3`、`SOABI`、include 路径、`patchlevel.h`。
- CinderX：commit、branch、`cinderx.__file__`、`cinderx.is_initialized()`、`cinderx.get_import_error()`、`_cinderx`。
- pyperformance：路径、`pyperformance 1.14`、benchmark 源码和 worker 能否继承环境。
- toolchain：GCC、libstdc++、openEuler / 宿主发行版、Docker 可用性。
- Docker 双线：`cinderx-test` 与 `cpython-baseline` 是否存在且 bind mount 指向正确源码。
- JIT flags：`PYTHONJITAUTO`、`PYTHONJITHUGEPAGES`、HIR/JIT dump 变量是否污染正式跑分。

## 判定

- `reusable`：依赖齐全、版本符合、smoke 通过，能直接交给 runner。
- `needs_bootstrap`：目标目录或容器不存在，需要初始化。
- `needs_clean_bootstrap`：存在但版本漂移、错误 editable install、错版本头文件或 CinderX 导入异常。

输出必须带环境指纹和失败项，不能只写“环境正常”。
