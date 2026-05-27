---
name: cpython-build
description: 在目标环境中编译 CPython 或 CinderX 并强制覆盖安装时使用，涵盖版本基线、编译选项和安装验证
---

# CPython/CinderX 编译与强制覆盖安装

## 目标

在目标环境中完成隔离构建，并确保安装结果真正覆盖到当前解释器。

## 原则

- 不在本地盲目编译，优先远端验证
- 明确 Python、编译器、`pyperformance` 版本
- 每次切分支或切验证目标后，优先 `--force-reinstall`
- 编译 CPython/CinderX 或扩展前必须先确认 API/ABI 版本，不按记忆选择“最新”接口

## CPython

- 版本基线：`3.14.3`
- 编译器基线：`gcc == 14.2.0`

## CinderX

- 版本基线：当前会话仓库
- Python：`3.14.3`
- `pyperformance == 1.14.0`
- 安装建议：

```bash
python -m pip install -e . --no-build-isolation --no-deps --force-reinstall
```

## API/ABI 版本门禁

目标解释器是版本事实源。当前容器基线是 **Python 3.14.3**；如果模型想到的修复依赖 **3.14.5** 才出现的 API，必须改为 3.14.3 可用的兼容实现，或先向用户确认是否升级环境。

编译前记录：

```bash
python - <<'PY'
import sys, sysconfig
print("executable =", sys.executable)
print("version =", sys.version)
print("SOABI =", sysconfig.get_config_var("SOABI"))
print("include =", sysconfig.get_paths().get("include"))
PY
```

同时检查目标头文件，例如 `patchlevel.h`，确认头文件与 `sys.version` 一致。若解释器、`SOABI`、`patchlevel.h` 或源码分支指向不同 Python 微版本，先停止编译修环境；不要通过继续加宏、换 API 或重跑安装来掩盖版本不一致。

## 验证

- 检查 `cinderx.__file__`
- 检查 `cinderx.is_initialized()`
- 检查 `cinderx.get_import_error()`
- 明确当前解释器路径
- 明确 `sys.version`、`SOABI` 和 `patchlevel.h` 与目标环境一致
