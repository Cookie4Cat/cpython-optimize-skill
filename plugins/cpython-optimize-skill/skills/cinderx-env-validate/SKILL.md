---
name: cinderx-env-validate
description: Use when 需要判断 CPython/CinderX 实验环境是否可复用，尤其涉及 Python 3.14.3、SOABI、patchlevel.h、_cinderx、pyperformance、Docker 双线或 JIT flags。
---

# CinderX Env Validate

给 `cinderx-environment-verifier` 使用。结论只能是 `reusable`、`needs_bootstrap` 或 `needs_clean_bootstrap`。

## 版本事实源

目标 Python 版本固定为 `Python 3.14.3`。环境校验必须以目标解释器、容器内头文件和 `patchlevel.h` 为事实源，不能把更高 patchlevel 才有的 C API 当成可用能力。

当前 checkout 不是事实源本身。比如本地 CPython 仓当前显示 `3.16.0a0`，只能说明当前工作树不符合目标版本，不能直接判定本地 CPython 仓整体不可信，也不能立刻改走远端下载。先尝试安全切换到本地已有的 3.14.3 可信来源。

## 本地 CPython 仓安全切换

当用户给出 `/opt/Codex/cpython`、`CPYTHON_ROOT` 或其它本地 CPython clone 时，按顺序检查：

- 仓库身份：`git remote -v`、`git show -s --format=%H`、`git describe --tags --always --dirty`。
- 污染风险：`git status --short`；有未提交改动时不能直接 `git checkout`。
- 本地 3.14.3 来源：本地 tag、branch、ref、现有 worktree、tarball/cache 或已有容器中的源码。
- 版本证据：`Include/patchlevel.h`、目标解释器 `sys.version`、`SOABI` 和 include 路径。

安全切换规则：

- 优先用 `git worktree add <dedicated-dir> <3.14.3-ref>` 或专用目录，不污染用户当前 checkout。
- 只有在专用目录或明确授权的干净仓库中，才能切换 ref。
- 切换后必须重新读取 `Include/patchlevel.h` 并运行目标解释器校验；通过后才可作为 baseline 事实源。
- 本地没有 3.14.3 ref/cache、dirty 状态无法隔离或需要 `git fetch --tags` 时，先询问用户。
- 外部网络不佳时，优先复用本地 clone、worktree、tarball/cache 和已有容器；远端下载/extract Python-3.14.3 只作为最后选项。

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
